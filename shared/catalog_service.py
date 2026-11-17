"""
catalog_service.py
Serviço de descoberta, indexação de metadados, busca e validação determinística
do catálogo de Agent Skills do Franklin Quebra-Galho.
"""

from __future__ import annotations

import difflib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shared.modular_orchestrator import LoadedSkill, ProgressiveSkillRegistry, SkillMetadata
from shared.tools.frontmatter_parser import parse_frontmatter as _parse_frontmatter

ROOT_DIR = Path(__file__).resolve().parent.parent
CANONICAL_SKILLS_DIR = ROOT_DIR / "skills"
GLOBAL_PLUGIN_SKILLS_DIR = Path(r"C:\Users\melki\.gemini\config\plugins\franklin-skills\skills")
SHREDDED_SHAPE_ROOT = ROOT_DIR.parent / "shredded-shape"
SHREDDED_SHAPE_SKILLS_DIR = SHREDDED_SHAPE_ROOT / "skills"

if CANONICAL_SKILLS_DIR.exists():
    SKILLS_ROOT = CANONICAL_SKILLS_DIR
elif GLOBAL_PLUGIN_SKILLS_DIR.exists():
    SKILLS_ROOT = GLOBAL_PLUGIN_SKILLS_DIR
else:
    SKILLS_ROOT = CANONICAL_SKILLS_DIR

AGENTS_MD_PATH = ROOT_DIR / "AGENTS.md"
MY_SKILLS_MD_PATH = ROOT_DIR / "MY_SKILLS.md"
EPIC_VOLTA_DIR = ROOT_DIR.parent / "epic-volta"
if not EPIC_VOLTA_DIR.exists():
    EPIC_VOLTA_DIR = Path(r"C:\Users\melki\dev\repos\epic-volta")

CANONICAL_PERSONA_MAPPING: Dict[str, str] = {
    "ui-frontend-analyst": "UI-Architect",
    "ui-brand-ux-planner": "UI-Architect",
    "ui-clean-worker": "UI-Architect",
    "ui-quality-judge": "UI-Architect",
    "complex-zero": "UI-Architect",
    "clinical-minimalist-ui": "UI-Architect",
    "gdrive-cleanup-auditor": "DriveMaster",
    "gdrive-taxonomy-organizer": "DriveMaster",
    "windows-disk-maintenance": "FileOpsLocal",
    "obsidian-vault-curator": "VaultMaster",
    "technical-markdown-writer": "DocMaker",
    "html-pdf-converter": "DocMaker",
    "flow-filetree-organizer": "DocMaker",
    "code-acceptability-auditor": "SkillCraft",
    "test-quality-auditor": "SkillCraft",
    "agent-server-auditor": "SkillCraft",
    "re-a-ndroid": "SkillCraft",
    "high-level-context-planner": "LoopPlanner",
    "gap-analyzer-auditor": "LoopPlanner",
    "chained-plan-orchestrator": "LoopPlanner",
    "solution-content-architect": "Franklin-Main",
    "system-project-auditor": "Franklin-Main",
    "android-agy-projects": "Franklin-Main",
    "project-idea-organizer": "Franklin-Main",
    "code-quality-audit-3d-physics": "Franklin-Main",
    "context-sentinel": "Franklin-Main",
    "refine-prompt": "Franklin-Main",
    "EcosystemMatrix": "Franklin-Main",
}

QUICK_SKILL_ALIASES: Dict[str, str] = {
    # Canonical English slugs & short English aliases
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
    "conversor-pdf": "html-pdf-converter",
    "conversor-html-pdf": "html-pdf-converter",
    "obsidian": "obsidian-vault-curator",
    "vault": "obsidian-vault-curator",
    "vault-curator": "obsidian-vault-curator",
    "curadoria-obsidian-vault": "obsidian-vault-curator",
    "drive-limpeza": "gdrive-cleanup-auditor",
    "drive-cleanup": "gdrive-cleanup-auditor",
    "gdrive-auditoria-limpeza": "gdrive-cleanup-auditor",
    "drive-taxonomia": "gdrive-taxonomy-organizer",
    "drive-taxonomy": "gdrive-taxonomy-organizer",
    "gdrive-taxonomia-organizacao": "gdrive-taxonomy-organizer",
    "disco": "windows-disk-maintenance",
    "windows": "windows-disk-maintenance",
    "disk-maintenance": "windows-disk-maintenance",
    "manutencao-disco-windows": "windows-disk-maintenance",
    "medica": "clinical-minimalist-ui",
    "medico": "clinical-minimalist-ui",
    "medical-ui": "clinical-minimalist-ui",
    "clinical-ui": "clinical-minimalist-ui",
    "design-interface-medica-minimalista": "clinical-minimalist-ui",
    "sentinel": "context-sentinel",
    "code-auditor": "code-acceptability-auditor",
    "acceptability": "code-acceptability-auditor",
    "ast-auditor": "code-acceptability-auditor",
    "test-auditor": "test-quality-auditor",
    "evals": "test-quality-auditor",
    "qa-testes": "test-quality-auditor",
    "arquitetura": "system-project-auditor",
    "arquitetura-design-implementacao-sistema": "system-project-auditor",
    "nav-x-func": "system-project-auditor",
    "nav": "system-project-auditor",
    "ilhas": "system-project-auditor",
    "design": "ui-brand-ux-planner",
    "design.md": "ui-brand-ux-planner",
    "design-md": "ui-brand-ux-planner",
    "code-architect": "ui-clean-worker",
    "atomic-ui": "ui-clean-worker",
    "frontend-code-architect": "ui-clean-worker",
    "ui-testing": "ui-quality-judge",
    "frontend-auditor": "ui-quality-judge",
    "frontend-testing-auditor": "ui-quality-judge",
    "ui-ux-auditor": "ui-quality-judge",
    "frontend-ui-ux-auditor": "ui-quality-judge",
    "ux-auditor": "ui-quality-judge",
    "wcag-auditor": "ui-quality-judge",
    "sombra": "ui-clean-worker",
    "sombras": "ui-clean-worker",
    "tatil": "ui-clean-worker",
    "tactile": "ui-clean-worker",
    "elevacao": "ui-clean-worker",
    "bevel": "ui-clean-worker",
    "frontend": "ui-brand-ux-planner",
    "ui": "ui-brand-ux-planner",
    "consultor-ui": "ui-brand-ux-planner",
    "consultor-frontend": "ui-brand-ux-planner",
    "analise-ui": "ui-frontend-analyst",
    "analise-frontend": "ui-frontend-analyst",
    "refatorar-ui": "ui-clean-worker",
    "refatoracao-frontend": "ui-clean-worker",
    "prompt": "refine-prompt",
    "refinar": "refine-prompt",
    "refinar-prompt": "refine-prompt",
    "prompt-refine": "refine-prompt",
    "baixa-entropia": "refine-prompt",
    "entropia": "refine-prompt",
    "desengessar": "refine-prompt",
    "fluidez": "refine-prompt",
    "memoria": "obsidian-vault-curator",
    "palacio": "obsidian-vault-curator",
    "mempalace": "obsidian-vault-curator",
    "notas": "obsidian-vault-curator",
    "auditar": "system-project-auditor",
    "auditoria": "system-project-auditor",
    "projeto": "system-project-auditor",
    "repo": "system-project-auditor",
    "auditoria-projetos-sistema": "system-project-auditor",
    "antigravity-project-auditor": "system-project-auditor",
    "mvp-auditor": "system-project-auditor",
    "project-auditor": "system-project-auditor",
    "system-auditor": "system-project-auditor",
    "diagnostico-mvp": "system-project-auditor",
    "mvp": "system-project-auditor",
    "android": "android-agy-projects",
    "android-agy": "android-agy-projects",
    "android-agy-projects": "android-agy-projects",
    "compose": "android-agy-projects",
    "jetpack-compose": "android-agy-projects",
    "kotlin-android": "android-agy-projects",
    "agp9": "android-agy-projects",
    "gradle-android": "android-agy-projects",
    "organizar": "project-idea-organizer",
    "organizador": "project-idea-organizer",
    "organizar-projeto": "project-idea-organizer",
    "sincronizar-projeto": "project-idea-organizer",
    "organizador-projetos-ideias": "project-idea-organizer",
    "idea-organizer": "project-idea-organizer",
    "ideia": "project-idea-organizer",
    "ideias": "project-idea-organizer",
    "solucao": "solution-content-architect",
    "solucoes": "solution-content-architect",
    "arquiteto": "solution-content-architect",
    "arquiteto-conteudo-solucoes": "solution-content-architect",
    "solution-architect": "solution-content-architect",
    "fluxo": "flow-filetree-organizer",
    "arvore": "flow-filetree-organizer",
    "mermaid": "flow-filetree-organizer",
    "organizador-fluxo-arvore-arquivos": "flow-filetree-organizer",
    "flow-organizer": "flow-filetree-organizer",
    "markdown": "technical-markdown-writer",
    "relatorio": "technical-markdown-writer",
    "doc": "technical-markdown-writer",
    "redator-tecnico-markdown": "technical-markdown-writer",
    "markdown-writer": "technical-markdown-writer",
    "plano": "high-level-context-planner",
    "planejar": "high-level-context-planner",
    "planner": "high-level-context-planner",
    "intent-cognitive-planner": "high-level-context-planner",
    "cognitive-planner": "high-level-context-planner",
    "intencao": "high-level-context-planner",
    "parede-complexidade": "high-level-context-planner",
    "gap": "gap-analyzer-auditor",
    "rca": "gap-analyzer-auditor",
    "brechas": "gap-analyzer-auditor",
    "orquestrar": "chained-plan-orchestrator",
    "orquestrador": "chained-plan-orchestrator",
    "dag": "chained-plan-orchestrator",
    "kahn": "chained-plan-orchestrator",
    "ondas": "chained-plan-orchestrator",
    "skill-orquestrador-planos-encadeados": "chained-plan-orchestrator",
    "dag-orchestrator": "chained-plan-orchestrator",
    "server-auditor": "agent-server-auditor",
    "agent-auditor": "agent-server-auditor",
    "mcp-auditor": "agent-server-auditor",
    "a2a-auditor": "agent-server-auditor",
    "audit-skills": "agent-server-auditor",
    "audit-skills-antigravity": "agent-server-auditor",
    "rea-skills": "agent-server-auditor",
    "plan-uiux": "ui-frontend-analyst",
    "rea-uiux": "ui-frontend-analyst",
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


def _parse_agent_table_line(line: str, mapping: Dict[str, str]) -> None:
    """Extrai persona e skills de uma linha de tabela Markdown de AGENTS.md."""
    if "|" not in line or "`" not in line:
        return
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 5:
        return
    persona_match = re.search(r"^\*\*`([A-Za-z][A-Za-z0-9_\-]+)`\*\*$", parts[1])
    if not persona_match:
        return
    persona = persona_match.group(1)
    for s in re.findall(r"`([a-zA-Z0-9_\-]+)`", parts[3]):
        if s in mapping or (SKILLS_ROOT / s).is_dir():
            mapping[s] = persona


def _load_agents_map() -> Dict[str, str]:
    """Mapeia cada skill à sua persona especialista correspondente via AGENTS.md."""
    mapping = dict(CANONICAL_PERSONA_MAPPING)
    if not AGENTS_MD_PATH.exists():
        return mapping
    try:
        content = AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
        for line in content.splitlines():
            _parse_agent_table_line(line, mapping)
    except OSError as exc:
        _ = exc
    return mapping


def _load_status_map() -> Dict[str, str]:
    """Carrega o status do ciclo de vida das skills a partir de MY_SKILLS.md."""
    status_map: Dict[str, str] = {}
    if not MY_SKILLS_MD_PATH.exists():
        return status_map
    try:
        content = MY_SKILLS_MD_PATH.read_text(encoding="utf-8", errors="replace")
        for line in content.splitlines():
            parts = [p.strip() for p in line.split("|")] if ("|" in line and "**`" in line) else []
            skill_match = re.search(r"\*\*`([a-zA-Z0-9_\-]+)`\*\*", parts[1]) if len(parts) >= 5 else None
            if skill_match:
                status_map[skill_match.group(1)] = parts[3].strip()
    except OSError as exc:
        _ = exc
    return status_map


def _resolve_skill_rules_file(skill_dir: Path) -> Path:
    """Resolve o arquivo de regras da skill priorizando rules/audit_criteria.md com fallback legado."""
    audit_path = skill_dir / "rules" / "audit_criteria.md"
    if audit_path.exists():
        return audit_path
    return skill_dir / "rules" / "criterios_auditoria.md"


def _extract_meta_tags(meta: Dict[str, Any]) -> List[str]:
    """Extrai tags bilíngues de frontmatter (topo ou metadata.tags)."""
    raw_nested = meta.get("metadata")
    nested_tags = raw_nested.get("tags") if isinstance(raw_nested, dict) else None
    raw_tags = meta.get("tags") or nested_tags or []
    if isinstance(raw_tags, str):
        return [raw_tags]
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


def _list_dir_filenames(folder: Path) -> List[str]:
    """Retorna os nomes dos arquivos regulares dentro de uma pasta."""
    return [f.name for f in folder.iterdir() if f.is_file()] if folder.is_dir() else []


def _collect_skill_data(
    skill_dir: Path,
    agents_map: Optional[Dict[str, str]] = None,
    status_map: Optional[Dict[str, str]] = None,
) -> Optional[Dict[str, Any]]:
    """Lê metadados completos e estrutura de uma pasta de skill."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None
    try:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        meta, body = _parse_frontmatter(content)
        name = meta.get("name", skill_dir.name)
        version = meta.get("version", "v1.0.0")
        description = meta.get("description") or next(
            (ln.strip() for ln in body.splitlines() if ln.strip() and not ln.startswith("#")),
            "Skill sem descrição detalhada.",
        )
        rules_file = _resolve_skill_rules_file(skill_dir)
        evals_file = skill_dir / "evals" / "evals.json"
        ref_list = _list_dir_filenames(skill_dir / "references")
        scripts_list = _list_dir_filenames(skill_dir / "scripts")
        active_agents_map = agents_map if agents_map is not None else _load_agents_map()
        active_status_map = status_map if status_map is not None else _load_status_map()
        return {
            "name": name, "directory": skill_dir.name, "version": version,
            "status": active_status_map.get(skill_dir.name, active_status_map.get(name, "✅ Validada")),
            "persona": active_agents_map.get(skill_dir.name, active_agents_map.get(name, "Franklin-Main")),
            "description": description, "path": str(skill_file),
            "has_rules": rules_file.exists(), "has_evals": evals_file.exists(),
            "has_references": bool(ref_list), "references": ref_list,
            "has_scripts": bool(scripts_list), "scripts": scripts_list,
            "tags": _build_skill_tags(name, skill_dir.name, str(description), meta),
        }
    except (OSError, ValueError, KeyError):
        return None


def _get_all_skills_data() -> List[Dict[str, Any]]:
    """Varre o diretório de skills e consolida todos os metadados."""
    if not SKILLS_ROOT.exists():
        return []
    agents_map = _load_agents_map()
    status_map = _load_status_map()
    skills = []
    for item in sorted(SKILLS_ROOT.iterdir()):
        if item.is_dir():
            data = _collect_skill_data(item, agents_map=agents_map, status_map=status_map)
            if data:
                skills.append(data)
    return skills


def _match_exact_or_ci_dir(base_root: Path, target: str) -> Optional[Path]:
    """Busca pasta com nome exato ou case-insensitive dentro de base_root."""
    exact_path = base_root / target
    if exact_path.is_dir():
        return exact_path
    return next((d for d in base_root.iterdir() if d.is_dir() and d.name.lower() == target), None)


def _get_skill_search_roots() -> List[Path]:
    """Retorna as raízes de busca de skills (franklin + shredded-shape quando disponível)."""
    if SHREDDED_SHAPE_SKILLS_DIR.is_dir():
        return [SKILLS_ROOT, SHREDDED_SHAPE_SKILLS_DIR]
    return [SKILLS_ROOT]


def _find_skill_dir(skill_name: str) -> Optional[Path]:
    """Localiza o diretório de uma skill em SKILLS_ROOT ou no satélite federado shredded-shape."""
    clean = skill_name.strip().lower()
    if not clean or "inexistente" in clean:
        return None
    search_roots = _get_skill_search_roots()
    candidates = [c for c in (clean, QUICK_SKILL_ALIASES.get(clean, "")) if c]
    for candidate in candidates:
        for base_root in search_roots:
            found = _match_exact_or_ci_dir(base_root, candidate)
            if found:
                return found
    for base_root in search_roots:
        sub_matches = [d for d in base_root.iterdir() if d.is_dir() and clean in d.name.lower()]
        if len(sub_matches) == 1:
            return sub_matches[0]
    return None


def _filter_skills_catalog(skills: List[Dict[str, Any]], status: str, persona: str, search: str) -> List[Dict[str, Any]]:
    """Filtra a lista de skills por status, persona e termo textual."""
    filtered: List[Dict[str, Any]] = []
    status_low, persona_low, term = status.lower(), persona.lower(), search.strip().lower()
    for s in skills:
        if status_low != "all" and status_low not in s["status"].lower():
            continue
        if persona_low != "all" and persona_low not in s["persona"].lower():
            continue
        if term and term not in s["name"].lower() and term not in s["description"].lower():
            continue
        filtered.append(s)
    return filtered


def _format_skill_components(s: Dict[str, Any]) -> str:
    """Formata o resumo de componentes modulares de uma skill."""
    comps: List[str] = []
    if s["has_rules"]:
        comps.append("Rules [PASS/FAIL]")
    if s["has_references"]:
        comps.append(f"{len(s['references'])} Ref(s)")
    if s["has_evals"]:
        comps.append("Evals")
    if s["has_scripts"]:
        comps.append(f"{len(s['scripts'])} Script(s)")
    return ", ".join(comps) if comps else "Apenas Contrato"


def get_progressive_registry() -> ProgressiveSkillRegistry:
    """Instancia e popula o registro de Divulgação Progressiva em 3 níveis com precedência local > global."""
    reg = ProgressiveSkillRegistry(
        search_paths=[CANONICAL_SKILLS_DIR, GLOBAL_PLUGIN_SKILLS_DIR],
        persona_map=_load_agents_map(),
    )
    reg.discover_skills()
    return reg


def skills_list_impl(status: str = "all", persona: str = "all", search: str = "", format: str = "markdown") -> str:
    """Implementação da listagem filtrada de skills em Markdown, JSON ou XML Nível 1 (<available_skills>)."""
    if format.lower() == "xml":
        return get_progressive_registry().render_catalog_prompt()
    skills = _get_all_skills_data()
    if not skills:
        return f"Nenhuma skill encontrada no diretório: {SKILLS_ROOT}"
    filtered = _filter_skills_catalog(skills, status, persona, search)
    if format.lower() == "json":
        return json.dumps(filtered, indent=2, ensure_ascii=False)
    lines = [
        f"### 📦 Catálogo de Skills do Franklin Quebra-Galho ({len(filtered)}/{len(skills)} ativas)\n",
        f"> **Diretório Raiz**: `{SKILLS_ROOT}`\n",
        "| Skill | Versão | Status | Subagente Especialista | Componentes Modulares |",
        "| :--- | :---: | :---: | :--- | :--- |",
    ]
    for s in filtered:
        lines.append(f"| **`{s['name']}`** | `{s['version']}` | {s['status']} | `{s['persona']}` | {_format_skill_components(s)} |")
    lines.append("\n**Dica de Uso**: Utilize `franklin_skills_get(skill_name, section='activate')` (Nível 2) ou `franklin_skills_search(query)` para encontrar a skill exata.")
    return "\n".join(lines)


def _build_full_skill_package(skill_dir: Path) -> str:
    """Concatena contrato, rules, evals e referências de uma pasta de skill."""
    skill_file = skill_dir / "SKILL.md"
    rules_file = _resolve_skill_rules_file(skill_dir)
    evals_file = skill_dir / "evals" / "evals.json"
    ref_dir = skill_dir / "references"
    parts = [f"# PACOTE COMPLETO: {skill_dir.name.upper()}\n"]
    if skill_file.exists():
        parts.extend(["## 1. Contrato Operacional (SKILL.md)", skill_file.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 50) + "\n"])
    if rules_file.exists():
        parts.extend([f"## 2. Regras e Critérios de Auditoria (rules/{rules_file.name})", rules_file.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 50) + "\n"])
    if evals_file.exists():
        parts.extend(["## 3. Testes Estruturados (evals/evals.json)", evals_file.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 50) + "\n"])
    if ref_dir.exists() and any(ref_dir.iterdir()):
        parts.append("## 4. Documentos de Referência (references/)")
        for f in sorted(ref_dir.iterdir()):
            if f.is_file():
                parts.extend([f"### Referência: `{f.name}`", f.read_text(encoding="utf-8", errors="replace")])
        parts.append("\n" + ("=" * 50) + "\n")
    return "\n".join(parts)


def _render_skill_references(skill_dir: Path) -> str:
    """Renderiza os arquivos de references/ de uma skill."""
    ref_dir = skill_dir / "references"
    files = sorted(f for f in ref_dir.iterdir() if f.is_file()) if ref_dir.exists() else []
    if not files:
        return f"A skill '{skill_dir.name}' não possui referências adicionais (references/)."
    parts = [f"### Referências da Skill `{skill_dir.name}`:\n"]
    for f in files:
        parts.extend([f"#### Arquivo: `{f.name}`", f.read_text(encoding="utf-8", errors="replace"), "\n" + ("-" * 40) + "\n"])
    return "\n".join(parts)


def _render_skill_scripts(skill_dir: Path) -> str:
    """Lista os scripts executáveis de uma skill."""
    scripts_dir = skill_dir / "scripts"
    files = sorted(f for f in scripts_dir.iterdir() if f.is_file()) if scripts_dir.exists() else []
    if not files:
        return f"A skill '{skill_dir.name}' não possui scripts executáveis próprios (scripts/)."
    return "\n".join([f"### Scripts da Skill `{skill_dir.name}`:\n"] + [f"- **`{f.name}`** ({f.stat().st_size} bytes)" for f in files])


def _resolve_registry_for_skill(skill_dir: Path) -> ProgressiveSkillRegistry:
    """Obtém o registro progressivo correspondente à raiz da skill."""
    if SHREDDED_SHAPE_SKILLS_DIR.is_dir() and skill_dir.parent.resolve() == SHREDDED_SHAPE_SKILLS_DIR.resolve():
        reg = ProgressiveSkillRegistry(search_paths=[SHREDDED_SHAPE_SKILLS_DIR], persona_map=_load_agents_map())
        reg.discover_skills()
        return reg
    return get_progressive_registry()


def _format_missing_skill_err(skill_name: str) -> str:
    """Formata mensagem de erro com sugestões de nomes próximos."""
    all_names = [d.name for d in SKILLS_ROOT.iterdir() if d.is_dir()]
    suggestions = difflib.get_close_matches(skill_name, all_names, n=3, cutoff=0.4)
    sug_text = f" Sugestões: {', '.join(suggestions)}" if suggestions else ""
    return f"Erro: Skill '{skill_name}' não encontrada em {SKILLS_ROOT}.{sug_text}"


def skills_get_impl(skill_name: str, section: str = "contract") -> str:
    """Implementação da recuperação granular e Divulgação Progressiva (Níveis 2 e 3) de uma skill."""
    skill_dir = _find_skill_dir(skill_name)
    if not skill_dir:
        return _format_missing_skill_err(skill_name)

    sec_raw = section.strip()
    sec = sec_raw.lower()
    if sec in ("activate", "tier2", "progressive") or sec.startswith("resource:"):
        reg = _resolve_registry_for_skill(skill_dir)
        if sec.startswith("resource:"):
            return reg.read_skill_resource(skill_dir.name, sec_raw.split(":", 1)[1].strip())
        return reg.activate_skill(skill_dir.name)

    rules_path = _resolve_skill_rules_file(skill_dir)
    direct_files = {
        "contract": (skill_dir / "SKILL.md", f"Erro: SKILL.md ausente na pasta {skill_dir.name}."),
        "rules": (rules_path, f"A skill '{skill_dir.name}' não possui arquivo dedicado de regras (rules/audit_criteria.md)."),
        "evals": (skill_dir / "evals" / "evals.json", f"A skill '{skill_dir.name}' não possui arquivo de evals (evals/evals.json)."),
    }
    if sec in direct_files:
        f_path, missing_msg = direct_files[sec]
        return f_path.read_text(encoding="utf-8", errors="replace") if f_path.exists() else missing_msg
    handlers = {
        "references": _render_skill_references,
        "scripts": _render_skill_scripts,
        "all": _build_full_skill_package,
    }
    if sec in handlers:
        return handlers[sec](skill_dir)
    return "Seção '" + section + "' inválida. Opções: 'contract', 'activate', 'resource:<path>', 'rules', 'references', 'evals', 'scripts', 'all'."


SEARCH_STOPWORDS: frozenset[str] = frozenset({
    "de", "da", "do", "das", "dos", "para", "por", "em", "no", "na", "nos", "nas",
    "com", "sem", "ou", "e", "o", "a", "os", "as", "um", "uma", "ao", "aos", "que", "se", "use", "nao",
    "the", "and", "for", "with", "from", "into", "that", "this", "when", "not", "dont", "only", "after", "before", "instead",
})


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
    tag_Allowed = (not is_neg_hit) or (t in p_toks) or (t in name_norm)
    score = 10 if (t in norm_tags and tag_Allowed) else 0
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


def rank_skills_for_query(query: str, limit: int = 5) -> List[Tuple[int, Dict[str, Any]]]:
    """Retorna a lista ranqueada (score, skill_dict) para uma consulta em linguagem natural."""
    clean_q = query.strip().lower()
    q_norm = _strip_accents(clean_q)
    terms = re.findall(r"[a-z0-9_\-]+", q_norm)
    if not terms:
        return []
    skills = _get_all_skills_data()
    scored = sorted(
        ((sc, s) for s in skills if (sc := _score_skill_query(s, clean_q, terms)) > 0),
        key=lambda x: x[0],
        reverse=True,
    )
    return scored[:limit]


def skills_search_impl(query: str, limit: int = 5) -> str:
    """Implementação da busca ranqueada de skills por intenção."""
    clean_q = query.strip().lower()
    if not re.findall(r"[a-zA-Z0-9_\-]+", _strip_accents(clean_q)):
        return "Por favor, forneça termos de busca válidos."
    top_matches = rank_skills_for_query(query, limit=limit)
    if not top_matches:
        return f"Nenhuma skill encontrada para '{query}'. Use 'franklin_skills_list()' para inspecionar todas as opções."
    output = [f"### 🎯 Recomendações de Skills para: \"{query}\"\n"]
    for rank, (score, s) in enumerate(top_matches, start=1):
        output.extend([
            f"#### {rank}. **`{s['name']}`** (Relevância: {score} pts)",
            f"- **Subagente Recomendado**: `{s['persona']}`",
            f"- **Status**: {s['status']} | **Versão**: `{s['version']}`",
            f"- **Descrição**: {s['description']}",
            f"- **Comando para ler**: `franklin_skills_get(skill_name='{s['name']}')`\n",
        ])
    return "\n".join(output)


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


def skills_validate_impl(target_skill: str = "") -> str:
    """Implementação da validação contratual e estrutural de uma ou todas as skills."""
    if target_skill.strip():
        found = _find_skill_dir(target_skill.strip())
        if not found:
            return f"[FAIL] Skill '{target_skill}' não encontrada para validação."
        skills_to_validate = [found]
    else:
        skills_to_validate = sorted([d for d in SKILLS_ROOT.iterdir() if d.is_dir()])

    passed = 0
    failures: Dict[str, List[str]] = {}
    for s_dir in skills_to_validate:
        errs = _validate_single_skill_dir(s_dir)
        if errs:
            failures[s_dir.name] = errs
        else:
            passed += 1

    lines = [
        "=== AUDITORIA DETERMINÍSTICA DE SKILLS DO FRANKLIN ===",
        f"Total Inspecionado: {len(skills_to_validate)} | Aprovadas: {passed} | Falhas: {len(failures)}",
        "-" * 60,
    ]
    if failures:
        lines.append("[STATUS]: REPROVADO COM INCONFORMIDADES\n")
        for s_name, err_list in failures.items():
            lines.append(f"[FAIL] {s_name}:")
            lines.extend([f"   ↳ {err}" for err in err_list])
    else:
        lines.append("[STATUS]: 100% PASS - TODAS AS SKILLS EM CONFORMIDADE DETERMINÍSTICA")
    return "\n".join(lines)
