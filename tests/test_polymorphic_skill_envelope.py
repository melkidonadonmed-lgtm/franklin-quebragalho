"""
test_polymorphic_skill_envelope.py
Suíte Determinística Nível 4 (100/100) para shared/polymorphic_skill_envelope.py.
Cobre os 5 Casos de Teste Essenciais das diretrizes de Code Quality + Estimador Formal Pass@k:
  1. Caminho limpo e nominal + Divulgação Progressiva JIT (Níveis 1 e 2)
  2. Entradas vazias e nulas
  3. Entradas malformadas, bloqueio de alucinação (extra="forbid") e Zero-Trust Path Traversal
  4. Falha de dependência/timeout sem vazamento de detalhes internos + Higiene de Streams (STDERR JSON)
  5. Valores de borda, idempotência concorrente (SHA-256), Context Bloat Guard e Pass@k
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import logging
from pathlib import Path
from typing import Any, Dict, Literal

import pytest
from pydantic import Field

from shared.polymorphic_skill_envelope import (
    ActionCategory,
    BaseActionPayload,
    DynamicSchemaRegistry,
    StructuredStderrFormatter,
    compute_pass_at_k,
    run_demonstration_suite,
)


def test_nominal_happy_path_and_jit_schema_disclosure(tmp_path: Path) -> None:
    """Caso 1: Valida o caminho nominal de despacho, catálogo Nível 1 e geração de esquema JIT Nível 2."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path)

    # 1. Nível 1: Catálogo enxuto
    catalog = registry.get_discovery_catalog()
    actions_found = {item["action"] for item in catalog}
    assert actions_found == {"inspect_code", "apply_mutation", "fetch_telemetry"}

    # 2. Nível 2: Esquema JIT isolado vs. polimórfico múltiplo
    single_schema = registry.generate_jit_schema(["inspect_code"])
    assert single_schema["title"] == "InspectCodePayload"
    assert single_schema.get("additionalProperties") is False

    multi_schema = registry.generate_jit_schema(["inspect_code", "apply_mutation"])
    assert "discriminator" in multi_schema
    assert multi_schema["discriminator"]["propertyName"] == "action"

    with pytest.raises(ValueError, match="Nenhuma ação válida"):
        registry.generate_jit_schema(["acao_inexistente"])

    # 3. Despacho nominal das 3 ações nativas
    res_inspect = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-nominal-01",
        "payload": {
            "action": "inspect_code",
            "target_path": "src/core/engine.py",
            "ruleset": ["ast_check", "type_hints"],
            "max_depth": 2,
        },
    })
    assert res_inspect["success"] is True
    assert res_inspect["isError"] is False
    assert res_inspect["data"]["target_evaluated"] == "src/core/engine.py"

    res_telemetry = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-nominal-02",
        "payload": {
            "action": "fetch_telemetry",
            "metric_name": "pass_at_k",
            "time_window_minutes": 30,
            "samples_n": 50,
            "passed_c": 45,
            "k_value": 1,
        },
    })
    assert res_telemetry["success"] is True
    assert res_telemetry["data"]["pass_at_k"] == 0.9
    assert res_telemetry["data"]["status"] == "HEALTHY"

    demo = run_demonstration_suite()
    assert demo["status"] == "VERIFIED"
    assert demo["dispatch_success"] is True
    assert demo["pass_at_1"] == 1.0


def test_empty_and_null_inputs_rejected(tmp_path: Path) -> None:
    """Caso 2: Valida rejeição determinística de entradas vazias, nulas ou apenas com espaços."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path)

    # Envelope totalmente vazio
    res_empty_env = registry.dispatch({})
    assert res_empty_env["success"] is False
    assert res_empty_env["isError"] is True
    assert res_empty_env["error"]["code"] == -32602

    # Payload vazio ou skill_id em branco
    res_blank_skill = registry.dispatch({
        "skill_id": "   ",
        "correlation_id": "trace-empty-01",
        "payload": {},
    })
    assert res_blank_skill["success"] is False
    assert res_blank_skill["isError"] is True
    assert res_blank_skill["error"]["code"] == -32602

    # Campos internos vazios (target_path="", ruleset=[], changes={})
    res_empty_path = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-empty-02",
        "payload": {"action": "inspect_code", "target_path": "   ", "ruleset": []},
    })
    assert res_empty_path["success"] is False
    assert res_empty_path["error"]["code"] == -32602

    res_empty_changes = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-empty-03",
        "payload": {
            "action": "apply_mutation",
            "target_entity_id": "ENT-01",
            "operation": "update",
            "changes": {},
            "idempotency_key": "idem-key-valid-0001",
        },
    })
    assert res_empty_changes["success"] is False
    assert res_empty_changes["error"]["code"] == -32602


def test_malformed_inputs_hallucination_and_zero_trust_guards(tmp_path: Path) -> None:
    """Caso 3: Valida bloqueio de campos alucinados (extra='forbid') na raiz/payload e Path Traversal."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path)

    # 1. Alucinação na raiz do envelope (PolymorphicSkillEnvelope)
    res_root_hallucination = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-sec-01",
        "campo_alucinado_na_raiz": "injetado",
        "payload": {"action": "inspect_code", "target_path": "src/app.py"},
    })
    assert res_root_hallucination["success"] is False
    assert res_root_hallucination["isError"] is True
    assert res_root_hallucination["error"]["code"] == -32602

    # 2. Alucinação dentro do payload da ação
    res_payload_hallucination = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-sec-02",
        "payload": {
            "action": "inspect_code",
            "target_path": "src/app.py",
            "parametro_inexistente": True,
        },
    })
    assert res_payload_hallucination["success"] is False
    assert res_payload_hallucination["error"]["code"] == -32602

    # 3. Ação não suportada (-32601 Method Not Found)
    res_unknown_action = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-sec-03",
        "payload": {"action": "gerenciar_sistema_total"},
    })
    assert res_unknown_action["success"] is False
    assert res_unknown_action["error"]["code"] == -32601
    assert "inspect_code" in res_unknown_action["error"]["available_actions"]

    # 4. Bloqueio Zero-Trust de Path Traversal em target_path e correlation_id
    for malicious_path in ("../../etc/passwd", "/etc/shadow", "C:\\Windows\\System32\\cmd.exe", "src/../../secret"):
        res_trav = registry.dispatch({
            "skill_id": "governance_architect",
            "correlation_id": "trace-sec-04",
            "payload": {"action": "inspect_code", "target_path": malicious_path},
        })
        assert res_trav["success"] is False
        assert res_trav["error"]["code"] == -32602

    res_bad_corr = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "../../outside_dir",
        "payload": {"action": "inspect_code", "target_path": "src/main.py"},
    })
    assert res_bad_corr["success"] is False
    assert res_bad_corr["error"]["code"] == -32602


def test_dependency_failure_timeout_and_stderr_stream_hygiene(tmp_path: Path) -> None:
    """Caso 4: Valida resposta controlada em timeout/falha externa sem vazar segredos e higiene JSON no stderr."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path)

    class ExternalQueryPayload(BaseActionPayload):
        action: Literal["external_query"] = Field(...)
        endpoint_alias: str = Field(..., min_length=2)

    def failing_timeout_handler(payload: ExternalQueryPayload) -> Dict[str, Any]:
        raise TimeoutError(f"Timeout ao conectar em {payload.endpoint_alias} (/internal/secret/db.sock)")

    registry.register_action(
        "external_query", ExternalQueryPayload, ActionCategory.READ_ONLY,
        "Simula consulta a dependência externa sujeita a timeout.", failing_timeout_handler,
    )

    res_fail = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-timeout-01",
        "payload": {"action": "external_query", "endpoint_alias": "bq-cluster-primary"},
    })
    assert res_fail["success"] is False
    assert res_fail["isError"] is True
    assert res_fail["error"]["code"] == -32000
    assert "/internal/secret/db.sock" not in res_fail["error"]["message"]

    # Valida que o StructuredStderrFormatter produz JSON válido mesmo com aspas e quebras de linha
    formatter = StructuredStderrFormatter()
    record = logging.LogRecord(
        name="SkillGovernor", level=logging.ERROR, pathname=__file__, lineno=10,
        msg='Falha com "aspas"\ne quebra de linha', args=(), exc_info=None,
    )
    formatted_json = formatter.format(record)
    parsed_log = json.loads(formatted_json)
    assert parsed_log["level"] == "ERROR"
    assert 'Falha com "aspas"\ne quebra de linha' == parsed_log["message"]


def test_edge_cases_and_concurrent_idempotency_ledger(tmp_path: Path) -> None:
    """Caso 5A: Valida valores de borda numéricos e idempotência concorrente thread-safe (SHA-256)."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path)

    for invalid_depth in (0, 11, -5):
        res_bound = registry.dispatch({
            "skill_id": "governance_architect",
            "correlation_id": "trace-bound",
            "payload": {"action": "inspect_code", "target_path": "a.py", "max_depth": invalid_depth},
        })
        assert res_bound["success"] is False
        assert res_bound["error"]["code"] == -32602

    call_counter = {"executions": 0}

    class CounterMutationPayload(BaseActionPayload):
        action: Literal["counter_mutation"] = Field(...)
        amount: int = Field(..., ge=1, le=10000)
        idempotency_key: str = Field(..., min_length=16, max_length=128)

    def counter_handler(payload: CounterMutationPayload) -> Dict[str, Any]:
        call_counter["executions"] += 1
        return {"applied_amount": payload.amount, "executions": call_counter["executions"]}

    registry.register_action(
        "counter_mutation", CounterMutationPayload, ActionCategory.MUTATION,
        "Incrementa contador de forma idempotente.", counter_handler,
    )

    idem_key = "idem-concurrent-key-998877"
    valid_req = {
        "skill_id": "governance_architect",
        "correlation_id": "trace-idem-01",
        "payload": {"action": "counter_mutation", "amount": 250, "idempotency_key": idem_key},
    }

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: registry.dispatch(valid_req), range(8)))

    assert all(r["success"] is True for r in results)
    assert call_counter["executions"] == 1
    assert sum(1 for r in results if r.get("is_idempotent_replay") is True) == 7

    conflict_req = {
        "skill_id": "governance_architect",
        "correlation_id": "trace-idem-conflict",
        "payload": {"action": "counter_mutation", "amount": 9999, "idempotency_key": idem_key},
    }
    res_conflict = registry.dispatch(conflict_req)
    assert res_conflict["success"] is False
    assert res_conflict["isError"] is True
    assert res_conflict["error"]["code"] == -32602
    assert "Conflito de Idempotência" in res_conflict["error"]["message"]


def test_context_bloat_offload_and_pass_at_k_estimator(tmp_path: Path) -> None:
    """Caso 5B: Valida guarda contra Context Bloat (offload em disco) e estimador formal Pass@k."""
    registry = DynamicSchemaRegistry(skill_name="governance_architect", scratch_dir=tmp_path, max_inline_chars=1_000)

    class HeavyPayload(BaseActionPayload):
        action: Literal["heavy_dump"] = Field(...)
        rows: int = Field(default=50, ge=1)

    registry.register_action(
        "heavy_dump", HeavyPayload, ActionCategory.READ_ONLY,
        "Gera payload acima do limite inline.",
        lambda p: {"items": [f"registro_extenso_numero_{i}_" + ("x" * 40) for i in range(p.rows)]},
    )
    res_heavy = registry.dispatch({
        "skill_id": "governance_architect",
        "correlation_id": "trace-heavy-01",
        "payload": {"action": "heavy_dump", "rows": 40},
    })
    assert res_heavy["success"] is True
    assert res_heavy["data_summary"]["status"] == "offloaded_to_disk"
    offload_file = Path(res_heavy["data_summary"]["file_path"])
    assert offload_file.exists()
    assert offload_file.is_relative_to(tmp_path)

    assert compute_pass_at_k(n=10, c=0, k=1) == 0.0
    assert compute_pass_at_k(n=10, c=10, k=5) == 1.0
    assert compute_pass_at_k(n=10, c=5, k=2) == round(1.0 - (10.0 / 45.0), 6)
    with pytest.raises(ValueError, match="Parâmetros inválidos"):
        compute_pass_at_k(n=5, c=3, k=6)
    with pytest.raises(ValueError, match="Contagem de aprovados inválida"):
        compute_pass_at_k(n=5, c=7, k=1)
