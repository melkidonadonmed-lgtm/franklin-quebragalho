"""
_catalog_scoring.py
Mapping tables, semantic intent scoring, and deterministic validation helpers
extracted from shared.catalog_service to keep modules concise (<= 600 lines).
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Tuple

from shared.tools.frontmatter_parser import parse_frontmatter as _parse_frontmatter

CANONICAL_PERSONA_MAPPING: Dict[str, str] = {
    "ui-frontend-analyst": "ui-suite",
    "ui-brand-ux-planner": "ui-suite",
    "ui-clean-worker": "ui-suite",
    "ui-quality-judge": "ui-suite",
    "complex-zero": "ui-suite",
    "clinical-minimalist-ui": "ui-suite",
    "stitch-canvas": "ui-suite",
    "gdrive-cleanup-auditor": "workspace-ops",
    "gdrive-taxonomy-organizer": "workspace-ops",
    "windows-disk-maintenance": "workspace-ops",
    "obsidian-vault-curator": "knowledge-docs",
    "technical-markdown-writer": "knowledge-docs",
    "html-pdf-converter": "knowledge-docs",
    "flow-filetree-organizer": "knowledge-docs",
    "code-acceptability-auditor": "quality-engineering",
    "test-quality-auditor": "quality-engineering",
    "agent-server-auditor": "quality-engineering",
    "re-a-ndroid": "quality-engineering",
    "high-level-context-planner": "planning-orchestration",
    "gap-analyzer-auditor": "planning-orchestration",
    "chained-plan-orchestrator": "planning-orchestration",
    "solution-content-architect": "core-engineering",
    "system-project-auditor": "core-engineering",
    "android-agy-projects": "core-engineering",
    "project-idea-organizer": "core-engineering",
    "code-quality-audit-3d-physics": "core-engineering",
    "context-sentinel": "core-engineering",
    "refine-prompt": "core-engineering",
}

QUICK_SKILL_ALIASES: Dict[str, str] = {
    "stitch": "stitch-canvas",
    "stitch-canvas": "stitch-canvas",
    "google-stitch": "stitch-canvas",
    "complex-zero": "complex-zero",
    "xyflow": "complex-zero",
    "react-flow": "complex-zero",
    "reactflow": "complex-zero",
    "ghost-node": "complex-zero",
    "3d": "code-quality-audit-3d-physics",
    "fisica": "code-quality-audit-3d-physics",
    "fisica-3d": "code-quality-audit-3d-physics",
    "physics": "code-quality-audit-3d-physics",
    "pdf": "html-pdf-converter",
    "pdf-converter": "html-pdf-converter",
    "html-pdf": "html-pdf-converter",
    "obsidian": "obsidian-vault-curator",
    "vault": "obsidian-vault-curator",
    "vault-curator": "obsidian-vault-curator",
    "memoria": "obsidian-vault-curator",
    "palacio": "obsidian-vault-curator",
    "mempalace": "obsidian-vault-curator",
    "notas": "obsidian-vault-curator",
    "drive-limpeza": "gdrive-cleanup-auditor",
    "drive-cleanup": "gdrive-cleanup-auditor",
    "drive-taxonomia": "gdrive-taxonomy-organizer",
    "drive-taxonomy": "gdrive-taxonomy-organizer",
    "disco": "windows-disk-maintenance",
    "windows": "windows-disk-maintenance",
    "disk-maintenance": "windows-disk-maintenance",
    "medica": "clinical-minimalist-ui",
    "medico": "clinical-minimalist-ui",
    "medical-ui": "clinical-minimalist-ui",
    "clinical-ui": "clinical-minimalist-ui",
    "sentinel": "context-sentinel",
    "code-auditor": "code-acceptability-auditor",
    "acceptability": "code-acceptability-auditor",
    "ast-auditor": "code-acceptability-auditor",
    "test-auditor": "test-quality-auditor",
    "evals": "test-quality-auditor",
    "qa-testes": "test-quality-auditor",
    "arquitetura": "system-project-auditor",
    "nav-x-func": "system-project-auditor",
    "nav": "system-project-auditor",
    "ilhas": "system-project-auditor",
    "auditar": "system-project-auditor",
    "auditoria": "system-project-auditor",
    "projeto": "system-project-auditor",
    "repo": "system-project-auditor",
    "antigravity-project-auditor": "system-project-auditor",
    "arquitetura-design-implementacao-sistema": "system-project-auditor",
    "auditoria-projetos-sistema": "system-project-auditor",
    "mvp-auditor": "system-project-auditor",
    "project-auditor": "system-project-auditor",
    "system-auditor": "system-project-auditor",
    "mvp": "system-project-auditor",
    "design": "ui-brand-ux-planner",
    "design.md": "ui-brand-ux-planner",
    "design-md": "ui-brand-ux-planner",
    "frontend": "ui-brand-ux-planner",
    "ui": "ui-brand-ux-planner",
    "analise-ui": "ui-frontend-analyst",
    "analise-frontend": "ui-frontend-analyst",
    "plan-uiux": "ui-frontend-analyst",
    "code-architect": "ui-clean-worker",
    "refatorar-ui": "ui-clean-worker",
    "sombra": "ui-clean-worker",
    "sombras": "ui-clean-worker",
    "tatil": "ui-clean-worker",
    "tactile": "ui-clean-worker",
    "ui-testing": "ui-quality-judge",
    "frontend-auditor": "ui-quality-judge",
    "ui-ux-auditor": "ui-quality-judge",
    "wcag-auditor": "ui-quality-judge",
    "prompt": "refine-prompt",
    "refinar": "refine-prompt",
    "refinar-prompt": "refine-prompt",
    "entropia": "refine-prompt",
    "android": "android-agy-projects",
    "android-agy": "android-agy-projects",
    "compose": "android-agy-projects",
    "jetpack-compose": "android-agy-projects",
    "agp9": "android-agy-projects",
    "organizar": "project-idea-organizer",
    "organizador": "project-idea-organizer",
    "organizar-projeto": "project-idea-organizer",
    "idea-organizer": "project-idea-organizer",
    "ideia": "project-idea-organizer",
    "ideias": "project-idea-organizer",
    "solucao": "solution-content-architect",
    "arquiteto": "solution-content-architect",
    "solution-architect": "solution-content-architect",
    "fluxo": "flow-filetree-organizer",
    "arvore": "flow-filetree-organizer",
    "mermaid": "flow-filetree-organizer",
    "flow-organizer": "flow-filetree-organizer",
    "markdown": "technical-markdown-writer",
    "relatorio": "technical-markdown-writer",
    "markdown-writer": "technical-markdown-writer",
    "plano": "high-level-context-planner",
    "planejar": "high-level-context-planner",
    "intent-cognitive-planner": "high-level-context-planner",
    "context-planner": "high-level-context-planner",
    "cognitive-planner": "high-level-context-planner",
    "gap": "gap-analyzer-auditor",
    "rca": "gap-analyzer-auditor",
    "brechas": "gap-analyzer-auditor",
    "orquestrar": "chained-plan-orchestrator",
    "orquestrador": "chained-plan-orchestrator",
    "dag": "chained-plan-orchestrator",
    "kahn": "chained-plan-orchestrator",
    "ondas": "chained-plan-orchestrator",
    "dag-orchestrator": "chained-plan-orchestrator",
    "server-auditor": "agent-server-auditor",
    "agent-auditor": "agent-server-auditor",
    "mcp-auditor": "agent-server-auditor",
    "a2a-auditor": "agent-server-auditor",
    "audit-skills": "agent-server-auditor",
    "audit-skills-antigravity": "agent-server-auditor",
    "re-a-ndroid": "re-a-ndroid",
    "rea-android": "re-a-ndroid",
    "apk-auditor": "re-a-ndroid",
    "apk": "re-a-ndroid",
    "adb-audit": "re-a-ndroid",
    "dex": "re-a-ndroid",
}

REQUIRED_SKILL_SECTIONS: List[Tuple[str, str]] = [
    (
        r"(#|##)\s+.*(Overview|Scope|Triggers|When to Use|Purpose|Objective|Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao)",
        "Overview & Scope / Triggers",
    ),
    (
        r"(#|##)\s+.*(Inputs|Prerequisites|Parameters|Context|Entradas|Pr[eé]-requisitos|Par[aâ]metros)",
        "Inputs & Prerequisites",
    ),
    (
        r"(#|##)\s+.*(Procedure|Step-by-Step|Operational Workflow|Workflow|Processing|Execution|Architecture|Processamento|Passo a Passo|Fluxo|Execução|Execucao)",
        "Step-by-Step Procedure",
    ),
    (
        r"(#|##)\s+.*(Output|Outputs|Deliverables|Validation Criteria|Report|Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida)",
        "Output Schema & Validation Criteria",
    ),
    (
        r"(#|##)\s+.*(Gotchas|Edge Cases|Failure Modes|Exceptions|Limits|When NOT to Use|Restrictions|Guardrails|Exceções|Excecoes|Limites|Quando N[AÃ]O Usar)",
        "Gotchas, Edge Cases & Limits",
    ),
]

SEARCH_STOPWORDS: frozenset[str] = frozenset({
    "de", "da", "do", "das", "dos", "para", "por", "em", "no", "na", "nos", "nas",
    "com", "sem", "ou", "e", "o", "a", "os", "as", "um", "uma", "ao", "aos", "que", "se", "use", "nao",
    "the", "and", "for", "with", "from", "into", "that", "this", "when", "not", "dont", "only", "after", "before", "instead",
})


def _resolve_skill_rules_file(skill_dir: Path) -> Path:
    """Resolve o arquivo de regras da skill priorizando rules/audit_criteria.md com fallback legado."""
    audit_path = skill_dir / "rules" / "audit_criteria.md"
    if audit_path.exists():
        return audit_path
    return skill_dir / "rules" / "criterios_auditoria.md"


def _strip_accents(text: str) -> str:
    """Remove acentos e normaliza para ASCII minúsculo."""
    cleaned = text.replace("\u2014", " ").replace("\u2013", " ")
    return unicodedata.normalize("NFKD", cleaned).encode("ascii", "ignore").decode("ascii").lower()


def _split_positive_and_negative_desc(desc_norm: str) -> Tuple[str, str]:
    """Separa a descrição Nível 1 em cláusula positiva (should-trigger) e cláusula de exclusão (bilíngue)."""
    parts = re.split(
        r"\b(?:nao use(?:\s+para|\s+quando)?|do not use(?:\s+for|\s+when)?|don'?t use(?:\s+for|\s+when)?|skip when)\b",
        desc_norm,
        maxsplit=1,
    )
    if len(parts) == 2:
        return parts[0], parts[1]
    return desc_norm, ""


def _extract_meta_tags(meta: Dict[str, Any]) -> List[str]:
    """Extrai tags bilíngues de frontmatter (topo ou metadata.tags)."""
    raw_nested = meta.get("metadata")
    nested_tags = raw_nested.get("tags") if isinstance(raw_nested, dict) else None
    raw_tags = meta.get("tags") or nested_tags or []
    if isinstance(raw_tags, str):
        return [t.strip() for t in raw_tags.split(",") if t.strip()]
    if isinstance(raw_tags, list):
        return [str(t) for t in raw_tags if str(t).strip()]
    return []


def _build_skill_tags(name: str, dir_name: str, description: str, meta: Dict[str, Any]) -> List[str]:
    """Constrói o conjunto ordenado de tags normalizadas (sem vazamento da cláusula negativa)."""
    tags: set[str] = set()
    pos_desc_only, _ = _split_positive_and_negative_desc(_strip_accents(str(description)))
    for tok in (name, dir_name, pos_desc_only):
        tags.update(re.findall(r"[a-z0-9_\-]+", _strip_accents(str(tok))))
    for mtag in _extract_meta_tags(meta):
        norm_mtag = _strip_accents(mtag)
        tags.update(re.findall(r"[a-z0-9_\-]+", norm_mtag))
        tags.update(re.findall(r"[a-z0-9]+", norm_mtag))
    return sorted(tags)


def _has_negative_token_match(t: str, n_toks: set[str]) -> bool:
    """Verifica se o termo t coincide com um token da cláusula de exclusão negativa."""
    if t in n_toks:
        return True
    if len(t) < 5:
        return False
    return any(nt.startswith(t) or t.startswith(nt) for nt in n_toks if len(nt) >= 5)


def _is_positive_desc_hit(t: str, p_toks: set[str], pos_desc: str) -> bool:
    """Verifica se o termo t ocorre nos tokens ou texto da cláusula positiva."""
    if t in p_toks:
        return True
    return len(t) >= 4 and t in pos_desc


def _score_desc_and_tag_hits(t: str, name_norm: str, p_toks: set[str], pos_desc: str, n_toks: set[str], norm_tags: set[str]) -> int:
    """Calcula a pontuação combinada de tags e cláusulas positiva/negativa."""
    is_pos_hit = _is_positive_desc_hit(t, p_toks, pos_desc)
    is_neg_hit = bool(n_toks) and _has_negative_token_match(t, n_toks)
    tag_allowed = (not is_neg_hit) or (t in p_toks) or (t in name_norm)
    score = 10 if (t in norm_tags and tag_allowed) else 0
    if is_pos_hit:
        return score + 7
    if is_neg_hit and t not in name_norm:
        return score - 18
    return score


def _score_single_term(
    t: str,
    s_name: str,
    name_norm: str,
    pos_desc: str,
    neg_desc: str,
    persona_norm: str,
    norm_tags: set[str],
    pos_tokens: set[str] | None = None,
    neg_tokens: set[str] | None = None,
) -> int:
    """Calcula a contribuição de pontuação de um único termo significativo da consulta."""
    delta = (25 if QUICK_SKILL_ALIASES.get(t) == s_name else 0) + (18 if t in name_norm else 0)
    p_toks = pos_tokens if pos_tokens is not None else set(re.findall(r"[a-z0-9]+", pos_desc))
    n_toks = neg_tokens if neg_tokens is not None else set(re.findall(r"[a-z0-9]+", neg_desc))
    delta += _score_desc_and_tag_hits(t, name_norm, p_toks, pos_desc, n_toks, norm_tags)
    return delta + (6 if t in persona_norm else 0)


def _score_skill_query(s: Dict[str, Any], clean_q: str, terms: List[str]) -> int:
    """Calcula a pontuação de relevância Nível 1 de uma skill com penalização de cláusulas negativas."""
    q_norm = _strip_accents(clean_q)
    name_norm = _strip_accents(s["name"])
    desc_norm = _strip_accents(s["description"])
    persona_norm = _strip_accents(s["persona"])
    pos_desc, neg_desc = _split_positive_and_negative_desc(desc_norm)
    pos_tokens = set(re.findall(r"[a-z0-9]+", pos_desc)) | set(re.findall(r"[a-z0-9_\-]+", pos_desc))
    neg_tokens = set(re.findall(r"[a-z0-9]+", neg_desc)) | set(re.findall(r"[a-z0-9_\-]+", neg_desc))
    norm_tags = {_strip_accents(tg) for tg in s.get("tags", [])}

    score = (60 if q_norm in name_norm else 0) + (35 if q_norm in pos_desc else 0)
    if neg_desc and len(q_norm) > 5 and q_norm in neg_desc:
        score -= 40

    short_tech = {"ui", "ux", "3d", "go", "ts", "js", "qa", "pe", "a4"}
    meaningful = [t for t in terms if t not in SEARCH_STOPWORDS and (len(t) > 2 or t in short_tech)]
    for t in meaningful:
        score += _score_single_term(
            t, s["name"], name_norm, pos_desc, neg_desc, persona_norm, norm_tags, pos_tokens, neg_tokens
        )
    return score


def _extract_eval_cases_list(evals_data: Any) -> Any:
    """Extrai a lista de casos de teste de evals.json (dict ou list)."""
    if isinstance(evals_data, dict):
        return evals_data.get("evals", [])
    return evals_data


def _validate_skill_rules_and_evals(s_dir: Path, errs: List[str]) -> None:
    """Valida rules/audit_criteria.md (ou fallback legado) e evals/evals.json de uma pasta de skill."""
    rules_file = _resolve_skill_rules_file(s_dir)
    if rules_file.exists():
        rules_text = rules_file.read_text(encoding="utf-8")
        has_fail = "[FAIL]" in rules_text or "[FAIL:" in rules_text
        if "[PASS]" not in rules_text or not has_fail:
            errs.append(f"rules/{rules_file.name} deve conter marcadores [PASS] e [FAIL]")
    evals_file = s_dir / "evals" / "evals.json"
    if not evals_file.exists():
        return
    try:
        evals_list = _extract_eval_cases_list(json.loads(evals_file.read_text(encoding="utf-8")))
        if not isinstance(evals_list, list) or not evals_list:
            errs.append("evals.json deve conter uma lista não-vazia de testes")
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as e:
        errs.append(f"Sintaxe JSON inválida em evals.json: {e}")


def _check_single_md_link(s_dir: Path, target: str, errs: List[str]) -> None:
    """Valida um link relativo individual extraído do SKILL.md."""
    if target.startswith(("http://", "https://", "file://", "mailto:", "#")):
        return
    rel_path = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not rel_path or any(ch in rel_path for ch in "<>{}[]"):
        return
    if ".." in Path(rel_path).parts or rel_path.startswith(("../", "..\\")):
        errs.append(f"Escape '../' proibido em SKILL.md: {target}")
    elif any(sep in rel_path for sep in (".", "/", "\\")) and not (s_dir / rel_path).exists():
        errs.append(f"Link relativo quebrado em SKILL.md: {target}")


def _validate_skill_links_in_body(s_dir: Path, body: str, errs: List[str]) -> None:
    """Valida links relativos Markdown no corpo L2 do SKILL.md."""
    clean_md = re.sub(r"`[^`\n]+`", "", re.sub(r"```.*?```", "", body, flags=re.DOTALL))
    for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", clean_md):
        _check_single_md_link(s_dir, target, errs)


def _validate_skill_desc_budget(desc_text: str, is_template: bool, errs: List[str]) -> None:
    """Valida o tamanho e a fronteira negativa da descrição Nível 1."""
    if len(desc_text) > 1024:
        errs.append(f"Descrição excede o teto rígido agentskills.io de 1024 chars ({len(desc_text)} chars)")
    elif len(desc_text) > 420:
        errs.append(f"Descrição excede o orçamento recomendado L1 de 420 chars ({len(desc_text)} chars)")
    if desc_text and not is_template and not re.search(r"\b(n[aã]o use|do not use|don't use|skip when)\b", desc_text, re.IGNORECASE):
        errs.append("Descrição deve declarar fronteira negativa ('Não use para...' / 'Do not use...')")


def _validate_skill_meta_fields(s_dir: Path, meta: Dict[str, Any], errs: List[str]) -> None:
    """Valida campos de frontmatter (name, description, version) de uma skill."""
    if not meta:
        errs.append("Frontmatter YAML ausente ou malformado")
    errs.extend([f"Campo obrigatório '{req}' ausente no frontmatter" for req in ("name", "description", "version") if not meta.get(req)])
    name_val = str(meta.get("name", "")).strip()
    is_template = s_dir.name == "_template" and name_val == "template-skill"
    if name_val and (len(name_val) > 64 or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name_val)):
        errs.append(f"Nome '{name_val}' viola o padrão kebab-case estrito (^[a-z0-9]+(-[a-z0-9]+)*$)")
    if name_val and name_val != s_dir.name and not is_template:
        errs.append(f"Nome no frontmatter ('{name_val}') difere da pasta ('{s_dir.name}')")
    _validate_skill_desc_budget(str(meta.get("description", "")).strip(), is_template, errs)


def _validate_single_skill_dir(s_dir: Path) -> List[str]:
    """Valida a conformidade contratual, frontmatter (regex + fronteiras L1), L2 (<500 linhas), links, rules e evals de uma skill."""
    errs: List[str] = []
    skill_file = s_dir / "SKILL.md"
    if not skill_file.exists():
        return ["Arquivo SKILL.md inexistente"]
    try:
        content = skill_file.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(content)
        _validate_skill_meta_fields(s_dir, meta, errs)
        if len(body.splitlines()) > 500:
            errs.append(f"Corpo L2 do SKILL.md excede 500 linhas ({len(body.splitlines())} linhas)")
        errs.extend([f"Seção obrigatória ausente: {sec_name}" for sec_pattern, sec_name in REQUIRED_SKILL_SECTIONS if not re.search(sec_pattern, body, re.IGNORECASE)])
        _validate_skill_links_in_body(s_dir, body, errs)
        _validate_skill_rules_and_evals(s_dir, errs)
    except (OSError, ValueError, KeyError) as e:
        errs.append(f"Erro ao analisar arquivo: {e}")
    return errs
