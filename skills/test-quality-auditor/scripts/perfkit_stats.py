#!/usr/bin/env python3
"""
perfkit_stats.py
Motor Estatístico e de Percentis (P50, P90, P95, P99, P99.9, StdDev, GeoMean)
inspirado em GoogleCloudPlatform/PerfKitBenchmarker (perfkitbenchmarker/sample.py),
refatorado sob ISO/IEC 25010: Standard Library First (zero NumPy), tipagem estrita,
imutabilidade (@dataclass(frozen=True)), M <= 10 (ARCH003) e <= 3 níveis (ARCH002).
"""

from __future__ import annotations

import enum
import math
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence, Union


class Aggregation(str, enum.Enum):
    """Estratégias de agregação estatística compatíveis com PerfKitBenchmarker."""

    MAX = "max"
    MIN = "min"
    MEAN = "mean"
    STDDEV = "stddev"
    AVERAGE = "average"
    TOTAL = "total"
    GEOMEAN = "geomean"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Percentile:
    """Representa um percentil validado no intervalo fechado [0.0, 100.0]."""

    value: float
    label: str = field(init=False)

    def __init__(self, val: float | int | str) -> None:
        try:
            numeric = float(val)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"'{val}' não é um percentil numérico válido.") from exc
        if math.isnan(numeric) or not (0.0 <= numeric <= 100.0):
            raise ValueError(f"O percentil {numeric} deve estar entre 0 e 100.")
        label_str = f"p{int(numeric)}" if numeric.is_integer() else f"p{numeric}"
        object.__setattr__(self, "value", numeric)
        object.__setattr__(self, "label", label_str)

    def __str__(self) -> str:
        return self.label


@dataclass(frozen=True)
class BenchmarkSample:
    """Amostra imutável e tipada de telemetria de performance (substitui sample.Sample namedtuple)."""

    metric: str
    value: float = 0.0
    unit: str = "ms"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __init__(
        self,
        metric: str,
        value: float | int | str | None = 0.0,
        unit: str = "ms",
        metadata: Mapping[str, Any] | None = None,
        timestamp: float | None = None,
    ) -> None:
        if not metric or not metric.strip():
            raise ValueError("O nome da métrica ('metric') não pode ser vazio.")
        numeric_val = 0.0 if value is None else float(value)
        copied_meta = dict(metadata) if metadata is not None else {}
        resolved_ts = time.time() if timestamp is None else float(timestamp)
        object.__setattr__(self, "metric", metric)
        object.__setattr__(self, "value", numeric_val)
        object.__setattr__(self, "unit", unit)
        object.__setattr__(self, "metadata", copied_meta)
        object.__setattr__(self, "timestamp", resolved_ts)

    def asdict(self) -> Dict[str, Any]:
        """Converte a amostra para dicionário serializável."""
        return asdict(self)


MetricSpec = Union[Aggregation, Percentile]


def linear_percentile(sorted_values: Sequence[float], pct: float) -> float:
    """Calcula o percentil por interpolação linear (idêntico a numpy.percentile method='linear')."""
    n = len(sorted_values)
    if n == 0:
        raise ValueError("Não é possível calcular percentil de uma sequência vazia.")
    if not (0.0 <= pct <= 100.0):
        raise ValueError(f"Percentil fora do intervalo [0, 100]: {pct}")
    if n == 1:
        return float(sorted_values[0])

    pos = (pct / 100.0) * (n - 1)
    lower_idx = int(math.floor(pos))
    upper_idx = int(math.ceil(pos))
    if lower_idx == upper_idx:
        return float(sorted_values[lower_idx])
    weight = pos - lower_idx
    return float(sorted_values[lower_idx] + weight * (sorted_values[upper_idx] - sorted_values[lower_idx]))


def geometric_mean(iterable: Iterable[float]) -> float:
    """Calcula a média geométrica de valores positivos em espaço logarítmico (evita overflow)."""
    values = [float(x) for x in iterable]
    if not values:
        raise ValueError("Não é possível calcular a média geométrica de uma sequência vazia.")
    if any(x <= 0.0 for x in values):
        raise ValueError("A média geométrica exige valores estritamente positivos (> 0).")
    log_sum = sum(math.log(x) for x in values)
    return float(math.exp(log_sum / len(values)))


def _sample_stddev(values: Sequence[float]) -> float:
    """Calcula o desvio-padrão amostral (ddof=1), retornando 0.0 para n <= 1."""
    n = len(values)
    if n <= 1:
        return 0.0
    mean_val = sum(values) / n
    variance = sum((x - mean_val) ** 2 for x in values) / (n - 1)
    return float(math.sqrt(variance))


_AGGREGATION_DISPATCH: Dict[Aggregation, Callable[[Sequence[float]], float]] = {
    Aggregation.MIN: lambda vals: float(vals[0]),
    Aggregation.MAX: lambda vals: float(vals[-1]),
    Aggregation.MEAN: lambda vals: float(sum(vals) / len(vals)),
    Aggregation.AVERAGE: lambda vals: float(sum(vals) / len(vals)),
    Aggregation.TOTAL: lambda vals: float(sum(vals)),
    Aggregation.STDDEV: _sample_stddev,
    Aggregation.GEOMEAN: geometric_mean,
}


def _compute_single_metric(sorted_values: Sequence[float], metric: MetricSpec) -> float:
    """Resolve uma única especificação de métrica (Percentile ou Aggregation) com M <= 4."""
    if isinstance(metric, Percentile):
        return linear_percentile(sorted_values, metric.value)
    if isinstance(metric, Aggregation) and metric in _AGGREGATION_DISPATCH:
        return _AGGREGATION_DISPATCH[metric](sorted_values)
    raise ValueError(f"Métrica de agregação inválida ou não suportada: {metric!r}")


DEFAULT_BENCHMARK_METRICS: Tuple[MetricSpec, ...] = (
    Aggregation.MEAN,
    Aggregation.STDDEV,
    Aggregation.MIN,
    Percentile(50),
    Percentile(90),
    Percentile(95),
    Percentile(99),
    Percentile(99.9),
    Aggregation.MAX,
)


def summarize_percentiles(
    numbers: Sequence[float],
    base_sample: BenchmarkSample,
    metrics: Sequence[MetricSpec] = DEFAULT_BENCHMARK_METRICS,
) -> List[BenchmarkSample]:
    """Gera amostras sumarizadas de percentis e agregações para uma série numérica."""
    if not numbers:
        raise ValueError("Não é possível sumarizar percentis de uma lista vazia.")
    sorted_vals = sorted(float(x) for x in numbers)
    return [
        BenchmarkSample(
            metric=f"{base_sample.metric}{metric}",
            value=_compute_single_metric(sorted_vals, metric),
            unit=base_sample.unit,
            metadata=base_sample.metadata,
            timestamp=base_sample.timestamp,
        )
        for metric in metrics
    ]


def summarize_latency_ms(times_ms: Sequence[float], decimals: int = 3) -> Dict[str, float]:
    """Sumariza uma série de tempos em milissegundos com percentis P50/P90/P95/P99/P99.9, stddev e geomean."""
    if not times_ms:
        return {
            "mean": 0.0, "stddev": 0.0, "min": 0.0,
            "p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "p99.9": 0.0,
            "max": 0.0, "geomean": 0.0,
        }
    sorted_vals = sorted(float(x) for x in times_ms)
    summary = {str(m): round(_compute_single_metric(sorted_vals, m), decimals) for m in DEFAULT_BENCHMARK_METRICS}
    positive_vals = [x for x in sorted_vals if x > 0.0]
    summary["geomean"] = round(geometric_mean(positive_vals), decimals) if positive_vals else 0.0
    return summary
