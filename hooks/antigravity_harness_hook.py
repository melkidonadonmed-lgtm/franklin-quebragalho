# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
antigravity_harness_hook.py
Hook de Ciclo de Vida Oficial do Antigravity (PreToolUse / PostToolUse / SessionStart / Stop)
integrado ao SemanticGuard, evaluate_action_risk (shared/harness.py) e Contract/Anti-Stub Gate.

Contrato Oficial Antigravity (camelCase JSON via stdin/stdout):
- PreToolUse (stdin): {"toolCall": {"name", "args"}, "stepIdx", ...common}
  -> stdout: {"decision": "allow"} | {"decision": "deny", "reason"} | {"decision": "ask", "reason"}
- PostToolUse (stdin): {"toolCall": {"name", "args"}, "stepIdx", "error"?, ...common} (sem `result`)
  -> stdout: {}
- SessionStart / PreInvocation / PostInvocation (stdin) -> stdout: {} | {"injectSteps": [{"systemMessage": ...}]}
- Stop (stdin) -> stdout: {} | {"decision": "continue", "reason": ...}
"""

from __future__ import annotations

import ast
import contextlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
for candidate_sys_path in (BASE_DIR / "lib", BASE_DIR):
    if (candidate_sys_path / "shared").is_dir() and str(candidate_sys_path) not in sys.path:
        sys.path.insert(0, str(candidate_sys_path))

_INSPECTED_ARG_KEYS: tuple[str, ...] = (
    "CommandLine",
    "command",
    "Target",
    "Replacement",
    "ReplacementContent",
    "CodeContent",
    "Content",
    "TargetFile",
    "TargetContent",
    "query",
    "Prompt",
    "Url",
    "url",
)
_SPEC_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60
_FORBIDDEN_AGENT_TOOLS = frozenset({
    "*", "call_mcp_tool", "view_file", "list_dir", "find_by_name",
    "grep_search", "write_to_file", "replace_file_content", "multi_replace_file_content",
})
_EXEMPT_STUB_DUNDERS = frozenset({
    "__init__", "__post_init__", "__enter__", "__exit__", "__aenter__", "__aexit__", "__del__",
})
_EXEMPT_STUB_DECS = frozenset({"abstractmethod", "overload", "abstractproperty"})
_EXEMPT_IFACE_BASES = frozenset({"Protocol", "ABC", "ABCMeta"})


def _extract_candidate_text(tool_call: Dict[str, Any]) -> str:
    """Extrai argumentos textuais relevantes de um toolCall camelCase."""
    args = tool_call.get("args")
    if not isinstance(args, dict):
        return ""
    parts: list[str] = []
    for key in _INSPECTED_ARG_KEYS:
        val = args.get(key)
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())
    nested_args = args.get("Arguments")
    if isinstance(nested_args, dict) and nested_args:
        parts.append(json.dumps(nested_args, ensure_ascii=False))
    elif isinstance(nested_args, str) and nested_args.strip():
        parts.append(nested_args.strip())
    return "\n".join(parts)


def _reconstruct_mutated_text(tool_name: str, args: Dict[str, Any], target_path: str) -> str | None:
    """Reconstrói em memória o conteúdo resultante de write_file ou edit_file."""
    if tool_name == "write_file" and not args.get("Append"):
        content = args.get("Content")
        return content if isinstance(content, str) else None
    if tool_name == "edit_file":
        tgt = args.get("Target")
        rep = args.get("Replacement")
        p = Path(target_path)
        if isinstance(tgt, str) and isinstance(rep, str) and p.is_file():
            with contextlib.suppress(OSError):
                raw = p.read_text(encoding="utf-8")
                if tgt in raw:
                    return raw.replace(tgt, rep)
    return None


def _validate_agent_markdown_contract(text: str, fname: str) -> str | None:
    """Valida frontmatter obrigatório de agents/*.md antes da gravação no disco."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text.lstrip("\ufeff"), re.DOTALL)
    if not match:
        return f"[Franklin ContractGate] {fname} requires YAML frontmatter (--- ... ---)."
    header = match.group(1)
    required_keys = ("name", "description", "subagent", "mainAgent", "model", "commandExecutionPolicy", "inheritCustomizations", "tools")
    present_keys = {m.group(1) for m in re.finditer(r"^([A-Za-z0-9_-]+)\s*:", header, re.MULTILINE)}
    missing = [k for k in required_keys if k not in present_keys]
    if missing:
        return f"[Franklin ContractGate] {fname} missing required fields: {', '.join(missing)}."
    tools_found = [m.group(1).strip().strip("\"'") for m in re.finditer(r"^\s*-\s*([^\r\n#]+)", header, re.MULTILINE)]
    bad_tools = sorted(t for t in tools_found if t in _FORBIDDEN_AGENT_TOOLS)
    if bad_tools:
        return f"[Franklin ContractGate] {fname} uses forbidden/legacy tools: {', '.join(bad_tools)}."
    return None


def _ast_term_name(expr: ast.AST) -> str:
    """Extrai o nome base de um nó AST de decorador, classe base ou exceção."""
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Subscript):
        return _ast_term_name(expr.value)
    if isinstance(expr, ast.Call):
        return _ast_term_name(expr.func)
    return ""


def _is_fn_stub_violation(fn: ast.FunctionDef | ast.AsyncFunctionDef, lines: list[str]) -> bool:
    """Verifica se uma função concreta fora de interface consiste apenas em stub vazio."""
    if fn.name in _EXEMPT_STUB_DUNDERS or fn.name.startswith("visit_"):
        return False
    if any(_ast_term_name(d) in _EXEMPT_STUB_DECS for d in fn.decorator_list):
        return False
    if 1 <= fn.lineno <= len(lines) and "noqa: STUB001" in lines[fn.lineno - 1]:
        return False
    eff = [
        s for s in fn.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]
    if len(eff) != 1:
        return False
    stmt = eff[0]
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
        return True
    return isinstance(stmt, ast.Raise) and stmt.exc is not None and _ast_term_name(stmt.exc) == "NotImplementedError"


def _collect_interface_fn_ids(tree: ast.AST) -> set[int]:
    """Coleta IDs de funções/métodos pertencentes a classes Protocol/ABC."""
    iface_classes = [
        n for n in ast.walk(tree)
        if isinstance(n, ast.ClassDef) and any(_ast_term_name(b) in _EXEMPT_IFACE_BASES for b in n.bases)
    ]
    return {
        id(child)
        for cls_node in iface_classes
        for child in ast.walk(cls_node)
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _find_python_stub_violation(source: str, fname: str) -> str | None:
    """Detecta funções stub (pass, ..., NotImplementedError) via AST em módulos de produção."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    lines = source.splitlines()
    iface_fns = _collect_interface_fn_ids(tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and id(node) not in iface_fns:
            if _is_fn_stub_violation(node, lines):
                return f"[Franklin AntiStubGate STUB001] Stub function '{node.name}' at L{node.lineno} in {fname}; implement complete logic."
    return None


def _check_write_edit_gates(tool_name: str, args: Dict[str, Any]) -> str | None:
    """Aplica o portão rápido de contrato em agents/*.md e STUB001 em *.py de produção."""
    if tool_name not in ("write_file", "edit_file"):
        return None
    raw_path = str(args.get("Path") or args.get("TargetFile") or "").strip()
    if not raw_path:
        return None
    norm = raw_path.replace("\\", "/")
    fname = Path(norm).name
    is_agent_md = bool(re.search(r"(?:^|/)agents/[^/]+\.md$", norm)) and "/skills/" not in norm and "/docs/" not in norm
    low_name = fname.lower()
    is_prod_py = (
        low_name.endswith(".py")
        and not low_name.startswith("test_")
        and not low_name.endswith("_test.py")
        and low_name != "conftest.py"
        and "/tests/" not in f"/{norm.lower()}/"
    )
    if not is_agent_md and not is_prod_py:
        return None
    text = _reconstruct_mutated_text(tool_name, args, raw_path)
    if not text:
        return None
    if is_agent_md:
        return _validate_agent_markdown_contract(text, fname)
    return _find_python_stub_violation(text, fname)


def handle_pre_tool_use(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Avalia PreToolUse sob o contrato oficial Antigravity (sempre devolve 'decision')."""
    tool_call = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return {"decision": "allow"}
    candidate = _extract_candidate_text(tool_call)
    if not candidate:
        return {"decision": "allow"}

    from shared.harness import (
        RiskLevel,
        SecurityViolationError,
        SemanticGuard,
        evaluate_action_risk,
    )

    try:
        SemanticGuard.sanitize_input(candidate)
    except SecurityViolationError as exc:
        return {"decision": "deny", "reason": str(exc)}

    tool_name = str(tool_call.get("name", ""))
    args = tool_call.get("args")
    if isinstance(args, dict):
        gate_err = _check_write_edit_gates(tool_name, args)
        if gate_err:
            return {"decision": "deny", "reason": gate_err}

    if tool_name in ("run_command", "execute_sql", "call_mcp_tool"):
        risk, reason = evaluate_action_risk(candidate)
        if risk == RiskLevel.CRITICAL:
            return {"decision": "ask", "reason": f"[Franklin Harness HITL] {reason}"}
    return {"decision": "allow"}


def _resolve_audit_log_path() -> Path | None:
    """Resolve caminho gravável de auditoria sem tocar stdout."""
    plugin_data = os.environ.get("PLUGIN_DATA", "").strip()
    if plugin_data:
        return Path(plugin_data) / "hooks_post_tool_audit.jsonl"
    default_dir = Path.home() / ".gemini" / "config" / "specs-cache"
    if default_dir.exists() or os.access(default_dir.parent, os.W_OK):
        return default_dir / "hooks_post_tool_audit.jsonl"
    return None


def handle_post_tool_use(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Registra erros/auditoria de PostToolUse (contrato oficial: sem 'result', retorna {})."""
    error_text = str(payload.get("error", "") or "").strip()
    if not error_text:
        return {}
    tool_call = payload.get("toolCall")
    tool_name = str(tool_call.get("name", "")) if isinstance(tool_call, dict) else ""
    log_path = _resolve_audit_log_path()
    if log_path is not None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "PostToolUse",
            "tool": tool_name,
            "stepIdx": payload.get("stepIdx"),
            "error": error_text[:512],
        }
        with contextlib.suppress(OSError):
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {}


def handle_session_start(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Executa sonda local rápida (<10ms) de drift/TTL da documentação oficial."""
    notices: list[str] = []
    for raw_ws in payload.get("workspacePaths") or []:
        proposal = Path(str(raw_ws)) / ".context" / "docs-drift-proposal.md"
        if proposal.is_file():
            notices.append(f"Proposta de atualização de specs oficiais pendente em {proposal}.")
            break

    lock_file = Path(
        os.environ.get(
            "FRANKLIN_SPECS_LOCK_PATH",
            str(Path.home() / ".gemini" / "config" / "specs-cache" / "official_specs_lock.json"),
        )
    )
    if lock_file.is_file():
        age_sec = time.time() - lock_file.stat().st_mtime
        if age_sec > _SPEC_CACHE_TTL_SECONDS:
            days = int(age_sec // 86400)
            notices.append(
                f"Cache oficial de specs está com {days} dias. Considere rodar sync_official_docs_specs.py --check --sync-cache."
            )

    if not notices:
        return {}
    return {
        "injectSteps": [
            {
                "systemMessage": {
                    "systemMessage": " ".join(notices),
                    "metadata": {"source": "franklin-docs-watcher"},
                }
            }
        ]
    }


def _passthrough(_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Resposta pass-through oficial vazia para PreInvocation, PostInvocation e Stop."""
    return {}


_EVENT_HANDLERS: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "PreToolUse": handle_pre_tool_use,
    "PostToolUse": handle_post_tool_use,
    "SessionStart": handle_session_start,
    "PreInvocation": _passthrough,
    "PostInvocation": _passthrough,
    "Stop": _passthrough,
}


def _default_response(event: str) -> Dict[str, Any]:
    """Fail-open compatível com o esquema obrigatório por evento."""
    return {"decision": "allow"} if event == "PreToolUse" else {}


def main() -> int:
    """Lê JSON camelCase da stdin, despacha pelo evento argv[1] e escreve JSON único na stdout."""
    event = sys.argv[1] if len(sys.argv) > 1 else "PreToolUse"
    raw_stdin = sys.stdin.read().strip()
    if not raw_stdin:
        sys.stdout.write(json.dumps(_default_response(event)) + "\n")
        return 0
    try:
        payload = json.loads(raw_stdin)
        if not isinstance(payload, dict):
            sys.stdout.write(json.dumps(_default_response(event)) + "\n")
            return 0
        handler = _EVENT_HANDLERS.get(event, _passthrough)
        out = handler(payload)
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    except (json.JSONDecodeError, ValueError, TypeError, KeyError, OSError) as exc:
        sys.stderr.write(f"[franklin-hook:{event}] fail-open: {exc}\n")
        sys.stdout.write(json.dumps(_default_response(event)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
