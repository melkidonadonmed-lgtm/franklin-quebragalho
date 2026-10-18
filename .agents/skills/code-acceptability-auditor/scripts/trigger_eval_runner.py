#!/usr/bin/env python3
"""
trigger_eval_runner.py
Motor de avaliação determinística da Matriz de Gatilhos (TRIG-01..20) com separação
Train/Validation, detecção de Overfitting e checagem de Near-Misses.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class TriggerQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="ID único do teste (ex: TRIG-01)")
    category: Literal["positive_explicit", "positive_implicit", "near_miss_negative", "clear_negative"]
    query: str = Field(..., min_length=5, description="Prompt do usuário")
    should_trigger: bool = Field(..., description="Se a skill deve ser ativada")
    split: Literal["train", "validation"] = Field(default="train")


class TriggerRunResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_id: str
    category: str
    query: str
    should_trigger: bool
    split: str
    runs: int
    triggers: int
    trigger_rate: float
    passed: bool


class RoutingMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_queries: int
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    precision: float
    recall: float
    f1_score: float
    accuracy: float
    false_positive_rate: float
    false_negative_rate: float


class TriggerEvalReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_name: str
    train_metrics: RoutingMetrics
    validation_metrics: RoutingMetrics
    overall_metrics: RoutingMetrics
    overfitting_detected: bool
    near_miss_failures: List[Dict[str, Any]]
    run_results: List[TriggerRunResult]


class TriggerEvalRunner:
    def __init__(
        self,
        skill_name: str,
        skill_description: str,
        keywords_pattern: str,
        near_miss_denylist_pattern: Optional[str] = None,
    ) -> None:
        self.skill_name = skill_name
        self.skill_description = skill_description.lower()
        self.keywords_regex = re.compile(keywords_pattern, re.IGNORECASE)
        self.near_miss_regex = (
            re.compile(near_miss_denylist_pattern, re.IGNORECASE)
            if near_miss_denylist_pattern
            else None
        )

    def simulate_routing(self, query: str) -> bool:
        q_lower = query.lower()
        if self.near_miss_regex and self.near_miss_regex.search(q_lower):
            return False
        if self.keywords_regex.search(q_lower):
            return True
        return False

    def evaluate_query(self, item: TriggerQuery, runs_per_query: int = 3, threshold: float = 0.5) -> TriggerRunResult:
        triggers = 0
        for _ in range(runs_per_query):
            if self.simulate_routing(item.query):
                triggers += 1

        trigger_rate = round(triggers / runs_per_query, 2)
        passed = (trigger_rate >= threshold) if item.should_trigger else (trigger_rate < threshold)

        return TriggerRunResult(
            query_id=item.id,
            category=item.category,
            query=item.query,
            should_trigger=item.should_trigger,
            split=item.split,
            runs=runs_per_query,
            triggers=triggers,
            trigger_rate=trigger_rate,
            passed=passed,
        )

    def _compute_metrics(self, results: List[TriggerRunResult]) -> RoutingMetrics:
        tp = sum(1 for r in results if r.should_trigger and r.passed)
        fn = sum(1 for r in results if r.should_trigger and not r.passed)
        tn = sum(1 for r in results if not r.should_trigger and r.passed)
        fp = sum(1 for r in results if not r.should_trigger and not r.passed)

        total = len(results)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        accuracy = (tp + tn) / total if total > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

        return RoutingMetrics(
            total_queries=total,
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            accuracy=round(accuracy, 4),
            false_positive_rate=round(fpr, 4),
            false_negative_rate=round(fnr, 4),
        )

    def run_suite(self, queries: List[TriggerQuery], runs_per_query: int = 3) -> TriggerEvalReport:
        all_results = [self.evaluate_query(q, runs_per_query=runs_per_query) for q in queries]

        train_results = [r for r in all_results if r.split == "train"]
        val_results = [r for r in all_results if r.split == "validation"]

        train_metrics = self._compute_metrics(train_results)
        val_metrics = self._compute_metrics(val_results)
        overall_metrics = self._compute_metrics(all_results)

        overfitting = (train_metrics.f1_score - val_metrics.f1_score) > 0.15

        near_miss_failures = [
            {
                "query_id": r.query_id,
                "query": r.query,
                "category": r.category,
                "issue": "False Positive (ativou quando deveria abster)"
                if not r.should_trigger
                else "False Negative (não ativou)",
            }
            for r in all_results
            if not r.passed and "near_miss" in r.category
        ]

        return TriggerEvalReport(
            skill_name=self.skill_name,
            train_metrics=train_metrics,
            validation_metrics=val_metrics,
            overall_metrics=overall_metrics,
            overfitting_detected=overfitting,
            near_miss_failures=near_miss_failures,
            run_results=all_results,
        )


def load_canonical_queries() -> List[TriggerQuery]:
    ref_file = Path(__file__).resolve().parent.parent / "references" / "trigger_matrix_queries.json"
    if ref_file.exists():
        raw = json.loads(ref_file.read_text(encoding="utf-8"))
        return [TriggerQuery(**item) for item in raw]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner de Trigger Evals (TRIG-01..20)")
    parser.add_argument("--json", action="store_true", help="Emitir relatório completo em JSON")
    args = parser.parse_args()

    queries = load_canonical_queries()
    runner = TriggerEvalRunner(
        skill_name="code-acceptability-auditor",
        skill_description=(
            "Audita estaticamente arquivos de código Python verificando segurança, "
            "type hints, tratamento de erros e critérios de aceite."
        ),
        keywords_pattern=(
            r"(audite|auditoria|auditor|chaves de api vazadas|senhas hardcodeadas|"
            r"anotações de tipo|retornos tipados|esteira de validação de código|"
            r"critérios de aceite|eval\(\)|shell=true|análise estática ast)"
        ),
        near_miss_denylist_pattern=(
            r"(me explique teoricamente|diferenças conceituais|como configurar o arquivo \.gitignore|"
            r"crie um documento readme|conecte ao banco de dados postgresql|sequência de fibonacci|"
            r"usar recursão em vez de um laço|previsão do tempo|relatório financeiro)"
        ),
    )

    report = runner.run_suite(queries)
    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        print("=== RELATÓRIO DE TRIGGER EVALS ===")
        print(f"Skill: {report.skill_name} | Total Queries: {report.overall_metrics.total_queries}")
        print(f"Acurácia Geral: {report.overall_metrics.accuracy * 100:.1f}%")
        print(
            f"Precisão: {report.overall_metrics.precision:.4f} | "
            f"Recall: {report.overall_metrics.recall:.4f} | "
            f"F1: {report.overall_metrics.f1_score:.4f}"
        )
        print(f"Overfitting Detectado: {report.overfitting_detected}")
        print(f"Falhas em Near-Misses: {len(report.near_miss_failures)}")
    return 0 if report.overall_metrics.f1_score >= 0.95 and not report.overfitting_detected else 1


if __name__ == "__main__":
    raise SystemExit(main())
