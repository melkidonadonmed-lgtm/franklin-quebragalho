"""
Franklin Skills MCP Server
Servidor MCP Global para o ecossistema de Skills do Franklin Quebra-Galho (Padrão 2026).
Fornece ferramentas, recursos e prompts para descoberta, inspeção progressiva,
pesquisa por intenção, validação determinística e execução segura de scripts de skills.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
import sys
import typing
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Compatibilidade Python 3.15+ para beartype/FastMCP durante serialização JSON-RPC tools/list
if not hasattr(typing, "no_type_check_decorator"):
    typing.no_type_check_decorator = lambda f: f  # type: ignore[attr-defined]
try:
    import beartype.claw
    beartype.claw.beartype_this_package = lambda *a, **kw: None  # type: ignore[assignment]
except ImportError as _beartype_err:
    _ = _beartype_err

from fastmcp import FastMCP

# Blindagem de codificação para consoles Windows (PowerShell/CMD)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# -----------------------------------------------------------------------------
# Inicialização da Instância FastMCP
# -----------------------------------------------------------------------------
mcp = FastMCP("Franklin Skills MCP")

# Diretórios Canônicos do Workspace e Plugins Globais
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

AGENTS_SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
GLOBAL_PLUGIN_SKILLS_DIR = Path(r"C:\Users\melki\.gemini\config\plugins\franklin-skills\skills")

# Resolução dinâmica do diretório de skills com prioridade para o repositório local
if AGENTS_SKILLS_DIR.exists():
    SKILLS_ROOT = AGENTS_SKILLS_DIR
elif GLOBAL_PLUGIN_SKILLS_DIR.exists():
    SKILLS_ROOT = GLOBAL_PLUGIN_SKILLS_DIR
else:
    SKILLS_ROOT = ROOT_DIR / "skills"

AGENTS_MD_PATH = ROOT_DIR / "AGENTS.md"
MY_SKILLS_MD_PATH = ROOT_DIR / "MY_SKILLS.md"
EPIC_VOLTA_DIR = ROOT_DIR.parent / "epic-volta"
if not EPIC_VOLTA_DIR.exists():
    EPIC_VOLTA_DIR = Path(r"C:\Users\melki\dev\repos\epic-volta")


# -----------------------------------------------------------------------------
# Utilitários de Parsing de Metadados e Estado
# -----------------------------------------------------------------------------
from shared.a2a_bridge import (
    FranklinA2ATaskManager,
    build_franklin_agent_card,
    sanitize_external_agent_card,
    verify_agent_card_signature,
)
from shared.tools.frontmatter_parser import parse_frontmatter as _parse_frontmatter
from shared.harness import (
    CheckpointRecord,
    CheckpointStore,
    RiskLevel,
    SecurityViolationError,
    SemanticGuard,
    dispatch_harness2_action,
    evaluate_action_risk,
)
from shared.mcp_2026_advisor import evaluate_mcp_2026_architecture

SESSIONS_DIR = ROOT_DIR / ".sessions"
CHECKPOINTS_FILE = SESSIONS_DIR / "harness_checkpoints.json"
harness_store = CheckpointStore(CHECKPOINTS_FILE)
a2a_task_manager = FranklinA2ATaskManager(SKILLS_ROOT, harness_store)

CANONICAL_PERSONA_MAPPING: Dict[str, str] = {
    "analise-design-tatil-frontend": "FrontCraftMaster",
    "refatoracao-design-tatil-frontend": "FrontCraftMaster",
    "consultor-design-tatil-frontend": "FrontCraftMaster",
    "design-interface-medica-minimalista": "FrontCraftMaster",
    "design-md": "FrontCraftMaster",
    "frontend-code-architect": "FrontCraftMaster",
    "frontend-testing-auditor": "FrontCraftMaster",
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
    "frontend": "consultor-design-tatil-frontend",
    "ui": "consultor-design-tatil-frontend",
    "consultor-ui": "consultor-design-tatil-frontend",
    "consultor-frontend": "consultor-design-tatil-frontend",
    "analise-ui": "analise-design-tatil-frontend",
    "analise-frontend": "analise-design-tatil-frontend",
    "refatorar-ui": "refatoracao-design-tatil-frontend",
    "refatoracao-frontend": "refatoracao-design-tatil-frontend",
}


def _load_agents_map() -> Dict[str, str]:
    """Mapeia cada skill à sua persona especialista correspondente via AGENTS.md."""
    mapping = dict(CANONICAL_PERSONA_MAPPING)
    if AGENTS_MD_PATH.exists():
        try:
            content = AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines():
                if "|" in line and "`" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 5:
                        persona_match = re.search(r"^\*\*`([A-Za-z][A-Za-z0-9_\-]+)`\*\*$", parts[1])
                        if persona_match:
                            persona = persona_match.group(1)
                            skills_in_line = re.findall(r"`([a-zA-Z0-9_\-]+)`", parts[3])
                            for s in skills_in_line:
                                if s in mapping or (SKILLS_ROOT / s).is_dir():
                                    mapping[s] = persona
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
            if "|" in line and "**`" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5:
                    skill_match = re.search(r"\*\*`([a-zA-Z0-9_\-]+)`\*\*", parts[1])
                    if skill_match:
                        skill_name = skill_match.group(1)
                        status_map[skill_name] = parts[3].strip()
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
            lines = [l.strip() for l in body.splitlines() if l.strip() and not l.startswith("#")]
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
            "name": name,
            "directory": skill_dir.name,
            "version": version,
            "status": status_map.get(skill_dir.name, status_map.get(name, "✅ Validada")),
            "persona": agents_map.get(skill_dir.name, agents_map.get(name, "Franklin-Main")),
            "description": description,
            "path": str(skill_file),
            "has_rules": rules_file.exists(),
            "has_evals": evals_file.exists(),
            "has_references": bool(ref_list),
            "references": ref_list,
            "has_scripts": bool(scripts_list),
            "scripts": scripts_list,
            "tags": sorted(tags),
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


# -----------------------------------------------------------------------------
# Ferramentas MCP (Tools) e Helpers Modulares (SRP <= 60 linhas)
# -----------------------------------------------------------------------------
def _filter_skills_catalog(
    skills: List[Dict[str, Any]],
    status: str,
    persona: str,
    search: str,
) -> List[Dict[str, Any]]:
    """Filtra a lista de skills por status, persona e termo textual."""
    filtered: List[Dict[str, Any]] = []
    status_low = status.lower()
    persona_low = persona.lower()
    term = search.strip().lower()
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


@mcp.tool()
def franklin_skills_list(
    status: str = "all",
    persona: str = "all",
    search: str = "",
    format: str = "markdown"
) -> str:
    """Lista todas as Agent Skills do catálogo do Franklin Quebra-Galho com filtros e status.
    Args:
        status: Filtro por status do ciclo de vida ('all', 'validada', 'producao', 'teste', 'ideia').
        persona: Filtro por subagente ('all', 'FrontCraftMaster', 'DriveMaster', 'FileOpsLocal', 'VaultMaster', 'DocMaker', 'SkillCraft', 'LoopPlanner', 'Franklin-Main').
        search: Termo opcional para filtrar por nome ou descrição.
        format: Formato de saída ('markdown' ou 'json').
    """
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
        comp_str = _format_skill_components(s)
        lines.append(f"| **`{s['name']}`** | `{s['version']}` | {s['status']} | `{s['persona']}` | {comp_str} |")

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


@mcp.tool()
def franklin_skills_get(
    skill_name: str,
    section: str = "contract"
) -> str:
    """Recupera as instruções, regras ou dados de uma skill com suporte a divulgação progressiva.
    Args:
        skill_name: Nome exato ou aproximado da skill (ex: 'arquiteto-conteudo-solucoes', 'conversor-html-pdf', 'gdrive-auditoria-limpeza').
        section: Seção para carregamento granular ('contract', 'rules', 'references', 'evals', 'scripts', 'all').
    """
    skill_dir = _find_skill_dir(skill_name)
    if not skill_dir:
        all_names = [d.name for d in SKILLS_ROOT.iterdir() if d.is_dir()]
        suggestions = difflib.get_close_matches(skill_name, all_names, n=3, cutoff=0.4)
        sug_text = f" Sugestões: {', '.join(suggestions)}" if suggestions else ""
        return f"Erro: Skill '{skill_name}' não encontrada em {SKILLS_ROOT}.{sug_text}"

    sec = section.strip().lower()
    if sec == "contract":
        skill_file = skill_dir / "SKILL.md"
        return skill_file.read_text(encoding="utf-8", errors="replace") if skill_file.exists() else f"Erro: SKILL.md ausente na pasta {skill_dir.name}."
    if sec == "rules":
        rules_file = skill_dir / "rules" / "criterios_auditoria.md"
        return rules_file.read_text(encoding="utf-8", errors="replace") if rules_file.exists() else f"A skill '{skill_dir.name}' não possui arquivo dedicado de regras (rules/criterios_auditoria.md)."
    if sec == "evals":
        evals_file = skill_dir / "evals" / "evals.json"
        return evals_file.read_text(encoding="utf-8", errors="replace") if evals_file.exists() else f"A skill '{skill_dir.name}' não possui arquivo de evals (evals/evals.json)."
    if sec == "references":
        ref_dir = skill_dir / "references"
        if not ref_dir.exists() or not any(ref_dir.iterdir()):
            return f"A skill '{skill_dir.name}' não possui referências adicionais (references/)."
        parts = [f"### Referências da Skill `{skill_dir.name}`:\n"]
        for f in sorted(ref_dir.iterdir()):
            if f.is_file():
                parts.extend([f"#### Arquivo: `{f.name}`", f.read_text(encoding="utf-8", errors="replace"), "\n" + ("-" * 40) + "\n"])
        return "\n".join(parts)
    if sec == "scripts":
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists() or not any(scripts_dir.iterdir()):
            return f"A skill '{skill_dir.name}' não possui scripts executáveis próprios (scripts/)."
        return "\n".join([f"### Scripts da Skill `{skill_dir.name}`:\n"] + [f"- **`{f.name}`** ({f.stat().st_size} bytes)" for f in sorted(scripts_dir.iterdir()) if f.is_file()])
    if sec == "all":
        return _build_full_skill_package(skill_dir)
    return f"Seção '{section}' inválida. Opções: 'contract', 'rules', 'references', 'evals', 'scripts', 'all'."


def _score_skill_query(s: Dict[str, Any], clean_q: str, terms: List[str]) -> int:
    """Calcula a pontuação de relevância de uma skill para uma consulta textual."""
    score = 0
    name_lower = s["name"].lower()
    desc_lower = s["description"].lower()
    persona_lower = s["persona"].lower()
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


@mcp.tool()
def franklin_skills_search(
    query: str,
    limit: int = 5
) -> str:
    """Busca inteligente de skills por intenção operacional, palavras-chave, tags ou descrição.
    Args:
        query: Descrição do que você deseja realizar (ex: 'limpar downloads e instaladores', 'converter markdown em pdf', 'auditar tela de frontend', 'organizar duplicatas no drive').
        limit: Quantidade máxima de recomendações sugeridas.
    """
    clean_q = query.strip().lower()
    terms = re.findall(r"[a-zA-Z0-9_\-]+", clean_q)
    if not terms:
        return "Por favor, forneça termos de busca válidos."

    skills = _get_all_skills_data()
    scored = [(sc, s) for s in skills if (sc := _score_skill_query(s, clean_q, terms)) > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
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


REQUIRED_SKILL_SECTIONS: List[Tuple[str, str]] = [
    (r"(#|##)\s+.*(Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao)", "Gatilhos / Quando Usar"),
    (r"(#|##)\s+.*(Entradas|Pr[eé]-requisitos|Par[aâ]metros)", "Entradas / Pré-requisitos"),
    (r"(#|##)\s+.*(Processamento|Passo a Passo|Fluxo|Execução|Execucao)", "Processamento / Fluxo"),
    (r"(#|##)\s+.*(Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida)", "Saídas / Entregáveis"),
    (r"(#|##)\s+.*(Exceções|Excecoes|Limites|Quando N[AÃ]O Usar)", "Exceções / Limites"),
]


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
        for req in ("name", "description", "version"):
            if req not in meta or not meta[req]:
                errs.append(f"Campo obrigatório '{req}' ausente no frontmatter")
        if "name" in meta and meta["name"] != s_dir.name:
            if not (s_dir.name == "_template" and meta["name"] == "template-skill"):
                errs.append(f"Nome no frontmatter ('{meta['name']}') difere da pasta ('{s_dir.name}')")
        for sec_pattern, sec_name in REQUIRED_SKILL_SECTIONS:
            if not re.search(sec_pattern, body, re.IGNORECASE):
                errs.append(f"Seção obrigatória ausente: {sec_name}")

        rules_file = s_dir / "rules" / "criterios_auditoria.md"
        if rules_file.exists():
            rules_text = rules_file.read_text(encoding="utf-8")
            if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
                errs.append("rules/criterios_auditoria.md deve conter marcadores [PASS] e [FAIL]")

        evals_file = s_dir / "evals" / "evals.json"
        if evals_file.exists():
            try:
                evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
                evals_list = evals_data.get("evals", []) if isinstance(evals_data, dict) else (evals_data if isinstance(evals_data, list) else [])
                if not isinstance(evals_list, list) or len(evals_list) == 0:
                    errs.append("evals.json deve conter uma lista não-vazia de testes")
            except (OSError, json.JSONDecodeError, ValueError, TypeError) as e:
                errs.append(f"Sintaxe JSON inválida em evals.json: {e}")
    except (OSError, ValueError, KeyError) as e:
        errs.append(f"Erro ao analisar arquivo: {e}")
    return errs


@mcp.tool()
def franklin_skills_validate(
    target_skill: str = ""
) -> str:
    """Executa auditoria determinística de conformidade estrutural, contratual e semântica das skills.
    Args:
        target_skill: Nome de uma skill específica para validar, ou vazio para validar todas as 29 skills.
    """
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

    total = len(skills_to_validate)
    lines = [
        "=== AUDITORIA DETERMINÍSTICA DE SKILLS DO FRANKLIN ===",
        f"Total Inspecionado: {total} | Aprovadas: {passed} | Falhas: {len(failures)}",
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


def _resolve_agents_dir() -> Path:
    """Localiza o diretório de contratos de subagentes (agents/)."""
    for candidate in (
        ROOT_DIR / ".agents" / "agents",
        ROOT_DIR / "agents",
        Path(r"C:\Users\melki\.gemini\config\plugins\franklin-skills\agents"),
        Path(r"C:\Users\melki\.gemini\config\agents"),
        Path(r"C:\Users\melki\.gemini\agents"),
    ):
        if candidate.exists() and candidate.is_dir():
            return candidate
    return ROOT_DIR / "agents"


UI_SUBAGENT_ALIASES: Dict[str, str] = {
    "shell": "ui-shell-navigator",
    "navigator": "ui-shell-navigator",
    "onda1": "ui-shell-navigator",
    "wave1": "ui-shell-navigator",
    "ui_shell_navigator": "ui-shell-navigator",
    "controls": "ui-controls-data",
    "data": "ui-controls-data",
    "onda2a": "ui-controls-data",
    "wave2a": "ui-controls-data",
    "ui_controls_data": "ui-controls-data",
    "motion": "ui-motion-interaction",
    "interaction": "ui-motion-interaction",
    "onda2b": "ui-motion-interaction",
    "wave2b": "ui-motion-interaction",
    "ui_motion_interaction": "ui-motion-interaction",
    "observer": "ui-deterministic-observer",
    "gatekeeper": "ui-deterministic-observer",
    "onda3": "ui-deterministic-observer",
    "wave3": "ui-deterministic-observer",
    "ui_deterministic_observer": "ui-deterministic-observer",
}

PERSONA_ALIASES: Dict[str, str] = {
    "franklin": "Franklin-Main",
    "franklin-main": "Franklin-Main",
    "main": "Franklin-Main",
    "drivemaster": "DriveMaster",
    "drive": "DriveMaster",
    "subagent-drive-master": "DriveMaster",
    "fileopslocal": "FileOpsLocal",
    "fileops": "FileOpsLocal",
    "subagent-file-ops-local": "FileOpsLocal",
    "docmaker": "DocMaker",
    "subagent-doc-maker": "DocMaker",
    "skillcraft": "SkillCraft",
    "subagent-skill-craft": "SkillCraft",
    "frontcraftmaster": "FrontCraftMaster",
    "frontcraft": "FrontCraftMaster",
    "subagent-frontcraft-master": "FrontCraftMaster",
    "vaultmaster": "VaultMaster",
    "subagent-vault-master": "VaultMaster",
    "loopplanner": "LoopPlanner",
    "subagent-loop-planner": "LoopPlanner",
}


def _render_ecosystem_topology() -> str:
    """Renderiza a topologia interativa de agentes em 5 camadas e 29 skills."""
    skills = _get_all_skills_data()
    by_persona: Dict[str, List[str]] = {}
    for s in skills:
        by_persona.setdefault(s["persona"], []).append(s["name"])
    lines = [
        "# ⚡ Topologia Interativa de Agentes Multi-Repo (5 Camadas • 13 Repositórios)\n",
        "## 1. Camadas de Execução e Custo Cognitivo",
        "- **Camada 0 (Bússola & Heartbeat Zero-LLM — 0 tokens)**: `franklin_smart_compass()`, `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1`, `POST /rpc` (`mesh/heartbeat` em `adk-tests`).",
        "- **Camada 1 (Orquestração & Loop Fechado)**: `Franklin-Main` (Execução Direta) e `LoopPlanner` (`high-level-context-planner` Fase 0 -> `skill-orquestrador-planos-encadeados` -> `gap-analyzer-auditor`).",
        "- **Camada 2 (Esquadrão Frontend Soft Tactile `DESIGN.md v4.5-soft` — Topologia 3+1)**: `FrontCraftMaster` + `ui-shell-navigator` (Onda 1) -> `ui-controls-data` + `ui-motion-interaction` (Onda 2) -> `ui-deterministic-observer` (Onda 3 Gatekeeper `AUDIT-VIS-01 >= 90`).",
        "- **Camada 3 (Gatekeepers Determinísticos AST/Pass@k — 0 tokens)**: `SkillCraft` (`code-acceptability-auditor` Score >= 75, `test-quality-auditor`), `3D Physics Auditor` (`franklin_execute_dag('physics')`) e `dispatch_skill_deterministic_tests` (Go Eval Harness).",
        "- **Camada 4 (Malha Multiagente Cloud/Web & Clínica)**: `adk-tests` (`mesh_hybrid_orchestrator`, `self_healing_specialist`, `customer_issue_reviewer`, `AgyCalcCluster`), `epic-volta` (`DAGEngine` Kahn + `MCPBridgeAgent` + `ContextSentinel`), `mcp-web-agents` (Gateway 4+1 + `watchdogBridge.ts`) e `PCM`/`scoreboard` (`prescmed-clinical-reviewer`).\n",
        "## 2. Personas Especialistas & Skills Vinculadas (`franklin-quebragalho`)",
    ]
    for p_name, s_list in sorted(by_persona.items()):
        lines.append(f"- **`{p_name}`** ({len(s_list)} skills): `{', '.join(sorted(s_list))}`")
    lines.extend([
        "\n## 3. Comandos Interativos de 1 Clique",
        "- **Terminal Hub Interativo**: `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1`",
        "- **Executar DAG UI (3 Ondas)**: `franklin_execute_dag(plan_path_or_json='ui')`",
        "- **Executar DAG Física 3D (3 Ondas)**: `franklin_execute_dag(plan_path_or_json='physics')`",
        "- **Auditar Código Python (AST)**: `franklin_run_skill_script(skill_name='code-auditor', script_name='code_acceptability_auditor.py', args=['--self-test'])`",
    ])
    return "\n".join(lines)


def _extract_persona_details(canonical_persona: str) -> str:
    """Extrai a seção dedicada de uma persona de MY_AGENTS.md e anexa suas skills ativas."""
    my_agents_path = ROOT_DIR / "MY_AGENTS.md"
    section_text = ""
    if my_agents_path.exists():
        raw = my_agents_path.read_text(encoding="utf-8", errors="replace")
        header_term = "Franklin Quebra-Galho" if canonical_persona == "Franklin-Main" else canonical_persona
        chunks = re.split(r"\n---\n", raw)
        for ch in chunks:
            if header_term.lower() in ch.lower() and "## " in ch:
                section_text = ch.strip()
                break
    skills = [s["name"] for s in _get_all_skills_data() if s["persona"].lower() == canonical_persona.lower()]
    skills_block = f"\n\n### Skills Vinculadas a `{canonical_persona}` ({len(skills)}):\n- `" + "`, `".join(sorted(skills)) + "`" if skills else ""
    return (section_text or f"## Persona: {canonical_persona}") + skills_block


@mcp.tool()
def franklin_get_agents(agent_name: str = "") -> str:
    """Retorna o catálogo oficial dos Subagentes Especialistas do Franklin Quebra-Galho, a Topologia Multi-Repo (5 Camadas) ou o contrato detalhado de um subagente de UI (Topologia 3+1).
    Args:
        agent_name: Vazio para retornar o AGENTS.md completo; 'ecosystem'/'matrix'/'topology' para a topologia de agentes nos 13 repos;
                    'ui' ou '3+1' para retornar todos os 4 subagentes de UI; nome da persona ('skillcraft', 'loopplanner', 'drivemaster', etc.);
                    ou o nome/atalho do subagente ('ui-shell-navigator', 'ui-controls-data', 'ui-motion-interaction', 'ui-deterministic-observer').
    """
    clean = agent_name.strip().lower()
    if not clean:
        return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace") if AGENTS_MD_PATH.exists() else "Arquivo AGENTS.md não encontrado na raiz do workspace."

    if clean in ("ecosystem", "topology", "matrix", "all", "multi-repo", "repos"):
        return _render_ecosystem_topology()

    agents_dir = _resolve_agents_dir()
    if clean in ("ui", "3+1", "all-ui", "subagentes-ui"):
        ordered = ("ui-shell-navigator.md", "ui-controls-data.md", "ui-motion-interaction.md", "ui-deterministic-observer.md")
        parts = ["# Esquadrão de Subagentes de UI (`Topologia 3+1` sob `FrontCraftMaster`)\n"]
        for fname in ordered:
            fpath = agents_dir / fname
            if fpath.exists():
                parts.extend([fpath.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 60) + "\n"])
        return "\n".join(parts)

    target_stem = UI_SUBAGENT_ALIASES.get(clean, clean.removesuffix(".md"))
    target_file = agents_dir / f"{target_stem}.md"
    if target_file.exists():
        return target_file.read_text(encoding="utf-8", errors="replace")

    if clean in PERSONA_ALIASES:
        return _extract_persona_details(PERSONA_ALIASES[clean])

    return f"Erro: Subagente '{agent_name}' não encontrado em {agents_dir}."


COMPASS_PROFILE_RULES: List[Tuple[Tuple[str, ...], str, List[str], List[Tuple[str, str, str]], str, str]] = [
    (
        ("3d", "fisica", "physics", "three", "webgl", "babylon", "shader", "quaternion", "fps"),
        "📐 Física 3D, Computação Gráfica & Simulação Numérica",
        ["code-quality-audit-3d-physics", "auditoria-projetos-sistema"],
        [
            ("code-quality-audit-3d-physics", "state_checker_observer.py", "Roda as 3 ondas (AST + Testes Pass@10 + Observador Pydantic Snorm)"),
            ("code-quality-audit-3d-physics", "static_ast_parser.py", "Analisador AST Python (12 regras + 5 sub-dimensões de física)"),
            ("code-quality-audit-3d-physics", "js_ts_ast_parser.js", "Analisador JS/TS para Three.js/WebGL (alocação em loop, dt, Euler)"),
            ("code-quality-audit-3d-physics", "physics_test_runner.py", "Runner de 5 baterias dinâmicas (60 vs 120Hz, Energia, NaN, CCD, Pass@10)"),
        ],
        "plans/physics_code_audit_dag.json",
        "Foco em zero alocação no hot-loop (GC), multiplicação por dt e guarda contra NaN (sem burocracia de docstrings em helpers matemáticos).",
    ),
    (
        ("medic", "saude", "clin", "prontuario", "receit", "calculadora", "paciente"),
        "🩺 Software Médico & SaaS Clínico Minimalista",
        ["design-interface-medica-minimalista", "arquitetura-design-implementacao-sistema", "consultor-design-tatil-frontend", "frontend-testing-auditor"],
        [
            ("auditoria-projetos-sistema", "frontiercode_maintainability_guardrail.py", "Auditoria adaptativa FrontierCode (Tipagem, Bare Except, Segurança)"),
            ("auditoria-projetos-sistema", "ai_ready_data_pipeline.py", "Sanitização e chunking SHA-256 para diretrizes clínicas/RAG"),
        ],
        "plans/ui_composition_dag.json",
        "Zero dados identificáveis de pacientes fora de .env, contraste WCAG AA/AAA, paleta mineral sem cobalto neon e tipagem estrita.",
    ),
    (
        ("ui", "ux", "front", "tela", "botao", "menu", "css", "tailwind", "react", "design"),
        "🎨 Engenharia de Interface & Design System Tátil Melki (`DESIGN.md v4.5-soft` • 4 Presets + 28 Temas)",
        ["consultor-design-tatil-frontend", "analise-design-tatil-frontend", "refatoracao-design-tatil-frontend", "design-md", "frontend-code-architect", "frontend-testing-auditor"],
        [("auditoria-projetos-sistema", "frontiercode_maintainability_guardrail.py", "Verificação rápida de código sem engessamento")],
        "plans/ui_composition_dag.json",
        "Alvos >= 44x44px anti-squish (flex-shrink: 0), L_card > L_canvas no dark mode, Iluminação 135° (DESIGN.md v4.5-soft) e zero azul cobalto (#0044FF).",
    ),
    (
        ("rag", "dado", "chunk", "jsonl", "vetor", "memoria", "obsidian", "nota", "vault"),
        "🧠 Dados AI-Ready, RAG & Curadoria Obsidian Vault",
        ["curadoria-obsidian-vault", "context-sentinel", "auditoria-projetos-sistema"],
        [
            ("curadoria-obsidian-vault", "vault_hygiene_scanner.py", "Scanner determinístico de Active Drift, Open Loops, Monólitos (>25KB) e Wikilinks"),
            ("auditoria-projetos-sistema", "ai_ready_data_pipeline.py", "Sanitização de texto, deduplicação SHA-256 e chunking com byte_range"),
        ],
        "N/A (Execução direta via script)",
        "Preservação de parágrafos lógicos, metadados source_id + byte_range e proteção absoluta da pasta .obsidian/.",
    ),
    (
        ("agente", "skill", "yaml", "mcp", "plano", "dag", "orquestra", "test", "auditor"),
        "🤖 Arquitetura de Agentes, Declarative YAML Spec, Qualidade AST & Skills (29 Canônicas)",
        ["evoluir-skills", "aprimoramento-expansibilidade-agentes-skills", "code-acceptability-auditor", "test-quality-auditor", "high-level-context-planner", "gap-analyzer-auditor"],
        [
            ("aprimoramento-expansibilidade-agentes-skills", "agent_spec_loader.py", "Carregador Declarative YAML Agent Spec com Zero-Config Defaults"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Auditor estático AST + Pydantic v2 (Segurança, Tipagem, Quality Score >= 75)"),
            ("test-quality-auditor", "test_quality_auditor.py", "Auditor de qualidade de suítes de testes em 5 módulos (Py/TS/Go/MCP/Harness)"),
            ("workspace", "validate_skills.py", "Validador determinístico das 29 skills canônicas"),
        ],
        "plans/ui_composition_dag.json | plans/physics_code_audit_dag.json",
        "Divulgação progressiva em 3 Tiers (<500 linhas no SKILL.md), Zero-Config Defaults no YAML e validação cruzada.",
    ),
]


def _resolve_compass_profile(
    q: str,
) -> Tuple[str, List[str], List[Tuple[str, str, str]], str, str]:
    """Seleciona o perfil cognitivo, skills recomendadas, scripts prontos e plano DAG conforme a intenção."""
    for keywords, title, rec_skills, scripts, dag_plan, guardrail in COMPASS_PROFILE_RULES:
        if any(k in q for k in keywords):
            return title, rec_skills, scripts, dag_plan, guardrail
    return (
        "🧭 Visão Geral Rápida do Ecossistema Franklin (Multi-Projeto • 29 Skills)",
        ["arquiteto-conteudo-solucoes", "auditoria-projetos-sistema", "code-acceptability-auditor", "code-quality-audit-3d-physics", "consultor-design-tatil-frontend", "evoluir-skills"],
        [
            ("auditoria-projetos-sistema", "frontiercode_maintainability_guardrail.py", "Auditoria Python adaptativa (detecta sozinho se é código Geral ou 3D)"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Portão AST pré-commit de segurança e tipagem Python (Score >= 75)"),
            ("code-quality-audit-3d-physics", "state_checker_observer.py", "Observador Pydantic com filtro anti-alucinação AST e nota Snorm"),
            ("auditoria-projetos-sistema", "ai_ready_data_pipeline.py", "Pipeline de sanitização e chunking JSONL para RAG"),
            ("aprimoramento-expansibilidade-agentes-skills", "agent_spec_loader.py", "Instanciação declarativa de agentes via YAML"),
        ],
        "plans/ui_composition_dag.json | plans/physics_code_audit_dag.json",
        "Portão gradual: bloqueia apenas falhas críticas/altas (Hard Gate) e trata estilo/docstrings como sugestões leves (Soft Advisory).",
    )


@mcp.tool()
def franklin_smart_compass(
    intent_or_path: str = ""
) -> str:
    """Bússola Cognitiva (TDAH-Friendly): Descobre automaticamente o que você já tem pronto no ecossistema
    (Skills, Scripts executáveis, Planos DAG e Guardrails Adaptativos) para qualquer ideia ou pasta de projeto.

    Args:
        intent_or_path: Descrição livre do que você quer fazer ou caminho de uma pasta/arquivo.
    """
    skills = _get_all_skills_data()
    q = intent_or_path.strip().lower()
    profile_title, recommended_skills, ready_scripts, dag_plan, linear_guardrail = _resolve_compass_profile(q)

    lines = [
        f"## 🧭 Bússola Cognitiva Franklin — {profile_title}",
        "",
        "### 1. Skills Prontas para Ativar neste Contexto:",
    ]
    for s_name in recommended_skills:
        s_obj = next((x for x in skills if x["name"] == s_name or x["directory"] == s_name), None)
        if s_obj:
            lines.append(f"- **`{s_obj['name']}`** (`{s_obj['persona']}`): {s_obj['description'][:140]}...")

    lines.append("\n### 2. Scripts Executáveis Prontos (Sem precisar recriar do zero):")
    for sk, sc_name, desc in ready_scripts:
        lines.append(f"- **`{sc_name}`** (Skill: `{sk}`) — {desc}")
        lines.append(f"  ↳ Disparo rápido: `franklin_run_skill_script(skill_name='{sk}', script_name='{sc_name}', args=['--self-test'])`")

    lines.extend([
        "",
        f"### 3. Planos DAG Disponíveis: `{dag_plan}`",
        "### 4. Qualidade Linear Sem Engessar (Regra de Bolso):",
        f"> {linear_guardrail}",
        "",
        "### 5. Central Interativa no Terminal (1-Clique):",
        "- `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1` (Menu interativo de agentes, portas e 13 repositórios)",
        "- `franklin_get_agents(agent_name='ecosystem')` (Mapa completo das 5 camadas de agentes)",
    ])
    return "\n".join(lines)


def _build_script_command(script_path: Path, args: Optional[List[str]]) -> Optional[List[str]]:
    """Monta a lista de argumentos de comando segura conforme a extensão do script."""
    suffix = script_path.suffix.lower()
    if suffix == ".py":
        cmd = [sys.executable, str(script_path)]
    elif suffix == ".js":
        cmd = ["node", str(script_path)]
    elif suffix == ".ps1":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    elif suffix in (".cmd", ".bat"):
        cmd = ["cmd.exe", "/c", str(script_path)]
    else:
        return None
    if args:
        cmd.extend(args)
    return cmd


@mcp.tool()
def franklin_run_skill_script(
    skill_name: str,
    script_name: str,
    args: Optional[List[str]] = None,
    timeout_seconds: int = 60
) -> str:
    """Executa de forma segura um script utilitário associado a uma skill ou ao workspace.
    Args:
        skill_name: Nome da skill (ou 'workspace' para scripts gerais em /scripts/).
        script_name: Nome do arquivo de script (ex: 'md-to-pdf.ps1', 'validate_skills.py').
        args: Argumentos opcionais para o script.
        timeout_seconds: Tempo limite de execução (padrão: 60s).
    """
    if ".." in script_name or "/" in script_name or "\\" in script_name:
        return "Erro de Segurança: Nome de script inválido (Path Traversal detectado)."

    if skill_name.lower() in ("workspace", "root", "global"):
        target_dir = ROOT_DIR / "scripts"
    else:
        skill_dir = _find_skill_dir(skill_name)
        if not skill_dir:
            return f"Erro: Skill '{skill_name}' não encontrada."
        target_dir = skill_dir / "scripts"

    script_path = target_dir / script_name
    if not script_path.exists():
        return f"Erro: Script '{script_name}' não existe em {target_dir}."

    cmd = _build_script_command(script_path, args)
    if not cmd:
        return f"Erro: Extensão de script '{script_path.suffix}' não suportada para execução direta."

    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout_seconds,
            cwd=str(ROOT_DIR),
            shell=False
        )
        out = res.stdout.strip()
        if res.stderr:
            out += "\n--- STDERR ---\n" + res.stderr.strip()
        return f"[Exit Code: {res.returncode}]\n{out if out else '(Script executado sem retorno textual)'}"
    except subprocess.TimeoutExpired:
        return f"Erro: Execução excedeu o tempo limite de {timeout_seconds} segundos."
    except (OSError, ValueError, RuntimeError) as e:
        return f"Erro ao executar script: {e}"


def _resolve_dag_plan_file(plan_str: str) -> Tuple[Optional[Path], Optional[Path], Optional[str]]:
    """Resolve o arquivo de plano DAG por alias, caminho existente ou JSON inline temporário."""
    plan_aliases = {
        "ui": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "frontend": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "3+1": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition_dag": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition_dag.json": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "physics": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "3d": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "fisica": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit_dag": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit_dag.json": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "sample": EPIC_VOLTA_DIR / "examples" / "sample_dag_plan.json",
        "sample_dag_plan.json": EPIC_VOLTA_DIR / "examples" / "sample_dag_plan.json",
    }
    if plan_str.lower() in plan_aliases:
        alias_candidate = plan_aliases[plan_str.lower()]
        if alias_candidate.is_file():
            return alias_candidate.resolve(), None, None

    for cp in (
        Path(plan_str),
        ROOT_DIR / plan_str,
        ROOT_DIR / "plans" / plan_str,
        EPIC_VOLTA_DIR / plan_str,
        EPIC_VOLTA_DIR / "examples" / plan_str,
        Path(r"C:\Users\melki\.gemini\plans") / plan_str,
    ):
        if cp.exists() and cp.is_file():
            return cp.resolve(), None, None

    try:
        parsed = json.loads(plan_str)
        if not isinstance(parsed, dict):
            return None, None, json.dumps({"status": "INVALID_PLAN", "error": "O payload JSON deve ser um objeto compatível com DAGExecutionPlan."}, ensure_ascii=False)
        import uuid
        temp_dir = ROOT_DIR / ".sessions" / "temp_plans"
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_file = temp_dir / f"plan_{uuid.uuid4().hex[:8]}.json"
        temp_file.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
        return temp_file.resolve(), temp_file, None
    except json.JSONDecodeError as exc:
        return None, None, json.dumps({"status": "FILE_NOT_FOUND_OR_INVALID_JSON", "error": f"Não foi possível localizar o arquivo nem interpretar como JSON válido: {exc}"}, ensure_ascii=False)


@mcp.tool()
def franklin_execute_dag(
    plan_path_or_json: str,
    run_id: str = "",
    resume: bool = False,
    timeout_seconds: float = 0,
    db_path: str = ""
) -> str:
    """Executa um plano de orquestração em grafo acíclico dirigido (DAG) via motor do Epic-Volta.
    Args:
        plan_path_or_json: Caminho para o arquivo JSON do plano, alias ('ui', 'physics') ou string JSON.
        run_id: Identificador único opcional da execução.
        resume: Se True, retoma a execução sem reexecutar nós já concluídos no SQLite.
        timeout_seconds: Tempo limite global da execução em segundos (0 para sem limite).
        db_path: Caminho do banco SQLite de persistência.
    """
    if not EPIC_VOLTA_DIR.exists():
        return json.dumps({"status": "FAILED", "error": f"Repositório Epic-Volta não encontrado em {EPIC_VOLTA_DIR}."}, ensure_ascii=False)

    resolved_plan_path, temp_file, err_json = _resolve_dag_plan_file(plan_path_or_json.strip())
    if err_json or not resolved_plan_path:
        return err_json or json.dumps({"status": "FAILED", "error": "Plano inválido."}, ensure_ascii=False)

    cmd = ["uv", "--directory", str(EPIC_VOLTA_DIR), "run", "python", "-m", "orchestrator.cli", str(resolved_plan_path), "--json"]
    if run_id.strip():
        cmd.extend(["--run-id", run_id.strip()])
    if resume:
        cmd.append("--resume")
    if timeout_seconds > 0:
        cmd.extend(["--timeout", str(timeout_seconds)])
    if db_path.strip():
        cmd.extend(["--db", db_path.strip()])

    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout_seconds + 30 if timeout_seconds > 0 else 120,
            cwd=str(EPIC_VOLTA_DIR),
            shell=False
        )
        stdout = res.stdout.strip()
        if res.returncode == 0:
            return stdout if stdout else json.dumps({"status": "COMPLETED", "note": "Sem saída stdout"}, ensure_ascii=False)
        return stdout if stdout.startswith("{") else json.dumps({"status": "FAILED", "exit_code": res.returncode, "stdout": stdout, "stderr": res.stderr.strip()}, ensure_ascii=False)
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "TIMEOUT", "error": f"Execução do DAG excedeu o limite de {timeout_seconds} segundos."}, ensure_ascii=False)
    except (OSError, ValueError, RuntimeError) as e:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    finally:
        if temp_file:
            temp_file.unlink(missing_ok=True)


def _match_best_skill_for_harness(combined_query: str) -> Tuple[str, str]:
    """Identifica a skill e persona mais aderentes à intenção para o Harness HITL."""
    best_skill: Optional[Dict[str, Any]] = None
    max_score = 0
    for s in _get_all_skills_data():
        score = 20 if s["name"].lower() in combined_query else 0
        for tag in s.get("tags", []):
            if len(tag) > 3 and tag.lower() in combined_query:
                score += len(tag)
        if score > max_score:
            max_score = score
            best_skill = s
    if best_skill:
        return best_skill["name"], best_skill["persona"]
    return "franklin-main", "Franklin-Main"


@mcp.tool()
def franklin_harness_guard(
    task_intent: str,
    proposed_tool_or_action: str = "",
    session_id: str = "default",
) -> str:
    """Aplica o Harness de Governança Determinística e Human-in-the-Loop antes de executar ações
    contra o ecossistema de 29 Skills do Franklin.
    """
    import uuid

    try:
        clean_intent = SemanticGuard.sanitize_input(task_intent)
        clean_action = SemanticGuard.sanitize_input(proposed_tool_or_action) if proposed_tool_or_action else ""
    except SecurityViolationError as e:
        return json.dumps({
            "status": "BLOCKED",
            "riskLevel": "CRITICAL",
            "reason": str(e),
            "instructions": "Execução terminantemente bloqueada pelo SemanticGuard fora da janela do LLM."
        }, indent=2, ensure_ascii=False)

    active_skill_name, persona = _match_best_skill_for_harness(f"{clean_intent} {clean_action}".lower())
    risk_level, risk_reason = evaluate_action_risk(f"{clean_intent} {clean_action}")

    if risk_level == RiskLevel.CRITICAL:
        chk_id = f"chk-{uuid.uuid4().hex[:8]}"
        harness_store.create(
            checkpoint_id=chk_id,
            session_id=session_id,
            task_intent=clean_intent,
            proposed_action=clean_action or "Ação de mutação no sistema",
            active_skill=active_skill_name,
            risk_level="CRITICAL",
            notes=risk_reason,
        )
        return json.dumps({
            "status": "APPROVAL_REQUIRED",
            "riskLevel": "CRITICAL",
            "checkpointId": chk_id,
            "activeSkill": active_skill_name,
            "persona": persona,
            "reason": risk_reason,
            "instructions": (
                f"AÇÃO CRÍTICA DETECTADA: O Harness pausou a execução para proteger o sistema. "
                f"Checkpoint registrado sob o ID '{chk_id}'. "
                f"OBRIGATÓRIO: Apresente o plano / simulação (Dry-Run) com a lista dos itens impactados ao usuário e solicite "
                f"sua aprovação expressa antes de executar. Para aprovar, use 'franklin_harness_checkpoint(action=\"approve\", checkpoint_id=\"{chk_id}\")'."
            )
        }, indent=2, ensure_ascii=False)

    return json.dumps({
        "status": "AUTHORIZED",
        "riskLevel": "LOW",
        "activeSkill": active_skill_name,
        "persona": persona,
        "reason": risk_reason,
        "instructions": f"Operação segura autorizada pelo Harness sob a persona {persona}. Siga os procedimentos e salvaguardas da skill '{active_skill_name}'."
    }, indent=2, ensure_ascii=False)


def _mutate_checkpoint_status(checkpoint_id: str, target_status: str, notes: str) -> str:
    """Aprova ou rejeita um checkpoint no CheckpointStore."""
    if not checkpoint_id:
        return json.dumps({"error": f"checkpoint_id é obrigatório para status '{target_status}'"}, ensure_ascii=False)
    default_note = "Aprovado pelo operador" if target_status == "APPROVED" else "Rejeitado pelo operador"
    rec = harness_store.update_status(checkpoint_id, status=target_status, notes=notes or default_note)
    if not rec:
        return json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
    msg = (
        f"Ação '{rec.proposed_action}' foi APROVADA pelo operador humano. A execução pode prosseguir."
        if target_status == "APPROVED"
        else f"Ação '{rec.proposed_action}' foi VETADA pelo operador humano. A execução está cancelada."
    )
    return json.dumps({"status": target_status, "checkpointId": checkpoint_id, "message": msg, "record": rec.to_dict()}, indent=2, ensure_ascii=False)


@mcp.tool()
def franklin_harness_checkpoint(
    action: str = "list",
    session_id: str = "default",
    checkpoint_id: str = "",
    approved: bool = False,
    notes: str = ""
) -> str:
    """Gerencia checkpoints de governança HITL e sub-ações recursivas Harness² (validate_tree, evolve, record_experience)."""
    _ = approved
    act = action.strip().lower()
    h2_res = dispatch_harness2_action(act, notes, SESSIONS_DIR)
    if h2_res is not None:
        return h2_res
    if act == "list":
        pending = harness_store.list(status="PENDING", session_id=session_id if session_id != "all" else None)
        return json.dumps({"totalPending": len(pending), "checkpoints": [r.to_dict() for r in pending]}, indent=2, ensure_ascii=False)
    if act == "get":
        if not checkpoint_id:
            return json.dumps({"error": "checkpoint_id é obrigatório para a ação 'get'"}, ensure_ascii=False)
        rec = harness_store.get(checkpoint_id)
        return json.dumps(rec.to_dict(), indent=2, ensure_ascii=False) if rec else json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
    if act == "approve":
        return _mutate_checkpoint_status(checkpoint_id, "APPROVED", notes)
    if act == "reject":
        return _mutate_checkpoint_status(checkpoint_id, "REJECTED", notes)
    if act == "clear":
        return json.dumps({"status": "CLEARED", "removedCount": harness_store.clear()}, indent=2, ensure_ascii=False)
    return json.dumps({"error": f"Ação '{action}' inválida. Use: list, get, approve, reject, clear, validate_tree, evolve ou record_experience."}, ensure_ascii=False)


@mcp.tool()
def franklin_a2a_agent_card(
    skill_filter: str = "",
    verify_signature: bool = True,
) -> str:
    """Gera e assina criptograficamente (JCS + JWS HMAC-SHA256) o AgentCard oficial A2A v1.0 / v0.3 do Franklin.

    Args:
        skill_filter: Filtro opcional para exportar apenas skills de um domínio ou palavra-chave.
        verify_signature: Se True, executa auto-verificação da assinatura JWS antes de retornar.
    """
    card = build_franklin_agent_card(
        skills_dir=SKILLS_ROOT,
        skill_filter=skill_filter,
        sign=True,
    )
    verified = verify_agent_card_signature(card) if verify_signature else True
    card["signatureVerified"] = verified
    return json.dumps(card, indent=2, ensure_ascii=False)


@mcp.tool()
def franklin_a2a_dispatch_task(
    query: str = "",
    skill_id: str = "",
    context_id: str = "ctx-default",
    task_id: str = "",
    action: str = "send",
) -> str:
    """Despacha, consulta ou cancela uma Task no protocolo Agent2Agent (A2A v1.0) acoplado ao Harness HITL.

    Args:
        query: Mensagem ou instrução A2A (obrigatória para action='send').
        skill_id: ID opcional da skill alvo no AgentCard.
        context_id: Identificador de contexto conversacional A2A (isolado de user_id por segurança Zero-Trust).
        task_id: ID opcional da Task A2A (obrigatório para action='get' ou 'cancel').
        action: Operação A2A ('send', 'get', 'cancel').
    """
    act = action.strip().lower()
    if act == "send":
        task = a2a_task_manager.submit_task(
            query=query,
            skill_id=skill_id,
            context_id=context_id,
            task_id=task_id.strip() or None,
        )
        return json.dumps(task, indent=2, ensure_ascii=False)

    if act == "get":
        if not task_id.strip():
            return json.dumps({"error": "task_id é obrigatório para action='get'"}, ensure_ascii=False)
        found = a2a_task_manager.get_task(task_id.strip())
        if not found:
            return json.dumps({"error": f"Task A2A '{task_id}' não encontrada"}, ensure_ascii=False)
        return json.dumps(found, indent=2, ensure_ascii=False)

    if act == "cancel":
        if not task_id.strip():
            return json.dumps({"error": "task_id é obrigatório para action='cancel'"}, ensure_ascii=False)
        canceled = a2a_task_manager.cancel_task(task_id.strip())
        if not canceled:
            return json.dumps({"error": f"Task A2A '{task_id}' não encontrada"}, ensure_ascii=False)
        return json.dumps(canceled, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"Ação A2A '{action}' inválida. Use: send, get ou cancel."}, ensure_ascii=False)


@mcp.tool()
def franklin_mcp_build_advisor(
    connects_to: str = "cloud_api",
    audience: str = "personal_or_team",
    action_count: int = 10,
    interaction_needs: str = "plain_text_or_json",
    upstream_auth: str = "none",
    preferred_language: str = "python",
    server_name: str = "franklin-mcp-service",
) -> str:
    """Consultor Arquitetural MCP 2026-07-28 (`build-with-agent-skills`).

    Executa a descoberta de 5 fases (build-mcp-server, build-mcp-app, build-mcpb),
    recomenda o modelo de deploy (remote-streamable-http, mcp-app, mcpb, local-stdio),
    o padrão de ferramentas (Pattern A one-per-action vs Pattern B search-and-execute),
    roteamento Elicitation vs Widget (`text/html;profile=mcp-app`), SDK oficial
    (TypeScript v2, Python v2/FastMCP 3.x, Go v1.7+) e gera o manifesto `.mcpb` v0.4.
    """
    result = evaluate_mcp_2026_architecture(
        connects_to=connects_to,
        audience=audience,
        action_count=action_count,
        interaction_needs=interaction_needs,
        upstream_auth=upstream_auth,
        preferred_language=preferred_language,
        server_name=server_name,
    )
    return json.dumps(result, indent=2, ensure_ascii=False)


# -----------------------------------------------------------------------------
# Recursos MCP (Resources)
# -----------------------------------------------------------------------------
@mcp.resource("skills://mcp-2026/spec")
def get_mcp_2026_spec_resource() -> str:
    """Recurso passivo expondo a matriz da especificação MCP 2026-07-28, SEP-2577 e Build with Agent Skills."""
    return json.dumps(evaluate_mcp_2026_architecture(), indent=2, ensure_ascii=False)


@mcp.resource("skills://a2a/agent-card")
def get_a2a_agent_card_resource() -> str:
    """Recurso passivo expondo o AgentCard oficial A2A v1.0 assinado do Franklin Quebra-Galho."""
    card = build_franklin_agent_card(skills_dir=SKILLS_ROOT, sign=True)
    return json.dumps(card, indent=2, ensure_ascii=False)


@mcp.resource("skills://harness/checkpoints")
def get_harness_checkpoints_resource() -> str:
    """Recurso passivo expondo a lista de checkpoints e aprovações pendentes do Harness."""
    records = harness_store.list()
    return json.dumps([r.to_dict() for r in records], indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog")
def get_catalog_resource() -> str:
    """Recurso passivo expondo o catálogo consolidado de skills em formato JSON."""
    skills = _get_all_skills_data()
    return json.dumps(skills, indent=2, ensure_ascii=False)


@mcp.resource("skills://manifest")
def get_manifest_resource() -> str:
    """Recurso passivo expondo o manifesto completo e ciclo de vida de MY_SKILLS.md."""
    if MY_SKILLS_MD_PATH.exists():
        return MY_SKILLS_MD_PATH.read_text(encoding="utf-8", errors="replace")
    return "MY_SKILLS.md não encontrado."


@mcp.resource("skills://agents")
def get_agents_resource() -> str:
    """Recurso passivo expondo a arquitetura e diretrizes de AGENTS.md."""
    if AGENTS_MD_PATH.exists():
        return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
    return "AGENTS.md não encontrado."


@mcp.resource("skills://agent/{agent_name}")
def get_agent_contract_resource(agent_name: str) -> str:
    """Recurso passivo para leitura direta do contrato de um subagente (ex: ui-shell-navigator)."""
    return franklin_get_agents(agent_name=agent_name)


@mcp.resource("skills://skill/{skill_name}")
def get_skill_resource(skill_name: str) -> str:
    """Recurso passivo para leitura direta do contrato SKILL.md de uma skill."""
    return franklin_skills_get(skill_name=skill_name, section="contract")


@mcp.resource("skills://rules/{skill_name}")
def get_rules_resource(skill_name: str) -> str:
    """Recurso passivo para leitura direta dos critérios de auditoria de uma skill."""
    return franklin_skills_get(skill_name=skill_name, section="rules")


# -----------------------------------------------------------------------------
# Prompts MCP (Prompts)
# -----------------------------------------------------------------------------
@mcp.prompt("activate_skill")
def activate_skill_prompt(skill_name: str, user_intent: str) -> str:
    """Gera o prompt estruturado de ativação de uma skill sob os padrões de 2026."""
    skill_content = franklin_skills_get(skill_name=skill_name, section="contract")
    rules_content = franklin_skills_get(skill_name=skill_name, section="rules")

    return f"""Você está assumindo o papel de executor especialista da skill '{skill_name}'.
Siga estritamente o contrato operacional e as regras determinísticas abaixo:

--- CONTRATO DA SKILL ({skill_name}) ---
{skill_content}

--- REGRAS DE AUDITORIA E RESTRIÇÕES ---
{rules_content}

--- INTENÇÃO DO USUÁRIO ---
{user_intent}

Proceda com a execução seguindo a taxonomia determinística e as salvaguardas necessárias.
"""


@mcp.prompt("tactile_frontend_audit")
def tactile_frontend_audit_prompt(component_or_url: str) -> str:
    """Gera prompt para auditoria tátil de frontend sob os padrões do FrontCraftMaster e Topologia 3+1."""
    return f"""Atue como FrontCraftMaster e audite a seguinte interface/código: {component_or_url}.
Coordene a Topologia 3+1 de Subagentes de UI (ui-shell-navigator, ui-controls-data, ui-motion-interaction, ui-deterministic-observer) via invoke_subagent (Modo Nativo Antigravity em 3 ondas) ou via franklin_get_agents(agent_name="ui") / franklin_execute_dag("plans/ui_composition_dag.json") (Modo Motor DAG Assíncrono) e avalie contra o Design System Tátil Melki:
1. Menus claustrofóbicos vs descompactados (padding nobre, min 240px em sidebar, CLS < 0.1).
2. Botões ergonômicos (altura mínima 44px, anti-squish shrink-0 whitespace-nowrap, micro-interação tátil).
3. Paleta Mineral Anti-Cobalto (fundo ardósia/creme, acentos minerais, banimento de azul cobalto puro).
4. Profundidade de sombras e elevação (Iluminação 135°, .ui-card-soft e cavidades surface-inset — DESIGN.md v4.5-soft).
Emita o Relatório Comparativo determinístico com marcadores [PASS], [FAIL] e notas explicativas.
"""


# -----------------------------------------------------------------------------
# Ponto de Entrada Principal
# -----------------------------------------------------------------------------
def run() -> None:
    """Ponto de entrada para execução STDIO do servidor MCP."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
