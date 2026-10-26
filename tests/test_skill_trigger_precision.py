"""
test_skill_trigger_precision.py
Suíte de testes determinísticos para a precisão de disparo Nível 1 (Should-Trigger vs. Near-Misses)
de todas as 25 Agent Skills Canônicas do Franklin Quebra-Galho.
"""

from __future__ import annotations

import server
from shared.trigger_eval_suite import CANONICAL_TRIGGER_EVAL_CASES, run_trigger_eval_suite


def test_all_25_canonical_skills_covered_in_trigger_suite() -> None:
    """Garante que todas as 25 skills canônicas do disco possuem casos should-trigger e near-miss."""
    disk_skills = {
        d.name for d in server.SKILLS_ROOT.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    }
    covered_skills = {c.expected_skill for c in CANONICAL_TRIGGER_EVAL_CASES}
    missing = disk_skills - covered_skills
    assert not missing, f"Skills sem cobertura na suíte de disparo: {sorted(missing)}"
    assert len(covered_skills) == len(disk_skills)


def test_should_trigger_and_near_miss_precision_100_percent() -> None:
    """Valida Top-1 Accuracy = 100%, Near-Miss Rejection Rate = 100% e F1 = 1.0 nos 26 casos."""
    report = run_trigger_eval_suite()
    assert report.status == "[PASS]", f"Falhas de disparo detectadas: {report.failures}"
    assert report.failures == []
    assert report.top1_accuracy == 1.0
    assert report.top3_recall == 1.0
    assert report.near_miss_rejection_rate == 1.0
    assert report.f1_score == 1.0


def test_negative_clause_penalization_on_near_misses() -> None:
    """Valida que cláusulas 'não use para ...' penalizam falsos positivos em consultas ambíguas."""
    report = run_trigger_eval_suite()
    by_id = {o.case_id: o for o in report.outcomes}

    # TRG-03: "auditoria epistêmica isolada..." -> refine-prompt deve vencer arquiteto-conteudo-solucoes
    trg03 = by_id["TRG-03"]
    assert trg03.top1_skill == "refine-prompt"
    assert trg03.expected_skill_score > trg03.near_miss_scores["arquiteto-conteudo-solucoes"]

    # TRG-12: "manutenção de arquivos locais..." -> manutencao-disco-windows deve vencer refine-prompt
    trg12 = by_id["TRG-12"]
    assert trg12.top1_skill == "manutencao-disco-windows"
    assert trg12.expected_skill_score > trg12.near_miss_scores["refine-prompt"]


def test_strict_yaml_frontmatter_and_malformed_rejection() -> None:
    """Garante que todos os SKILL.md passam em yaml.safe_load estrito e que frontmatter malformado é rejeitado."""
    import yaml
    from shared.tools.frontmatter_parser import _parse_fallback_lines, parse_frontmatter

    for skill_md in sorted(server.SKILLS_ROOT.glob("*/SKILL.md")):
        raw = skill_md.read_text(encoding="utf-8")
        parts = raw.split("---", 2)
        parsed_yaml = yaml.safe_load(parts[1])
        assert isinstance(parsed_yaml, dict), f"Frontmatter inválido em {skill_md.parent.name}"
        assert parsed_yaml.get("name") == skill_md.parent.name

    broken_doc = (
        "---\n"
        "name: broken-skill\n"
        "metadata:\n"
        "  \n"
        'version: "2.0.0"\n'
        '  author: "Test"\n'
        "---\n"
        "# Corpo\n"
    )
    meta, _ = parse_frontmatter(broken_doc)
    assert meta == {}
    assert _parse_fallback_lines('name: broken\nmetadata:\n  \nversion: "1.0"\n  author: "X"') == {}
