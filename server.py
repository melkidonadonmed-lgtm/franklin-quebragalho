"""Servidor MCP Oficial do Franklin Quebra-Galho (Ecossistema de Skills 2026).

Ponto de entrada enxuto que registra as ferramentas (@mcp.tool), recursos (@mcp.resource)
e prompts (@mcp.prompt) delegando a lógica de negócio para os módulos de domínio em shared/:
- shared.catalog_service: Descoberta, busca híbrida, leitura e validação de skills.
- shared.compass_topology: Subagentes, Topologia 3+1 de UI e Smart Compass.
- shared.execution_orchestrator: Execução isolada de scripts, motor DAG, Harness² e A2A v1.0.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.a2a_bridge import FranklinA2ATaskManager, build_franklin_agent_card
from shared.catalog_service import (
    AGENTS_MD_PATH,
    CANONICAL_PERSONA_MAPPING,
    EPIC_VOLTA_DIR,
    MY_SKILLS_MD_PATH,
    QUICK_SKILL_ALIASES,
    SKILLS_ROOT,
    _find_skill_dir,
    _get_all_skills_data,
    _load_agents_map,
    skills_get_impl,
    skills_list_impl,
    skills_search_impl,
    skills_validate_impl,
)
from shared.compass_topology import (
    COMPASS_PROFILE_RULES,
    PERSONA_ALIASES,
    UI_SUBAGENT_ALIASES,
    get_agents_impl,
    smart_compass_impl,
)
from shared.execution_orchestrator import (
    a2a_agent_card_impl,
    a2a_dispatch_task_impl,
    execute_dag_impl,
    harness_checkpoint_impl,
    harness_guard_impl,
    run_skill_script_impl,
)
from shared.harness import CheckpointStore
from shared.mcp_2026_advisor import evaluate_mcp_2026_architecture

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    class FastMCP:  # type: ignore[no-redef]
        """Fallback de FastMCP para ambientes de inspeção sem o SDK instalado."""

        def __init__(self, name: str, **kwargs: Any) -> None:
            self.name = name

        def _identity_decorator(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
                return fn
            return decorator

        tool = _identity_decorator
        resource = _identity_decorator
        prompt = _identity_decorator

        def run(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("O pacote 'mcp' não está instalado. Execute: pip install -e .")


mcp = FastMCP("Franklin Skills MCP")
SESSIONS_DIR = ROOT_DIR / ".sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
harness_store = CheckpointStore(SESSIONS_DIR / "harness_checkpoints.json")
a2a_task_manager = FranklinA2ATaskManager(skills_dir=SKILLS_ROOT, checkpoint_store=harness_store)


# -----------------------------------------------------------------------------
# Ferramentas MCP (@mcp.tool) — Catálogo, Subagentes, Execução, Harness² e A2A
# -----------------------------------------------------------------------------
@mcp.tool()
def franklin_skills_list(
    status: str = "all", persona: str = "all", search: str = "", format: str = "markdown"
) -> str:
    """Lista todas as skills disponíveis no ecossistema Franklin Quebra-Galho."""
    return skills_list_impl(status=status, persona=persona, search=search, format=format)


@mcp.tool()
def franklin_skills_get(skill_name: str, section: str = "contract") -> str:
    """Obtém o contrato completo (SKILL.md) ou seções específicas de uma skill."""
    return skills_get_impl(skill_name=skill_name, section=section)


@mcp.tool()
def franklin_skills_search(query: str, limit: int = 5) -> str:
    """Busca semântica e por palavras-chave qual skill e persona ativar para uma tarefa."""
    return skills_search_impl(query=query, limit=limit)


@mcp.tool()
def franklin_skills_validate(target_skill: str = "") -> str:
    """Valida a integridade estrutural e de segurança das skills contra o padrão de 2026."""
    return skills_validate_impl(target_skill=target_skill)


@mcp.tool()
def franklin_get_agents(agent_name: str = "") -> str:
    """Obtém as definições dos agentes mestres (AGENTS.md), subagentes do Epic-Volta ou Topologia 3+1 de UI."""
    return get_agents_impl(agent_name=agent_name)


@mcp.tool()
def franklin_smart_compass(
    intent_or_path: str = "", auto_dispatch_dag: bool = False, target_dir: str = ""
) -> str:
    """Bússola Inteligente (Smart Compass) do ecossistema Franklin + Epic-Volta."""
    return smart_compass_impl(
        intent_or_path=intent_or_path,
        auto_dispatch_dag=auto_dispatch_dag,
        target_dir=target_dir,
        dag_executor=lambda alias, t_dir: franklin_execute_dag(alias, target_dir=t_dir),
    )


@mcp.tool()
def franklin_run_skill_script(
    skill_name: str, script_name: str, args: Optional[List[str]] = None, timeout_seconds: int = 60
) -> str:
    """Executa um script determinístico localizado na pasta scripts/ de uma skill."""
    return run_skill_script_impl(
        skill_name=skill_name, script_name=script_name, args=args, timeout_seconds=timeout_seconds
    )


@mcp.tool()
def franklin_execute_dag(
    plan_path_or_json: str,
    run_id: str = "",
    resume: bool = False,
    timeout_seconds: float = 0,
    db_path: str = "",
    target_dir: str = "",
) -> str:
    """Executa um plano de orquestração em Grafo Acíclico Dirigido (DAG) no motor Epic-Volta."""
    return execute_dag_impl(
        plan_path_or_json=plan_path_or_json,
        run_id=run_id,
        resume=resume,
        timeout_seconds=timeout_seconds,
        db_path=db_path,
        target_dir=target_dir,
    )


@mcp.tool()
def franklin_harness_guard(
    task_intent: str, proposed_tool_or_action: str = "", session_id: str = "default"
) -> str:
    """Guardrail Central do Agent Harness (Engenharia de Governança 2026)."""
    return harness_guard_impl(
        harness_store=harness_store,
        task_intent=task_intent,
        proposed_tool_or_action=proposed_tool_or_action,
        session_id=session_id,
    )


@mcp.tool()
def franklin_harness_checkpoint(
    action: str = "list",
    session_id: str = "default",
    checkpoint_id: str = "",
    approved: bool = False,
    notes: str = "",
) -> str:
    """Gerencia checkpoints de governança HITL e sub-ações recursivas Harness²."""
    _ = approved
    return harness_checkpoint_impl(
        harness_store=harness_store,
        sessions_dir=SESSIONS_DIR,
        action=action,
        session_id=session_id,
        checkpoint_id=checkpoint_id,
        notes=notes,
    )


@mcp.tool()
def franklin_a2a_agent_card(skill_filter: str = "", verify_signature: bool = True) -> str:
    """Gera e assina criptograficamente (JCS + JWS HMAC-SHA256) o AgentCard oficial A2A v1.0."""
    return a2a_agent_card_impl(skill_filter=skill_filter, verify_signature=verify_signature)


@mcp.tool()
def franklin_a2a_dispatch_task(
    query: str = "",
    skill_id: str = "",
    context_id: str = "ctx-default",
    task_id: str = "",
    action: str = "send",
    execute_dag: bool = False,
    target_dir: str = "",
) -> str:
    """Despacha, consulta ou cancela uma Task no protocolo Agent2Agent (A2A v1.0) acoplado ao Harness HITL."""
    return a2a_dispatch_task_impl(
        a2a_task_manager=a2a_task_manager,
        query=query,
        skill_id=skill_id,
        context_id=context_id,
        task_id=task_id,
        action=action,
        execute_dag=execute_dag,
        target_dir=target_dir,
    )


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
    """Consultor Arquitetural MCP 2026-07-28 (build-with-agent-skills)."""
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
# Recursos MCP (@mcp.resource) e Prompts (@mcp.prompt)
# -----------------------------------------------------------------------------
@mcp.resource("skills://mcp-2026/spec")
def get_mcp_2026_spec_resource() -> str:
    """Recurso passivo expondo a matriz da especificação MCP 2026-07-28, SEP-2577 e Build with Agent Skills."""
    return json.dumps(evaluate_mcp_2026_architecture(), indent=2, ensure_ascii=False)


@mcp.resource("skills://a2a/agent-card")
def get_a2a_agent_card_resource() -> str:
    """Recurso passivo expondo o AgentCard oficial A2A v1.0 assinado do Franklin Quebra-Galho."""
    return json.dumps(build_franklin_agent_card(skills_dir=SKILLS_ROOT, sign=True), indent=2, ensure_ascii=False)


@mcp.resource("skills://harness/checkpoints")
def get_harness_checkpoints_resource() -> str:
    """Recurso passivo expondo a lista de checkpoints e aprovações pendentes do Harness."""
    return json.dumps([r.to_dict() for r in harness_store.list()], indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog")
def get_catalog_resource() -> str:
    """Recurso passivo expondo o catálogo consolidado de skills em formato JSON."""
    return json.dumps(_get_all_skills_data(), indent=2, ensure_ascii=False)


@mcp.resource("skills://manifest")
def get_manifest_resource() -> str:
    """Recurso passivo expondo o manifesto completo e ciclo de vida de MY_SKILLS.md."""
    return MY_SKILLS_MD_PATH.read_text(encoding="utf-8", errors="replace") if MY_SKILLS_MD_PATH.exists() else "MY_SKILLS.md não encontrado."


@mcp.resource("skills://agents")
def get_agents_resource() -> str:
    """Recurso passivo expondo a arquitetura e diretrizes de AGENTS.md."""
    return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace") if AGENTS_MD_PATH.exists() else "AGENTS.md não encontrado."


@mcp.resource("skills://agent/{agent_name}")
def get_agent_contract_resource(agent_name: str) -> str:
    """Recurso passivo para leitura direta do contrato de um subagente."""
    return franklin_get_agents(agent_name=agent_name)


@mcp.resource("skills://skill/{skill_name}")
def get_skill_resource(skill_name: str) -> str:
    """Recurso passivo para leitura direta do contrato SKILL.md de uma skill."""
    return franklin_skills_get(skill_name=skill_name, section="contract")


@mcp.resource("skills://rules/{skill_name}")
def get_rules_resource(skill_name: str) -> str:
    """Recurso passivo para leitura direta dos critérios de auditoria de uma skill."""
    return franklin_skills_get(skill_name=skill_name, section="rules")


@mcp.prompt("activate_skill")
def activate_skill_prompt(skill_name: str, user_intent: str) -> str:
    """Gera o prompt estruturado de ativação de uma skill sob os padrões de 2026."""
    skill_content = franklin_skills_get(skill_name=skill_name, section="contract")
    rules_content = franklin_skills_get(skill_name=skill_name, section="rules")
    return (
        f"Você está assumindo o papel de executor especialista da skill '{skill_name}'.\n"
        f"Siga estritamente o contrato operacional e as regras determinísticas abaixo:\n\n"
        f"--- CONTRATO DA SKILL ({skill_name}) ---\n{skill_content}\n\n"
        f"--- REGRAS DE AUDITORIA E RESTRIÇÕES ---\n{rules_content}\n\n"
        f"--- INTENÇÃO DO USUÁRIO ---\n{user_intent}\n\n"
        f"Proceda com a execução seguindo a taxonomia determinística e as salvaguardas necessárias.\n"
    )


@mcp.prompt("tactile_frontend_audit")
def tactile_frontend_audit_prompt(component_or_url: str) -> str:
    """Gera prompt para auditoria tátil de frontend sob os padrões do FrontCraftMaster e Topologia 3+1."""
    return (
        f"Atue como FrontCraftMaster e audite a seguinte interface/código: {component_or_url}.\n"
        "Coordene a Topologia 3+1 de Subagentes de UI (ui-shell-navigator, ui-controls-data, "
        "ui-motion-interaction, ui-deterministic-observer) via invoke_subagent (Modo Nativo Antigravity em 3 ondas) "
        "ou via franklin_get_agents(agent_name=\"ui\") / franklin_execute_dag(\"plans/ui_composition_dag.json\") "
        "(Modo Motor DAG Assíncrono) e avalie contra o Design System Tátil Melki:\n"
        "1. Menus claustrofóbicos vs descompactados (padding nobre, min 240px em sidebar, CLS < 0.1).\n"
        "2. Botões ergonômicos (altura mínima 44px, anti-squish shrink-0 whitespace-nowrap, micro-interação tátil).\n"
        "3. Paleta Mineral Anti-Cobalto (fundo ardósia/creme, acentos minerais, banimento de azul cobalto puro).\n"
        "4. Profundidade de sombras e elevação (Iluminação 135°, .ui-card-soft e cavidades surface-inset — DESIGN.md v4.5-soft).\n"
        "Emita o Relatório Comparativo determinístico com marcadores [PASS], [FAIL] e notas explicativas.\n"
    )


def run() -> None:
    """Ponto de entrada para execução STDIO do servidor MCP."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
