#!/usr/bin/env python3
"""
go_test_auditor.py
Módulo Determinístico de Auditoria de Qualidade de Testes para Go (*_test.go, testing.T, ADK Go v2).
Inspeciona padrão AAA, falhas tautológicas, erros silenciados, goroutines inseguras e isolamento de estado.
"""

from __future__ import annotations

import re
from typing import List, Tuple

from models import AuditIssue, FileAuditReport, TestDossierRecord, classify_quality_level


def _strip_go_comments_and_strings(line: str) -> str:
    """Remove comentários de linha e literais de string para contagem exata de chaves {}."""
    no_comment = re.sub(r"//.*$", "", line)
    return re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`[^`]*`", '""', no_comment)


def _extract_go_test_blocks(lines: List[str]) -> List[Tuple[str, int, int, List[str]]]:
    """Extrai funções func Test*(t *testing.T) com linha inicial, final e corpo."""
    func_pattern = re.compile(r"^\s*func\s+(Test\w+)\s*\(\s*(\w+)\s+\*testing\.T\s*\)")
    blocks: List[Tuple[str, int, int, List[str]]] = []
    i = 0
    n = len(lines)

    while i < n:
        match = func_pattern.match(lines[i])
        if not match:
            i += 1
            continue

        test_name = match.group(1)
        start_line = i + 1
        brace_depth = 0
        started = False
        end_idx = n - 1

        for j in range(i, n):
            clean = _strip_go_comments_and_strings(lines[j])
            for ch in clean:
                if ch == "{":
                    brace_depth += 1
                    started = True
                elif ch == "}":
                    brace_depth -= 1
            if started and brace_depth <= 0:
                end_idx = j
                break

        blocks.append((test_name, start_line, end_idx + 1, lines[i : end_idx + 1]))
        i = end_idx + 1

    return blocks


def audit_go_test_file(code_str: str, filename: str = "suite_test.go") -> FileAuditReport:
    """Audita um arquivo de teste Go (*_test.go) nos 7 módulos e classifica nos Níveis 1 a 4."""
    lines = code_str.splitlines()
    issues: List[AuditIssue] = []
    dossiers: List[TestDossierRecord] = []
    blocks = _extract_go_test_blocks(lines)

    for test_name, start_line, _end_line, block_lines in blocks:
        block_text = "\n".join(block_lines)
        test_issues: List[AuditIssue] = []

        def add_go_issue(
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
                test_name=test_name,
                line=start_line + max(0, rel_offset),
                col=1,
                penalty=penalty,
                description=desc,
                recommendation=rec,
            )
            issues.append(iss)
            test_issues.append(iss)

        # Filtra linhas executáveis internas (excluindo assinatura, chave final, comentários e t.Log)
        inner_lines = [
            re.sub(r"//.*$", "", bl).strip()
            for bl in block_lines[1:-1]
            if re.sub(r"//.*$", "", bl).strip() and re.sub(r"//.*$", "", bl).strip() != "}"
        ]
        meaningful_lines = [
            ln for ln in inner_lines if not re.match(r"^(?:t\.Log|t\.Logf|fmt\.Print)", ln)
        ]

        # Contagem de asserções Go (t.Fatal*, t.Error*, t.Fail*, assert.*, require.*)
        assertion_matches = re.findall(
            r"\b(?:t\.(?:Fatal|Fatalf|Error|Errorf|Fail|FailNow)|(?:assert|require)\.\w+)\s*\(",
            block_text,
        )
        assertion_count = len(assertion_matches)

        # 1. Corpo vazio / Placebo (apenas comentários ou t.Log)
        if len(meaningful_lines) == 0:
            add_go_issue(
                "EMPTY_TEST_BODY",
                "Teste Go Vazio ou Apenas Log (Placebo)",
                "Integridade do Teste (Go)",
                "Crítica",
                0,
                85,
                f"[FATO] A função '{test_name}' está vazia ou contém apenas chamadas informativas (t.Log/fmt.Print) sem validar o SUT.",
                "Implemente a montagem Arrange-Act-Assert invocando o SUT e verificando o retorno com t.Fatalf/t.Errorf.",
            )

        # 2. Ausência total de asserções
        elif assertion_count == 0:
            add_go_issue(
                "MISSING_ASSERTIONS",
                "Teste Go Sem Asserções (Green go test Illusion)",
                "Eficácia da Verificação (Go)",
                "Crítica",
                0,
                80,
                f"[FATO] A função '{test_name}' executa código (Act), mas não possui nenhuma verificação (t.Fatal*, t.Error*, assert.* ou require.*).",
                "Adicione guardas determinísticas (if err != nil { t.Fatalf(...) } e if got != want { t.Errorf(...) }).",
            )

        # Inspeção linha a linha dentro da função de teste
        in_goroutine_depth = 0
        nil_check_count = 0
        strong_check_count = 0

        for idx_l, raw_line in enumerate(block_lines):
            clean_ln = re.sub(r"//.*$", "", raw_line).strip()
            if not clean_ln:
                continue

            # Rastreamento de goroutine anônima: go func(...) {
            if re.search(r"\bgo\s+func\s*\(", clean_ln):
                in_goroutine_depth = 1
            elif in_goroutine_depth > 0:
                in_goroutine_depth += clean_ln.count("{") - clean_ln.count("}")
                if in_goroutine_depth < 0:
                    in_goroutine_depth = 0

            # 3. Asserção Tautológica em Go
            if re.search(
                r"if\s+false\s*\{|(?:assert|require)\.True\s*\(\s*t\s*,\s*true\s*\)|if\s+1\s*==\s*2\s*\{",
                clean_ln,
            ):
                add_go_issue(
                    "TAUTOLOGICAL_ASSERT",
                    "Asserção Tautológica em Go (if false / assert.True(t, true))",
                    "Qualidade da Asserção (Go)",
                    "Crítica",
                    idx_l,
                    80,
                    f"[FATO] O teste '{test_name}' contém condição tautológica na linha {start_line + idx_l} que nunca falha.",
                    "Valide o estado real ou valor de retorno do SUT contra o contrato esperado.",
                )

            # 4.a Descarte explícito de erro no Act (ex: res, _ := sut(...) fora de Cleanup/Close/ReadDir)
            if (
                re.search(r"^\w+\s*,\s*_\s*:?=\s*\w+", clean_ln)
                and not any(safe in clean_ln for safe in ("os.ReadDir", "t.Cleanup", "defer ", ".Close("))
            ):
                add_go_issue(
                    "SILENCED_ERROR_IN_TEST",
                    "Erro Descartado com Blank Identifier (_) em Teste Go",
                    "Tratamento de Erros & Robustez (Go)",
                    "Crítica",
                    idx_l,
                    65,
                    f"[FATO] O teste '{test_name}' descarta o erro retornado com '_' na linha {start_line + idx_l}, mascarando falhas do SUT.",
                    "Capture 'err' explicitamente e valide com 'if err != nil { t.Fatalf(\"unexpected error: %v\", err) }' ou 'errors.Is'.",
                )

            # 4.b Bloco if err != nil que apenas loga ou ignora sem falhar o teste
            if re.match(r"^if\s+err\s*!=\s*nil\s*\{", clean_ln):
                err_window = "\n".join(block_lines[idx_l : min(idx_l + 5, len(block_lines))])
                if not re.search(r"t\.(?:Fatal|Fatalf|Error|Errorf|Fail|FailNow)|return|panic", err_window):
                    add_go_issue(
                        "SILENCED_ERROR_IN_TEST",
                        "Bloco 'if err != nil' Sem Falhar o Teste (t.Log ou Vazio)",
                        "Tratamento de Erros & Robustez (Go)",
                        "Crítica",
                        idx_l,
                        70,
                        f"[FATO] O teste '{test_name}' intercepta 'if err != nil' na linha {start_line + idx_l} sem acionar t.Fatalf/t.Errorf.",
                        "Substitua logs passivos em 'if err != nil' por 't.Fatalf(\"unexpected error: %v\", err)'.",
                    )

            # 5. Contabiliza checagens puramente nil vs checagens fortes de valor/regra
            if re.search(r"^if\s+\w+\s*==\s*nil\s*\{|(?:assert|require)\.NotNil\s*\(", clean_ln):
                nil_check_count += 1
            elif re.search(
                r"^if\s+.*(?:!=|==|<|>|!strings\.|!errors\.|!memorybridge\.|!triage\.|!handled|handled)",
                clean_ln,
            ) or re.search(r"(?:assert|require)\.(?:Equal|ErrorIs|Contains|Len|True|False)\s*\(", clean_ln):
                strong_check_count += 1

            # 6. t.Fatal / t.FailNow dentro de goroutine secundária
            if in_goroutine_depth > 0 and re.search(r"\bt\.(?:Fatal|Fatalf|FailNow)\s*\(", clean_ln):
                add_go_issue(
                    "UNSAFE_GOROUTINE_FATAL",
                    "Chamada Ilegal a t.Fatal/t.FailNow Dentro de Goroutine",
                    "Concorrência & Segurança (Go)",
                    "Alta",
                    idx_l,
                    40,
                    f"[FATO] O teste '{test_name}' chama t.Fatal/t.FailNow dentro de uma goroutine na linha {start_line + idx_l}, violando o contrato de runtime.Goexit do pacote testing.",
                    "Use t.Errorf(...) combinado com canal de erro ou errgroup na goroutine principal.",
                )

            # 7. Vazamento de estado global (os.Setenv / os.Chdir sem t.Setenv / t.Cleanup / defer)
            if re.search(r"\bos\.(?:Setenv|Chdir)\s*\(", clean_ln):
                if "t.Cleanup" not in block_text and "defer " not in block_text:
                    add_go_issue(
                        "GLOBAL_STATE_LEAKAGE",
                        "Mutação de Ambiente Global (os.Setenv/os.Chdir) sem t.Setenv ou t.Cleanup",
                        "Isolamento de Estado (Go AAA)",
                        "Alta",
                        idx_l,
                        25,
                        f"[FATO] O teste '{test_name}' muta o processo com os.Setenv/os.Chdir na linha {start_line + idx_l} sem restauração garantida.",
                        "Substitua os.Setenv por t.Setenv(k, v) e use t.TempDir() / t.Cleanup() para isolamento automático.",
                    )

        # 5.b Verifica se o teste só possui checagem superficial 'if res == nil'
        if assertion_count > 0 and nil_check_count > 0 and strong_check_count == 0 and not any(
            i.id == "TAUTOLOGICAL_ASSERT" for i in test_issues
        ):
            add_go_issue(
                "WEAK_NIL_ONLY_ASSERT",
                "Asserção Superficial Isolada (if res == nil / assert.NotNil)",
                "Qualidade da Asserção (Go)",
                "Média",
                0,
                55,
                f"[FATO] O teste '{test_name}' verifica apenas se o ponteiro/objeto não é nil, sem inspecionar campos de negócio, invariantes ou erros específicos.",
                "Valide os atributos estruturais do retorno (ex: if got.Status != want { t.Errorf(...) }) e erros com errors.Is.",
            )

        # 8. Uso de time.Sleep sem contexto legítimo de sincronismo/debounce atômico
        if "time.Sleep(" in block_text:
            has_concurrency_sync = any(
                tok in block_text
                for tok in ("atomic.", "Debouncer", "FlushAndClose", "WaitGroup", "chan ", "WithTimeout")
            )
            if not has_concurrency_sync:
                sleep_offset = next(
                    (idx for idx, bl in enumerate(block_lines) if "time.Sleep(" in bl), 0
                )
                add_go_issue(
                    "NON_DETERMINISTIC_TIME",
                    "Uso de time.Sleep Arbitrário em Teste Unitário Go (Flaky Test Risk)",
                    "Determinismo & Reprodutibilidade (Go)",
                    "Alta",
                    sleep_offset,
                    25,
                    f"[FATO] O teste '{test_name}' utiliza time.Sleep() na linha {start_line + sleep_offset} sem primitiva de sincronização determinística.",
                    "Injete um Clock/Ticker mockado, utilize canais de sincronização ou valide a coalescência com contadores atômicos (sync/atomic).",
                )

        total_penalty = sum(iss.penalty for iss in test_issues)
        score = max(0, 100 - total_penalty)
        level = classify_quality_level(score)
        status = "[PASS]" if len(test_issues) == 0 and score >= 81 else "[FAIL]"
        evidence_str = (
            f"{assertion_count} verificação(ões) Go testing.T, isolamento íntegro."
            if not test_issues
            else "; ".join(f"{iss.id} (L{iss.line})" for iss in test_issues)
        )

        dossiers.append(
            TestDossierRecord(
                test_name=test_name,
                file=filename,
                line=start_line,
                assertion_count=assertion_count,
                score=score,
                level=level,
                status=status,
                issues=[iss.id for iss in test_issues],
                evidence=evidence_str,
                domain="go",
            )
        )

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
        language="go",
    )
