"""Servidor MCP Oficial do Franklin Quebra-Galho (`franklin-skills` • MCP Spec 2026-07-28 + A2A v1.0 JWS).

Registra de forma concisa as 13 ferramentas (`@mcp.tool`), os recursos passivos (`@mcp.resource`)
e os 2 prompts (`@mcp.prompt`), delegando toda a lógica de domínio aos módulos em `shared/`:
- `shared.catalog_service`: Discovery, search, 3-Tier loading, and validation of the 21 Canonical Agent Skills (+ 6 Federated UI Skills).
- `shared.compass_topology`: Bússola Zero-LLM (`franklin_smart_compass`), 8 Personas, 5 Local Subagents, and 4 Federated UI Subagents.
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
    """List all canonical Agent Skills available in the Franklin Quebra-Galho ecosystem."""
    return skills_list_impl(status=status, persona=persona, search=search, format=format)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_get(skill_name: str, section: str = "contract") -> str:
    """Retrieve the full SKILL.md contract or specific sections (rules, scripts, references) of a skill."""
    return skills_get_impl(skill_name=skill_name, section=section)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_search(query: str, limit: int = 5) -> str:
    """Search by semantics and keywords to identify which skill and persona to activate for a task."""
    return skills_search_impl(query=query, limit=limit)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_skills_validate(target_skill: str = "") -> str:
    """Validate structural integrity, frontmatter contracts, and security boundaries of Agent Skills."""
    return skills_validate_impl(target_skill=target_skill)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_get_agents(agent_name: str = "") -> str:
    """Retrieve definitions of master agents (AGENTS.md), subagents, or UI topology roles."""
    return get_agents_impl(agent_name=agent_name)


@mcp.tool(annotations=RO_ANNOTATIONS, meta=MCP_2026_META)
def franklin_smart_compass(
    intent_or_path: str = "", auto_dispatch_dag: bool = False, target_dir: str = ""
) -> str:
    """Zero-LLM Smart Compass router mapping natural intent or paths to skills, subagents, and DAG plans."""
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
    """Execute a deterministic script located in a skill's scripts/ directory with cross-project target_dir support."""
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
    """Execute a Directed Acyclic Graph (DAG) orchestration plan on the Epic-Volta Kahn wave engine."""
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
    """Evaluate a proposed tool or action through the Agent Harness semantic guard and HITL risk policy."""
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
    """Manage HITL governance checkpoints and recursive Harness2 execution states."""
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
    """Generate and cryptographically sign (JCS + JWS HMAC-SHA256) the official A2A v1.0 AgentCard."""
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
    """Dispatch, inspect, resume, or cancel an Agent2Agent (A2A v1.0) task coupled with HITL governance."""
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
    """Evaluate MCP 2026-07-28 architecture options (deployment, Pattern A/B, Elicitation vs Widget, .mcpb)."""
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
# MCP Resources (@mcp.resource) & Prompts (@mcp.prompt)
# -----------------------------------------------------------------------------
@mcp.resource("skills://mcp-2026/spec")
def get_mcp_2026_spec_resource() -> str:
    """MCP 2026-07-28 architectural matrix and build-with-agent-skills guidelines."""
    return json.dumps(evaluate_mcp_2026_architecture(), indent=2, ensure_ascii=False)


@mcp.resource("skills://a2a/agent-card")
def get_a2a_agent_card_resource() -> str:
    """Official A2A v1.0 AgentCard signed with JWS (HMAC-SHA256)."""
    return json.dumps(build_franklin_agent_card(skills_dir=SKILLS_ROOT, sign=True), indent=2, ensure_ascii=False)


@mcp.resource("skills://harness/checkpoints")
def get_harness_checkpoints_resource() -> str:
    """Pending HITL checkpoints and Harness execution history."""
    return json.dumps([r.to_dict() for r in harness_store.list()], indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog")
def get_catalog_resource() -> str:
    """Consolidated JSON catalog of all Canonical Agent Skills."""
    return json.dumps(_get_all_skills_data(), indent=2, ensure_ascii=False)


@mcp.resource("skills://catalog/xml")
def get_catalog_xml_resource() -> str:
    """Level 1 (<available_skills>) progressive disclosure catalog in compact XML."""
    return get_progressive_registry().render_catalog_prompt()


@mcp.resource("skills://manifest")
def get_manifest_resource() -> str:
    """Complete skills lifecycle manifest (`MY_SKILLS.md`)."""
    return MY_SKILLS_MD_PATH.read_text(encoding="utf-8", errors="replace") if MY_SKILLS_MD_PATH.exists() else "MY_SKILLS.md not found."


@mcp.resource("skills://agents")
def get_agents_resource() -> str:
    """Master agents and subagent architecture (`AGENTS.md`)."""
    return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace") if AGENTS_MD_PATH.exists() else "AGENTS.md not found."


@mcp.resource("skills://agent/{agent_name}")
def get_agent_contract_resource(agent_name: str) -> str:
    """Declarative contract for a persona or subagent (`agents/*.md`)."""
    return franklin_get_agents(agent_name=agent_name)


@mcp.resource("skills://skill/{skill_name}")
def get_skill_resource(skill_name: str) -> str:
    """Operational Tier 2 contract (`SKILL.md`) for a skill."""
    return franklin_skills_get(skill_name=skill_name, section="contract")


@mcp.prompt("activate_skill")
def activate_skill_prompt(skill_name: str, user_intent: str) -> str:
    """Structured activation prompt for executing a skill with its contract and audit rules."""
    skill_content = franklin_skills_get(skill_name=skill_name, section="contract")
    rules_content = franklin_skills_get(skill_name=skill_name, section="rules")
    return (
        f"You are assuming the specialist executor role for skill '{skill_name}'.\n"
        f"Follow the operational contract and deterministic criteria below:\n\n"
        f"--- CONTRACT ({skill_name}) ---\n{skill_content}\n\n"
        f"--- AUDIT RULES ---\n{rules_content}\n\n"
        f"--- INTENT ---\n{user_intent}\n"
    )


@mcp.prompt("tactile_frontend_audit")
def tactile_frontend_audit_prompt(component_or_url: str) -> str:
    """Concise UI-Architect frontend audit prompt bound to the 9-axis SSOT (`rules/frontend-9-axes-guidelines.md`)."""
    return (
        f"Act as UI-Architect and audit `{component_or_url}` against `DESIGN.md` and the 9-Axis SSOT:\n"
        "1. 60-30-10 rule in `OKLCH` + `light-dark()` and 3-layer tokens (`--bg-canvas`, `--surface-card`, `--surface-elevated`, `--surface-sunken`).\n"
        "2. 3-level multi-layer shadows (`--shadow-elevation-1..3` + `--shadow-inset`: Contact Umbra + Penumbra + Zenith Catch-Light `inset 0 1px 0 0`).\n"
        "3. 3-layer navigation, `@container`, 4 Card variants, `tabular-nums`/`font-synthesis: none`, and Real-State Engineering.\n"
        "Run `audit_tactile_ui.py`, `ui_ux_frontend_auditor.py`, and `deterministic_scorer.py` (`system-project-auditor`).\n"
    )


__all__ = [
    "AGENTS_MD_PATH",
    "AgentOrchestrator",
    "CANONICAL_PERSONA_MAPPING",
    "COMPASS_PROFILE_RULES",
    "CheckpointStore",
    "EPIC_VOLTA_DIR",
    "MY_SKILLS_MD_PATH",
    "PERSONA_ALIASES",
    "ProgressiveSkillRegistry",
    "QUICK_SKILL_ALIASES",
    "SKILLS_ROOT",
    "UI_SUBAGENT_ALIASES",
    "_find_skill_dir",
    "_get_all_skills_data",
    "_load_agents_map",
    "dispatch_harness2_action",
    "execute_with_idempotency",
    "get_progressive_registry",
    "mcp",
    "run",
]


def run() -> None:
    """Ponto de entrada para execução STDIO do servidor MCP."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
