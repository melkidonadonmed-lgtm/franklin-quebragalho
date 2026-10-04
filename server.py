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


# -----------------------------------------------------------------------------
# Utilitários de Parsing de Metadados e Estado
# -----------------------------------------------------------------------------
def _parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extrai frontmatter YAML simples e corpo do documento Markdown."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    raw_yaml, body = match.group(1), match.group(2)
    meta: Dict[str, Any] = {}
    current_key: Optional[str] = None
    multiline_val: List[str] = []

    for line in raw_yaml.splitlines():
        if re.match(r"^\s+", line) and current_key:
            multiline_val.append(line.strip())
            continue

        if current_key and multiline_val:
            meta[current_key] = " ".join(multiline_val)
            multiline_val = []
            current_key = None

        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            key, val = kv_match.group(1), kv_match.group(2).strip()
            if val in (">-", ">", "|", "|-"):
                current_key = key
                multiline_val = []
            else:
                val = val.strip("'\"")
                meta[key] = val
                current_key = None

    if current_key and multiline_val:
        meta[current_key] = " ".join(multiline_val)

    return meta, body


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
                        if not isinstance(evals_data, list) or len(evals_data) == 0:
                            errs.append("evals.json deve ser uma lista não-vazia")
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


# -----------------------------------------------------------------------------
# Recursos MCP (Resources)
# -----------------------------------------------------------------------------
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
