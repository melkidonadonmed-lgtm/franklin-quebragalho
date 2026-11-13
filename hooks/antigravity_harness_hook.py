"""
antigravity_harness_hook.py
Hook de Ciclo de Vida Oficial do Antigravity (PreToolUse / PostToolUse / SessionStart / Stop)
integrado ao SemanticGuard e evaluate_action_risk (shared/harness.py).

Contrato Oficial Antigravity (camelCase JSON via stdin/stdout):
- PreToolUse (stdin): {"toolCall": {"name", "args"}, "stepIdx", ...common}
  -> stdout: {"decision": "allow"} | {"decision": "deny", "reason"} | {"decision": "ask", "reason"}
- PostToolUse (stdin): {"toolCall": {"name", "args"}, "stepIdx", "error"?, ...common} (sem `result`)
  -> stdout: {}
- SessionStart / PreInvocation / PostInvocation (stdin) -> stdout: {} | {"injectSteps": [{"systemMessage": ...}]}
- Stop (stdin) -> stdout: {} | {"decision": "continue", "reason": ...}
"""

from __future__ import annotations

import contextlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict

BASE_DIR = Path(__file__).resolve().parent.parent
for candidate_sys_path in (BASE_DIR / "lib", BASE_DIR):
    if (candidate_sys_path / "shared").is_dir() and str(candidate_sys_path) not in sys.path:
        sys.path.insert(0, str(candidate_sys_path))

from shared.harness import (  # noqa: E402
    RiskLevel,
    SecurityViolationError,
    SemanticGuard,
    evaluate_action_risk,
)

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


def handle_pre_tool_use(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Avalia PreToolUse sob o contrato oficial Antigravity (sempre devolve 'decision')."""
    tool_call = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return {"decision": "allow"}
    candidate = _extract_candidate_text(tool_call)
    if not candidate:
        return {"decision": "allow"}
    try:
        SemanticGuard.sanitize_input(candidate)
    except SecurityViolationError as exc:
        return {"decision": "deny", "reason": str(exc)}

    tool_name = str(tool_call.get("name", ""))
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
