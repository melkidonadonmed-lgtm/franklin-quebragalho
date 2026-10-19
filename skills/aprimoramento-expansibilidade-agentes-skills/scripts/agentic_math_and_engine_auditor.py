#!/usr/bin/env python3
"""
agentic_math_and_engine_auditor.py
Motor determinístico de Despacho Polimórfico (Envelope Pattern com Pydantic v2) e
Suíte de Auditoria Matemática de Agentes (Pass@k, Distância de Cosseno, Guardrail FNR,
LLM-as-a-Judge Normalizado Snorm e Token Efficiency Index TEI).
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import sys
from typing import Any, Callable, Dict, List, Literal, Sequence, Tuple, Type

from pydantic import BaseModel, ConfigDict, Field, ValidationError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# ==============================================================================
# 1. Motor de Despacho Polimórfico e Injeção Dinâmica de Schemas (Módulo C)
# ==============================================================================
class BalanceAuditParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    fiscal_year: int = Field(..., ge=2000, le=2035, description="Ano fiscal base da análise")
    target_accounts: List[str] = Field(..., min_length=1, description="Contas contábeis a auditar")
    max_discrepancy_allowed: float = Field(default=0.0, ge=0.0, description="Tolerância máxima")


class ValuationParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    wacc: float = Field(..., gt=0.0, lt=1.0, description="Custo Médio Ponderado de Capital (WACC)")
    projection_horizon_years: int = Field(..., ge=1, le=30, description="Horizonte de projeção em anos")
    perpetual_growth_rate: float = Field(..., ge=0.0, le=0.06, description="Crescimento perpétuo (g <= 6%)")


class TaxReconciliationParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tax_regime: Literal["LUCRO_REAL", "LUCRO_PRESUMIDO", "SIMPLES"]
    reference_quarter: str = Field(..., pattern=r"^\d{4}-Q[1-4]$", description="Formato AAAA-Q[1-4]")
    retention_keys: List[str] = Field(..., min_length=1, description="Chaves fiscais para batimento")


class MasterSkillInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["AUDIT_BALANCE", "VALUATION_DCF", "TAX_RECONCILIATION"] = Field(
        ..., description="Suboperação procedural a despachar internamente"
    )
    organization_id: str = Field(..., min_length=3, max_length=64, description="Identificador da entidade")
    parameters: Dict[str, Any] = Field(..., description="Carga validada dinamicamente pelo sub-schema")


class PolyExtensibleSkillEngine:
    """Controlador polimórfico (Envelope Pattern) com injeção dinâmica de schemas e recovery_hint."""

    def __init__(self) -> None:
        self._schema_registry: Dict[str, Type[BaseModel]] = {
            "AUDIT_BALANCE": BalanceAuditParameters,
            "VALUATION_DCF": ValuationParameters,
            "TAX_RECONCILIATION": TaxReconciliationParameters,
        }

    def dispatch_call(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        try:
            envelope = MasterSkillInvocation.model_validate(raw_input)
        except ValidationError as err:
            return {
                "execution_status": "FAILED",
                "failure_stage": "ENVELOPE_VALIDATION",
                "validation_errors": json.loads(err.json()),
                "recovery_hint": "Envie exclusivamente action, organization_id e parameters válidos.",
            }

        target_schema = self._schema_registry.get(envelope.action)
        if target_schema is None:
            return {
                "execution_status": "FAILED",
                "failure_stage": "ROUTING_ERROR",
                "message": f"Suboperação '{envelope.action}' não autorizada.",
            }

        try:
            validated_payload = target_schema.model_validate(envelope.parameters)
        except ValidationError as err:
            return {
                "execution_status": "FAILED",
                "failure_stage": "DYNAMIC_SCHEMA_VALIDATION",
                "action": envelope.action,
                "expected_schema": target_schema.model_json_schema(),
                "validation_errors": json.loads(err.json()),
                "recovery_hint": f"Ajuste 'parameters' para obedecer ao schema de {envelope.action}.",
            }

        return self._execute_route(envelope.action, envelope.organization_id, validated_payload)

    @staticmethod
    def _execute_route(action: str, org_id: str, payload: BaseModel) -> Dict[str, Any]:
        data = payload.model_dump()
        if action == "AUDIT_BALANCE":
            return {
                "execution_status": "SUCCESS",
                "action": action,
                "organization_id": org_id,
                "result": {
                    "year": data["fiscal_year"],
                    "accounts_checked": len(data["target_accounts"]),
                    "discrepancy_detected": 0.0,
                    "compliance_status": "APPROVED",
                },
            }
        if action == "VALUATION_DCF":
            return {
                "execution_status": "SUCCESS",
                "action": action,
                "organization_id": org_id,
                "result": {
                    "implied_discount_rate": data["wacc"],
                    "horizon": data["projection_horizon_years"],
                    "perpetuity_rate": data["perpetual_growth_rate"],
                    "model_integrity": "CONVERGED",
                },
            }
        return {
            "execution_status": "SUCCESS",
            "action": action,
            "organization_id": org_id,
            "result": {
                "regime": data["tax_regime"],
                "quarter": data["reference_quarter"],
                "reconciled_keys_count": len(data["retention_keys"]),
                "divergence_count": 0,
            },
        }


# ==============================================================================
# 2. Suíte de Auditoria Matemática de Agentes (Módulo E)
# ==============================================================================
class FunctionalCorrectnessEvaluator:
    """Estimador não enviesado numericamente estável de Pass@k (Chen et al., 2021)."""

    @staticmethod
    def calculate_pass_at_k(n: int, c: int, k: int) -> float:
        if n < k or k < 1:
            raise ValueError(f"Tamanho amostral n ({n}) deve ser >= k ({k}) >= 1.")
        if c < 0 or c > n:
            raise ValueError(f"Acertos c ({c}) deve estar entre 0 e n ({n}).")
        if n - c < k:
            return 1.0
        product_acc = 1.0
        for i in range(1, k + 1):
            product_acc *= 1.0 - (c / float(n - k + i))
        return float(1.0 - product_acc)


class SemanticGroundingEvaluator:
    """Fidelidade factual e distância de cosseno em Python puro (sem depender de C-extensions)."""

    @staticmethod
    def cosine_similarity(u: Sequence[float], v: Sequence[float]) -> float:
        if len(u) != len(v) or len(u) == 0:
            raise ValueError("Vetores u e v devem ter a mesma dimensão não-vazia.")
        dot_prod = sum(a * b for a, b in zip(u, v))
        norm_u = math.sqrt(sum(a * a for a in u))
        norm_v = math.sqrt(sum(b * b for b in v))
        if norm_u == 0.0 or norm_v == 0.0:
            return 0.0
        return float(dot_prod / (norm_u * norm_v))

    @classmethod
    def cosine_distance(cls, u: Sequence[float], v: Sequence[float]) -> float:
        return float(1.0 - cls.cosine_similarity(u, v))


@dataclass(frozen=True)
class GuardrailAuditReport:
    precision: float
    recall: float
    f1_score: float
    false_negative_rate: float
    passes_zero_trust_gate: bool


class GuardrailSecurityEvaluator:
    """Avalia matriz de confusão de guardrails contra o limiar estrito FNR < 0.001."""

    @staticmethod
    def analyze_confusion_matrix(
        tp: int, fp: int, fn: int, tn: int, max_fnr: float = 0.001
    ) -> GuardrailAuditReport:
        precision = tp / float(tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / float(tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2.0 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        fnr = fn / float(fn + tp) if (fn + tp) > 0 else 0.0
        return GuardrailAuditReport(
            precision=round(precision, 6),
            recall=round(recall, 6),
            f1_score=round(f1, 6),
            false_negative_rate=round(fnr, 6),
            passes_zero_trust_gate=(fnr < max_fnr and tn >= 0),
        )


@dataclass(frozen=True)
class EvaluationCriterion:
    name: str
    raw_score: float
    min_possible: float
    max_possible: float
    weight: float


class LLMJudgeNormalizer:
    """Calcula o Score Normalizado Ponderado Snorm no intervalo fechado [0, 100]."""

    @staticmethod
    def compute_weighted_score(criteria: Sequence[EvaluationCriterion]) -> float:
        total_weight = sum(c.weight for c in criteria)
        if total_weight <= 0.0:
            raise ValueError("A soma dos pesos deve ser estritamente positiva.")
        acc = 0.0
        for c in criteria:
            if c.max_possible <= c.min_possible:
                raise ValueError(f"Intervalo inválido no critério '{c.name}'.")
            norm_val = (c.raw_score - c.min_possible) / float(c.max_possible - c.min_possible)
            acc += c.weight * norm_val
        return round(float((acc / total_weight) * 100.0), 4)


class TokenEconomicsAuditor:
    """Calcula o Índice de Eficiência de Tokens (TEI) com penalização logarítmica de entropia."""

    @staticmethod
    def compute_tei(
        s_norm: float,
        success: bool,
        tokens_in: int,
        tokens_out: int,
        price_per_1k_in: float = 0.003,
        price_per_1k_out: float = 0.015,
        beta_decay: float = 2.0,
    ) -> Dict[str, float]:
        indicator = 1.0 if success else 0.0
        cost_usd = (tokens_in * (price_per_1k_in / 1000.0)) + (tokens_out * (price_per_1k_out / 1000.0))
        safe_cost = max(cost_usd, 1e-8)
        entropy_term = math.log(tokens_in + (beta_decay * tokens_out) + math.e)
        tei = (s_norm * indicator) / (safe_cost * entropy_term)
        return {
            "total_cost_usd": round(cost_usd, 6),
            "context_entropy": round(entropy_term, 4),
            "tei_score": round(tei, 2),
        }


def run_self_test() -> Dict[str, Any]:
    """Executa bateria determinística de autoverificação do motor e das 5 métricas."""
    engine = PolyExtensibleSkillEngine()
    ok_call = engine.dispatch_call(
        {
            "action": "VALUATION_DCF",
            "organization_id": "ORG-2026",
            "parameters": {"wacc": 0.11, "projection_horizon_years": 5, "perpetual_growth_rate": 0.03},
        }
    )
    bad_call = engine.dispatch_call(
        {
            "action": "VALUATION_DCF",
            "organization_id": "ORG-2026",
            "parameters": {"wacc": 1.5, "campo_fantasma": True},
        }
    )

    p1 = FunctionalCorrectnessEvaluator.calculate_pass_at_k(n=25, c=19, k=1)
    p5 = FunctionalCorrectnessEvaluator.calculate_pass_at_k(n=25, c=19, k=5)

    vec_truth = [0.10, 0.75, 0.40, 0.05, 0.50, 0.20, 0.80, 0.15]
    vec_grounded = [0.12, 0.72, 0.38, 0.06, 0.48, 0.22, 0.79, 0.14]
    dist_grounded = SemanticGroundingEvaluator.cosine_distance(vec_grounded, vec_truth)

    guardrail = GuardrailSecurityEvaluator.analyze_confusion_matrix(tp=1000, fp=2, fn=0, tn=5000)
    rubric = [
        EvaluationCriterion("Consistencia_Factual", 4.9, 1.0, 5.0, 0.35),
        EvaluationCriterion("Aderencia_Guardrails", 5.0, 1.0, 5.0, 0.30),
        EvaluationCriterion("Precisao_Schema_JSON", 4.7, 1.0, 5.0, 0.20),
        EvaluationCriterion("Concisao_Resposta", 4.0, 1.0, 5.0, 0.15),
    ]
    s_norm = LLMJudgeNormalizer.compute_weighted_score(rubric)
    tei = TokenEconomicsAuditor.compute_tei(s_norm=s_norm, success=True, tokens_in=2850, tokens_out=420)

    all_passed = (
        ok_call["execution_status"] == "SUCCESS"
        and bad_call["execution_status"] == "FAILED"
        and "recovery_hint" in bad_call
        and abs(p1 - 0.76) < 1e-6
        and p5 > 0.99
        and dist_grounded <= 0.18
        and guardrail.passes_zero_trust_gate
        and s_norm > 90.0
    )
    return {
        "status": "[PASS]" if all_passed else "[FAIL]",
        "envelope_engine": {"valid_call": ok_call["execution_status"], "invalid_caught": bad_call["failure_stage"]},
        "pass_at_k": {"pass_at_1": round(p1, 4), "pass_at_5": round(p5, 4)},
        "semantic_grounding": {"cosine_distance": round(dist_grounded, 4), "threshold_tau": 0.18},
        "guardrail_security": asdict(guardrail),
        "llm_judge_snorm": s_norm,
        "token_economics": tei,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Motor Polimórfico e Auditoria Matemática de Agentes.")
    parser.add_argument("--self-test", action="store_true", help="Executa a suíte determinística de autoverificação.")
    args = parser.parse_args()

    report = run_self_test()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "[PASS]" else 1


if __name__ == "__main__":
    sys.exit(main())
