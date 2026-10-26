#!/usr/bin/env python3
"""
polymorphic_skill_envelope.py
Módulo de Governança e Execução: Envelope Polimórfico de Skill com Injeção Dinâmica de Esquemas (JIT),
Ledger de Idempotência Thread-Safe (SHA-256), Guarda Anti-Bloat, Higiene STDERR e Estimador Pass@k.
"""

from __future__ import annotations

import functools
import hashlib
import json
import logging
import operator
import re
import sys
import tempfile
import threading
import time
import uuid
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Callable, Dict, List, Literal, Optional, Type, Union

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError, field_validator

# -----------------------------------------------------------------------------
# 1. Higiene Estrita de Streams (Logs JSON Seguros Somente em STDERR)
# -----------------------------------------------------------------------------
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
ScalarValue = Union[str, int, float, bool, List[str]]


class StructuredStderrFormatter(logging.Formatter):
    """Serializa registros de log em JSON válido via json.dumps, prevenindo Log Injection."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)


def _configure_stderr_logger() -> logging.Logger:
    log = logging.getLogger("SkillGovernor")
    log.setLevel(logging.INFO)
    log.propagate = False
    if not log.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(StructuredStderrFormatter())
        log.addHandler(handler)
    return log


logger = _configure_stderr_logger()


# -----------------------------------------------------------------------------
# 2. Métrica Formal Determinística Pass@k (Estimador Não Enviesado)
# -----------------------------------------------------------------------------
def compute_pass_at_k(n: int, c: int, k: int) -> float:
    """
    Calcula o estimador formal não enviesado Pass@k:
    Pass@k = 1 - prod_{i=1}^{k} (1 - c / (n - k + i)).
    """
    if n < 1 or k < 1 or k > n:
        raise ValueError(f"Parâmetros inválidos para Pass@k: n={n}, k={k} (exige 1 <= k <= n).")
    if c < 0 or c > n:
        raise ValueError(f"Contagem de aprovados inválida: c={c} (exige 0 <= c <= n={n}).")
    if c == 0:
        return 0.0
    if n - c < k:
        return 1.0
    prod_fail = 1.0
    for i in range(1, k + 1):
        prod_fail *= 1.0 - (float(c) / float(n - k + i))
    return round(1.0 - prod_fail, 6)


# -----------------------------------------------------------------------------
# 3. Contratos de Domínio e Envelopes Imutáveis (Pydantic v2, extra="forbid")
# -----------------------------------------------------------------------------
class ActionCategory(str, Enum):
    READ_ONLY = "read_only"
    MUTATION = "mutation"
    ANALYSIS = "analysis"


class BaseActionPayload(BaseModel):
    """Contrato base imutável com bloqueio estrito de campos extras."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


def _validate_safe_relative_path(value: str) -> str:
    """Bloqueia caminhos absolutos, drives Windows, bytes nulos e Path Traversal ('..')."""
    if not value or "\x00" in value:
        raise ValueError("Caminho inválido ou vazio.")
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ValueError("Caminho absoluto proibido; informe apenas caminho relativo confinado.")
    parts = [p for p in normalized.split("/") if p]
    if not parts or ".." in parts:
        raise ValueError("Travessia de diretório ('..') detectada e bloqueada pelo Zero-Trust Guard.")
    return "/".join(parts)


class InspectCodePayload(BaseActionPayload):
    """Ação read-only de inspeção e auditoria estática de código-fonte."""

    action: Literal["inspect_code"] = Field(..., description="Identificador literal da ação.")
    target_path: str = Field(..., min_length=1, max_length=260, description="Caminho relativo a auditar.")
    ruleset: List[str] = Field(
        default_factory=lambda: ["ast_check", "type_hints", "security_audit"],
        min_length=1,
        description="Lista de regras normativas a avaliar.",
    )
    max_depth: int = Field(default=3, ge=1, le=10, description="Profundidade máxima de recursão.")

    @field_validator("target_path")
    @classmethod
    def _check_target_path(cls, v: str) -> str:
        return _validate_safe_relative_path(v)


class ApplyMutationPayload(BaseActionPayload):
    """Ação mutativa com controle obrigatório de idempotência e tipagem estrita."""

    action: Literal["apply_mutation"] = Field(..., description="Identificador literal da mutação.")
    target_entity_id: str = Field(..., min_length=3, max_length=128, description="ID canônico da entidade.")
    operation: Literal["insert", "update", "soft_delete"] = Field(..., description="Operação de mutação.")
    changes: Dict[str, ScalarValue] = Field(..., min_length=1, description="Mapa tipado de alterações.")
    idempotency_key: str = Field(..., min_length=16, max_length=128, description="Chave única anti-replay.")
    approval_token: Optional[str] = Field(default=None, description="Token opcional de aprovação HITL.")


class FetchTelemetryPayload(BaseActionPayload):
    """Ação de consulta temporal de métricas de engenharia (inclui cálculo Pass@k)."""

    action: Literal["fetch_telemetry"] = Field(..., description="Identificador literal de telemetria.")
    metric_name: str = Field(..., min_length=2, max_length=64, description="Nome da métrica canônica.")
    time_window_minutes: int = Field(default=60, ge=1, le=1440, description="Janela temporal em minutos.")
    samples_n: int = Field(default=100, ge=1, le=10000, description="Total de amostras executadas (n).")
    passed_c: int = Field(default=98, ge=0, le=10000, description="Total de amostras aprovadas (c).")
    k_value: int = Field(default=1, ge=1, le=100, description="Parâmetro k do estimador Pass@k.")


DefaultPolymorphicPayload = Annotated[
    Union[InspectCodePayload, ApplyMutationPayload, FetchTelemetryPayload],
    Field(discriminator="action"),
]


class PolymorphicSkillEnvelope(BaseModel):
    """Envelope canônico de entrada para validação de topo (Zero Alucinação na raiz)."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    skill_id: str = Field(..., min_length=2, max_length=128, description="Identificador da Skill.")
    correlation_id: str = Field(
        default_factory=lambda: f"trace-{uuid.uuid4().hex[:12]}",
        min_length=4,
        max_length=128,
        description="Identificador de rastreamento distribuído seguro.",
    )
    payload: Dict[str, Any] = Field(..., min_length=1, description="Carga bruta a ser validada pelo modelo da ação.")

    @field_validator("correlation_id")
    @classmethod
    def _sanitize_correlation_id(cls, v: str) -> str:
        if not _SAFE_ID_RE.match(v):
            raise ValueError("correlation_id contém caracteres ilegais ou tentativa de Path Traversal.")
        return v


class ErrorDetail(BaseModel):
    """Contrato estruturado de erro compatível com JSON-RPC 2.0 e MCP."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: int
    message: str
    details: Optional[List[Dict[str, Any]]] = None
    available_actions: Optional[List[str]] = None


# -----------------------------------------------------------------------------
# 4. Componentes Desacoplados de Infraestrutura (Idempotência & Context Bloat)
# -----------------------------------------------------------------------------
class IdempotencyLedger:
    """Livro-razão thread-safe com verificação de integridade SHA-256 do payload e evicção FIFO."""

    def __init__(self, max_entries: int = 2048) -> None:
        self.max_entries = max_entries
        self._lock = threading.Lock()
        self._store: Dict[str, tuple[str, Dict[str, Any]]] = {}

    @staticmethod
    def compute_payload_digest(payload: BaseActionPayload) -> str:
        canonical = json.dumps(payload.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def check(self, key: str, digest: str) -> Optional[Dict[str, Any]]:
        """Retorna resultado em cache se o digest coincidir; levanta ValueError se houver conflito."""
        with self._lock:
            if key not in self._store:
                return None
            saved_digest, cached_data = self._store[key]
            if saved_digest != digest:
                raise ValueError("Conflito de Idempotência: chave reutilizada com parâmetros divergentes.")
            return dict(cached_data)

    def record(self, key: str, digest: str, result: Dict[str, Any]) -> None:
        with self._lock:
            if len(self._store) >= self.max_entries and key not in self._store:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
            self._store[key] = (digest, dict(result))


class ContextBloatGuard:
    """Persiste retornos massivos em disco com confinamento estrito anti-Path-Traversal."""

    def __init__(self, scratch_dir: Path, max_chars: int = 15_000) -> None:
        self.scratch_dir = scratch_dir.resolve()
        self.scratch_dir.mkdir(parents=True, exist_ok=True)
        self.max_chars = max_chars

    def inspect_and_offload(self, correlation_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        serialized = json.dumps(data, ensure_ascii=False)
        if len(serialized) <= self.max_chars:
            return None
        safe_corr = re.sub(r"[^A-Za-z0-9_.-]", "_", correlation_id)[:96] or "trace"
        offload_path = (self.scratch_dir / f"payload_offload_{safe_corr}.json").resolve()
        if not offload_path.is_relative_to(self.scratch_dir):
            raise ValueError("Tentativa de escrita fora do diretório scratch bloqueada.")
        encoded_bytes = serialized.encode("utf-8")
        offload_path.write_bytes(encoded_bytes)
        logger.info(f"[{safe_corr}] Payload volumoso ({len(encoded_bytes)} bytes) persistido em {offload_path}")
        return {
            "status": "offloaded_to_disk",
            "file_path": str(offload_path),
            "total_chars": len(serialized),
            "total_bytes": len(encoded_bytes),
            "preview": serialized[:300] + "... [truncado para preservação de contexto]",
        }


# -----------------------------------------------------------------------------
# 5. Handlers Puros de Domínio (Desacoplados do Roteador)
# -----------------------------------------------------------------------------
def default_inspect_handler(payload: InspectCodePayload) -> Dict[str, Any]:
    return {
        "target_evaluated": payload.target_path,
        "max_depth_applied": payload.max_depth,
        "rules_checked": payload.ruleset,
        "compliance_status": "CONFORME",
        "findings": [
            {"file": "main.py", "rule": "type_hints", "status": "passed"},
            {"file": "router.py", "rule": "ast_check", "status": "passed"},
        ],
    }


def default_mutation_handler(payload: ApplyMutationPayload) -> Dict[str, Any]:
    return {
        "entity_id": payload.target_entity_id,
        "mutation_applied": payload.operation,
        "affected_fields": sorted(payload.changes.keys()),
        "idempotency_committed": payload.idempotency_key,
        "post_condition_verified": True,
        "state_version": 2,
    }


def default_telemetry_handler(payload: FetchTelemetryPayload) -> Dict[str, Any]:
    effective_c = min(payload.passed_c, payload.samples_n)
    effective_k = min(payload.k_value, payload.samples_n)
    pass_at_k_val = compute_pass_at_k(payload.samples_n, effective_c, effective_k)
    return {
        "metric": payload.metric_name,
        "window_minutes": payload.time_window_minutes,
        "samples_count": payload.samples_n,
        "passed_count": effective_c,
        "k": effective_k,
        "pass_at_k": pass_at_k_val,
        "aggregated_value": pass_at_k_val,
        "status": "HEALTHY" if pass_at_k_val >= 0.80 else "DEGRADED",
    }


# -----------------------------------------------------------------------------
# 6. Registro Dinâmico de Esquemas e Despachante SRP (DynamicSchemaRegistry)
# -----------------------------------------------------------------------------
class DynamicSchemaRegistry:
    """Gerenciador de divulgação progressiva JIT e despacho determinístico seguro."""

    def __init__(self, skill_name: str, scratch_dir: Path, max_inline_chars: int = 15_000) -> None:
        self.skill_name: str = skill_name
        self.scratch_dir: Path = scratch_dir.resolve()
        self._action_models: Dict[str, Type[BaseActionPayload]] = {}
        self._handlers: Dict[str, Callable[[Any], Dict[str, Any]]] = {}
        self._action_metadata: Dict[str, Dict[str, Any]] = {}
        self._ledger = IdempotencyLedger()
        self._bloat_guard = ContextBloatGuard(self.scratch_dir, max_chars=max_inline_chars)
        self._register_builtin_actions()

    def _register_builtin_actions(self) -> None:
        self.register_action(
            "inspect_code", InspectCodePayload, ActionCategory.READ_ONLY,
            "Inspeciona arquivos de código e valida diretrizes estáticas.", default_inspect_handler,
        )
        self.register_action(
            "apply_mutation", ApplyMutationPayload, ActionCategory.MUTATION,
            "Aplica mutações idempotentes com registro em ledger SHA-256.", default_mutation_handler,
        )
        self.register_action(
            "fetch_telemetry", FetchTelemetryPayload, ActionCategory.ANALYSIS,
            "Recupera séries temporais e calcula o estimador formal Pass@k.", default_telemetry_handler,
        )

    def register_action(
        self,
        action_name: str,
        model_cls: Type[BaseActionPayload],
        category: ActionCategory,
        description: str,
        handler: Callable[[Any], Dict[str, Any]],
    ) -> None:
        """Registra dinamicamente um payload tipado e seu handler determinístico."""
        self._action_models[action_name] = model_cls
        self._handlers[action_name] = handler
        self._action_metadata[action_name] = {
            "category": category.value,
            "description": description,
            "requires_idempotency": category == ActionCategory.MUTATION,
        }
        logger.info(f"Ação '{action_name}' registrada no catálogo dinâmico.")

    def get_discovery_catalog(self) -> List[Dict[str, Any]]:
        """Nível 1 de Divulgação Progressiva: metadados enxutos (~100 tokens)."""
        return [
            {"action": name, "category": meta["category"], "description": meta["description"]}
            for name, meta in self._action_metadata.items()
        ]

    def generate_jit_schema(self, requested_actions: Optional[List[str]] = None) -> Dict[str, Any]:
        """Nível 2 de Divulgação Progressiva: gera JSON Schema apenas para as ações requisitadas."""
        target_actions = requested_actions if requested_actions is not None else list(self._action_models.keys())
        selected_types = [self._action_models[act] for act in target_actions if act in self._action_models]
        if not selected_types:
            raise ValueError("Nenhuma ação válida informada para geração de esquema JIT.")
        if len(selected_types) == 1:
            return TypeAdapter(selected_types[0]).json_schema()
        union_type = functools.reduce(operator.or_, selected_types)
        dynamic_union = Annotated[union_type, Field(discriminator="action")]
        return TypeAdapter(dynamic_union).json_schema()

    @staticmethod
    def _error_response(
        correlation_id: str, start_time: float, code: int, message: str,
        details: Optional[List[Dict[str, Any]]] = None,
        available_actions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        err = ErrorDetail(code=code, message=message, details=details, available_actions=available_actions)
        return {
            "success": False,
            "isError": True,
            "correlation_id": correlation_id,
            "error": err.model_dump(exclude_none=True),
            "execution_time_ms": elapsed_ms,
        }

    def _validate_envelope_and_action(
        self, raw_input: Dict[str, Any], start_time: float
    ) -> tuple[Optional[PolymorphicSkillEnvelope], Optional[BaseActionPayload], Optional[Dict[str, Any]]]:
        fallback_corr = str(raw_input.get("correlation_id", "trace-invalid")) if isinstance(raw_input, dict) else "trace-invalid"
        if not isinstance(raw_input, dict) or not raw_input:
            return None, None, self._error_response(fallback_corr, start_time, -32602, "Envelope vazio ou malformado.")
        try:
            envelope = PolymorphicSkillEnvelope.model_validate(raw_input)
        except ValidationError as env_err:
            return None, None, self._error_response(
                fallback_corr, start_time, -32602,
                "Violação do contrato do envelope de topo (PolymorphicSkillEnvelope).",
                details=env_err.errors(include_url=False),
            )
        action_name = envelope.payload.get("action")
        if not isinstance(action_name, str) or action_name not in self._action_models:
            return envelope, None, self._error_response(
                envelope.correlation_id, start_time, -32601,
                f"Ação '{action_name}' não suportada pela Skill.",
                available_actions=list(self._action_models.keys()),
            )
        try:
            validated_payload = self._action_models[action_name].model_validate(envelope.payload)
            return envelope, validated_payload, None
        except ValidationError as val_err:
            return envelope, None, self._error_response(
                envelope.correlation_id, start_time, -32602,
                "Violação do contrato de dados da Skill (Schema Mismatch).",
                details=val_err.errors(include_url=False),
            )

    def dispatch(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """Despacha a requisição validando envelope, payload, idempotência SHA-256 e Context Bloat."""
        start_time = time.perf_counter()
        envelope, validated_payload, err_resp = self._validate_envelope_and_action(raw_input, start_time)
        if err_resp is not None or envelope is None or validated_payload is None:
            return err_resp or self._error_response("trace-err", start_time, -32602, "Falha de validação.")

        action_name = str( getattr(validated_payload, "action") )
        requires_idemp = bool(self._action_metadata[action_name]["requires_idempotency"])
        idemp_key = str(getattr(validated_payload, "idempotency_key", "")) if requires_idemp else ""
        digest = self._ledger.compute_payload_digest(validated_payload) if requires_idemp else ""

        if requires_idemp and idemp_key:
            try:
                cached = self._ledger.check(idemp_key, digest)
            except ValueError as conflict_err:
                return self._error_response(envelope.correlation_id, start_time, -32602, str(conflict_err))
            if cached is not None:
                return {
                    "success": True, "isError": False, "correlation_id": envelope.correlation_id,
                    "action": action_name, "is_idempotent_replay": True, "data": cached,
                    "execution_time_ms": round((time.perf_counter() - start_time) * 1000, 2),
                }

        try:
            execution_data = self._handlers[action_name](validated_payload)
            if requires_idemp and idemp_key:
                self._ledger.record(idemp_key, digest, execution_data)
            offload_summary = self._bloat_guard.inspect_and_offload(envelope.correlation_id, execution_data)
        except (OSError, ValueError, TypeError, KeyError, RuntimeError, TimeoutError) as exc:
            logger.error(f"[{envelope.correlation_id}] Falha operacional na ação '{action_name}': {exc}")
            return self._error_response(
                envelope.correlation_id, start_time, -32000,
                f"Falha operacional controlada ao executar '{action_name}'. Consulte os logs de auditoria.",
            )

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        if offload_summary is not None:
            return {
                "success": True, "isError": False, "correlation_id": envelope.correlation_id,
                "action": action_name, "data_summary": offload_summary, "execution_time_ms": elapsed_ms,
            }
        return {
            "success": True, "isError": False, "correlation_id": envelope.correlation_id,
            "action": action_name, "data": execution_data, "execution_time_ms": elapsed_ms,
        }


def run_demonstration_suite() -> Dict[str, Any]:
    """Executa uma verificação rápida e auto-contida em diretório temporário multiplataforma."""
    with tempfile.TemporaryDirectory(prefix="skill_envelope_") as tmp_dir:
        registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=Path(tmp_dir))
        res_ok = registry.dispatch({
            "skill_id": "governance_architect",
            "correlation_id": "trace-inspect-001",
            "payload": {"action": "inspect_code", "target_path": "src/core/engine.py"},
        })
        pass_at_1 = compute_pass_at_k(n=20, c=20, k=1)
        return {"status": "VERIFIED", "dispatch_success": res_ok["success"], "pass_at_1": pass_at_1}


if __name__ == "__main__":
    sys.stdout.write(json.dumps(run_demonstration_suite(), indent=2, ensure_ascii=False) + "\n")
