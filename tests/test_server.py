"""
test_server.py
Testes determinísticos para validação do Franklin Skills MCP Server.
"""

import json
import pytest
from pathlib import Path

import server


def test_server_initialization():
    """Valida se o servidor e os diretórios base estão configurados corretamente."""
    assert server.mcp.name == "Franklin Skills MCP"
    assert server.SKILLS_ROOT.exists()
    assert server.SKILLS_ROOT.is_dir()


def test_skills_list_all():
    """Valida se a listagem retorna todas as 26 skills ativas."""
    res = server.franklin_skills_list()
    assert "Catálogo de Skills do Franklin Quebra-Galho" in res
    assert "arquiteto-conteudo-solucoes" in res
    assert "conversor-html-pdf" in res
    assert "gdrive-auditoria-limpeza" in res
    assert "analise-design-tatil-frontend" in res

    # Formato JSON
    json_res = server.franklin_skills_list(format="json")
    data = json.loads(json_res)
    assert isinstance(data, list)
    assert len(data) >= 25


def test_skills_list_filters():
    """Valida os filtros por persona e status."""
    frontcraft_res = server.franklin_skills_list(persona="FrontCraftMaster")
    assert "analise-design-tatil-frontend" in frontcraft_res
    assert "gdrive-auditoria-limpeza" not in frontcraft_res

    drive_res = server.franklin_skills_list(persona="DriveMaster")
    assert "gdrive-auditoria-limpeza" in drive_res
    assert "analise-design-tatil-frontend" not in drive_res


def test_skills_get_contract_and_sections():
    """Valida o carregamento granular com divulgação progressiva."""
    # Contrato nuclear
    contract = server.franklin_skills_get("redator-tecnico-markdown", section="contract")
    contract_upper = contract.upper()
    assert "GATILHOS" in contract_upper or "MISSÃO" in contract_upper or "PROPÓSITO" in contract_upper

    # Rules
    rules = server.franklin_skills_get("redator-tecnico-markdown", section="rules")
    assert "[PASS]" in rules

    # Evals
    evals = server.franklin_skills_get("redator-tecnico-markdown", section="evals")
    eval_json = json.loads(evals)
    assert isinstance(eval_json, list)

    # Inexistente com fuzzy match
    missing = server.franklin_skills_get("redator-tecnico-inexistente")
    assert "Erro: Skill" in missing


def test_skills_search():
    """Valida a busca por intenção operacional e relevância."""
    # Busca por PDF
    pdf_res = server.franklin_skills_search("gerar relatório executivo e converter em pdf")
    assert "conversor-html-pdf" in pdf_res or "redator-tecnico-markdown" in pdf_res or "gerar-docs-pdf" in pdf_res

    # Busca por Google Drive
    drive_res = server.franklin_skills_search("limpeza de arquivos duplicados no drive")
    assert "gdrive-auditoria-limpeza" in drive_res or "organizar-gdrive" in drive_res

    # Busca por Frontend Tátil
    front_res = server.franklin_skills_search("inspecionar menu compactado e botões pequenos")
    assert "analise-design-tatil-frontend" in front_res or "refatoracao-design-tatil-frontend" in front_res


def test_skills_validate_deterministic():
    """Valida se a auditoria determinística do MCP aprova as 26 skills com 100% PASS."""
    res = server.franklin_skills_validate()
    assert "[STATUS]: 100% PASS" in res
    assert "REPROVADO" not in res


def test_get_agents():
    """Valida a extração do catálogo de subagentes."""
    res = server.franklin_get_agents()
    assert "FrontCraftMaster" in res
    assert "DriveMaster" in res
    assert "DocMaker" in res
    assert "LoopPlanner" in res


def test_run_skill_script_security():
    """Valida as travas de segurança contra Path Traversal no executor de scripts."""
    res_traversal = server.franklin_run_skill_script("workspace", "../secrets.txt")
    assert "Erro de Segurança" in res_traversal

    res_missing = server.franklin_run_skill_script("workspace", "script_fantasma.py")
    assert "não existe" in res_missing


def test_resources():
    """Valida a renderização dos recursos MCP passivos."""
    catalog = server.get_catalog_resource()
    assert "arquiteto-conteudo-solucoes" in catalog

    manifest = server.get_manifest_resource()
    assert "Minhas Skills" in manifest

    agents = server.get_agents_resource()
    assert "Franklin Quebra-Galho" in agents


def test_prompts():
    """Valida os prompts estruturados de 2026."""
    p_act = server.activate_skill_prompt("redator-tecnico-markdown", "Escrever ata de reunião")
    assert "Você está assumindo o papel de executor especialista" in p_act
    assert "redator-tecnico-markdown" in p_act

    p_front = server.tactile_frontend_audit_prompt("https://meuapp.com")
    assert "FrontCraftMaster" in p_front
    assert "Design System Tátil Melki" in p_front
