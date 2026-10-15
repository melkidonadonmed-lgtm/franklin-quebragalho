#!/usr/bin/env python3
"""
ts_js_auditor.py
Analisador Estático Estrutural para Auditoria de Qualidade de Testes em TypeScript / JavaScript.
"""

from __future__ import annotations

import re
from typing import List

from models import AuditIssue, FileAuditReport, TestDossierRecord, classify_quality_level


def audit_ts_js_test_file(code_str: str, filename: str) -> FileAuditReport:
    """Analisa arquivos .test.ts / .test.js extraindo blocos test(...)/it(...) e inspecionando AAA e isolamento."""
    lines = code_str.splitlines()
    issues: List[AuditIssue] = []
    dossiers: List[TestDossierRecord] = []

    test_pattern = re.compile(r"^\s*(?:test|it)\s*\(\s*(['\"`])(.*?)\1\s*,")
    i = 0
    n = len(lines)

    while i < n:
        match = test_pattern.match(lines[i])
        if not match:
            i += 1
            continue

        test_title = match.group(2)
        start_line = i + 1
        brace_depth = 0
        started_block = False
        end_idx = n - 1

        for j in range(i, n):
            clean_line = re.sub(r"//.*$", "", lines[j])
            clean_line = re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`", '""', clean_line)
            clean_line = re.sub(r"/(?![/*])(?:\\.|\[(?:\\.|[^\]\\])*\]|[^/\\\n])+/[dgimsuvy]*", "//", clean_line)
            for ch in clean_line:
                if ch == "{":
                    brace_depth += 1
                    started_block = True
                elif ch == "}":
                    brace_depth -= 1
            if started_block and brace_depth <= 0:
                end_idx = j
                break

        block_lines = lines[i : end_idx + 1]
        block_text = "\n".join(block_lines)
        test_issues: List[AuditIssue] = []

        assert_matches = re.findall(r"\b(?:assert\.\w+|expect\s*\()", block_text)
        assertion_count = len(assert_matches)

        def add_ts_issue(
            issue_id: str,
            title: str,
            category: str,
            severity: str,
            rel_offset: int,
            penalty: int,
            desc: str,
            rec: str,
        ) -> None:
            iss = AuditIssue(
                id=issue_id,
                title=title,
                category=category,
                severity=severity,
                file=filename,
                test_name=test_title,
                line=start_line + rel_offset,
                col=1,
                penalty=penalty,
                description=desc,
                recommendation=rec,
            )
            issues.append(iss)
            test_issues.append(iss)

        if assertion_count == 0:
            add_ts_issue(
                "MISSING_ASSERTIONS",
                "Teste Sem Asserções (False Positive Potential)",
                "Eficácia da Verificação",
                "Crítica",
                0,
                80,
                f"[FATO] O teste '{test_title}' não contém nenhuma chamada a assert.* ou expect().",
                "Adicione asserções estritas (assert.strictEqual / assert.rejects).",
            )

        for idx_l, bl in enumerate(block_lines):
            if re.search(r"assert\.ok\(\s*true\s*\)|expect\(\s*true\s*\)\.toBe\(\s*true\s*\)", bl):
                add_ts_issue(
                    "TAUTOLOGICAL_ASSERT",
                    "Asserção Tautológica (assert.ok(true))",
                    "Qualidade da Asserção",
                    "Crítica",
                    idx_l,
                    80,
                    f"[FATO] O teste '{test_title}' executa asserção tautológica constante.",
                    "Substitua por assert.strictEqual com o valor esperado da regra de negócio.",
                )

            if re.search(r"assert\.ok\(\s*\w+\.length\s*>\s*\d+", bl):
                add_ts_issue(
                    "WEAK_SURFACE_ASSERT",
                    "Asserção Superficial de Comprimento (length > N)",
                    "Qualidade da Asserção",
                    "Média",
                    idx_l,
                    22,
                    f"[FATO] O teste '{test_title}' valida apenas se a string tem comprimento > N na linha {start_line + idx_l}.",
                    "Valide o padrão real da string com expressão regular (assert.match) ou valor exato.",
                )

            if re.search(r"Date\.now\(\)", bl) and ("duration" in block_text or "start" in block_text):
                add_ts_issue(
                    "NON_DETERMINISTIC_TIME",
                    "Medição de Tempo Real com Date.now() (Flaky Test Risk)",
                    "Determinismo & Reprodutibilidade",
                    "Alta",
                    idx_l,
                    22,
                    f"[FATO] O teste '{test_title}' mede tempo real de parede via Date.now() na linha {start_line + idx_l}.",
                    "Valide o contrato de resolução assíncrona ou utilize timers controlados/injetados.",
                )

        mutates_global_window = "globalThis" in block_text and ".window =" in block_text
        mutates_global_fetch = "globalThis.fetch =" in block_text
        has_finally = "finally" in block_text

        if (mutates_global_window or mutates_global_fetch) and not has_finally:
            mut_offset = 0
            for idx_l, bl in enumerate(block_lines):
                if "globalThis" in bl and "=" in bl:
                    mut_offset = idx_l
                    break
            add_ts_issue(
                "GLOBAL_STATE_LEAKAGE",
                "Mutação de globalThis sem Restauração em try/finally",
                "Isolamento de Estado (AAA)",
                "Alta",
                mut_offset,
                25,
                f"[FATO] O teste '{test_title}' sobrescreve 'globalThis' na linha {start_line + mut_offset} sem restaurar em 'try...finally'.",
                "Salve a referência original e restaure obrigatoriamente dentro de 'finally { ... }'.",
            )

        total_penalty = sum(iss.penalty for iss in test_issues)
        score = max(0, 100 - total_penalty)
        level = classify_quality_level(score)
        status = "[PASS]" if len(test_issues) == 0 and score >= 81 else "[FAIL]"
        evidence_str = (
            f"{assertion_count} asserção(ões) estrita(s), isolamento íntegro."
            if not test_issues
            else "; ".join(f"{iss.id} (L{iss.line})" for iss in test_issues)
        )

        dossiers.append(
            TestDossierRecord(
                test_name=test_title,
                file=filename,
                line=start_line,
                assertion_count=assertion_count,
                score=score,
                level=level,
                status=status,
                issues=[iss.id for iss in test_issues],
                evidence=evidence_str,
                domain="typescript",
            )
        )

        i = end_idx + 1

    avg_score = sum(d.score for d in dossiers) / len(dossiers) if dossiers else 100.0
    return FileAuditReport(
        aprovado=len(issues) == 0 and avg_score >= 81.0,
        filename=filename,
        total_tests=len(dossiers),
        score_medio=avg_score,
        nivel_espectro=classify_quality_level(avg_score),
        total_inconformidades=len(issues),
        dossiers=dossiers,
        issues=issues,
        language="typescript",
    )
