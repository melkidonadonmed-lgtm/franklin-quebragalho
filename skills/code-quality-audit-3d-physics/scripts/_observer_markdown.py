"""
_observer_markdown.py
Markdown report formatters for state_checker_observer extracted to keep modules <= 600 lines.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def _format_issue_markdown(idx: int, iss: Dict[str, Any]) -> List[str]:
    err_code = f"ERR-{idx:03d} / {iss['id']}"
    loc = f"{Path(iss['file']).name}:{iss['line']}"
    block = [
        f"### 🚨 [{err_code}] — {iss['title']}",
        f"* **Dimensão Atingida:** {iss['category']} (`{iss['subskill']}`)",
        f"* **Severidade:** {iss['severity']} (Penalidade: -{iss['penalty']} pts)",
        f"* **Localização:** `{loc}`",
        f"* **Veredito do Observador:** `{iss.get('observer_verification', '[PASS] Confirmado')}`",
        "",
        "#### 1. Descrição Detalhada do Problema e Causa Raiz",
        f"* {iss['description']}",
        f"* **Causa Raiz:** {iss.get('root_cause', iss['description'])}",
        "",
        "#### 2. A MELHOR Forma de Resolver e Justificativa Técnica",
    ]
    if iss.get("best_fix_code"):
        block.extend(["```python", iss["best_fix_code"], "```"])
    block.extend(
        [
            f"* **Por que é a melhor forma:** {iss.get('why_best_fix', iss['recommendation'])}",
            "",
            "#### 3. Resultado Esperado Após a Correção",
            f"* {iss.get('expected_result', 'Estabilidade numérica e conformidade arquitetural restabelecidas.')}",
            "",
        ]
    )
    return block


def _format_subdimensions_and_tests_md(subdims: Dict[str, Any], tests: Dict[str, Any]) -> List[str]:
    lines = [
        "---",
        "",
        "## 📐 Decomposição das 5 Sub-dimensões de Física 3D ($s_{\\text{Física}}$)",
        "",
        "| Sub-dimensão Técnica | Peso ($w_k$) | Nota ($S_k$) | Status |",
        "| :--- | :---: | :---: | :---: |",
    ]
    labels_map = {
        "S1_integracao_temporal_dt": "1. Integração Temporal & Delta Time (`dt`)",
        "S2_algebra_vetorial_rotacoes": "2. Álgebra Vetorial & Rotações 3D (Quaternions / Normalize)",
        "S3_conservacao_estabilidade": "3. Leis de Conservação & Estabilidade (`damping` / `restitution`)",
        "S4_colisao_ccd": "4. Detecção de Colisão & CCD (Anti-Tunneling)",
        "S5_robustez_numerica_float": "5. Robustez Numérica & Float (`EPSILON` / Anti-NaN)",
    }
    for key, label in labels_map.items():
        info = subdims[key]
        sc = info["score"]
        wt = int(info["weight"] * 100)
        st = "[PASS]" if sc >= 80 else "[FAIL]"
        lines.append(f"| **{label}** | {wt}% | {sc:.1f} / 100 | `{st}` |")

    lines.extend(
        [
            "",
            "---",
            "",
            f"## 🧪 Resultados da Suíte de Testes Determinísticos (`{tests['target_label']}`)",
            "",
            "| ID do Teste | Bateria | Status | Métrica Obtida |",
            "| :--- | :--- | :---: | :--- |",
        ]
    )
    for tr in tests["results"]:
        badge = "[PASS]" if tr["status"] == "PASSED" else "[FAIL]"
        lines.append(f"| `{tr['id']}` | {tr['title']} | `{badge}` | {tr['metric']} |")
    return lines


def format_markdown_report(audit_data: Dict[str, Any]) -> str:
    """Formats the consolidated 3D physics & AST audit payload as Markdown."""
    m = audit_data["module_scores"]
    obs = audit_data["observer_summary"]
    tests = audit_data["deterministic_tests"]
    subdims = audit_data["physics_3d_subdimensions"]
    issues = audit_data["verified_issues"]

    lines = [
        "# 🛡️ Relatório Final de Auditoria Integrada (Física 3D, Sanitização & Testes)",
        "",
        f"**Arquivo Auditado:** `{audit_data['target_file']}`",
        f"**Escore Normalizado Final ($S_{{\\text{{norm}}}}$):** **{audit_data['s_norm']} / 100** ({audit_data['classification']})",
        "",
        "### Breakdown por Módulo de Subskill:",
        f"- 🧹 **Sanitização Estática (`static-sanitization-auditor`):** {m['s1_static_sanitization']} / 100 (Peso: 20%)",
        f"- 🏗️ **Arquitetura & Hardcoded (`architecture-hardcoded-auditor`):** {m['s2_architecture_hardcoded']} / 100 (Peso: 15%)",
        f"- 📐 **Física 3D & Matemática (`physics-3d-math-auditor`):** {m['s3_physics_3d_math']} / 100 (Peso: 25% | Sub-dimensões ponderadas: {m['s3_subdimensions_weighted']}/100)",
        f"- 🧪 **Testes Determinísticos (`deterministic-tests-auditor`):** {m['s4_deterministic_tests']} / 100 (Peso: 20% — {tests['passed_tests']}/{tests['total_tests']} testes aprovados)",
        f"- 👁️ **Qualidade & Observabilidade (`state-checker-observer`):** {m['s5_state_observer']} / 100 (Peso: 20% — Cobertura: {obs['files_covered_pct']:.0f}%, Falsos Positivos Filtrados: {obs['false_positives_filtered']})",
        "",
    ]
    lines.extend(_format_subdimensions_and_tests_md(subdims, tests))
    lines.extend(["", "---", "", "## 🚨 Diagnóstico Detalhado de Problemas Validados pelo Observador", ""])

    if not issues:
        lines.append("> `[PASS]` Nenhum problema estático confirmado após a validação cruzada do Observador.")
    else:
        for idx, iss in enumerate(issues, start=1):
            lines.extend(_format_issue_markdown(idx, iss))

    return "\n".join(lines)
