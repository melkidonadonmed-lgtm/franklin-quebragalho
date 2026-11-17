#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
validate_skills.py
Validador determinístico de integridade estrutural, contratual e semântica
do catálogo de skills e do ecossistema Antigravity (Padrão agentskills.io + 2026).
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
DUPLICATE_META_TOP_KEYS = ("version", "updated_at", "allowed-tools")
NEGATIVE_TRIGGER_RE = re.compile(r"\b(n[aã]o use|do not use|don't use|skip when)\b", re.IGNORECASE)
POSITIVE_TRIGGER_RE = re.compile(r"\b(use|activate|invoke|when to use|ative|acion[ea])\b", re.IGNORECASE)
MAX_DESC_RECOMMENDED = 420
MAX_DESC_HARD = 1024
STOPWORDS = frozenset({
    "a", "an", "and", "as", "at", "by", "com", "da", "das", "de", "do", "dos", "e",
    "em", "for", "from", "in", "into", "is", "na", "nas", "no", "nos", "not", "o", "of", "on", "only", "or",
    "ou", "para", "por", "quando", "se", "that", "the", "this", "to", "um", "uma", "use", "via", "when", "with",
})

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.tools.frontmatter_parser import parse_frontmatter  # noqa: E402

REQUIRED_SECTIONS: List[Tuple[str, str]] = [
    (
        r"(#|##)\s+.*(Overview|Scope|Triggers|When to Use|Purpose|Objective|Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao|Visão Geral|Visao Geral|Objetivo)",
        "Overview & Scope / Triggers",
    ),
    (
        r"(#|##)\s+.*(Inputs|Prerequisites|Parameters|Context|Entradas|Pr[eé]-requisitos|Par[aâ]metros|Contexto|Configura[cç][aã]o|Insumos)",
        "Inputs & Prerequisites",
    ),
    (
        r"(#|##)\s+.*(Procedure|Step-by-Step|Operational Workflow|Workflow|Processing|Execution|Architecture|Processamento|Passo a Passo|Fluxo|Execução|Execucao|Arquitetura|M[oó]dulos|Como Funciona)",
        "Step-by-Step Procedure",
    ),
    (
        r"(#|##)\s+.*(Output|Outputs|Deliverables|Validation Criteria|Report|Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida|Formato|Relat[oó]rio)",
        "Output Schema & Validation Criteria",
    ),
    (
        r"(#|##)\s+.*(Gotchas|Edge Cases|Failure Modes|Exceptions|Limits|When NOT to Use|Restrictions|Guardrails|Exceções|Excecoes|Limites|Quando N[AÃ]O Usar|Restri[cç][oõ]es)",
        "Gotchas, Edge Cases & Limits",
    ),
]
ALLOWED_RULE_TRIGGERS = frozenset({"always_on", "model_decision", "glob", "manual"})
ALLOWED_HOOK_EVENTS = frozenset({"PreToolUse", "PostToolUse", "SessionStart", "PreInvocation", "PostInvocation", "Stop"})
ALLOWED_PLUGIN_KEYS = frozenset({
    "$schema", "name", "displayName", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "logo", "suggestedPrompts", "disabled",
})
FORBIDDEN_AGENT_TOOLS = frozenset({
    "*", "call_mcp_tool", "view_file", "list_dir", "find_by_name",
    "grep_search", "write_to_file", "replace_file_content", "multi_replace_file_content",
})
ALLOWED_EXEC_POLICIES = frozenset({"auto", "sandbox", "off"})
REQUIRED_AGENT_KEYS = ("name", "description", "subagent", "mainAgent", "model", "commandExecutionPolicy", "tools")


def _validate_description_field(
    desc: str, is_template: bool, errors: List[str], *, strict_budget: bool = True
) -> None:
    """Valida comprimento e gatilhos positivos/negativos da descrição Nível 1."""
    if not desc:
        return
    if len(desc) > MAX_DESC_HARD:
        errors.append(f"[FAIL] Descrição excede teto agentskills.io de {MAX_DESC_HARD} chars ({len(desc)} chars)")
    elif strict_budget and len(desc) > MAX_DESC_RECOMMENDED:
        errors.append(f"[FAIL] Descrição excede orçamento recomendado L1 de {MAX_DESC_RECOMMENDED} chars ({len(desc)} chars)")
    if len(desc) < 30:
        errors.append(f"[FAIL] Descrição muito curta ou rasa ({len(desc)} chars)")
    if not strict_budget:
        return
    if not POSITIVE_TRIGGER_RE.search(desc):
        errors.append("[FAIL] Descrição deve conter formulação imperativa ('Use quando...' / 'Use para...')")
    if not is_template and not NEGATIVE_TRIGGER_RE.search(desc):
        errors.append("[FAIL] Descrição deve declarar fronteira negativa ('Não use para...' / 'Don't use for...')")


def _extract_raw_top_level_keys(content: str) -> Tuple[Set[str], bool]:
    """Extrai chaves raiz reais do frontmatter YAML sem achatamento de metadata."""
    cleaned = content.lstrip("\ufeff")
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", cleaned, re.DOTALL)
    if not match:
        return set(), False
    raw_yaml = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", match.group(1))
    try:
        import yaml
    except ImportError as exc:
        _ = exc
    else:
        try:
            loaded = yaml.safe_load(raw_yaml)
            if isinstance(loaded, dict):
                return {str(k) for k in loaded.keys()}, isinstance(loaded.get("metadata"), dict)
        except (yaml.YAMLError, ValueError, TypeError, AttributeError) as exc:
            _ = exc
    top_keys = {m.group(1) for m in re.finditer(r"^([A-Za-z0-9_-]+):", raw_yaml, re.MULTILINE)}
    return top_keys, "metadata" in top_keys


def _check_top_keys_and_semver(
    meta: Dict[str, Any],
    errors: List[str],
    *,
    external_mode: bool,
    strict_mode: bool,
    raw_top_keys: Set[str] | None,
    has_metadata_dict: bool,
) -> None:
    """Valida ausência de chaves órfãs no topo e conformidade SemVer em modo estrito."""
    orphan_keys = [k for k in DUPLICATE_META_TOP_KEYS if k in (raw_top_keys or set())] if has_metadata_dict else []
    if orphan_keys:
        errors.append(f"[FAIL] Chaves duplicadas/órfãs no topo com 'metadata:' presente: {orphan_keys}")
    if not strict_mode:
        return
    if not external_mode and not has_metadata_dict:
        errors.append("[FAIL] Modo --strict exige bloco 'metadata:' para version/updated_at")
    ver_val = str(meta.get("version", "")).strip()
    if ver_val and not SEMVER_RE.match(ver_val):
        errors.append(f"[FAIL] metadata.version inválido em --strict (exige SemVer X.Y.Z): '{ver_val}'")


def _validate_skill_name_field(name_val: str, dir_name: str, is_template: bool, errors: List[str]) -> None:
    """Valida formato kebab-case e correspondência com o nome da pasta."""
    if not name_val:
        return
    if len(name_val) > 64 or not SKILL_NAME_RE.match(name_val):
        errors.append(f"[FAIL] Nome '{name_val}' viola kebab-case estrito (^[a-z0-9]+(-[a-z0-9]+)*$, máx 64)")
    if name_val != dir_name and not is_template:
        errors.append(f"[FAIL] Nome no frontmatter ('{name_val}') difere da pasta ('{dir_name}')")


def _validate_frontmatter_fields(
    meta: Dict[str, Any],
    dir_name: str,
    errors: List[str],
    *,
    external_mode: bool = False,
    strict_mode: bool = False,
    raw_top_keys: Set[str] | None = None,
    has_metadata_dict: bool = False,
) -> None:
    """Valida campos obrigatórios, chaves órfãs no topo, SemVer, regex kebab-case e gatilhos."""
    if not meta:
        errors.append("[FAIL] Frontmatter YAML ausente ou malformado")
    req_fields = ("name", "description") if external_mode else ("name", "description", "version")
    errors.extend([f"[FAIL] Campo obrigatório '{req}' ausente no frontmatter" for req in req_fields if not meta.get(req)])
    _check_top_keys_and_semver(
        meta, errors, external_mode=external_mode, strict_mode=strict_mode,
        raw_top_keys=raw_top_keys, has_metadata_dict=has_metadata_dict,
    )
    name_val = str(meta.get("name", "")).strip()
    is_template = dir_name == "_template" and name_val == "template-skill"
    _validate_skill_name_field(name_val, dir_name, is_template, errors)
    _validate_description_field(
        str(meta.get("description", "")).strip(), is_template, errors, strict_budget=not external_mode
    )


def _validate_scripts_dir(skill_dir: Path, errors: List[str]) -> None:
    """Audita scripts executáveis em scripts/ contra bloqueios TTY (input()) e sintaxe AST."""
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for py_file in sorted(scripts_dir.glob("*.py")):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=py_file.name)
        except (OSError, SyntaxError) as exc:
            errors.append(f"[FAIL] Erro de sintaxe em scripts/{py_file.name}: {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":
                errors.append(f"[FAIL] Bloqueio TTY proibido: 'input()' em scripts/{py_file.name}")


_EVAL_PROMPT_KEYS = frozenset({"prompt", "query", "input", "scenario"})
_EVAL_ASSERT_KEYS = frozenset({
    "assertions", "expected_assertions", "expected_output", "expected_behavior",
    "expected", "criteria", "expected_status", "should_trigger",
})


def _validate_single_eval_case(idx: int, tc: Any, errors: List[str]) -> tuple[int, int]:
    """Valida um caso de eval individual e retorna incremento (pos, neg)."""
    if not isinstance(tc, dict) or not ({"eval_id", "id"} & set(tc)):
        errors.append(f"[FAIL] Test case #{idx} em evals.json requer 'eval_id' (ou 'id')")
        return 0, 0
    if not (_EVAL_PROMPT_KEYS & set(tc)):
        errors.append(f"[FAIL] Test case #{idx} em evals.json requer 'prompt' (ou 'query'/'input')")
    if not (_EVAL_ASSERT_KEYS & set(tc)):
        errors.append(f"[FAIL] Test case #{idx} em evals.json requer critério/asserção esperada")
    trig = tc.get("should_trigger")
    return (1 if trig is True else 0), (1 if trig is False else 0)


def _validate_evals_file(skill_dir: Path, errors: List[str], *, strict_mode: bool = False, external_mode: bool = False) -> None:
    """Valida a estrutura e sintaxe JSON de evals/evals.json quando presente."""
    evals_file = skill_dir / "evals" / "evals.json"
    if not evals_file.exists():
        return
    try:
        evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"[FAIL] Erro de sintaxe JSON em evals/evals.json: {exc}")
        return

    evals_list = evals_data.get("evals", []) if isinstance(evals_data, dict) else evals_data
    if not isinstance(evals_list, list) or not evals_list:
        errors.append("[FAIL] evals.json deve conter uma lista não-vazia de testes")
        return

    counts = [_validate_single_eval_case(idx, tc, errors) for idx, tc in enumerate(evals_list)]
    pos_triggers = sum(p for p, _ in counts)
    neg_triggers = sum(n for _, n in counts)
    if strict_mode and not external_mode and min(pos_triggers, neg_triggers) < 1:
        errors.append(
            f"[FAIL] evals/evals.json em modo --strict exige ao menos 1 should_trigger=true e 1 should_trigger=false (+{pos_triggers}/-{neg_triggers})"
        )


def _is_relative_file_link(rel_path: str) -> bool:
    """Retorna True se o link parecer um caminho relativo de arquivo verificável."""
    return bool(rel_path) and not any(ch in rel_path for ch in "<>{}[]") and any(sep in rel_path for sep in (".", "/", "\\"))


def _validate_markdown_links(
    skill_dir: Path, body: str, errors: List[str], *, context_dir: Path | None = None
) -> None:
    """Valida que links Markdown respeitam 1 nível relativo sem escapes '../' e existem no disco."""
    clean_md = re.sub(r"`[^`\n]+`", "", re.sub(r"```.*?```", "", body, flags=re.DOTALL))
    base_dir = context_dir or skill_dir
    for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", clean_md):
        if target.startswith(("http://", "https://", "file://", "mailto:", "#")):
            continue
        rel_path = target.split("#", 1)[0].split("?", 1)[0].strip()
        if not _is_relative_file_link(rel_path):
            continue
        if ".." in Path(rel_path).parts or rel_path.startswith(("../", "..\\")):
            errors.append(f"[FAIL] Parent path escape '../' forbidden in SKILL.md: {target}")
        elif not ((skill_dir / rel_path).exists() or (base_dir / rel_path).exists()):
            errors.append(f"[FAIL] Broken relative link in SKILL.md: {target}")


def _validate_rules_and_references(skill_dir: Path, errors: List[str]) -> None:
    """Valida marcadores determinísticos em rules/audit_criteria.md (ou fallback legado) e JSONs/MDs em references/."""
    audit_file = skill_dir / "rules" / "audit_criteria.md"
    legacy_file = skill_dir / "rules" / "criterios_auditoria.md"
    rules_file = audit_file if audit_file.exists() else legacy_file
    if rules_file.exists():
        rules_text = rules_file.read_text(encoding="utf-8")
        if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
            errors.append(f"[FAIL] rules/{rules_file.name} deve conter [PASS] e [FAIL]")

    ref_dir = skill_dir / "references"
    if not ref_dir.is_dir():
        return
    for json_ref in ref_dir.glob("*.json"):
        try:
            json.loads(json_ref.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"[FAIL] Erro no JSON de referência {json_ref.name}: {exc}")
    for md_ref in sorted(ref_dir.glob("*.md")):
        _validate_markdown_links(
            skill_dir, md_ref.read_text(encoding="utf-8", errors="replace"), errors, context_dir=ref_dir
        )


def validate_skill_dir(
    skill_dir: Path, *, external_mode: bool = False, strict_mode: bool = False
) -> List[str]:
    """Valida uma pasta de skill individual."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"[FAIL] Arquivo SKILL.md inexistente em {skill_dir.name}"]
    try:
        content = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"[FAIL] Erro ao ler SKILL.md: {exc}"]

    errors: List[str] = []
    meta, body = parse_frontmatter(content)
    raw_top_keys, has_metadata_dict = _extract_raw_top_level_keys(content)
    _validate_frontmatter_fields(
        meta,
        skill_dir.name,
        errors,
        external_mode=external_mode,
        strict_mode=strict_mode,
        raw_top_keys=raw_top_keys,
        has_metadata_dict=has_metadata_dict,
    )

    body_lines = len(body.splitlines())
    if body_lines > 500:
        errors.append(f"[FAIL] Corpo L2 do SKILL.md excede o limite de 500 linhas ({body_lines} linhas)")

    if not external_mode:
        for sec_pattern, sec_name in REQUIRED_SECTIONS:
            if not re.search(sec_pattern, body, re.IGNORECASE):
                errors.append(f"[FAIL] Seção essencial ausente: {sec_name}")

    _validate_markdown_links(skill_dir, body, errors)
    _validate_scripts_dir(skill_dir, errors)
    _validate_evals_file(skill_dir, errors, strict_mode=strict_mode, external_mode=external_mode)
    _validate_rules_and_references(skill_dir, errors)
    return errors


def _tokenize_positive_desc(skill_dir: Path) -> Set[str]:
    """Extrai conjunto de tokens da porção positiva de description para detecção de colisão."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return set()
    meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="ignore"))
    desc = str(meta.get("description", ""))
    pos = NEGATIVE_TRIGGER_RE.split(desc, maxsplit=1)[0].lower()
    return {w for w in re.findall(r"[a-z0-9áéíóúãõç_-]{3,}", pos) if w not in STOPWORDS}


def check_jaccard_overlaps(skill_dirs: List[Path], threshold: float = 0.80) -> List[str]:
    """Detecta colisões semânticas (>= threshold Jaccard) entre descrições de skills irmãs."""
    tokens_by_name = {d.name: _tokenize_positive_desc(d) for d in skill_dirs}
    names = sorted(tokens_by_name)
    overlaps: List[str] = []
    for idx, left in enumerate(names):
        tok_l = tokens_by_name[left]
        if not tok_l:
            continue
        for right in names[idx + 1 :]:
            tok_r = tokens_by_name[right]
            if not tok_r:
                continue
            sim = len(tok_l & tok_r) / len(tok_l | tok_r)
            if sim >= threshold:
                overlaps.append(f"[FAIL] Sobreposição semântica L1 ({sim:.2f} >= {threshold:.2f}): '{left}' vs '{right}'")
    return overlaps


def _validate_single_rule_file(rule_file: Path, errors: List[str]) -> int:
    """Valida frontmatter e tamanho de um arquivo rules/*.md e retorna sua contagem de caracteres."""
    raw = rule_file.read_text(encoding="utf-8")
    if rule_file.stat().st_size > 24 * 1024:
        errors.append(f"[FAIL] Rule {rule_file.name} excede 24 KB")
    meta, _ = parse_frontmatter(raw)
    trig = str(meta.get("trigger", "")).strip()
    if trig not in ALLOWED_RULE_TRIGGERS:
        errors.append(f"[FAIL] Rule {rule_file.name} possui trigger inválido: '{trig}'")
    if trig == "model_decision":
        desc_val = str(meta.get("description", "")).strip().lower()
        if not desc_val:
            errors.append(f"[FAIL] Rule model_decision {rule_file.name} exige 'description'")
        elif not any(neg in desc_val for neg in ("do not", "don't")):
            errors.append(f"[FAIL] Rule model_decision {rule_file.name} exige fronteira negativa ('Do NOT load...') na description")
    if trig == "glob" and not str(meta.get("globs", "")).strip():
        errors.append(f"[FAIL] Rule glob {rule_file.name} exige 'globs' como string")
    return len(raw)


def _validate_rules_dir(rules_dir: Path) -> List[str]:
    """Valida frontmatter, trigger, globs e teto de tamanho em rules/*.md."""
    if not rules_dir.is_dir():
        return [f"[FAIL] Diretório rules ausente: {rules_dir}"]
    errors: List[str] = []
    total_chars = sum(_validate_single_rule_file(rf, errors) for rf in sorted(rules_dir.glob("*.md")))
    if total_chars // 4 > 20000:
        errors.append(f"[FAIL] Orçamento agregado de rules excede 20.000 tokens (~{total_chars // 4})")
    return errors


def _validate_hooks_manifest(hooks_file: Path, repo_root: Path) -> List[str]:
    """Valida contrato camelCase Antigravity e portabilidade em hooks/hooks.json."""
    if not hooks_file.is_file():
        return [f"[FAIL] hooks.json ausente: {hooks_file}"]
    try:
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"[FAIL] JSON inválido em hooks.json: {exc}"]
    errors: List[str] = []
    for hook_name, cfg in data.items():
        if isinstance(cfg, dict):
            errors.extend([
                f"[FAIL] Evento hook inválido/não-Antigravity '{key}' em '{hook_name}'"
                for key in cfg if key != "enabled" and key not in ALLOWED_HOOK_EVENTS
            ])
    serialized = json.dumps(data)
    if any(abs_tok in serialized for abs_tok in ("C:\\\\", "/Users/", "C:/Users/")):
        errors.append("[FAIL] hooks.json contém caminho absoluto hardcoded em vez de ./scripts/...")
    if "antigravity_harness_hook.py" in serialized and not (repo_root / "hooks" / "antigravity_harness_hook.py").is_file():
        errors.append("[FAIL] Script hooks/antigravity_harness_hook.py referenciado não existe")
    return errors


def _validate_agent_tools_list(af_name: str, tools: Any, errors: List[str]) -> None:
    """Valida a lista de tools de um manifesto de subagente."""
    if not isinstance(tools, list) or not tools:
        errors.append(f"[FAIL] Agente {af_name} exige lista explícita não-vazia em 'tools'")
        return
    bad_tools = sorted(str(t) for t in tools if str(t) in FORBIDDEN_AGENT_TOOLS)
    if bad_tools:
        errors.append(f"[FAIL] Agente {af_name} declara tools proibidas/legadas em tools: {bad_tools}")


def _validate_single_agent_manifest(af: Path, errors: List[str]) -> None:
    """Valida frontmatter completo de um arquivo declarativo agents/*.md."""
    legacy_agent_keys = {"enable_write_tools", "enable_mcp_tools", "enable_subagent_tools", "wave", "parent_persona", "covered_modules"}
    meta, _ = parse_frontmatter(af.read_text(encoding="utf-8"))
    if not (meta.get("name") and meta.get("description")):
        errors.append(f"[FAIL] Agente {af.name} sem 'name' ou 'description'")
    missing_req = [k for k in REQUIRED_AGENT_KEYS if k not in meta]
    if missing_req:
        errors.append(f"[FAIL] Agente {af.name} sem chaves obrigatórias: {missing_req}")
    bad_keys = sorted(legacy_agent_keys & set(meta))
    if bad_keys:
        errors.append(f"[FAIL] Agente {af.name} usa chaves legadas não-Antigravity: {bad_keys}")
    raw_pol = meta.get("commandExecutionPolicy")
    policy = "false" if raw_pol is False else str(raw_pol or "").strip()
    if policy not in ALLOWED_EXEC_POLICIES:
        errors.append(f"[FAIL] Agente {af.name} com commandExecutionPolicy inválido: '{policy}'")
    if "inheritCustomizations" not in meta:
        errors.append(f"[FAIL] Agente {af.name} exige 'inheritCustomizations' explícito")
    if meta.get("subagent") is True and not (meta.get("max_steps") and meta.get("stop_condition")):
        errors.append(f"[FAIL] Subagente {af.name} exige 'max_steps' e 'stop_condition'")
    _validate_agent_tools_list(af.name, meta.get("tools"), errors)


def _validate_plugin_and_agents(repo_root: Path) -> List[str]:
    """Valida schema plugin.json e frontmatter/tools de agents/*.md."""
    errors: List[str] = []
    pfile = repo_root / "plugin.json"
    if not pfile.is_file():
        errors.append("[FAIL] plugin.json ausente")
    else:
        pdata = json.loads(pfile.read_text(encoding="utf-8"))
        extra = set(pdata) - ALLOWED_PLUGIN_KEYS
        if extra:
            errors.append(f"[FAIL] Chaves não permitidas em plugin.json: {sorted(extra)}")
        logo = pdata.get("logo", "")
        if logo and not (repo_root / logo).is_file():
            errors.append(f"[FAIL] Logo do plugin inexistente: {logo}")

    agents_dir = repo_root / "agents"
    if agents_dir.is_dir():
        for af in sorted(agents_dir.glob("*.md")):
            _validate_single_agent_manifest(af, errors)
    return errors


def validate_global_agents() -> List[str]:
    """Valida todos os subagentes instalados globalmente e no repositório irmão shredded-shape."""
    errors: List[str] = []
    home = Path.home()
    candidate_dirs = (
        home / ".gemini" / "config" / "agents",
        home / ".gemini" / "agents",
        ROOT_DIR.parent / "shredded-shape" / "agents",
        home / ".gemini" / "config" / "plugins" / "shredded-shape" / "agents",
    )
    for d in candidate_dirs:
        if d.is_dir():
            for af in sorted(d.glob("*.md")):
                _validate_single_agent_manifest(af, errors)
    cfg_agents = home / ".gemini" / "config" / "agents"
    if cfg_agents.is_dir():
        leaked_ui = sorted(p.name for p in cfg_agents.glob("ui-*.md"))
        if leaked_ui:
            errors.append(f"[FAIL] Drift 3-vias em ~/.gemini/config/agents/: {leaked_ui}")
    return errors


def validate_ecosystem(repo_root: Path) -> List[str]:
    """Executa auditoria contratual completa de rules, hooks, plugin.json e subagents."""
    errors: List[str] = []
    errors.extend(_validate_rules_dir(repo_root / "rules"))
    errors.extend(_validate_hooks_manifest(repo_root / "hooks" / "hooks.json", repo_root))
    errors.extend(_validate_plugin_and_agents(repo_root))
    return errors


def _resolve_skill_dirs(skills_root: Path, targets_arg: str | None) -> List[Path]:
    """Resolve a lista de diretórios de skills a inspecionar."""
    if not targets_arg:
        return sorted(d for d in skills_root.iterdir() if d.is_dir() and not d.name.startswith("."))
    targets = [t.strip() for t in targets_arg.split(",") if t.strip()]
    return [skills_root / t for t in targets if (skills_root / t).is_dir()]


def _collect_extra_validation_errors(skill_dirs: List[Path], args: argparse.Namespace) -> List[str]:
    """Consolida erros de colisão Jaccard, ecossistema e subagentes globais."""
    extra_errors = [] if args.targets else check_jaccard_overlaps(skill_dirs)
    if args.ecosystem:
        extra_errors.extend(validate_ecosystem(ROOT_DIR))
    if args.global_agents:
        extra_errors.extend(validate_global_agents())
    return extra_errors


def main() -> int:
    """Ponto de entrada CLI do validador determinístico de skills e ecossistema."""
    parser = argparse.ArgumentParser(description="Validador determinístico de integridade de skills e ecossistema.")
    parser.add_argument("--targets", type=str, help="Skills específicas separadas por vírgula.")
    parser.add_argument("--root", type=str, help="Diretório alternativo de skills (ex.: ~/.agents/skills).")
    parser.add_argument("--external", action="store_true", help="Modo agentskills.io enxuto para skills externas.")
    parser.add_argument("--strict", action="store_true", help="Reprova chaves duplicadas no topo e exige SemVer em metadata.version.")
    parser.add_argument("--ecosystem", action="store_true", help="Valida rules/, hooks/hooks.json, plugin.json e agents/.")
    parser.add_argument("--global-agents", action="store_true", help="Valida subagentes em ~/.gemini e shredded-shape.")
    args = parser.parse_args()

    skills_root = Path(args.root).expanduser().resolve() if args.root else ROOT_DIR / "skills"
    if not skills_root.exists():
        print(f"[ERROR] Diretório skills não encontrado em {skills_root}")
        return 1

    print(f"=== AUDITORIA DETERMINISTICA ({skills_root}) ===")
    skill_dirs = _resolve_skill_dirs(skills_root, args.targets)
    failures: Dict[str, List[str]] = {}
    passed_skills = 0

    for s_dir in skill_dirs:
        errs = validate_skill_dir(s_dir, external_mode=args.external, strict_mode=args.strict)
        if errs:
            failures[s_dir.name] = errs
            print(f"[FAIL] {s_dir.name:<45}")
            for err in errs:
                print(f"   ↳ {err}")
        else:
            passed_skills += 1
            print(f"[PASS] {s_dir.name:<45}")

    extra_errors = _collect_extra_validation_errors(skill_dirs, args)
    for err in extra_errors:
        print(err)

    print("-" * 65)
    print(f"Resultado: {passed_skills}/{len(skill_dirs)} skills | Extra failures: {len(extra_errors)}")
    return 1 if (failures or extra_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
