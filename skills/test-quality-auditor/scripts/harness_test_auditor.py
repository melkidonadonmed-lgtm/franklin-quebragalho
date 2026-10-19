#!/usr/bin/env python3
"""
harness_test_auditor.py
Módulo Determinístico de Auditoria de Qualidade de Testes de Harness:
1. Execution & Governance Harness (SemanticGuard, evaluate_action_risk, CheckpointStore HITL, MemoryPolicy).
2. Eval-Driven Harness (run_eval_harness, grading.json, benchmark.json, Trigger Matrix).
"""

from __future__ import annotations

import re
from typing import Dict, List

from go_test_auditor import audit_go_test_file
from mcp_test_auditor import _extract_test_blocks_generic
from models import AuditIssue, FileAuditReport, classify_quality_level
from python_ast_auditor import audit_python_test_file
from ts_js_auditor import audit_ts_js_test_file

HARNESS_MARKERS = (
    "SemanticGuard",
    "sanitize_input",
    "SecurityViolationError",
    "evaluate_action_risk",
    "RiskLevel",
    "CheckpointStore",
    "CheckpointRecord",
    "franklin_harness_guard",
    "franklin_harness_checkpoint",
    "run_eval_harness",
    "ShouldSkipMemorySync",
    "SanitizeAndChunk",
)


def is_harness_test_content(code_str: str, filename: str = "") -> bool:
    """Detecta se o arquivo ou bloco de teste exercita primitivas de Harness (Governança HITL ou Eval Harness)."""
    lower_name = filename.lower()
    if "harness" in lower_name:
        return True
    return any(marker in code_str for marker in HARNESS_MARKERS)


def _make_harness_issue(
    issue_id: str,
    title: str,
    severity: str,
    filename: str,
    test_name: str,
    start_line: int,
    penalty: int,
    desc: str,
    rec: str,
) -> AuditIssue:
    """Cria uma instância padronizada de AuditIssue para testes de Harness."""
    return AuditIssue(
        id=issue_id,
        title=title,
        category="Governança & Isolamento de Harness (HITL / Zero-Trust)",
        severity=severity,
        file=filename,
        test_name=test_name,
        line=start_line,
        col=1,
        penalty=penalty,
        description=desc,
        recommendation=rec,
    )


def _check_harness_guard_and_risk(
    block_text: str,
    filename: str,
    test_name: str,
    start_line: int,
    has_destructive_cmd: bool,
) -> List[AuditIssue]:
    """Verifica invariantes de SemanticGuard (injeção) e evaluate_action_risk (ação destrutiva)."""
    found: List[AuditIssue] = []
    has_injection_payload = any(
        inj in block_text.lower()
        for inj in ("ignore all previous instructions", "system prompt override", "<script")
    )
    if ("SemanticGuard" in block_text or "sanitize_input" in block_text) and has_injection_payload:
        if not any(tok in block_text for tok in ("pytest.raises", "SecurityViolationError", "assertRaises", "BLOCKED")):
            found.append(
                _make_harness_issue(
                    "HARNESS_WEAK_INJECTION_GUARD_TEST",
                    "Teste do SemanticGuard Com Injeção Sem Exigir SecurityViolationError",
                    "Crítica",
                    filename,
                    test_name,
                    start_line,
                    50,
                    f"[FATO] O teste de Harness '{test_name}' passa payload de injeção ao SemanticGuard sem validar o disparo de SecurityViolationError.",
                    "Utilize 'with pytest.raises(SecurityViolationError, match=...):' para comprovar o bloqueio determinístico.",
                )
            )
    if ("evaluate_action_risk" in block_text or "franklin_harness_guard" in block_text) and has_destructive_cmd:
        if not any(tok in block_text for tok in ("RiskLevel.CRITICAL", '"CRITICAL"', "'CRITICAL'", "APPROVAL_REQUIRED")):
            found.append(
                _make_harness_issue(
                    "HARNESS_UNVERIFIED_RISK_TRANSITION",
                    "Teste de Policy Gate HITL Sem Validar Classificação CRITICAL / APPROVAL_REQUIRED",
                    "Crítica",
                    filename,
                    test_name,
                    start_line,
                    45,
                    f"[FATO] O teste de Harness '{test_name}' submete ação destrutiva ao avaliador de risco, mas não verifica RiskLevel.CRITICAL ou status APPROVAL_REQUIRED.",
                    "Valide explicitamente 'assert risk == RiskLevel.CRITICAL' e a exigência de checkpoint HITL.",
                )
            )
    return found


def _check_harness_checkpoint_and_eval(
    block_text: str,
    filename: str,
    test_name: str,
    start_line: int,
    has_destructive_cmd: bool,
) -> List[AuditIssue]:
    """Verifica isolamento de CheckpointStore, ciclo de vida HITL e métricas de run_eval_harness."""
    found: List[AuditIssue] = []
    mutates_checkpoints = (
        ("franklin_harness_guard(" in block_text and has_destructive_cmd)
        or (".create(" in block_text and "CheckpointStore" in block_text)
    )
    has_isolated_storage = any(
        iso in block_text for iso in ("tmp_path", "TempDir(", "tempfile", "finally:", "t.Cleanup(")
    )
    if mutates_checkpoints and not has_isolated_storage:
        found.append(
            _make_harness_issue(
                "HARNESS_MISSING_TEARDOWN_CLEANUP",
                "Mutação de Checkpoints HITL Sem Isolamento (tmp_path) ou Bloco try/finally",
                "Alta", filename, test_name, start_line, 35,
                f"[FATO] O teste de Harness '{test_name}' persiste checkpoints sem usar diretório temporário isolado (tmp_path/t.TempDir) nem limpeza garantida em 'try...finally'.",
                "Injete 'tmp_path / \"checkpoints.json\"' no CheckpointStore ou limpe o estado dentro de 'finally: ...'.",
            )
        )
    if "CheckpointStore" in block_text and ".create(" in block_text:
        if not any(m in block_text for m in (".update_status(", ".get(", ".list(")):
            found.append(
                _make_harness_issue(
                    "HARNESS_INCOMPLETE_CHECKPOINT_LIFECYCLE",
                    "Teste de CheckpointStore Sem Validar Persistência ou Transição de Status (PENDING -> APPROVED/REJECTED)",
                    "Média", filename, test_name, start_line, 25,
                    f"[FATO] O teste de Harness '{test_name}' invoca 'CheckpointStore.create()', mas não verifica a leitura (.get/.list) nem a transição de aprovação (.update_status).",
                    "Valide o ciclo completo HITL: criação (PENDING) -> listagem/busca -> update_status(APPROVED/REJECTED) -> clear().",
                )
            )
    if "run_eval_harness(" in block_text and not any(
        k in block_text for k in ("pass_rate", "pass_rate_gain", "evidence", "failed")
    ):
        found.append(
            _make_harness_issue(
                "HARNESS_EVAL_MISSING_EVIDENCE_OR_DELTA",
                "Teste do Eval-Driven Harness Sem Validar 'pass_rate', 'evidence' ou 'delta'",
                "Alta", filename, test_name, start_line, 35,
                f"[FATO] O teste '{test_name}' executa 'run_eval_harness()', mas não inspeciona 'pass_rate', 'evidence' ou o ganho sobre o baseline ('delta').",
                "Valide explicitamente summary['pass_rate'] == 1.0, presença de 'evidence' não-vazia e delta['pass_rate_gain'] > 0.",
            )
        )
    return found


def _inspect_single_harness_block(
    test_name: str,
    start_line: int,
    raw_block_text: str,
    report: FileAuditReport,
    dossier_map: Dict[str, int],
) -> None:
    """Inspeciona um único bloco de teste quanto às invariantes de Harness e atualiza o dossiê."""
    meta_fns = ("audit_harness_test_file(", "audit_mcp_test_file(", "audit_go_test_file(", "audit_test_file(")
    block_text = (
        re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '""', raw_block_text)
        if any(fn in raw_block_text for fn in meta_fns)
        else raw_block_text
    )
    if not is_harness_test_content(block_text, ""):
        return

    has_destructive_cmd = any(
        cmd in block_text.lower()
        for cmd in ("remove-item", "rm -rf", "drop table", "drop database", "exclusão definitiva", "apagar tudo")
    )
    candidates = _check_harness_guard_and_risk(
        block_text, report.filename, test_name, start_line, has_destructive_cmd
    ) + _check_harness_checkpoint_and_eval(
        block_text, report.filename, test_name, start_line, has_destructive_cmd
    )

    harness_issues: List[AuditIssue] = []
    for cand in candidates:
        if not any(existing.id == cand.id and existing.test_name == test_name for existing in report.issues):
            report.issues.append(cand)
            harness_issues.append(cand)

    if test_name in dossier_map:
        d = report.dossiers[dossier_map[test_name]]
        if not d.domain.startswith("harness"):
            d.domain = f"harness/{report.language}"
        if harness_issues:
            for h_iss in harness_issues:
                d.issues.append(h_iss.id)
                d.score = max(0, d.score - h_iss.penalty)
            d.level = classify_quality_level(d.score)
            d.status = "[PASS]" if len(d.issues) == 0 and d.score >= 81 else "[FAIL]"
            d.evidence = "; ".join(f"{i_id}" for i_id in d.issues)


def enrich_with_harness_audit(report: FileAuditReport, code_str: str) -> FileAuditReport:
    """Inspeciona invariantes de qualidade de testes de Harness (Zero-Trust, HITL Checkpoints, Isolamento e Evals)."""
    if not is_harness_test_content(code_str, report.filename):
        return report

    blocks = _extract_test_blocks_generic(code_str, report.language)
    dossier_map: Dict[str, int] = {d.test_name: idx for idx, d in enumerate(report.dossiers)}

    for test_name, start_line, raw_block_text in blocks:
        _inspect_single_harness_block(test_name, start_line, raw_block_text, report, dossier_map)

    report.total_inconformidades = len(report.issues)
    report.score_medio = (
        sum(d.score for d in report.dossiers) / len(report.dossiers) if report.dossiers else report.score_medio
    )
    report.nivel_espectro = classify_quality_level(report.score_medio)
    report.aprovado = report.total_inconformidades == 0 and report.score_medio >= 81.0
    return report



def audit_harness_test_file(code_str: str, filename: str = "test_harness_suite.py") -> FileAuditReport:
    """Ponto de entrada direto para auditar qualquer suíte de testes de Harness (Python, Go ou TS/JS)."""
    if filename.endswith(".go"):
        base_report = audit_go_test_file(code_str, filename)
    elif filename.endswith((".ts", ".js", ".tsx", ".jsx")):
        base_report = audit_ts_js_test_file(code_str, filename)
    else:
        base_report = audit_python_test_file(code_str, filename)
    return enrich_with_harness_audit(base_report, code_str)
