#!/usr/bin/env python3
"""
standardize_skills_metadata.py
Aplica a padronização canônica do bloco metadata e license em todas as skills
do ecossistema Franklin Quebra-Galho, sincronizando .agents/skills/, skills/
e o plugin global franklin-skills.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# Blindagem de codificação para consoles Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
AGENTS_SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
MIRROR_SKILLS_DIR = ROOT_DIR / "skills"
GLOBAL_PLUGIN_DIR = Path.home() / ".gemini" / "config" / "plugins" / "franklin-skills" / "skills"

SKILL_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "_template": {
        "name": "template-skill",
        "folder": "_template",
        "version": "1.2.0",
        "author": "Franklin-Main & Melki",
        "category": "Engenharia e Governança de Skills",
        "tags": ["template", "padrao-2026", "design-tatil"],
    },
    "analise-design-tatil-frontend": {
        "name": "analise-design-tatil-frontend",
        "folder": "analise-design-tatil-frontend",
        "version": "1.0.0",
        "author": "FrontCraftMaster & Melki",
        "category": "Design System Tátil e Frontend",
        "tags": ["design-tatil", "auditoria-ui", "anti-cobalto", "ergonomia"],
    },
    "aprimoramento-expansibilidade-agentes-skills": {
        "name": "aprimoramento-expansibilidade-agentes-skills",
        "folder": "aprimoramento-expansibilidade-agentes-skills",
        "version": "1.0.0",
        "author": "SkillCraft & Melki",
        "category": "Arquitetura e Expansibilidade de Agentes",
        "tags": ["multiagente", "otimizacao-contexto", "cot", "react"],
    },
    "arquiteto-conteudo-solucoes": {
        "name": "arquiteto-conteudo-solucoes",
        "folder": "arquiteto-conteudo-solucoes",
        "version": "2.2.0",
        "author": "Franklin-Main & Melki",
        "category": "Arquitetura de Soluções e Engenharia de Conteúdo",
        "tags": ["prompt-engineering", "arquitetura", "anti-alucinacao"],
    },
    "arquitetura-design-implementacao-sistema": {
        "name": "arquitetura-design-implementacao-sistema",
        "folder": "arquitetura-design-implementacao-sistema",
        "version": "1.1.0",
        "author": "Franklin-Main & Melki",
        "category": "Arquitetura e Implementação de Software",
        "tags": ["especificacao-funcional", "arquitetura", "design-tatil"],
    },
    "auditoria-projetos-sistema": {
        "name": "auditoria-projetos-sistema",
        "folder": "auditoria-projetos-sistema",
        "version": "2.1.0",
        "author": "Franklin-Main & Melki",
        "category": "Auditoria Estrutural e Higiene de Repositório",
        "tags": ["auditoria", "agent-browser", "higiene-repo", "qualidade"],
    },
    "consultor-design-tatil-frontend": {
        "name": "consultor-design-tatil-frontend",
        "folder": "consultor-design-tatil-frontend",
        "version": "1.1.0",
        "author": "FrontCraftMaster & Melki",
        "category": "Consultoria de Design Tátil e UX",
        "tags": ["consultoria-ux", "design-tatil", "paleta-mineral", "design-md"],
    },
    "context-sentinel": {
        "name": "context-sentinel",
        "folder": "context-sentinel",
        "version": "1.0.0",
        "author": "Franklin-Main & Melki",
        "category": "Auditoria e Integridade de Janela de Contexto",
        "tags": ["context-rot", "sqlite", "snapshots", "pydantic"],
    },
    "conversor-html-pdf": {
        "name": "conversor-html-pdf",
        "folder": "conversor-html-pdf",
        "version": "1.0.0",
        "author": "DocMaker & Melki",
        "category": "Publicação e Conversão de Documentos",
        "tags": ["pdf", "headless-browser", "css-print", "conversao"],
    },
    "curadoria-obsidian-vault": {
        "name": "curadoria-obsidian-vault",
        "folder": "curadoria-obsidian-vault",
        "version": "1.0.0",
        "author": "VaultMaster & Melki",
        "category": "Gestão de Conhecimento e PKM",
        "tags": ["obsidian", "wikilinks", "frontmatter", "anexos-orfaos"],
    },
    "design-interface-medica-minimalista": {
        "name": "design-interface-medica-minimalista",
        "folder": "design-interface-medica-minimalista",
        "version": "1.0.0",
        "author": "Franklin-Main & Melki",
        "category": "Design de Interface Médica Minimalista",
        "tags": ["saude", "clinico", "prontuario", "minimalista", "tailwind"],
    },
    "evoluir-skills": {
        "name": "evoluir-skills",
        "folder": "evoluir-skills",
        "version": "1.1.0",
        "author": "SkillCraft & Melki",
        "category": "Engenharia e Governança de Skills",
        "tags": ["skills", "evals", "ciclo-de-vida", "governanca"],
    },
    "gap-analyzer-auditor": {
        "name": "gap-analyzer-auditor",
        "folder": "gap-analyzer-auditor",
        "version": "2.0.0",
        "author": "LoopPlanner & Melki",
        "category": "Auditoria de Processos, RCA e Hand-off Multiagente",
        "tags": ["rca", "closed-loop", "hand-off", "auditoria"],
    },
    "gdrive-auditoria-limpeza": {
        "name": "gdrive-auditoria-limpeza",
        "folder": "gdrive-auditoria-limpeza",
        "version": "1.0.0",
        "author": "DriveMaster & Melki",
        "category": "Gestão Cloud e Higienização de Armazenamento",
        "tags": ["google-drive", "limpeza", "sha256", "dry-run"],
    },
    "gdrive-taxonomia-organizacao": {
        "name": "gdrive-taxonomia-organizacao",
        "folder": "gdrive-taxonomia-organizacao",
        "version": "1.0.0",
        "author": "DriveMaster & Melki",
        "category": "Gestão Cloud e Taxonomia Documental",
        "tags": ["google-drive", "taxonomia", "datas-iso", "organizacao"],
    },
    "gerar-docs-pdf": {
        "name": "gerar-docs-pdf",
        "folder": "gerar-docs-pdf",
        "version": "1.0.0",
        "author": "DocMaker & Melki",
        "category": "Geração e Conversão de Documentos PDF",
        "tags": ["markdown", "pdf", "relatorios", "conversao"],
    },
    "high-level-context-planner": {
        "name": "high-level-context-planner",
        "folder": "high-level-context-planner",
        "version": "2.0.0",
        "author": "LoopPlanner & Melki",
        "category": "Planejamento Estratégico, Orquestração Multiagente e Workflows",
        "tags": ["planejamento", "fase-zero", "closed-loop", "replanning"],
    },
    "manutencao-disco-windows": {
        "name": "manutencao-disco-windows",
        "folder": "manutencao-disco-windows",
        "version": "1.0.0",
        "author": "FileOpsLocal & Melki",
        "category": "Sistema Operacional e Automação Local",
        "tags": ["windows-11", "powershell", "downloads", "disco"],
    },
    "organizador-fluxo-arvore-arquivos": {
        "name": "organizador-fluxo-arvore-arquivos",
        "folder": "organizador-fluxo-arvore-arquivos",
        "version": "1.1.0",
        "author": "DocMaker & Melki",
        "category": "Planejamento Visual e Diagramação de Diretórios",
        "tags": ["mermaid", "arvore-arquivos", "fluxogramas", "planejamento"],
    },
    "organizar-gdrive": {
        "name": "organizar-gdrive",
        "folder": "organizar-gdrive",
        "version": "1.0.0",
        "author": "DriveMaster & Melki",
        "category": "Gestão Cloud e Armazenamento Google Drive",
        "tags": ["google-drive", "mcp-drive", "classificacao", "arquivos"],
    },
    "organizar-local": {
        "name": "organizar-local",
        "folder": "organizar-local",
        "version": "1.0.0",
        "author": "FileOpsLocal & Melki",
        "category": "Organização e Manutenção de Disco Local",
        "tags": ["windows-11", "local-storage", "powershell", "dev-folder"],
    },
    "redator-tecnico-markdown": {
        "name": "redator-tecnico-markdown",
        "folder": "redator-tecnico-markdown",
        "version": "1.1.0",
        "author": "DocMaker & Melki",
        "category": "Documentação Técnica e Redação Estruturada",
        "tags": ["markdown", "obsidian", "google-styleguides", "documentacao"],
    },
    "refatoracao-design-tatil-frontend": {
        "name": "refatoracao-design-tatil-frontend",
        "folder": "refatoracao-design-tatil-frontend",
        "version": "1.1.0",
        "author": "FrontCraftMaster & Melki",
        "category": "Implementação e Refatoração Frontend",
        "tags": ["frontend", "design-tatil", "tailwind", "refatoracao", "anti-cobalto"],
    },
    "refine-prompt": {
        "name": "refine-prompt",
        "folder": "refine-prompt",
        "version": "3.0.0",
        "author": "Franklin-Main & Melki",
        "category": "Engenharia de Prompts, Auditoria Epistêmica e Segurança Zero-Trust",
        "tags": ["refine-prompt", "zero-trust", "epistemica", "owasp-llm"],
    },
    "skill-auditor-refatorador-skills": {
        "name": "skill-auditor-refatorador-skills",
        "folder": "skill-auditor-refatorador-skills",
        "version": "1.2.0",
        "author": "SkillCraft & Melki",
        "category": "Governança, Metaprompting e Arquitetura de Agentes",
        "tags": ["auditoria", "refatoracao", "metaprompting", "governanca-skills"],
    },
    "skill-orquestrador-planos-encadeados": {
        "name": "skill-orquestrador-planos-encadeados",
        "folder": "skill-orquestrador-planos-encadeados",
        "version": "1.1.0",
        "author": "LoopPlanner & Melki",
        "category": "Orquestração, Workflows e Execução Multiagente",
        "tags": ["orquestrador", "planos-encadeados", "workflow", "multiagente"],
    },
}


def extract_description(content: str) -> str:
    """Extrai a descrição atual do frontmatter preservando seu texto exato."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return ""
    raw_yaml = match.group(1)
    
    desc_lines = []
    capturing = False
    for line in raw_yaml.splitlines():
        if re.match(r"^description\s*:\s*(.*)$", line):
            capturing = True
            first_val = re.match(r"^description\s*:\s*(.*)$", line).group(1).strip()
            if first_val not in (">-", ">", "|", "|-", ""):
                desc_lines.append(first_val.strip("'\""))
            continue
        if capturing:
            if re.match(r"^[a-zA-Z0-9_\-]+:", line):
                break
            desc_lines.append(line.strip())
            
    desc = " ".join([d for d in desc_lines if d]).strip()
    return desc


def extract_body(content: str) -> str:
    """Extrai o corpo do documento markdown após o frontmatter."""
    match = re.match(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$", content, re.DOTALL)
    if match:
        return match.group(1)
    return content


def build_frontmatter(defn: Dict[str, Any], description: str) -> str:
    """Gera o frontmatter canônico padronizado com licença e bloco metadata."""
    tag_lines = "\n".join([f'    - "{t}"' for t in defn["tags"]])
    
    fm = f"""---
name: {defn['name']}
description: >-
  {description}
license: MIT
metadata:
  version: "{defn['version']}"
  author: "{defn['author']}"
  category: "{defn['category']}"
  updated_at: "2026-10-04"
  tags:
{tag_lines}
version: {defn['version']}
updated_at: 2026-10-04
author: {defn['author']}
category: {defn['category']}
---
"""
    return fm


def main():
    print("=== PADRONIZANDO METADADOS E FRONTMATTER DE SKILLS ===")
    updated_count = 0

    for folder_name, defn in SKILL_DEFINITIONS.items():
        src_skill = AGENTS_SKILLS_DIR / folder_name / "SKILL.md"
        if not src_skill.exists():
            print(f"[WARN] Skill não encontrada: {src_skill}")
            continue

        raw_content = src_skill.read_text(encoding="utf-8")
        desc = extract_description(raw_content)
        if not desc:
            print(f"[FAIL] Não foi possível extrair descrição de {folder_name}")
            continue

        body = extract_body(raw_content)
        new_fm = build_frontmatter(defn, desc)
        new_full_content = new_fm + "\n" + body.lstrip()

        # Grava em .agents/skills/
        src_skill.write_text(new_full_content, encoding="utf-8")

        # Espelha em skills/
        mirror_skill = MIRROR_SKILLS_DIR / folder_name / "SKILL.md"
        if mirror_skill.parent.exists():
            mirror_skill.write_text(new_full_content, encoding="utf-8")

        # Espelha no plugin global franklin-skills se existir
        if GLOBAL_PLUGIN_DIR.exists():
            plugin_skill = GLOBAL_PLUGIN_DIR / folder_name / "SKILL.md"
            if plugin_skill.parent.exists():
                plugin_skill.write_text(new_full_content, encoding="utf-8")

        updated_count += 1
        print(f"[OK] Padronizada: {folder_name:<40} (v{defn['version']})")

    print("-" * 65)
    print(f"Sucesso: {updated_count} skills padronizadas com sucesso.")


if __name__ == "__main__":
    main()
