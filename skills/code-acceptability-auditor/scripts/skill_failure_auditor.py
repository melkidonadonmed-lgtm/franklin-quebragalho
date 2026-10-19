#!/usr/bin/env python3
"""
skill_failure_auditor.py
Motor Pydantic v2 para auditoria de modos de falha, eficácia de fallbacks e
cálculo de delta Baseline (sem skill) vs Treatment (com skill).
"""

import sys
from typing import Dict, List, Literal
from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class EvalAssertion(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    assertion_id: str
    description: str
    passed_with_skill: bool
    passed_without_skill: bool
    evidence: str


class FailureTestCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    prompt: str
    expected_outcome: str
    failure_type: Literal[
        "routing_false_negative",
        "routing_false_positive",
        "instruction_ambiguity",
        "context_poisoning",
        "silent_degradation",
        "assertion_failure",
        "none",
    ]
    with_skill_pass: bool
    without_skill_pass: bool
    tokens_with_skill: int = Field(ge=0)
    tokens_without_skill: int = Field(ge=0)
    duration_ms_with_skill: int = Field(ge=0)
    duration_ms_without_skill: int = Field(ge=0)
    fallback_triggered: bool = Field(default=False)
    fallback_success: bool = Field(default=False)
    assertions: List[EvalAssertion] = Field(default_factory=list)


class BaselineVsTreatmentDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pass_rate_with_skill: float = Field(ge=0.0, le=1.0)
    pass_rate_without_skill: float = Field(ge=0.0, le=1.0)
    pass_rate_delta: float
    avg_tokens_with_skill: float
    avg_tokens_without_skill: float
    token_delta: float
    avg_duration_ms_with_skill: float
    avg_duration_ms_without_skill: float
    duration_delta_ms: float


class SkillFailureAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_name: str
    total_test_cases: int
    successful_cases: int
    failed_cases: int
    failure_breakdown: Dict[str, int]
    fallback_effectiveness_rate: float
    benchmark_delta: BaselineVsTreatmentDelta
    recommendations: List[str]


class SkillFailureAuditor:
    def __init__(self, skill_name: str) -> None:
        self.skill_name = skill_name

    @staticmethod
    def _build_recommendations(breakdown: Dict[str, int], pass_rate_delta: float) -> List[str]:
        recs: List[str] = []
        if breakdown["routing_false_negative"] > 0:
            recs.append("Amplie o escopo da 'description' no SKILL.md para capturar gatilhos implícitos e paráfrases.")
        if breakdown["routing_false_positive"] > 0:
            recs.append("Adicione termos de exclusão e delimite a fronteira da skill contra near-misses.")
        if breakdown["instruction_ambiguity"] > 0:
            recs.append("Simplifique o corpo das instruções em SKILL.md; substitua regras declarativas por procedimentos com exemplos.")
        if breakdown["context_poisoning"] > 0:
            recs.append("Exija validação rigorosa de saídas intermediárias e delimite dados em tags estruturadas (<context>).")
        if breakdown["silent_degradation"] > 0:
            recs.append("Remova validações e passos redundantes do SKILL.md para evitar consumo desnecessário de tokens.")
        if pass_rate_delta <= 0:
            recs.append("ALERTA CRÍTICO: A skill não apresentou ganho de qualidade em relação à baseline sem a skill. Redesenhe o fluxo.")
        if not recs:
            recs.append("A skill apresenta alta robustez e superou a baseline sem falhas detectadas.")
        return recs

    def audit_cases(self, test_cases: List[FailureTestCase]) -> SkillFailureAuditReport:
        total = len(test_cases)
        if total == 0:
            raise ValueError("O conjunto de testes de falha não pode estar vazio.")

        successful = sum(1 for c in test_cases if c.failure_type == "none" and c.with_skill_pass)
        breakdown: Dict[str, int] = {
            "routing_false_negative": 0,
            "routing_false_positive": 0,
            "instruction_ambiguity": 0,
            "context_poisoning": 0,
            "silent_degradation": 0,
            "assertion_failure": 0,
        }
        fallback_attempts, fallback_successes = 0, 0
        for c in test_cases:
            if c.failure_type != "none":
                breakdown[c.failure_type] = breakdown.get(c.failure_type, 0) + 1
            if c.fallback_triggered:
                fallback_attempts += 1
                if c.fallback_success:
                    fallback_successes += 1

        fallback_rate = (fallback_successes / fallback_attempts) if fallback_attempts > 0 else 1.0
        pass_with = sum(1 for c in test_cases if c.with_skill_pass) / total
        pass_without = sum(1 for c in test_cases if c.without_skill_pass) / total
        avg_tokens_with = sum(c.tokens_with_skill for c in test_cases) / total
        avg_tokens_without = sum(c.tokens_without_skill for c in test_cases) / total
        avg_dur_with = sum(c.duration_ms_with_skill for c in test_cases) / total
        avg_dur_without = sum(c.duration_ms_without_skill for c in test_cases) / total

        delta = BaselineVsTreatmentDelta(
            pass_rate_with_skill=round(pass_with, 4),
            pass_rate_without_skill=round(pass_without, 4),
            pass_rate_delta=round(pass_with - pass_without, 4),
            avg_tokens_with_skill=round(avg_tokens_with, 1),
            avg_tokens_without_skill=round(avg_tokens_without, 1),
            token_delta=round(avg_tokens_with - avg_tokens_without, 1),
            avg_duration_ms_with_skill=round(avg_dur_with, 1),
            avg_duration_ms_without_skill=round(avg_dur_without, 1),
            duration_delta_ms=round(avg_dur_with - avg_dur_without, 1),
        )
        return SkillFailureAuditReport(
            skill_name=self.skill_name,
            total_test_cases=total,
            successful_cases=successful,
            failed_cases=total - successful,
            failure_breakdown=breakdown,
            fallback_effectiveness_rate=round(fallback_rate, 4),
            benchmark_delta=delta,
            recommendations=self._build_recommendations(breakdown, delta.pass_rate_delta),
        )


if __name__ == "__main__":
    sample_cases = [
        FailureTestCase(
            case_id="EVAL-01",
            prompt="Audite este script Python em busca de vulnerabilidades.",
            expected_outcome="Relatório contendo violações estritas e Quality Score.",
            failure_type="none",
            with_skill_pass=True,
            without_skill_pass=False,
            tokens_with_skill=1200,
            tokens_without_skill=800,
            duration_ms_with_skill=1500,
            duration_ms_without_skill=900,
            assertions=[
                EvalAssertion(
                    assertion_id="A1",
                    description="O relatório atribui penalidade para credenciais hardcodeadas.",
                    passed_with_skill=True,
                    passed_without_skill=False,
                    evidence="Atribuiu -25 para SEC003.",
                )
            ],
        ),
        FailureTestCase(
            case_id="EVAL-02",
            prompt="Explicar sintaxe de exceção em Python.",
            expected_outcome="Abster da auditoria e apenas responder a dúvida em texto.",
            failure_type="none",
            with_skill_pass=True,
            without_skill_pass=True,
            tokens_with_skill=420,
            tokens_without_skill=400,
            duration_ms_with_skill=510,
            duration_ms_without_skill=500,
            assertions=[
                EvalAssertion(
                    assertion_id="A2",
                    description="Não deve carregar o auditor AST para dúvidas conceituais.",
                    passed_with_skill=True,
                    passed_without_skill=True,
                    evidence="Absteve corretamente com denylist de near-miss.",
                )
            ],
        ),
        FailureTestCase(
            case_id="EVAL-03",
            prompt="Valide se este código sem type hints pode ir para produção.",
            expected_outcome="Rejeitar o código por falta de type hints e exceção genérica.",
            failure_type="none",
            with_skill_pass=True,
            without_skill_pass=False,
            tokens_with_skill=1400,
            tokens_without_skill=750,
            duration_ms_with_skill=1600,
            duration_ms_without_skill=800,
        ),
    ]

    auditor = SkillFailureAuditor(skill_name="code-acceptability-auditor")
    report = auditor.audit_cases(sample_cases)

    print("=== RELATÓRIO DE AVALIAÇÃO DE FALHAS E BENCHMARK ===")
    print(f"Skill: {report.skill_name}")
    print(f"Casos Totais: {report.total_test_cases} | Aprovados: {report.successful_cases} | Falhas: {report.failed_cases}")
    print(
        f"Taxa de Sucesso da Skill: {report.benchmark_delta.pass_rate_with_skill * 100:.1f}% "
        f"vs Baseline: {report.benchmark_delta.pass_rate_without_skill * 100:.1f}% "
        f"(Delta: {report.benchmark_delta.pass_rate_delta * 100:+.1f}%)"
    )
    print(
        f"Consumo de Tokens: {report.benchmark_delta.avg_tokens_with_skill} (Skill) "
        f"vs {report.benchmark_delta.avg_tokens_without_skill} (Baseline) | "
        f"Delta: {report.benchmark_delta.token_delta:+.1f} tokens"
    )
    print("\nRecomendações de Melhoria:")
    for rec in report.recommendations:
        print(f" - {rec}")
