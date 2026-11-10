"""Servidor MCP Oficial do Franklin Quebra-Galho (`franklin-skills` • MCP Spec 2026-07-28 + A2A v1.0 JWS).

Registra de forma concisa as 13 ferramentas (`@mcp.tool`), os recursos passivos (`@mcp.resource`)
e os 2 prompts (`@mcp.prompt`), delegando toda a lógica de domínio aos módulos em `shared/`:
- `shared.catalog_service`: Descoberta, busca, leitura em 3 Tiers e validação das 29 Agent Skills.
- `shared.compass_topology`: Bússola Zero-LLM (`franklin_smart_compass`), 8 Personas e 10 Subagentes.
- `shared.execution_orchestrator`: Execução confinada de scripts, motor DAG Kahn, Harness HITL e A2A v1.0.
"""

from __future__ import annotations

import json
import sys
import typing
from pathlib import Path
from typing import Any, Callable, List, Optional

if not hasattr(typing, "no_type_check_decorator"):
    typing.no_type_check_decorator = lambda f: f  # type: ignore[attr-defined]
try:
    import beartype.claw
    beartype.claw.beartype_this_package = lambda *a, **kw: None  # type: ignore[assignment]
except ImportError as _beartype_err:
    _ = _beartype_err

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

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
    get_progressive_registry,
    skills_get_impl,
    skills_list_impl,
    skills_search_impl,
    skills_validate_impl,
)
from shared.modular_orchestrator import AgentOrchestrator, ProgressiveSkillRegistry
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
from shared.harness import CheckpointStore, dispatch_harness2_action, execute_with_idempotency
from shared.mcp_2026_advisor import evaluate_mcp_2026_architecture

try:
    from fastmcp import FastMCP
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
MCP_2026_META = {"io.modelcontextprotocol/protocolVersion": "2026-07-28"}
RO_ANNOTATIONS = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
MUT_ANNOTATIONS = {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False}


# -----------------------------------------------------------------------------
# Ferramentas MCP (@mcp.tool) — Catálogo, Subagentes, Execução, Harness² e A2A
# -----------------------------------------------------------------------------
@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_list(
    status: str = "all", persona: str = "all", search: str = "", format: str = "markdown"
) -> str:
    """Lista todas as skills disponíveis no ecossistema Franklin Quebra-Galho."""
    return skills_list_impl(status=status, persona=persona, search=search, format=format)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_get(skill_name: str, section: str = "contract") -> str:
    """Obtém o contrato completo (SKILL.md) ou seções específicas de uma skill."""
    return skills_get_impl(skill_name=skill_name, section=section)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_search(query: str, limit: int = 5) -> str:
    """Busca semântica e por palavras-chave qual skill e persona ativar para uma tarefa."""
    return skills_search_impl(query=query, limit=limit)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_validate(target_skill: str = "") -> str:
    """Valida a integridade estrutural e de segurança das skills contra o padrão de 2026."""
    return skills_validate_impl(target_skill=target_skill)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_get_agents(agent_name: str = "") -> str:
    """Obtém as definições dos agentes mestres (AGENTS.md), subagentes do Epic-Volta ou Topologia 3+1 de UI."""
    return get_agents_impl(agent_name=agent_name)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
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


@mcp.tool(annotations=MUT_ANNOTATIONS, meta=MCP_2026_META)
def franklin_run_skill_script(
    skill_name: str,
    script_name: str,
    args: Optional[List[str]] = None,
    timeout_seconds: int = 60,
    target_dir: str = "",
    idempotency_key: str = "",
) -> str:
    """Executa um script determinístico localizado na pasta scripts/ de uma skill (suporta target_dir cross-project)."""
    return execute_with_idempotency(
        SESSIONS_DIR,
        idempotency_key,
        "franklin_run_skill_script",
        lambda: run_skill_script_impl(
            skill_name=skill_name,
            script_name=script_name,
            args=args,
            timeout_seconds=timeout_seconds,
            target_dir=target_dir,
        ),
    )


@mcp.tool(annotations=MUT_ANNOTATIONS, meta=MCP_2026_META)
def franklin_execute_dag(
    plan_path_or_json: str,
    run_id: str = "",
    resume: bool = False,
    timeout_seconds: float = 0,
    db_path: str = "",
    target_dir: str = "",
    idempotency_key: str = "",
) -> str:
    """Executa um plano de orquestração em Grafo Acíclico Dirigido (DAG) no motor Epic-Volta."""
    return execute_with_idempotency(
        SESSIONS_DIR,
        idempotency_key,
        "franklin_execute_dag",
        lambda: execute_dag_impl(
            plan_path_or_json=plan_path_or_json,
            run_id=run_id,
            resume=resume,
            timeout_seconds=timeout_seconds,
            db_path=db_path,
            target_dir=target_dir,
        ),
    )


@mcp.tool(annotations=MUT_ANNOTATIONS, meta=MCP_2026_META)
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


@mcp.tool(annotations=MUT_ANNOTATIONS, meta=MCP_2026_META)
def franklin_harness_checkpoint(
    action: str = "list",
    session_id: str = "default",
    checkpoint_id: str = "",
    approved: bool = False,
    notes: str = "",
    approval_token: str = "",
    idempotency_key: str = "",
) -> str:
    """Gerencia checkpoints de governança HITL e sub-ações recursivas Harness²."""
    effective_notes = notes
    if approval_token.strip() and not notes.strip().startswith("{"):
        effective_notes = f"{notes} [approval_token={approval_token.strip()}]".strip()
    return execute_with_idempotency(
        SESSIONS_DIR,
        idempotency_key,
        "franklin_harness_checkpoint",
        lambda: harness_checkpoint_impl(
            harness_store=harness_store,
            sessions_dir=SESSIONS_DIR,
            action=action,
            session_id=session_id,
            checkpoint_id=checkpoint_id,
            approved=approved,
            notes=effective_notes,
        ),
    )


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_a2a_agent_card(skill_filter: str = "", verify_signature: bool = True) -> str:
    """Gera e assina criptograficamente (JCS + JWS HMAC-SHA256) o AgentCard oficial A2A v1.0."""
    return a2a_agent_card_impl(skill_filter=skill_filter, verify_signature=verify_signature)


@mcp.tool(annotations=MUT_ANNOTATIONS, meta=MCP_2026_META)
def franklin_a2a_dispatch_task(
    query: str = "",
    skill_id: str = "",
    context_id: str = "ctx-default",
    task_id: str = "",
    action: str = "send",
    execute_dag: bool = False,
    target_dir: str = "",
    approval_token: str = "",
    idempotency_key: str = "",
) -> str:
    """Despacha, consulta, retoma ou cancela uma Task no protocolo Agent2Agent (A2A v1.0) acoplado ao Harness HITL."""
    return a2a_dispatch_task_impl(
        a2a_task_manager=a2a_task_manager,
        query=query,
        skill_id=skill_id,
        context_id=context_id,
        task_id=task_id,
        action=action,
        execute_dag=execute_dag,
        target_dir=target_dir,
        approval_token=approval_token,
        idempotency_key=idempotency_key,
    )


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
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
# Recursos MCP (@mcp.resource) e Prompts (@mcp.prompt) — Enxutos e Sincronizados
# -----------------------------------------------------------------------------
@mcp.resource("skills://mcp-2026/spec")
def get_mcp_2026_spec_resource() -> str:
    """Matriz arquitetural MCP 2026-07-28 e diretrizes build-with-agent-skills."""
    return json.dumps(evaluate_mcp_2026_architecture(), indent=2, ensure_ascii=False)


@mcp.resource("skills://a2a/agent-card")
def get_a2a_agent_card_resource() -> str:
    """AgentCard oficial A2A v1.0 assinado com JWS (HMAC-SHA256)."""
    return json.dumps(build_franklin_agent_card(skills_dir=SKILLS_ROOT, sign=True), indent=2, ensure_ascii=False)


@mcp.resource("skills://harness/checkpoints")
def get_harness_checkpoints_resource() -> str:
    """Checkpoints pendentes e histórico HITL do Harness."""
    return json.dumps([r.to_dict() for r in harness_store.list()], indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog")
def get_catalog_resource() -> str:
    """Catálogo consolidado das 29 Agent Skills em JSON."""
    return json.dumps(_get_all_skills_data(), indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog/xml")
def get_catalog_xml_resource() -> str:
    """Catálogo Nível 1 (<available_skills>) em XML enxuto."""
    return get_progressive_registry().render_catalog_prompt()


@mcp.resource("skills://manifest")
def get_manifest_resource() -> str:
    """Manifesto completo de ciclo de vida (`MY_SKILLS.md`)."""
    return MY_SKILLS_MD_PATH.read_text(encoding="utf-8", errors="replace") if MY_SKILLS_MD_PATH.exists() else "MY_SKILLS.md não encontrado."


@mcp.resource("skills://agents")
def get_agents_resource() -> str:
    """Arquitetura de Personas e Subagentes (`AGENTS.md`)."""
    return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace") if AGENTS_MD_PATH.exists() else "AGENTS.md não encontrado."


@mcp.resource("skills://agent/{agent_name}")
def get_agent_contract_resource(agent_name: str) -> str:
    """Contrato declarativo de uma persona ou subagente (`agents/*.md`)."""
    return franklin_get_agents(agent_name=agent_name)


@mcp.resource("skills://skill/{skill_name}")
def get_skill_resource(skill_name: str) -> str:
    """Contrato operacional `SKILL.md` (Tier 2) de uma skill."""
    return franklin_skills_get(skill_name=skill_name, section="contract")


@mcp.prompt("activate_skill")
def activate_skill_prompt(skill_name: str, user_intent: str) -> str:
    """Prompt estruturado de ativação de uma skill com seu contrato e regras."""
    skill_content = franklin_skills_get(skill_name=skill_name, section="contract")
    rules_content = franklin_skills_get(skill_name=skill_name, section="rules")
    return (
        f"Você está assumindo o papel de executor especialista da skill '{skill_name}'.\n"
        f"Siga o contrato operacional e os critérios determinísticos abaixo:\n\n"
        f"--- CONTRATO ({skill_name}) ---\n{skill_content}\n\n"
        f"--- REGRAS ---\n{rules_content}\n\n"
        f"--- INTENÇÃO ---\n{user_intent}\n"
    )


@mcp.prompt("tactile_frontend_audit")
def tactile_frontend_audit_prompt(component_or_url: str) -> str:
    """Prompt conciso para auditoria Frontend/UI-Architect acoplado ao SSOT (`rules/diretrizes-frontend-9-eixos.md`)."""
    return (
        f"Atue como UI-Architect e audite `{component_or_url}` contra `DESIGN.md` e os 9 Eixos do SSOT:\n"
        "1. Regra 60-30-10 em `OKLCH` + `light-dark()` e tokens em 3 camadas (`--bg-canvas`, `--surface-card`, `--surface-elevated`, `--surface-sunken`).\n"
        "2. Sombras Multi-Camadas em 3 Níveis (`--shadow-elevation-1..3` + `--shadow-inset`: Umbra + Penumbra + Luz Zenital `inset 0 1px 0 0`).\n"
        "3. Navegação em 3 Camadas, `@container`, 4 Variantes de Cards, nitidez `tabular-nums`/`font-synthesis: none` e Engenharia Real-State.\n"
        "Execute `audit_tactile_ui.py`, `ui_ux_frontend_auditor.py` e `deterministic_scorer.py` (`auditoria-projetos-sistema`).\n"
    )


def run() -> None:
    """Ponto de entrada para execução STDIO do servidor MCP."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
