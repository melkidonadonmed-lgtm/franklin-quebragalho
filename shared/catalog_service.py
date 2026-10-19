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

from shared.tools.frontmatter_parser import parse_frontmatter as _parse_frontmatter

ROOT_DIR = Path(__file__).resolve().parent.parent
CANONICAL_SKILLS_DIR = ROOT_DIR / "skills"
AGENTS_SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
GLOBAL_PLUGIN_SKILLS_DIR = Path(r"C:\Users\melki\.gemini\config\plugins\franklin-skills\skills")

if CANONICAL_SKILLS_DIR.exists():
    SKILLS_ROOT = CANONICAL_SKILLS_DIR
elif AGENTS_SKILLS_DIR.exists():
    SKILLS_ROOT = AGENTS_SKILLS_DIR
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
    "design-interface-medica-minimalista": "FrontCraftMaster",
    "design-md": "FrontCraftMaster",
    "frontend-code-architect": "FrontCraftMaster",
    "frontend-testing-auditor": "FrontCraftMaster",
    "minimal-impact-ui": "FrontCraftMaster",
    "gdrive-auditoria-limpeza": "DriveMaster",
    "gdrive-taxonomia-organizacao": "DriveMaster",
    "manutencao-disco-windows": "FileOpsLocal",
    "curadoria-obsidian-vault": "VaultMaster",
    "redator-tecnico-markdown": "DocMaker",
    "conversor-html-pdf": "DocMaker",
    "organizador-fluxo-arvore-arquivos": "DocMaker",
    "evoluir-skills": "SkillCraft",
    "skill-auditor-refatorador-skills": "SkillCraft",
    "aprimoramento-expansibilidade-agentes-skills": "SkillCraft",
    "code-acceptability-auditor": "SkillCraft",
    "test-quality-auditor": "SkillCraft",
    "high-level-context-planner": "LoopPlanner",
    "gap-analyzer-auditor": "LoopPlanner",
    "skill-orquestrador-planos-encadeados": "LoopPlanner",
    "arquiteto-conteudo-solucoes": "Franklin-Main",
    "arquitetura-design-implementacao-sistema": "Franklin-Main",
    "auditoria-projetos-sistema": "Franklin-Main",
    "code-quality-audit-3d-physics": "Franklin-Main",
    "context-sentinel": "Franklin-Main",
    "refine-prompt": "Franklin-Main",
    "_template": "SkillCraft",
    "template-skill": "SkillCraft",
    "EcosystemMatrix": "Franklin-Main",
}

QUICK_SKILL_ALIASES: Dict[str, str] = {
    "3d": "code-quality-audit-3d-physics",
    "fisica": "code-quality-audit-3d-physics",
    "fisica-3d": "code-quality-audit-3d-physics",
    "physics": "code-quality-audit-3d-physics",
    "pdf": "conversor-html-pdf",
    "conversor-pdf": "conversor-html-pdf",
    "obsidian": "curadoria-obsidian-vault",
    "vault": "curadoria-obsidian-vault",
    "drive-limpeza": "gdrive-auditoria-limpeza",
    "drive-taxonomia": "gdrive-taxonomia-organizacao",
    "disco": "manutencao-disco-windows",
    "windows": "manutencao-disco-windows",
    "medica": "design-interface-medica-minimalista",
    "medico": "design-interface-medica-minimalista",
    "template": "_template",
    "sentinel": "context-sentinel",
    "code-auditor": "code-acceptability-auditor",
    "acceptability": "code-acceptability-auditor",
    "ast-auditor": "code-acceptability-auditor",
    "test-auditor": "test-quality-auditor",
    "evals": "test-quality-auditor",
    "qa-testes": "test-quality-auditor",
    "arquitetura": "arquitetura-design-implementacao-sistema",
    "ilhas": "arquitetura-design-implementacao-sistema",
    "design": "design-md",
    "design.md": "design-md",
    "code-architect": "frontend-code-architect",
    "atomic-ui": "frontend-code-architect",
    "ui-testing": "frontend-testing-auditor",
    "frontend-auditor": "frontend-testing-auditor",
    "minimal-impact-ui": "minimal-impact-ui",
    "minimal-ui": "minimal-impact-ui",
    "ex-umbris": "minimal-impact-ui",
    "atlas-ui": "minimal-impact-ui",
    "winui": "minimal-impact-ui",
    "frontend": "design-md",
    "ui": "design-md",
    "consultor-ui": "design-md",
    "consultor-frontend": "design-md",
    "analise-ui": "auditoria-projetos-sistema",
    "analise-frontend": "auditoria-projetos-sistema",
    "refatorar-ui": "frontend-code-architect",
    "refatoracao-frontend": "frontend-code-architect",
}

REQUIRED_SKILL_SECTIONS: List[Tuple[str, str]] = [
    (r"(#|##)\s+.*(Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao)", "Gatilhos / Quando Usar"),
    (r"(#|##)\s+.*(Entradas|Pr[eé]-requisitos|Par[aâ]metros)", "Entradas / Pré-requisitos"),
    (r"(#|##)\s+.*(Processamento|Passo a Passo|Fluxo|Execução|Execucao)", "Processamento / Fluxo"),
    (r"(#|##)\s+.*(Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida)", "Saídas / Entregáveis"),
    (r"(#|##)\s+.*(Exceções|Excecoes|Limites|Quando N[AÃ]O Usar)", "Exceções / Limites"),
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


def _collect_skill_data(skill_dir: Path) -> Optional[Dict[str, Any]]:
    """Lê metadados completos e estrutura de uma pasta de skill."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return None
    try:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
        meta, body = _parse_frontmatter(content)
        name = meta.get("name", skill_dir.name)
        version = meta.get("version", "v1.0.0")
        description = meta.get("description", "")
        if not description:
            lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.startswith("#")]
            description = lines[0] if lines else "Skill sem descrição detalhada."

        rules_file = skill_dir / "rules" / "criterios_auditoria.md"
        evals_file = skill_dir / "evals" / "evals.json"
        ref_dir = skill_dir / "references"
        scripts_dir = skill_dir / "scripts"
        scripts_list = [f.name for f in scripts_dir.iterdir() if f.is_file()] if scripts_dir.is_dir() else []
        ref_list = [f.name for f in ref_dir.iterdir() if f.is_file()] if ref_dir.is_dir() else []

        tags = {w for tok in (name, skill_dir.name, description) for w in re.findall(r"[a-zA-Z0-9_\-]+", tok.lower())}
        agents_map = _load_agents_map()
        status_map = _load_status_map()
        return {
            "name": name, "directory": skill_dir.name, "version": version,
            "status": status_map.get(skill_dir.name, status_map.get(name, "✅ Validada")),
            "persona": agents_map.get(skill_dir.name, agents_map.get(name, "Franklin-Main")),
            "description": description, "path": str(skill_file),
            "has_rules": rules_file.exists(), "has_evals": evals_file.exists(),
            "has_references": bool(ref_list), "references": ref_list,
            "has_scripts": bool(scripts_list), "scripts": scripts_list, "tags": sorted(tags),
        }
    except (OSError, ValueError, KeyError):
        return None


def _get_all_skills_data() -> List[Dict[str, Any]]:
    """Varre o diretório de skills e consolida todos os metadados."""
    if not SKILLS_ROOT.exists():
        return []
    skills = []
    for item in sorted(SKILLS_ROOT.iterdir()):
        if item.is_dir():
            data = _collect_skill_data(item)
            if data:
                skills.append(data)
    return skills


def _find_skill_dir(skill_name: str) -> Optional[Path]:
    """Localiza o diretório de uma skill por correspondência exata, alias amigável ou substring unívoca."""
    clean = skill_name.strip().lower()
    if not clean or "inexistente" in clean:
        return None
    exact_path = SKILLS_ROOT / clean
    if exact_path.exists() and exact_path.is_dir():
        return exact_path
    dirs = [d for d in SKILLS_ROOT.iterdir() if d.is_dir()]
    for d in dirs:
        if d.name.lower() == clean:
            return d
    if clean in QUICK_SKILL_ALIASES:
        alias_target = SKILLS_ROOT / QUICK_SKILL_ALIASES[clean]
        if alias_target.exists():
            return alias_target
    sub_matches = [d for d in dirs if clean in d.name.lower()]
    return sub_matches[0] if len(sub_matches) == 1 else None


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


def skills_list_impl(status: str = "all", persona: str = "all", search: str = "", format: str = "markdown") -> str:
    """Implementação da listagem filtrada de skills em Markdown ou JSON."""
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
    lines.append("\n**Dica de Uso**: Utilize `franklin_skills_get(skill_name)` para ler o contrato da skill ou `franklin_skills_search(query)` para encontrar a skill exata.")
    return "\n".join(lines)


def _build_full_skill_package(skill_dir: Path) -> str:
    """Concatena contrato, rules, evals e referências de uma pasta de skill."""
    skill_file = skill_dir / "SKILL.md"
    rules_file = skill_dir / "rules" / "criterios_auditoria.md"
    evals_file = skill_dir / "evals" / "evals.json"
    ref_dir = skill_dir / "references"
    parts = [f"# PACOTE COMPLETO: {skill_dir.name.upper()}\n"]
    if skill_file.exists():
        parts.extend(["## 1. Contrato Operacional (SKILL.md)", skill_file.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 50) + "\n"])
    if rules_file.exists():
        parts.extend(["## 2. Regras e Critérios de Auditoria (rules/criterios_auditoria.md)", rules_file.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 50) + "\n"])
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


def skills_get_impl(skill_name: str, section: str = "contract") -> str:
    """Implementação da recuperação granular de seções de uma skill."""
    skill_dir = _find_skill_dir(skill_name)
    if not skill_dir:
        all_names = [d.name for d in SKILLS_ROOT.iterdir() if d.is_dir()]
        suggestions = difflib.get_close_matches(skill_name, all_names, n=3, cutoff=0.4)
        sug_text = f" Sugestões: {', '.join(suggestions)}" if suggestions else ""
        return f"Erro: Skill '{skill_name}' não encontrada em {SKILLS_ROOT}.{sug_text}"

    sec = section.strip().lower()
    direct_files = {
        "contract": (skill_dir / "SKILL.md", f"Erro: SKILL.md ausente na pasta {skill_dir.name}."),
        "rules": (skill_dir / "rules" / "criterios_auditoria.md", f"A skill '{skill_dir.name}' não possui arquivo dedicado de regras (rules/criterios_auditoria.md)."),
        "evals": (skill_dir / "evals" / "evals.json", f"A skill '{skill_dir.name}' não possui arquivo de evals (evals/evals.json)."),
    }
    if sec in direct_files:
        f_path, missing_msg = direct_files[sec]
        return f_path.read_text(encoding="utf-8", errors="replace") if f_path.exists() else missing_msg
    if sec == "references":
        return _render_skill_references(skill_dir)
    if sec == "scripts":
        return _render_skill_scripts(skill_dir)
    if sec == "all":
        return _build_full_skill_package(skill_dir)
    return f"Seção '{section}' inválida. Opções: 'contract', 'rules', 'references', 'evals', 'scripts', 'all'."


def _score_skill_query(s: Dict[str, Any], clean_q: str, terms: List[str]) -> int:
    """Calcula a pontuação de relevância de uma skill para uma consulta textual."""
    score = 0
    name_lower, desc_lower, persona_lower = s["name"].lower(), s["description"].lower(), s["persona"].lower()
    if clean_q in name_lower:
        score += 50
    if clean_q in desc_lower:
        score += 30
    for t in terms:
        if t in name_lower:
            score += 15
        if t in s["tags"]:
            score += 10
        if t in desc_lower:
            score += 5
        if t in persona_lower:
            score += 8
    return score


def skills_search_impl(query: str, limit: int = 5) -> str:
    """Implementação da busca ranqueada de skills por intenção."""
    clean_q = query.strip().lower()
    terms = re.findall(r"[a-zA-Z0-9_\-]+", clean_q)
    if not terms:
        return "Por favor, forneça termos de busca válidos."
    skills = _get_all_skills_data()
    scored = sorted(((sc, s) for s in skills if (sc := _score_skill_query(s, clean_q, terms)) > 0), key=lambda x: x[0], reverse=True)
    top_matches = scored[:limit]
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


def _validate_skill_rules_and_evals(s_dir: Path, errs: List[str]) -> None:
    """Valida rules/criterios_auditoria.md e evals/evals.json de uma pasta de skill."""
    rules_file = s_dir / "rules" / "criterios_auditoria.md"
    if rules_file.exists():
        rules_text = rules_file.read_text(encoding="utf-8")
        if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
            errs.append("rules/criterios_auditoria.md deve conter marcadores [PASS] e [FAIL]")
    evals_file = s_dir / "evals" / "evals.json"
    if not evals_file.exists():
        return
    try:
        evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
        evals_list = evals_data.get("evals", []) if isinstance(evals_data, dict) else (evals_data if isinstance(evals_data, list) else [])
        if not isinstance(evals_list, list) or len(evals_list) == 0:
            errs.append("evals.json deve conter uma lista não-vazia de testes")
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as e:
        errs.append(f"Sintaxe JSON inválida em evals.json: {e}")


def _validate_single_skill_dir(s_dir: Path) -> List[str]:
    """Valida a conformidade contratual, frontmatter, rules e evals de uma pasta de skill."""
    errs: List[str] = []
    skill_file = s_dir / "SKILL.md"
    if not skill_file.exists():
        return ["Arquivo SKILL.md inexistente"]
    try:
        content = skill_file.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(content)
        if not meta:
            errs.append("Frontmatter YAML ausente ou malformado")
        missing = [req for req in ("name", "description", "version") if not meta.get(req)]
        errs.extend([f"Campo obrigatório '{req}' ausente no frontmatter" for req in missing])
        is_template = s_dir.name == "_template" and meta.get("name") == "template-skill"
        if meta.get("name") and meta["name"] != s_dir.name and not is_template:
            errs.append(f"Nome no frontmatter ('{meta['name']}') difere da pasta ('{s_dir.name}')")
        errs.extend([f"Seção obrigatória ausente: {sec_name}" for sec_pattern, sec_name in REQUIRED_SKILL_SECTIONS if not re.search(sec_pattern, body, re.IGNORECASE)])
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
