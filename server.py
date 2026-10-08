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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
    EPIC_VOLTA_DIR = Path(r"C:\Users\melki\dev\agents\epic-volta")



# -----------------------------------------------------------------------------
# Utilitários de Parsing de Metadados e Estado
# -----------------------------------------------------------------------------
from shared.tools.frontmatter_parser import parse_frontmatter as _parse_frontmatter
from shared.harness import (
    CheckpointRecord,
    CheckpointStore,
    RiskLevel,
    SecurityViolationError,
    SemanticGuard,
    evaluate_action_risk,
)

SESSIONS_DIR = ROOT_DIR / ".sessions"
CHECKPOINTS_FILE = SESSIONS_DIR / "harness_checkpoints.json"
harness_store = CheckpointStore(CHECKPOINTS_FILE)


def _load_agents_map() -> Dict[str, str]:
    """Mapeia cada skill à sua persona especialista correspondente via AGENTS.md."""
    mapping = {
        "analise-design-tatil-frontend": "FrontCraftMaster",
        "refatoracao-design-tatil-frontend": "FrontCraftMaster",
        "consultor-design-tatil-frontend": "FrontCraftMaster",
        "design-interface-medica-minimalista": "FrontCraftMaster",
        "gdrive-auditoria-limpeza": "DriveMaster",
        "gdrive-taxonomia-organizacao": "DriveMaster",
        "organizar-gdrive": "DriveMaster",
        "manutencao-disco-windows": "FileOpsLocal",
        "organizar-local": "FileOpsLocal",
        "curadoria-obsidian-vault": "VaultMaster",
        "redator-tecnico-markdown": "DocMaker",
        "conversor-html-pdf": "DocMaker",
        "gerar-docs-pdf": "DocMaker",
        "organizador-fluxo-arvore-arquivos": "DocMaker",
        "evoluir-skills": "SkillCraft",
        "skill-auditor-refatorador-skills": "SkillCraft",
        "aprimoramento-expansibilidade-agentes-skills": "SkillCraft",
        "high-level-context-planner": "LoopPlanner",
        "gap-analyzer-auditor": "LoopPlanner",
        "skill-orquestrador-planos-encadeados": "LoopPlanner",
        "arquiteto-conteudo-solucoes": "Franklin-Main",
        "arquitetura-design-implementacao-sistema": "Franklin-Main",
        "auditoria-projetos-sistema": "Franklin-Main",
        "context-sentinel": "Franklin-Main",
        "refine-prompt": "Franklin-Main",
        "_template": "Franklin-Main",
    }

    if AGENTS_MD_PATH.exists():
        try:
            content = AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
            # Extração de padrões em tabelas do Markdown
            for line in content.splitlines():
                if "|" in line and "`" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 5:
                        persona_match = re.search(r"\*\*`?([a-zA-Z0-9_\-]+)`?\*\*", parts[1])
                        if persona_match:
                            persona = persona_match.group(1)
                            skills_in_line = re.findall(r"`([a-zA-Z0-9_\-]+)`", parts[3])
                            for s in skills_in_line:
                                mapping[s] = persona
        except Exception:
            pass

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
                        status_str = parts[3].strip()
                        status_map[skill_name] = status_str
    except Exception:
        pass

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

        scripts_list: List[str] = []
        if scripts_dir.exists() and scripts_dir.is_dir():
            scripts_list = [f.name for f in scripts_dir.iterdir() if f.is_file()]

        ref_list: List[str] = []
        if ref_dir.exists() and ref_dir.is_dir():
            ref_list = [f.name for f in ref_dir.iterdir() if f.is_file()]

        # Tags inferidas
        tags = set()
        for token in [name, skill_dir.name, description]:
            words = re.findall(r"[a-zA-Z0-9_\-]+", token.lower())
            tags.update(words)

        agents_map = _load_agents_map()
        status_map = _load_status_map()

        persona = agents_map.get(skill_dir.name, agents_map.get(name, "Franklin-Main"))
        status = status_map.get(skill_dir.name, status_map.get(name, "✅ Validada"))

        return {
            "name": name,
            "directory": skill_dir.name,
            "version": version,
            "status": status,
            "persona": persona,
            "description": description,
            "path": str(skill_file),
            "has_rules": rules_file.exists(),
            "has_evals": evals_file.exists(),
            "has_references": bool(ref_list),
            "references": ref_list,
            "has_scripts": bool(scripts_list),
            "scripts": scripts_list,
            "tags": sorted(list(tags)),
        }
    except Exception:
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
    """Localiza o diretório de uma skill por correspondência exata ou substring unívoca."""
    clean = skill_name.strip().lower()
    exact_path = SKILLS_ROOT / clean
    if exact_path.exists() and exact_path.is_dir():
        return exact_path

    dirs = [d for d in SKILLS_ROOT.iterdir() if d.is_dir()]
    # 1. Correspondência exata case-insensitive
    for d in dirs:
        if d.name.lower() == clean:
            return d

    # 2. Correspondência de prefixo ou nome único (ex: 'conversor-html-pdf' ao buscar 'conversor-pdf')
    matching_dirs = [d for d in dirs if clean == d.name.lower() or d.name.lower() == clean]
    if matching_dirs:
        return matching_dirs[0]

    return None


# -----------------------------------------------------------------------------
# Ferramentas MCP (Tools)
# -----------------------------------------------------------------------------
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

    filtered = []
    for s in skills:
        # Filtro de status
        if status.lower() != "all":
            if status.lower() not in s["status"].lower():
                continue

        # Filtro de persona
        if persona.lower() != "all":
            if persona.lower() not in s["persona"].lower():
                continue

        # Filtro de busca textual
        if search.strip():
            term = search.strip().lower()
            if term not in s["name"].lower() and term not in s["description"].lower():
                continue

        filtered.append(s)

    if format.lower() == "json":
        return json.dumps(filtered, indent=2, ensure_ascii=False)

    # Renderização em Markdown estruturado e limpo
    lines = [
        f"### 📦 Catálogo de Skills do Franklin Quebra-Galho ({len(filtered)}/{len(skills)} ativas)\n",
        f"> **Diretório Raiz**: `{SKILLS_ROOT}`\n",
        "| Skill | Versão | Status | Subagente Especialista | Componentes Modulares |",
        "| :--- | :---: | :---: | :--- | :--- |",
    ]

    for s in filtered:
        comps = []
        if s["has_rules"]:
            comps.append("Rules [PASS/FAIL]")
        if s["has_references"]:
            comps.append(f"{len(s['references'])} Ref(s)")
        if s["has_evals"]:
            comps.append("Evals")
        if s["has_scripts"]:
            comps.append(f"{len(s['scripts'])} Script(s)")
        comp_str = ", ".join(comps) if comps else "Apenas Contrato"

        lines.append(f"| **`{s['name']}`** | `{s['version']}` | {s['status']} | `{s['persona']}` | {comp_str} |")

    lines.append("\n**Dica de Uso**: Utilize `franklin_skills_get(skill_name)` para ler o contrato da skill ou `franklin_skills_search(query)` para encontrar a skill exata.")
    return "\n".join(lines)


@mcp.tool()
def franklin_skills_get(
    skill_name: str,
    section: str = "contract"
) -> str:
    """Recupera as instruções, regras ou dados de uma skill com suporte a divulgação progressiva.
    Args:
        skill_name: Nome exato ou aproximado da skill (ex: 'arquiteto-conteudo-solucoes', 'conversor-html-pdf', 'gdrive-auditoria-limpeza').
        section: Seção para carregamento granular:
                 - 'contract': Apenas o SKILL.md enxuto (Ideal para preservar Token Budget).
                 - 'rules': Apenas os critérios determinísticos de auditoria (rules/criterios_auditoria.md).
                 - 'references': Lista e conteúdos dos manuais de referência (references/).
                 - 'evals': Suíte de testes estruturados (evals/evals.json).
                 - 'scripts': Lista dos scripts executáveis disponíveis.
                 - 'all': Pacote completo da skill concatenado.
    """
    skill_dir = _find_skill_dir(skill_name)
    if not skill_dir:
        # Sugestões próximas
        all_names = [d.name for d in SKILLS_ROOT.iterdir() if d.is_dir()]
        suggestions = difflib.get_close_matches(skill_name, all_names, n=3, cutoff=0.4)
        sug_text = f" Sugestões: {', '.join(suggestions)}" if suggestions else ""
        return f"Erro: Skill '{skill_name}' não encontrada em {SKILLS_ROOT}.{sug_text}"

    skill_file = skill_dir / "SKILL.md"
    rules_file = skill_dir / "rules" / "criterios_auditoria.md"
    evals_file = skill_dir / "evals" / "evals.json"
    ref_dir = skill_dir / "references"
    scripts_dir = skill_dir / "scripts"

    sec = section.strip().lower()

    if sec == "contract":
        if not skill_file.exists():
            return f"Erro: SKILL.md ausente na pasta {skill_dir.name}."
        return skill_file.read_text(encoding="utf-8", errors="replace")

    elif sec == "rules":
        if not rules_file.exists():
            return f"A skill '{skill_dir.name}' não possui arquivo dedicado de regras (rules/criterios_auditoria.md)."
        return rules_file.read_text(encoding="utf-8", errors="replace")

    elif sec == "evals":
        if not evals_file.exists():
            return f"A skill '{skill_dir.name}' não possui arquivo de evals (evals/evals.json)."
        return evals_file.read_text(encoding="utf-8", errors="replace")

    elif sec == "references":
        if not ref_dir.exists() or not any(ref_dir.iterdir()):
            return f"A skill '{skill_dir.name}' não possui referências adicionais (references/)."
        parts = [f"### Referências da Skill `{skill_dir.name}`:\n"]
        for f in sorted(ref_dir.iterdir()):
            if f.is_file():
                parts.append(f"#### Arquivo: `{f.name}`")
                parts.append(f.read_text(encoding="utf-8", errors="replace"))
                parts.append("\n" + ("-" * 40) + "\n")
        return "\n".join(parts)

    elif sec == "scripts":
        if not scripts_dir.exists() or not any(scripts_dir.iterdir()):
            return f"A skill '{skill_dir.name}' não possui scripts executáveis próprios (scripts/)."
        parts = [f"### Scripts da Skill `{skill_dir.name}`:\n"]
        for f in sorted(scripts_dir.iterdir()):
            if f.is_file():
                parts.append(f"- **`{f.name}`** ({f.stat().st_size} bytes)")
        return "\n".join(parts)

    elif sec == "all":
        parts = [f"# PACOTE COMPLETO: {skill_dir.name.upper()}\n"]
        if skill_file.exists():
            parts.append("## 1. Contrato Operacional (SKILL.md)")
            parts.append(skill_file.read_text(encoding="utf-8", errors="replace"))
            parts.append("\n" + ("=" * 50) + "\n")

        if rules_file.exists():
            parts.append("## 2. Regras e Critérios de Auditoria (rules/criterios_auditoria.md)")
            parts.append(rules_file.read_text(encoding="utf-8", errors="replace"))
            parts.append("\n" + ("=" * 50) + "\n")

        if evals_file.exists():
            parts.append("## 3. Testes Estruturados (evals/evals.json)")
            parts.append(evals_file.read_text(encoding="utf-8", errors="replace"))
            parts.append("\n" + ("=" * 50) + "\n")

        if ref_dir.exists() and any(ref_dir.iterdir()):
            parts.append("## 4. Documentos de Referência (references/)")
            for f in sorted(ref_dir.iterdir()):
                if f.is_file():
                    parts.append(f"### Referência: `{f.name}`")
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
            parts.append("\n" + ("=" * 50) + "\n")

        return "\n".join(parts)

    return f"Seção '{section}' inválida. Opções: 'contract', 'rules', 'references', 'evals', 'scripts', 'all'."


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
    scored = []

    for s in skills:
        score = 0
        name_lower = s["name"].lower()
        desc_lower = s["description"].lower()
        persona_lower = s["persona"].lower()

        # Correspondência de frase completa
        if clean_q in name_lower:
            score += 50
        if clean_q in desc_lower:
            score += 30

        # Correspondência por tokens
        for t in terms:
            if t in name_lower:
                score += 15
            if t in s["tags"]:
                score += 10
            if t in desc_lower:
                score += 5
            if t in persona_lower:
                score += 8

        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_matches = scored[:limit]

    if not top_matches:
        return f"Nenhuma skill encontrada para '{query}'. Use 'franklin_skills_list()' para inspecionar todas as opções."

    output = [
        f"### 🎯 Recomendações de Skills para: \"{query}\"\n",
    ]

    for rank, (score, s) in enumerate(top_matches, start=1):
        output.append(f"#### {rank}. **`{s['name']}`** (Relevância: {score} pts)")
        output.append(f"- **Subagente Recomendado**: `{s['persona']}`")
        output.append(f"- **Status**: {s['status']} | **Versão**: `{s['version']}`")
        output.append(f"- **Descrição**: {s['description']}")
        output.append(f"- **Comando para ler**: `franklin_skills_get(skill_name='{s['name']}')`\n")

    return "\n".join(output)


@mcp.tool()
def franklin_skills_validate(
    target_skill: str = ""
) -> str:
    """Executa auditoria determinística de conformidade estrutural, contratual e semântica das skills.
    Args:
        target_skill: Nome de uma skill específica para validar, ou vazio para validar todas as 26 skills.
    """
    skills_to_validate: List[Path] = []
    if target_skill.strip():
        found = _find_skill_dir(target_skill.strip())
        if not found:
            return f"[FAIL] Skill '{target_skill}' não encontrada para validação."
        skills_to_validate = [found]
    else:
        skills_to_validate = sorted([d for d in SKILLS_ROOT.iterdir() if d.is_dir()])

    total = 0
    passed = 0
    failures: Dict[str, List[str]] = {}

    required_sections = [
        (r"(#|##)\s+.*(Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao)", "Gatilhos / Quando Usar"),
        (r"(#|##)\s+.*(Entradas|Pr[eé]-requisitos|Par[aâ]metros)", "Entradas / Pré-requisitos"),
        (r"(#|##)\s+.*(Processamento|Passo a Passo|Fluxo|Execução|Execucao)", "Processamento / Fluxo"),
        (r"(#|##)\s+.*(Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida)", "Saídas / Entregáveis"),
        (r"(#|##)\s+.*(Exceções|Excecoes|Limites|Quando N[AÃ]O Usar)", "Exceções / Limites"),
    ]

    for s_dir in skills_to_validate:
        total += 1
        errs: List[str] = []
        skill_file = s_dir / "SKILL.md"

        if not skill_file.exists():
            errs.append("Arquivo SKILL.md inexistente")
        else:
            try:
                content = skill_file.read_text(encoding="utf-8")
                meta, body = _parse_frontmatter(content)
                if not meta:
                    errs.append("Frontmatter YAML ausente ou malformado")
                for req in ["name", "description", "version"]:
                    if req not in meta or not meta[req]:
                        errs.append(f"Campo obrigatório '{req}' ausente no frontmatter")

                if "name" in meta and meta["name"] != s_dir.name:
                    if not (s_dir.name == "_template" and meta["name"] == "template-skill"):
                        errs.append(f"Nome no frontmatter ('{meta['name']}') difere da pasta ('{s_dir.name}')")

                for sec_pattern, sec_name in required_sections:
                    if not re.search(sec_pattern, body, re.IGNORECASE):
                        errs.append(f"Seção obrigatória ausente: {sec_name}")

                # Checagem de rules/criterios_auditoria.md
                rules_file = s_dir / "rules" / "criterios_auditoria.md"
                if rules_file.exists():
                    rules_text = rules_file.read_text(encoding="utf-8")
                    if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
                        errs.append("rules/criterios_auditoria.md deve conter marcadores [PASS] e [FAIL]")

                # Checagem de evals/evals.json
                evals_file = s_dir / "evals" / "evals.json"
                if evals_file.exists():
                    try:
                        evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
                        if isinstance(evals_data, dict) and "evals" in evals_data:
                            evals_list = evals_data["evals"]
                        elif isinstance(evals_data, list):
                            evals_list = evals_data
                        else:
                            evals_list = []
                        if not isinstance(evals_list, list) or len(evals_list) == 0:
                            errs.append("evals.json deve conter uma lista não-vazia de testes")
                    except Exception as e:
                        errs.append(f"Sintaxe JSON inválida em evals.json: {e}")

            except Exception as e:
                errs.append(f"Erro ao analisar arquivo: {e}")

        if errs:
            failures[s_dir.name] = errs
        else:
            passed += 1

    lines = [
        "=== AUDITORIA DETERMINÍSTICA DE SKILLS DO FRANKLIN ===",
        f"Total Inspecionado: {total} | Aprovadas: {passed} | Falhas: {len(failures)}",
        "-" * 60,
    ]

    if failures:
        lines.append("[STATUS]: REPROVADO COM INCONFORMIDADES\n")
        for s_name, err_list in failures.items():
            lines.append(f"[FAIL] {s_name}:")
            for err in err_list:
                lines.append(f"   ↳ {err}")
    else:
        lines.append("[STATUS]: 100% PASS - TODAS AS SKILLS EM CONFORMIDADE DETERMINÍSTICA")

    return "\n".join(lines)


@mcp.tool()
def franklin_get_agents() -> str:
    """Retorna o catálogo oficial dos 7 Subagentes Especialistas do Franklin Quebra-Galho e suas diretrizes."""
    if AGENTS_MD_PATH.exists():
        return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace")
    return "Arquivo AGENTS.md não encontrado na raiz do workspace."


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

    # Determina o interpretador
    cmd: List[str] = []
    if script_path.suffix.lower() == ".py":
        cmd = [sys.executable, str(script_path)]
    elif script_path.suffix.lower() == ".ps1":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    elif script_path.suffix.lower() == ".cmd" or script_path.suffix.lower() == ".bat":
        cmd = ["cmd.exe", "/c", str(script_path)]
    else:
        return f"Erro: Extensão de script '{script_path.suffix}' não suportada para execução direta."

    if args:
        cmd.extend(args)

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
        status_code = f"[Exit Code: {res.returncode}]"
        return f"{status_code}\n{out if out else '(Script executado sem retorno textual)'}"
    except subprocess.TimeoutExpired:
        return f"Erro: Execução excedeu o tempo limite de {timeout_seconds} segundos."
    except Exception as e:
        return f"Erro ao executar script: {e}"


@mcp.tool()
def franklin_execute_dag(
    plan_path_or_json: str,
    run_id: str = "",
    resume: bool = False,
    timeout_seconds: float = 0,
    db_path: str = ""
) -> str:
    """Executa um plano de orquestração em grafo acíclico dirigido (DAG) via motor do Epic-Volta.

    Despacha o plano com ordenação topológica (Kahn), concorrência por ondas,
    projeção de campos upstream por dot-notation e persistência transacional SQLite WAL.

    Args:
        plan_path_or_json: Caminho para o arquivo JSON do plano ou string JSON contendo o DAGExecutionPlan.
        run_id: Identificador único opcional da execução (essencial para retomar execuções com resume=True).
        resume: Se True, retoma a execução sem reexecutar nós já concluídos no SQLite.
        timeout_seconds: Tempo limite global da execução em segundos (0 para sem limite).
        db_path: Caminho do banco SQLite de persistência (padrão: .sessions/dag_cli.db do epic-volta).
    """
    if not EPIC_VOLTA_DIR.exists():
        return json.dumps({
            "status": "FAILED",
            "error": f"Repositório Epic-Volta não encontrado em {EPIC_VOLTA_DIR}."
        }, ensure_ascii=False)

    plan_str = plan_path_or_json.strip()
    resolved_plan_path: Optional[Path] = None
    temp_file: Optional[Path] = None

    # 1. Verifica se é um arquivo existente
    candidate_paths = [
        Path(plan_str),
        ROOT_DIR / plan_str,
        EPIC_VOLTA_DIR / plan_str,
    ]
    for cp in candidate_paths:
        if cp.exists() and cp.is_file():
            resolved_plan_path = cp.resolve()
            break

    # 2. Se não for arquivo, tenta interpretar como JSON embutido
    if not resolved_plan_path:
        try:
            parsed = json.loads(plan_str)
            if not isinstance(parsed, dict):
                return json.dumps({
                    "status": "INVALID_PLAN",
                    "error": "O payload JSON deve ser um objeto compatível com DAGExecutionPlan."
                }, ensure_ascii=False)

            temp_dir = ROOT_DIR / ".sessions" / "temp_plans"
            temp_dir.mkdir(parents=True, exist_ok=True)
            import uuid
            temp_file = temp_dir / f"plan_{uuid.uuid4().hex[:8]}.json"
            temp_file.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
            resolved_plan_path = temp_file.resolve()
        except json.JSONDecodeError as exc:
            return json.dumps({
                "status": "FILE_NOT_FOUND_OR_INVALID_JSON",
                "error": f"Não foi possível localizar o arquivo nem interpretar como JSON válido: {exc}"
            }, ensure_ascii=False)

    # 3. Monta comando CLI via uv
    cmd = [
        "uv",
        "--directory",
        str(EPIC_VOLTA_DIR),
        "run",
        "python",
        "-m",
        "orchestrator.cli",
        str(resolved_plan_path),
        "--json"
    ]

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
        else:
            stderr = res.stderr.strip()
            return stdout if stdout.startswith("{") else json.dumps({
                "status": "FAILED",
                "exit_code": res.returncode,
                "stdout": stdout,
                "stderr": stderr
            }, ensure_ascii=False)
    except subprocess.TimeoutExpired:
        return json.dumps({
            "status": "TIMEOUT",
            "error": f"Execução do DAG excedeu o limite de {timeout_seconds} segundos."
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "error": str(e)
        }, ensure_ascii=False)
    finally:
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except OSError:
                pass


@mcp.tool()
def franklin_harness_guard(
    task_intent: str,
    proposed_tool_or_action: str = "",
    session_id: str = "default",
) -> str:
    """Aplica o Harness de Governança Determinística e Human-in-the-Loop antes de executar ações.

    Avalia a intenção da tarefa e a ferramenta proposta contra o ecossistema de 26 Skills do Franklin:
    1. Executa sanitização semântica preventiva contra injeções de prompt e tokens maliciosos.
    2. Aplica Divulgação Progressiva: identifica a Skill mais adequada e suas regras de corte.
    3. Avalia o nível de risco: se a intenção ou ferramenta envolver mutações destrutivas no disco ou Drive
       (Remove-Item, deleção, expurgo, format, descarte), classifica como CRITICAL, pausa a execução
       e cria um Checkpoint persistente pendente de aprovação humana.
    4. Se for operação de leitura/segura (análise, auditoria, conversão, Get-ChildItem), classifica como
       LOW e retorna AUTHORIZED com as diretrizes da Skill.

    Args:
        task_intent: O que se pretende realizar em linguagem natural.
        proposed_tool_or_action: Ferramenta MCP, script ou comando de terminal pretendido.
        session_id: Identificador da sessão para rastreabilidade de checkpoint.

    Returns:
        JSON com status ('AUTHORIZED'|'APPROVAL_REQUIRED'|'BLOCKED'), riskLevel, activeSkill, reason, instructions, checkpointId.
    """
    import uuid

    # 1. Sanitização Semântica
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

    # 2. Resolução Progressiva de Skills entre as 26 skills reais
    skills = _get_all_skills_data()
    combined_query = f"{clean_intent} {clean_action}".lower()

    best_skill: dict[str, Any] | None = None
    max_score = 0
    for s in skills:
        score = 0
        name = s["name"].lower()
        if name in combined_query:
            score += 20
        for tag in s.get("tags", []):
            if len(tag) > 3 and tag.lower() in combined_query:
                score += len(tag)
        if score > max_score:
            max_score = score
            best_skill = s

    active_skill_name = best_skill["name"] if best_skill else "franklin-main"
    persona = best_skill["persona"] if best_skill else "Franklin-Main"

    # 3. Avaliação Determinística de Risco
    risk_level, risk_reason = evaluate_action_risk(f"{clean_intent} {clean_action}")

    # 4. Ação Crítica: Pausa Operacional e Checkpoint Durável (HITL)
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

    # 5. Ação Segura: Autorização Imediata
    return json.dumps({
        "status": "AUTHORIZED",
        "riskLevel": "LOW",
        "activeSkill": active_skill_name,
        "persona": persona,
        "reason": risk_reason,
        "instructions": (
            f"Operação segura autorizada pelo Harness sob a persona {persona}. "
            f"Siga os procedimentos e salvaguardas da skill '{active_skill_name}'."
        )
    }, indent=2, ensure_ascii=False)


@mcp.tool()
def franklin_harness_checkpoint(
    action: str = "list",
    session_id: str = "default",
    checkpoint_id: str = "",
    approved: bool = False,
    notes: str = ""
) -> str:
    """Gerencia checkpoints de governança e aprovações humanas no ecossistema do Franklin.

    Args:
        action: 'list' (listar checkpoints pendentes), 'get' (detalhes de um ID), 'approve' (aprovar ação retida), 'reject' (vetar ação), 'clear' (limpar histórico).
        session_id: Filtro de sessão opcional para a listagem.
        checkpoint_id: ID do checkpoint alvo (ex: 'chk-a1b2c3d4').
        approved: True quando ação for 'approve'.
        notes: Justificativa ou notas do operador humano.

    Returns:
        JSON com a lista de pendências ou confirmação da deliberação humana.
    """
    act = action.strip().lower()

    if act == "list":
        pending = harness_store.list(status="PENDING", session_id=session_id if session_id != "all" else None)
        return json.dumps({
            "totalPending": len(pending),
            "checkpoints": [r.to_dict() for r in pending]
        }, indent=2, ensure_ascii=False)

    if act == "get":
        if not checkpoint_id:
            return json.dumps({"error": "checkpoint_id é obrigatório para a ação 'get'"}, ensure_ascii=False)
        rec = harness_store.get(checkpoint_id)
        if not rec:
            return json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
        return json.dumps(rec.to_dict(), indent=2, ensure_ascii=False)

    if act == "approve":
        if not checkpoint_id:
            return json.dumps({"error": "checkpoint_id é obrigatório para aprovação"}, ensure_ascii=False)
        rec = harness_store.update_status(checkpoint_id, status="APPROVED", notes=notes or "Aprovado pelo operador")
        if not rec:
            return json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
        return json.dumps({
            "status": "APPROVED",
            "checkpointId": checkpoint_id,
            "message": f"Ação '{rec.proposed_action}' foi APROVADA pelo operador humano. A execução pode prosseguir.",
            "record": rec.to_dict()
        }, indent=2, ensure_ascii=False)

    if act == "reject":
        if not checkpoint_id:
            return json.dumps({"error": "checkpoint_id é obrigatório para rejeição"}, ensure_ascii=False)
        rec = harness_store.update_status(checkpoint_id, status="REJECTED", notes=notes or "Rejeitado pelo operador")
        if not rec:
            return json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
        return json.dumps({
            "status": "REJECTED",
            "checkpointId": checkpoint_id,
            "message": f"Ação '{rec.proposed_action}' foi VETADA pelo operador humano. A execução está cancelada.",
            "record": rec.to_dict()
        }, indent=2, ensure_ascii=False)

    if act == "clear":
        count = harness_store.clear()
        return json.dumps({"status": "CLEARED", "removedCount": count}, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"Ação '{action}' inválida. Use: list, get, approve, reject ou clear."}, ensure_ascii=False)


# -----------------------------------------------------------------------------
# Recursos MCP (Resources)
# -----------------------------------------------------------------------------
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
    """Gera prompt para auditoria tátil de frontend sob os padrões do FrontCraftMaster."""
    return f"""Atue como FrontCraftMaster e audite a seguinte interface/código: {component_or_url}.
Avalie contra o Design System Tátil Melki:
1. Menus claustrofóbicos vs descompactados (padding nobre, min 240px em sidebar).
2. Botões ergonômicos (altura mínima 40px, padding horizontal generoso, micro-interação tátil).
3. Paleta Mineral Anti-Cobalto (fundo ardósia/creme, acentos minerais, banimento de azul cobalto puro).
4. Profundidade de sombras e elevação (Tactile Matte 4K).
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
