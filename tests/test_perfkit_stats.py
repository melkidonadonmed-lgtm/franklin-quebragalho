#!/usr/bin/env python3
"""
test_perfkit_stats.py
Suíte de Testes Nível 4 (Determinístico & Resiliente) validando paridade matemática
com GoogleCloudPlatform/PerfKitBenchmarker (tests/sample_test.py) e integração com eval_harness.py.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "test-quality-auditor" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from perfkit_stats import (  # noqa: E402
    Aggregation,
    BenchmarkSample,
    Percentile,
    geometric_mean,
    linear_percentile,
    summarize_latency_ms,
    summarize_percentiles,
)


def test_sample_metadata_isolation_and_float_coercion() -> None:
    """Garante cópia defensiva de metadata e coerção de None/str/int para float (paridade SampleTestCase)."""
    raw_meta = {"origin": "unit_test"}
    sample = BenchmarkSample(metric="throughput", value=None, unit="Mbps", metadata=raw_meta)
    raw_meta["mutated"] = "blocked"

    assert sample.value == 0.0
    assert isinstance(sample.value, float)
    assert sample.metadata == {"origin": "unit_test"}
    assert "mutated" not in sample.metadata

    sample_str = BenchmarkSample(metric="latency", value="42.5", unit="ms")
    assert sample_str.value == 42.5
    assert sample_str.asdict()["metric"] == "latency"


def test_summarize_percentiles_0_to_100_parity() -> None:
    """Valida P0, P10, P50, P90, P95, P99.9, P100, MEAN e STDDEV na série 0..100 (paridade TestSummarizePercentiles)."""
    latencies = [float(x) for x in range(0, 101)]
    metrics = [
        Aggregation.MEAN,
        Aggregation.MIN,
        Aggregation.MAX,
        Aggregation.TOTAL,
        Aggregation.STDDEV,
        Percentile(0),
        Percentile(10),
        Percentile(50),
        Percentile(90),
        Percentile(95),
        Percentile(99.9),
        Percentile(100),
    ]
    base = BenchmarkSample(metric="rpc_", value=0.0, unit="ms", metadata={"env": "ci"})
    samples = summarize_percentiles(latencies, base, metrics=metrics)
    by_metric = {s.metric: s.value for s in samples}

    assert by_metric["rpc_mean"] == 50.0
    assert by_metric["rpc_min"] == 0.0
    assert by_metric["rpc_max"] == 100.0
    assert by_metric["rpc_total"] == 5050.0
    assert by_metric["rpc_p0"] == 0.0
    assert by_metric["rpc_p10"] == 10.0
    assert by_metric["rpc_p50"] == 50.0
    assert by_metric["rpc_p90"] == 90.0
    assert by_metric["rpc_p95"] == 95.0
    assert round(by_metric["rpc_p99.9"], 2) == 99.90
    assert by_metric["rpc_p100"] == 100.0
    assert round(by_metric["rpc_stddev"], 4) == 29.3002


def test_geometric_mean_and_single_element_stddev() -> None:
    """Valida média geométrica livre de overflow e desvio-padrão zero para amostra unitária."""
    assert round(geometric_mean([1.0, 4.0, 16.0]), 6) == 4.0
    single_base = BenchmarkSample(metric="single_", value=0.0, unit="ms")
    single_res = summarize_percentiles([12.5], single_base, metrics=[Aggregation.STDDEV, Percentile(95)])
    by_metric = {s.metric: s.value for s in single_res}

    assert by_metric["single_stddev"] == 0.0
    assert by_metric["single_p95"] == 12.5


def test_percentile_and_summary_error_boundaries() -> None:
    """Verifica rejeição explícita de entradas inválidas (percentis fora de [0, 100], listas vazias e métrica nula)."""
    with pytest.raises(ValueError, match="entre 0 e 100"):
        Percentile(-1.0)
    with pytest.raises(ValueError, match="entre 0 e 100"):
        Percentile(100.5)
    with pytest.raises(ValueError, match="percentil numérico válido"):
        Percentile("not-a-number")
    with pytest.raises(ValueError, match="lista vazia"):
        summarize_percentiles([], BenchmarkSample(metric="empty_", value=0.0))
    with pytest.raises(ValueError, match="sequência vazia"):
        linear_percentile([], 50.0)
    with pytest.raises(ValueError, match="estritamente positivos"):
        geometric_mean([2.0, 0.0, 8.0])
    with pytest.raises(ValueError, match="não pode ser vazio"):
        BenchmarkSample(metric="   ", value=1.0)


def test_summarize_latency_ms_contract() -> None:
    """Verifica o dicionário completo de telemetria emitido para o benchmark.json do eval_harness."""
    summary = summarize_latency_ms([10.0, 20.0, 30.0, 40.0, 100.0])
    expected_keys = {"mean", "stddev", "min", "p50", "p90", "p95", "p99", "p99.9", "max", "geomean"}

    assert set(summary.keys()) == expected_keys
    assert summary["min"] == 10.0
    assert summary["p50"] == 30.0
    assert summary["max"] == 100.0
    assert summary["p95"] > summary["p50"]
    assert summarize_latency_ms([])["p99"] == 0.0
