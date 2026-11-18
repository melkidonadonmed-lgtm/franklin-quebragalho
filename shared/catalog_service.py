"""
catalog_service.py
Serviço de descoberta, indexação de metadados, busca e validação determinística
do catálogo de Agent Skills do Franklin Quebra-Galho.
"""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shared._catalog_scoring import (
    CANONICAL_PERSONA_MAPPING,
    QUICK_SKILL_ALIASES,
    REQUIRED_SKILL_SECTIONS,
    SEARCH_STOPWORDS,
    _build_skill_tags,
    _extract_eval_cases_list,
    _extract_meta_tags,
    _has_negative_token_match,
    _is_positive_desc_hit,
    _resolve_skill_rules_file,
    _score_desc_and_tag_hits,
    _score_single_term,
    _score_skill_query,
    _split_positive_and_negative_desc,
    _strip_accents,
    _validate_single_skill_dir,
    _validate_skill_desc_budget,
    _validate_skill_links_in_body,
    _validate_skill_meta_fields,
    _validate_skill_rules_and_evals,
)
from shared.modular_orchestrator import ProgressiveSkillRegistry
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


__all__ = [
    "AGENTS_MD_PATH",
    "CANONICAL_PERSONA_MAPPING",
    "CANONICAL_SKILLS_DIR",
    "EPIC_VOLTA_DIR",
    "GLOBAL_PLUGIN_SKILLS_DIR",
    "MY_SKILLS_MD_PATH",
    "QUICK_SKILL_ALIASES",
    "REQUIRED_SKILL_SECTIONS",
    "ROOT_DIR",
    "SEARCH_STOPWORDS",
    "SHREDDED_SHAPE_ROOT",
    "SHREDDED_SHAPE_SKILLS_DIR",
    "SKILLS_ROOT",
    "_build_skill_tags",
    "_extract_eval_cases_list",
    "_extract_meta_tags",
    "_find_skill_dir",
    "_get_all_skills_data",
    "_has_negative_token_match",
    "_is_positive_desc_hit",
    "_load_agents_map",
    "_resolve_skill_rules_file",
    "_score_desc_and_tag_hits",
    "_score_single_term",
    "_score_skill_query",
    "_split_positive_and_negative_desc",
    "_strip_accents",
    "_validate_single_skill_dir",
    "_validate_skill_desc_budget",
    "_validate_skill_links_in_body",
    "_validate_skill_meta_fields",
    "_validate_skill_rules_and_evals",
    "get_progressive_registry",
    "rank_skills_for_query",
    "skills_get_impl",
    "skills_list_impl",
    "skills_search_impl",
    "skills_validate_impl",
]
