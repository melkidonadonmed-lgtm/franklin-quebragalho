#!/usr/bin/env python3
"""
test_code_acceptability_auditor.py
Suíte determinística de testes unitários para o Code Acceptability Auditor,
TriggerEvalRunner e SkillFailureAuditor.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from code_acceptability_auditor import CodeAcceptabilityAuditor
from skill_failure_auditor import EvalAssertion, FailureTestCase, SkillFailureAuditor
from trigger_eval_runner import TriggerEvalRunner, load_canonical_queries


def test_clean_typed_code_is_approved() -> None:
    auditor = CodeAcceptabilityAuditor()
    code = (
        "def calculate_tax(amount: float, rate: float) -> float:\n"
        "    if amount < 0:\n"
        "        raise ValueError('Invalid amount')\n"
        "    return round(amount * rate, 2)\n"
    )
    report = auditor.audit_code(code)
    assert report.passed_syntax is True
    assert report.status == "APPROVED"
    assert report.quality_score == 100.0
    assert report.critical_violations == 0
    assert "[PASS]" in report.deterministic_markers


def test_detects_hardcoded_secret_and_eval_and_shell_true() -> None:
    auditor = CodeAcceptabilityAuditor()
    prefix = "sk-" + "live-"
    token_val = prefix + "9876543210abcdef123456"
    code = (
        "import subprocess\n"
        f"API_KEY = '{token_val}'\n"
        "def run_unsafe(cmd: str) -> None:\n"
        "    eval(cmd)\n"
        "    subprocess.run(cmd, shell=True)\n"
    )
    report = auditor.audit_code(code)
    rule_ids = {v.rule_id for v in report.violations}
    assert "SEC001" in rule_ids
    assert "SEC002" in rule_ids
    assert "SEC003" in rule_ids
    assert report.status == "REJECTED"
    assert report.critical_violations == 3
    assert report.quality_score == 25.0


def test_detects_silent_and_bare_except_and_missing_types() -> None:
    auditor = CodeAcceptabilityAuditor()
    code = (
        "def process_item(x):\n"
        "    try:\n"
        "        return int(x)\n"
        "    except:\n"
        "        pass\n"
    )
    report = auditor.audit_code(code)
    rule_ids = {v.rule_id for v in report.violations}
    assert "TYP001" in rule_ids
    assert "TYP002" in rule_ids
    assert "ERR001" in rule_ids
    assert "ERR003" in rule_ids
    assert report.status == "REJECTED"


def test_detects_syntax_error_and_long_function() -> None:
    auditor = CodeAcceptabilityAuditor(max_function_lines=10)
    bad_syntax = "def broken(x: int) -> int\n    return x\n"
    syn_report = auditor.audit_code(bad_syntax)
    assert syn_report.passed_syntax is False
    assert syn_report.status == "REJECTED"
    assert syn_report.violations[0].rule_id == "SYN001"

    long_lines = "\n".join([f"    v_{i} = {i}" for i in range(15)])
    long_code = f"def big_fn(a: int) -> int:\n{long_lines}\n    return a\n"
    arch_report = auditor.audit_code(long_code)
    assert any(v.rule_id == "ARCH001" for v in arch_report.violations)


def test_detects_cognitive_nesting_arch002_and_cyclomatic_arch003() -> None:
    auditor = CodeAcceptabilityAuditor(max_nesting_depth=3, max_cyclomatic_complexity=10)
    deep_and_branchy = (
        "def complex_fn(x: int) -> int:\n"
        "    if x > 0:\n"
        "        for i in range(x):\n"
        "            if i % 2 == 0:\n"
        "                while i > 10:\n"
        "                    i -= 1\n"
        "    if x == 1: return 1\n"
        "    if x == 2: return 2\n"
        "    if x == 3: return 3\n"
        "    if x == 4: return 4\n"
        "    if x == 5: return 5\n"
        "    if x == 6: return 6\n"
        "    if x == 7: return 7\n"
        "    return 0\n"
    )
    report = auditor.audit_code(deep_and_branchy)
    rule_ids = {v.rule_id for v in report.violations}
    assert "ARCH002" in rule_ids
    assert "ARCH003" in rule_ids
    assert report.quality_score == 90.0

    elif_chain = (
        "def flat_elif(code: int) -> str:\n"
        "    if code == 1:\n"
        "        return 'a'\n"
        "    elif code == 2:\n"
        "        return 'b'\n"
        "    elif code == 3:\n"
        "        return 'c'\n"
        "    elif code == 4:\n"
        "        return 'd'\n"
        "    return 'z'\n"
    )
    flat_report = auditor.audit_code(elif_chain)
    assert not any(v.rule_id == "ARCH002" for v in flat_report.violations)
    assert flat_report.quality_score == 100.0


def test_trigger_eval_suite_achieves_100_percent_f1() -> None:
    queries = load_canonical_queries()
    assert len(queries) == 20
    runner = TriggerEvalRunner(
        skill_name="code-acceptability-auditor",
        skill_description="Audita estaticamente arquivos Python via AST.",
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
    assert report.overall_metrics.f1_score == 1.0
    assert report.overall_metrics.accuracy == 1.0
    assert report.overfitting_detected is False
    assert len(report.near_miss_failures) == 0


def test_skill_failure_auditor_computes_positive_delta() -> None:
    auditor = SkillFailureAuditor(skill_name="code-acceptability-auditor")
    cases = [
        FailureTestCase(
            case_id="TC-1",
            prompt="Audite payment.py",
            expected_outcome="Detecta SEC003",
            failure_type="none",
            with_skill_pass=True,
            without_skill_pass=False,
            tokens_with_skill=950,
            tokens_without_skill=600,
            duration_ms_with_skill=1100,
            duration_ms_without_skill=800,
            assertions=[
                EvalAssertion(
                    assertion_id="A1",
                    description="Detecta SEC003",
                    passed_with_skill=True,
                    passed_without_skill=False,
                    evidence="[FAIL: SEC003]",
                )
            ],
        )
    ]
    res = auditor.audit_cases(cases)
    assert res.successful_cases == 1
    assert res.benchmark_delta.pass_rate_delta == 1.0
