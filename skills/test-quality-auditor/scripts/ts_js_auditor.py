#!/usr/bin/env python3
"""
ts_js_auditor.py
Analisador Estático Estrutural para Auditoria de Qualidade de Testes em TypeScript / JavaScript.
"""

from __future__ import annotations

import re
from typing import List, Tuple

from models import AuditIssue, FileAuditReport, TestDossierRecord, classify_quality_level


def _find_ts_block_end(lines: List[str], start_idx: int) -> int:
    """Localiza o índice final de um bloco JS/TS balanceando chaves fora de strings/comentários."""
    brace_depth = 0
    started_block = False
    for j in range(start_idx, len(lines)):
        clean_line = re.sub(r"//.*$", "", lines[j])
        clean_line = re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`", '""', clean_line)
        clean_line = re.sub(r"/(?![/*])(?:\\.|\[(?:\\.|[^\]\\])*\]|[^/\\\n])+/[dgimsuvy]*", "//", clean_line)
        opens = clean_line.count("{")
        closes = clean_line.count("}")
        if opens > 0:
            started_block = True
        brace_depth += opens - closes
        if started_block and brace_depth <= 0:
            return j
    return len(lines) - 1


def _extract_ts_js_blocks(lines: List[str]) -> List[Tuple[str, int, List[str]]]:
    """Extrai blocos test(...)/it(...) com título, linha inicial e lista de linhas."""
    test_pattern = re.compile(r"^\s*(?:test|it)\s*\(\s*(['\"`])(.*?)\1\s*,")
    blocks: List[Tuple[str, int, List[str]]] = []
    i = 0
    while i < len(lines):
        match = test_pattern.match(lines[i])
        if not match:
            i += 1
            continue
        end_idx = _find_ts_block_end(lines, i)
        blocks.append((match.group(2), i + 1, lines[i : end_idx + 1]))
        i = end_idx + 1
    return blocks


def _make_ts_issue(
    issue_id: str,
    title: str,
    category: str,
    severity: str,
    filename: str,
    test_title: str,
    line: int,
    penalty: int,
    desc: str,
    rec: str,
) -> AuditIssue:
    """Cria uma instância padronizada de AuditIssue para testes TypeScript/JavaScript."""
    return AuditIssue(
        id=issue_id,
        title=title,
        category=category,
        severity=severity,
        file=filename,
        test_name=test_title,
        line=line,
        col=1,
        penalty=penalty,
        description=desc,
        recommendation=rec,
    )


def _check_ts_block_lines(
    block_lines: List[str],
    block_text: str,
    filename: str,
    test_title: str,
    start_line: int,
) -> List[AuditIssue]:
    """Inspeciona linhas individuais de um bloco TS/JS contra tautologia, superficialidade e Date.now()."""
    found: List[AuditIssue] = []
    for idx_l, bl in enumerate(block_lines):
        line_no = start_line + idx_l
        if re.search(r"assert\.ok\(\s*true\s*\)|expect\(\s*true\s*\)\.toBe\(\s*true\s*\)", bl):
            found.append(
                _make_ts_issue(
                    "TAUTOLOGICAL_ASSERT",
                    "Asserção Tautológica (assert.ok(true))",
                    "Qualidade da Asserção",
                    "Crítica",
                    filename,
                    test_title,
                    line_no,
                    80,
                    f"[FATO] O teste '{test_title}' executa asserção tautológica constante.",
                    "Substitua por assert.strictEqual com o valor esperado da regra de negócio.",
                )
            )
        if re.search(r"assert\.ok\(\s*\w+\.length\s*>\s*\d+", bl):
            found.append(
                _make_ts_issue(
                    "WEAK_SURFACE_ASSERT",
                    "Asserção Superficial de Comprimento (length > N)",
                    "Qualidade da Asserção",
                    "Média",
                    filename,
                    test_title,
                    line_no,
                    22,
                    f"[FATO] O teste '{test_title}' valida apenas se a string tem comprimento > N na linha {line_no}.",
                    "Valide o padrão real da string com expressão regular (assert.match) ou valor exato.",
                )
            )
        if re.search(r"Date\.now\(\)", bl) and ("duration" in block_text or "start" in block_text):
            found.append(
                _make_ts_issue(
                    "NON_DETERMINISTIC_TIME",
                    "Medição de Tempo Real com Date.now() (Flaky Test Risk)",
                    "Determinismo & Reprodutibilidade",
                    "Alta",
                    filename,
                    test_title,
                    line_no,
                    22,
                    f"[FATO] O teste '{test_title}' mede tempo real de parede via Date.now() na linha {line_no}.",
                    "Valide o contrato de resolução assíncrona ou utilize timers controlados/injetados.",
                )
            )
    return found


def _audit_single_ts_block(
    test_title: str,
    start_line: int,
    block_lines: List[str],
    filename: str,
) -> Tuple[TestDossierRecord, List[AuditIssue]]:
    """Audita um bloco de teste TS/JS e retorna seu dossiê e lista de inconformidades."""
    block_text = "\n".join(block_lines)
    test_issues: List[AuditIssue] = []
    assertion_count = len(re.findall(r"\b(?:assert(?:\.\w+)?\s*\(|expect\s*\()", block_text))

    if assertion_count == 0:
        test_issues.append(
            _make_ts_issue(
                "MISSING_ASSERTIONS", "Teste Sem Asserções (False Positive Potential)",
                "Eficácia da Verificação", "Crítica", filename, test_title, start_line, 80,
                f"[FATO] O teste '{test_title}' não contém nenhuma chamada a assert.* ou expect().",
                "Adicione asserções estritas (assert.strictEqual / assert.rejects).",
            )
        )

    test_issues.extend(_check_ts_block_lines(block_lines, block_text, filename, test_title, start_line))

    mutates_global = ("globalThis" in block_text and ".window =" in block_text) or ("globalThis.fetch =" in block_text)
    if mutates_global and "finally" not in block_text:
        mut_offset = next((idx_l for idx_l, bl in enumerate(block_lines) if "globalThis" in bl and "=" in bl), 0)
        test_issues.append(
            _make_ts_issue(
                "GLOBAL_STATE_LEAKAGE", "Mutação de globalThis sem Restauração em try/finally",
                "Isolamento de Estado (AAA)", "Alta", filename, test_title, start_line + mut_offset, 25,
                f"[FATO] O teste '{test_title}' sobrescreve 'globalThis' na linha {start_line + mut_offset} sem restaurar em 'try...finally'.",
                "Salve a referência original e restaure obrigatoriamente dentro de 'finally { ... }'.",
            )
        )

    score = max(0, 100 - sum(iss.penalty for iss in test_issues))
    evidence_str = (
        f"{assertion_count} asserção(ões) estrita(s), isolamento íntegro."
        if not test_issues
        else "; ".join(f"{iss.id} (L{iss.line})" for iss in test_issues)
    )
    return (
        TestDossierRecord(
            test_name=test_title, file=filename, line=start_line, assertion_count=assertion_count,
            score=score, level=classify_quality_level(score),
            status="[PASS]" if len(test_issues) == 0 and score >= 81 else "[FAIL]",
            issues=[iss.id for iss in test_issues], evidence=evidence_str, domain="typescript",
        ),
        test_issues,
    )


def audit_ts_js_test_file(code_str: str, filename: str) -> FileAuditReport:
    """Analisa arquivos .test.ts / .test.js extraindo blocos test(...)/it(...) e inspecionando AAA e isolamento."""
    lines = code_str.splitlines()
    issues: List[AuditIssue] = []
    dossiers: List[TestDossierRecord] = []

    for test_title, start_line, block_lines in _extract_ts_js_blocks(lines):
        dossier, test_issues = _audit_single_ts_block(test_title, start_line, block_lines, filename)
        dossiers.append(dossier)
        issues.extend(test_issues)

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

