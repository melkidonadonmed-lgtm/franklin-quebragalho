"""
modular_orchestrator.py
Arquitetura Multiagente Modular em 6 Papéis + Motor de Divulgação Progressiva (Progressive Disclosure)
em 3 Níveis para o Ecossistema Franklin Quebra-Galho (Padrão 2026).

Componentes:
1. ProgressiveSkillRegistry (Nível 1: Catálogo <available_skills>, Nível 2: Ativação <skill_content>,
   Nível 3: Leitura de Recurso <resource_content> com proteção contra Path Traversal).
2. Contratos Estritos de Handoff (Pydantic v2): MasterSkillInvocation, IntentAnalysisResult,
   PlanDecompositionResult, TaskExecutionResult e QualityAuditResult.
3. Topologia de 6 Papéis: IntentAnalysisAgent, PlannerAgent, MCPWorkerAgent (Context Fork),
   HITL Security Gate, CriticAuditorAgent (Critic Loop) e ReporterAgent.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from shared._progressive_registry import (
    BUNDLED_SUBDIRS,
    LoadedSkill,
    ProgressiveSkillRegistry,
    SkillMetadata,
)
from shared.harness import (
    CheckpointStore,
    RefinementTelemetryRecord,
    RefinementTelemetryStore,
    RiskLevel,
    RootCauseCategory,
    SemanticGuard,
    classify_failure_root_cause,
    evaluate_action_risk,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("AgentArchitecture")


# ==============================================================================
# Contratos Estritos de Handoff (Pydantic v2)
# ==============================================================================
class MasterSkillInvocation(BaseModel):
    """Envelope polimórfico para invocação tipada de skills, scripts ou recursos."""

    model_config = ConfigDict(extra="forbid")

    skill_name: str = Field(..., min_length=1)
    action: Literal["activate", "read_resource", "run_script", "execute_dag"] = "activate"
    resource_or_script: str = ""
    args: List[str] = Field(default_factory=list)
    target_dir: str = ""


class IntentAnalysisResult(BaseModel):
    """Contrato emitido pelo Subagente 1 (Intenção & Triagem Read-Only)."""

    model_config = ConfigDict(extra="forbid")

    intent: str = Field(..., description="Objetivo principal identificado")
    category: Literal["DIRECT", "RESEARCH", "MUTATION", "DAG_WORKFLOW", "AMBIGUOUS"]
    recommended_worker: Literal["research_worker", "data_worker", "dag_worker", "direct_handler"]
    recommended_skill: str = "franklin-main"
    persona: str = "Franklin-Main"
    structural_framework: Literal["CLAREZA", "CREATE", "RTF", "TAG", "TASS"] = "CLAREZA"
    cognitive_patterns: List[Literal["CoT", "ReAct", "ToT", "Self-Refine"]] = Field(
        default_factory=lambda: ["CoT", "ReAct"]
    )
    action_parameters: Dict[str, Any] = Field(default_factory=dict)
    requires_hitl: bool = False


class PlanDecompositionResult(BaseModel):
    """Contrato emitido pelo Subagente 2 (Planejador / Decompositor Read-Only com Complexity Wall Shield)."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str
    disclosure_tier: Literal[1, 2, 3] = 2
    max_rules_per_node: int = Field(default=3, ge=1, le=5)
    complexity_shield_status: Literal["SHIELDED", "SUBDIVIDED"] = "SHIELDED"
    execution_mode: Literal["AGENT_TOOL", "SUBAGENT_FORK"] = "AGENT_TOOL"
    expected_evidence_keys: List[str] = Field(default_factory=lambda: ["records_analyzed", "output"])
    steps: List[str] = Field(default_factory=list)
    dag_alias: str = ""
    target_dir: str = ""


class TaskExecutionResult(BaseModel):
    """Resultado emitido pelo Subagente 3 (Worker Especialista em Context Fork)."""

    model_config = ConfigDict(extra="forbid")

    worker_id: str
    status: Literal["SUCCESS", "FAILED", "NEEDS_INFO"]
    data_payload: Dict[str, Any]
    error_message: Optional[str] = None


class QualityAuditResult(BaseModel):
    """Veredito emitido pelo Subagente 5 (Crítico / Avaliador com Self-Refine)."""

    model_config = ConfigDict(extra="forbid")

    approved: bool
    score: float = Field(..., ge=0.0, le=1.0)
    critique_feedback: str
    should_retry: bool = False
    root_cause_category: Optional[str] = None
    post_condition_verified: bool = False


# ==============================================================================
# Topologia Hierárquica de 6 Subagentes
# ==============================================================================
class BaseSubAgent(ABC):
    """Interface abstrata para todos os nós agênticos da topologia."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    async def process(self, context_payload: Dict[str, Any]) -> Any:
        """Executa a transformação determinística do subagente."""
        raise NotImplementedError("Subclasses devem implementar process(context_payload)")


class IntentAnalysisAgent(BaseSubAgent):
    """1. Subagente de Análise de Intenção & Triagem (Read-only, sem tools destrutivas)."""

    MUTATION_KEYWORDS: tuple[str, ...] = (
        "atualizar", "deletar", "apagar", "pagar", "gravar", "remove-item", "rm -rf", "drop table", "excluir",
    )
    RESEARCH_KEYWORDS: tuple[str, ...] = (
        "pesquisar", "buscar", "analisar", "explicar", "auditar", "listar", "verificar", "inspecionar",
    )
    DAG_KEYWORDS: tuple[str, ...] = ("dag", "4-stage", "actor-critic", "ondas", "multiagente", "pipeline ui", "pipeline fisica")

    async def process(self, context_payload: Dict[str, Any]) -> IntentAnalysisResult:
        raw_query = str(context_payload.get("user_query", "")).strip()
        target_dir = str(context_payload.get("target_dir", "")).strip()
        cleaned_query = SemanticGuard.sanitize_input(raw_query)
        q_low = cleaned_query.lower()

        risk_level, _ = evaluate_action_risk(cleaned_query)
        is_mutation = risk_level == RiskLevel.CRITICAL or any(w in q_low for w in self.MUTATION_KEYWORDS)
        is_dag = any(w in q_low for w in self.DAG_KEYWORDS)
        is_research = any(w in q_low for w in self.RESEARCH_KEYWORDS)

        skill = str(context_payload.get("skill_name", "system-project-auditor"))
        persona = str(context_payload.get("persona", "Franklin-Main"))
        params: Dict[str, Any] = {"query": cleaned_query, "target_dir": target_dir, "skill_name": skill}

        if is_mutation:
            return IntentAnalysisResult(
                intent="Operação de mutação ou alteração de estado crítico", category="MUTATION",
                recommended_worker="data_worker", recommended_skill=skill, persona=persona,
                structural_framework="CLAREZA", cognitive_patterns=["CoT", "ReAct", "Self-Refine"],
                action_parameters=params, requires_hitl=True,
            )
        if is_dag:
            return IntentAnalysisResult(
                intent="Orquestração em Grafo Acíclico Dirigido (DAG)", category="DAG_WORKFLOW",
                recommended_worker="dag_worker", recommended_skill=skill, persona=persona,
                structural_framework="CLAREZA", cognitive_patterns=["CoT", "ReAct", "ToT", "Self-Refine"],
                action_parameters=params, requires_hitl=False,
            )
        if is_research:
            return IntentAnalysisResult(
                intent="Pesquisa, auditoria read-only e consolidação de conhecimento", category="RESEARCH",
                recommended_worker="research_worker", recommended_skill=skill, persona=persona,
                structural_framework="CLAREZA", cognitive_patterns=["CoT", "ReAct"],
                action_parameters=params, requires_hitl=False,
            )
        return IntentAnalysisResult(
            intent="Interação conversacional ou ativação direta", category="DIRECT",
            recommended_worker="direct_handler", recommended_skill=skill, persona=persona,
            structural_framework="TAG", cognitive_patterns=["CoT"],
            action_parameters=params, requires_hitl=False,
        )


class PlannerAgent(BaseSubAgent):
    """2. Subagente Planejador / Decompositor (Read-only, gera etapas atômicas <= 5 regras/nó e DAG)."""

    async def process(self, context_payload: Dict[str, Any]) -> PlanDecompositionResult:
        intent_res: IntentAnalysisResult = context_payload["intent_result"]
        q_low = str(intent_res.action_parameters.get("query", "")).lower()
        dag_alias = "physics" if ("3d" in q_low or "fisica" in q_low or "physics" in q_low) else "ui"
        tier: Literal[1, 2, 3] = 3 if intent_res.category in ("RESEARCH", "MUTATION") else 2
        exec_mode: Literal["AGENT_TOOL", "SUBAGENT_FORK"] = (
            "AGENT_TOOL" if intent_res.category == "DIRECT" else "SUBAGENT_FORK"
        )
        cog_str = "+".join(intent_res.cognitive_patterns)
        return PlanDecompositionResult(
            plan_id=f"plan-{uuid.uuid4().hex[:8]}",
            disclosure_tier=tier,
            max_rules_per_node=3,
            complexity_shield_status="SHIELDED",
            execution_mode=exec_mode,
            expected_evidence_keys=["records_analyzed", "output"],
            steps=[
                f"1. [CoT | Tier {tier}] Ativar contrato '{intent_res.recommended_skill}' sob framework {intent_res.structural_framework} (<= 5 regras/nó)",
                f"2. [{cog_str}] Executar worker '{intent_res.recommended_worker}' via {exec_mode}",
                "3. [Self-Refine] Auditar saída pelo CriticAuditorAgent via verificação Read-After-Write determinística",
            ],
            dag_alias=dag_alias if intent_res.category == "DAG_WORKFLOW" else "",
            target_dir=str(intent_res.action_parameters.get("target_dir", "")),
        )


class MCPWorkerAgent(BaseSubAgent):
    """3. Subagente Especialista Executor em Context Fork isolado ou Agent Tool determinística."""

    def __init__(self, name: str, tool_dispatcher: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None) -> None:
        super().__init__(name)
        self.tool_dispatcher = tool_dispatcher

    def _execute_default_inspection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Performs default read-only filesystem verification when no tool dispatcher is wired."""
        target_str = str(params.get("target_dir", "")).strip()
        skill_name = str(params.get("skill_name", "system-project-auditor")).strip()
        repo_skills_dir = Path(__file__).resolve().parent.parent / "skills" / skill_name
        if target_str and Path(target_str).exists():
            t_path = Path(target_str)
            files_count = sum(1 for _ in t_path.iterdir()) if t_path.is_dir() else 1
            return {
                "records_analyzed": max(1, files_count),
                "skill_activated": skill_name,
                "target_dir": target_str,
                "output": f"[PASS] Inspeção determinística de {files_count} item(ns) em {target_str}.",
            }
        if not target_str and repo_skills_dir.exists():
            return {
                "records_analyzed": 1,
                "skill_activated": skill_name,
                "target_dir": str(repo_skills_dir),
                "output": f"[PASS] Contrato da skill '{skill_name}' verificado no disco.",
            }
        return {}

    async def process(self, context_payload: Dict[str, Any]) -> TaskExecutionResult:
        params = dict(context_payload.get("action_parameters", {}))
        plan: Optional[PlanDecompositionResult] = context_payload.get("plan")
        feedback = str(context_payload.get("feedback", "")).strip()
        if feedback:
            params["retry_feedback"] = feedback

        try:
            execution_data = (
                dict(self.tool_dispatcher(params) or {})
                if self.tool_dispatcher is not None
                else self._execute_default_inspection(params)
            )
            if execution_data and plan is not None:
                execution_data.setdefault("plan_id_executed", plan.plan_id)
                execution_data.setdefault("execution_mode", plan.execution_mode)
                execution_data.setdefault("steps_completed", len(plan.steps))
            return TaskExecutionResult(worker_id=self.name, status="SUCCESS", data_payload=execution_data)
        except (OSError, ValueError, RuntimeError, KeyError) as exc:
            logger.error("[%s] Erro na execução isolada da tool MCP: %s", self.name, exc)
            return TaskExecutionResult(worker_id=self.name, status="FAILED", data_payload={}, error_message=str(exc))


class CriticAuditorAgent(BaseSubAgent):
    """5. Subagente Crítico / Observador Read-After-Write Determinístico (0 tokens LLM)."""

    @staticmethod
    def _reject(score: float, feedback: str, cause: str) -> QualityAuditResult:
        return QualityAuditResult(
            approved=False, score=score, critique_feedback=feedback,
            should_retry=True, root_cause_category=cause, post_condition_verified=False,
        )

    @staticmethod
    def _check_written_files(written_files: Any) -> Optional[QualityAuditResult]:
        if not isinstance(written_files, list):
            return None
        missing = [f for f in written_files if not Path(str(f)).is_file() or Path(str(f)).stat().st_size == 0]
        if not missing:
            return None
        cause = RootCauseCategory.POST_CONDITION_FAILED.value
        return CriticAuditorAgent._reject(0.25, f"[FAIL:{cause}] Read-After-Write falhou para arquivos: {missing}", cause)

    async def process(self, context_payload: Dict[str, Any]) -> QualityAuditResult:
        task_result: TaskExecutionResult = context_payload["task_result"]
        plan: Optional[PlanDecompositionResult] = context_payload.get("plan")
        payload = task_result.data_payload or {}

        if task_result.status != "SUCCESS":
            cat, why = classify_failure_root_cause(task_result.error_message or "FAILED", payload)
            return self._reject(0.0, f"[FAIL:{cat.value}] Falha de execução no worker '{task_result.worker_id}': {why}", cat.value)

        job_status = str(payload.get("job_status", "")).upper()
        if job_status in ("PENDING", "RUNNING", "IN_PROGRESS"):
            cause = RootCauseCategory.PREMATURE_RETURN_NO_WAIT.value
            return self._reject(0.20, f"[FAIL:{cause}] O worker retornou antes da conclusão do job ({job_status}).", cause)

        target_dir = str(payload.get("target_dir", "")).strip()
        if target_dir and not Path(target_dir).exists():
            cause = RootCauseCategory.POST_CONDITION_FAILED.value
            return self._reject(0.10, f"[FAIL:{cause}] Read-After-Write falhou: target_dir '{target_dir}' não existe no disco.", cause)

        file_err = self._check_written_files(payload.get("written_files"))
        if file_err is not None:
            return file_err

        if "records_analyzed" in payload or "output" in payload:
            plan_verified = bool(plan is None or payload.get("plan_id_executed") == plan.plan_id)
            return QualityAuditResult(
                approved=True, score=0.98 if plan_verified else 0.90,
                critique_feedback="[PASS] Pós-condição Read-After-Write e vínculo Planejador-Executor verificados.",
                should_retry=False, root_cause_category=None, post_condition_verified=True,
            )

        cat, why = classify_failure_root_cause("[FAIL] Saída vazia ou sem marcadores verificáveis.", payload)
        return self._reject(0.40, f"[FAIL:{cat.value}] {why}", cat.value)


class ReporterAgent(BaseSubAgent):
    """6. Subagente Sintetizador / Formatador (Isola a camada de apresentação)."""

    async def process(self, context_payload: Dict[str, Any]) -> str:
        intent: IntentAnalysisResult = context_payload["intent"]
        plan: PlanDecompositionResult = context_payload["plan"]
        task_result: TaskExecutionResult = context_payload["task_result"]
        audit: QualityAuditResult = context_payload["audit"]
        telemetry_info: Optional[Dict[str, Any]] = context_payload.get("telemetry_info")
        report_envelope: Dict[str, Any] = {
            "status": "APPROVED" if audit.approved else "REJECTED",
            "intentCategory": intent.category,
            "persona": intent.persona,
            "skill": intent.recommended_skill,
            "planId": plan.plan_id,
            "executionMode": plan.execution_mode,
            "workerId": task_result.worker_id,
            "qualityScore": audit.score,
            "postConditionVerified": audit.post_condition_verified,
            "critique": audit.critique_feedback,
            "data": task_result.data_payload,
        }
        if telemetry_info:
            report_envelope["refinementTelemetry"] = telemetry_info
        return json.dumps(report_envelope, indent=2, ensure_ascii=False)


class AgentOrchestrator:
    """Orquestrador Central Desacoplado coordenando os 6 papéis, Gate HITL e Telemetria Pós-Refinamento."""

    def __init__(
        self,
        checkpoint_store: Optional[CheckpointStore] = None,
        tool_dispatcher: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        max_retries: int = 3,
        telemetry_store: Optional[RefinementTelemetryStore] = None,
    ) -> None:
        self.intent_agent = IntentAnalysisAgent("IntentClassifier")
        self.planner_agent = PlannerAgent("ContractPlanner")
        self.workers: Dict[str, BaseSubAgent] = {
            "research_worker": MCPWorkerAgent("ResearchWorker", tool_dispatcher=tool_dispatcher),
            "data_worker": MCPWorkerAgent("DataMutationWorker", tool_dispatcher=tool_dispatcher),
            "dag_worker": MCPWorkerAgent("DAGWorkflowWorker", tool_dispatcher=tool_dispatcher),
            "direct_handler": MCPWorkerAgent("DirectHandlerWorker", tool_dispatcher=tool_dispatcher),
        }
        self.critic_agent = CriticAuditorAgent("CriticAuditor")
        self.reporter_agent = ReporterAgent("ReporterSynthesizer")
        self.checkpoint_store = checkpoint_store
        self.max_retries = max_retries
        self.telemetry_store = telemetry_store

    def _create_hitl_approval_response(self, user_query: str, intent: IntentAnalysisResult, session_id: str) -> str:
        """Registra checkpoint HITL para mutações críticas e retorna o envelope de pausa."""
        chk_id = f"chk-{uuid.uuid4().hex[:8]}"
        if self.checkpoint_store is not None:
            self.checkpoint_store.create(
                checkpoint_id=chk_id, session_id=session_id, task_intent=user_query,
                proposed_action=intent.intent, active_skill=intent.recommended_skill,
                risk_level="CRITICAL", notes="Intercepção preventiva pelo Gate HITL da Topologia de 6 Papéis.",
            )
        return json.dumps({
            "status": "APPROVAL_REQUIRED",
            "checkpointId": chk_id,
            "intentCategory": intent.category,
            "message": f"[Aguardando Aprovação Humana]: A operação '{intent.intent}' requer confirmação.",
        }, indent=2, ensure_ascii=False)

    def _record_turn_telemetry(
        self,
        plan_id: str,
        intent: IntentAnalysisResult,
        attempts: int,
        root_cause: str,
        why_failed: str,
        recovery_action: str,
        verified: bool,
        user_query: str,
    ) -> Optional[Dict[str, Any]]:
        """Registra telemetria pós-refinamento quando telemetry_store está configurado."""
        if self.telemetry_store is None:
            return None
        rec = RefinementTelemetryRecord(
            run_id=plan_id,
            step_id=intent.recommended_worker,
            attempt=attempts,
            root_cause=root_cause,
            why_failed_first_time=why_failed,
            chosen_path=f"{intent.recommended_skill}:{intent.recommended_worker}",
            recovery_action=recovery_action,
            post_condition_verified=verified,
        )
        return self.telemetry_store.record_refinement(rec, user_query=user_query)

    async def _run_worker_critic_loop(
        self,
        user_query: str,
        intent: IntentAnalysisResult,
        plan: PlanDecompositionResult,
        worker: BaseSubAgent,
    ) -> str:
        """Executes worker retries under CriticAuditorAgent RAW validation and telemetry capture."""
        attempts, current_feedback, first_fail_cause, first_fail_why = 0, "", "", ""
        while attempts < self.max_retries:
            attempts += 1
            task_result = await worker.process({"action_parameters": intent.action_parameters, "plan": plan, "feedback": current_feedback})
            audit = await self.critic_agent.process({"task_result": task_result, "plan": plan})
            if audit.approved:
                telemetry_info = self._record_turn_telemetry(
                    plan.plan_id, intent, attempts,
                    first_fail_cause or RootCauseCategory.POST_CONDITION_FAILED.value,
                    first_fail_why or current_feedback,
                    f"Refined execution with deterministic critic feedback on attempt {attempts}",
                    True, user_query,
                ) if attempts > 1 else None
                return await self.reporter_agent.process({
                    "intent": intent, "plan": plan, "task_result": task_result,
                    "audit": audit, "telemetry_info": telemetry_info,
                })
            if attempts == 1:
                first_fail_cause = audit.root_cause_category or RootCauseCategory.POST_CONDITION_FAILED.value
                first_fail_why = audit.critique_feedback
            current_feedback = audit.critique_feedback
            if not audit.should_retry:
                break

        exhaust_cause = RootCauseCategory.STUCK_IN_LOOP.value if attempts >= self.max_retries else (first_fail_cause or RootCauseCategory.POST_CONDITION_FAILED.value)
        self._record_turn_telemetry(
            plan.plan_id, intent, attempts, exhaust_cause, first_fail_why or current_feedback,
            "Exhausted retries without satisfying deterministic post-condition", False, user_query,
        )
        return json.dumps({
            "status": "FAILED", "attempts": attempts, "critique": current_feedback,
            "rootCause": first_fail_cause or RootCauseCategory.STUCK_IN_LOOP.value,
            "message": f"Falha na entrega após {attempts} tentativa(s).",
        }, indent=2, ensure_ascii=False)

    async def execute_turn(
        self,
        user_query: str,
        *,
        skill_name: str = "system-project-auditor",
        persona: str = "Franklin-Main",
        target_dir: str = "",
        session_id: str = "default",
    ) -> str:
        """Executa o ciclo completo em 6 estágios com proteção Zero-Trust, HITL, Critic Loop e Telemetria."""
        intent = await self.intent_agent.process({
            "user_query": user_query, "skill_name": skill_name, "persona": persona, "target_dir": target_dir,
        })
        plan = await self.planner_agent.process({"intent_result": intent})
        if intent.requires_hitl:
            return self._create_hitl_approval_response(user_query, intent, session_id)
        worker = self.workers.get(intent.recommended_worker)
        if not worker:
            return json.dumps({"status": "ERROR", "error": f"Worker '{intent.recommended_worker}' não registrado."}, ensure_ascii=False)
        return await self._run_worker_critic_loop(user_query, intent, plan, worker)

    def execute_turn_sync(self, user_query: str, **kwargs: Any) -> str:
        """Wrapper síncrono seguro para invocação a partir de tools MCP síncronas."""
        return asyncio.run(self.execute_turn(user_query, **kwargs))


__all__ = [
    "AgentOrchestrator",
    "BUNDLED_SUBDIRS",
    "BaseSubAgent",
    "CriticAuditorAgent",
    "IntentAnalysisAgent",
    "IntentAnalysisResult",
    "LoadedSkill",
    "MCPWorkerAgent",
    "MasterSkillInvocation",
    "PlanDecompositionResult",
    "PlannerAgent",
    "ProgressiveSkillRegistry",
    "QualityAuditResult",
    "ReporterAgent",
    "SkillMetadata",
    "TaskExecutionResult",
]
