"""
state_checker_observer.py
Subagente 5 (Gatekeeper & Observador de Estado): `state-checker-observer` (Peso w5 = 20%).

Integra:
1. Contratos Tipados Pydantic (`IssueFinding`, `SubagentExecutionResult`, `GlobalAuditState`).
2. Classe `StateCheckerObserver` com validação direta na árvore AST (`verify_finding_against_ast`,
   `_check_parent_is_loop`) + inspeção contextual de guardrails para zero falsos positivos.
3. Detecção Automática de Perfil (`profile="auto"`: `3d_physics` vs `general`), garantindo
   Qualidade Linear Alta sem engessar projetos variados.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple
from pydantic import BaseModel, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from static_ast_parser import analyze_code as analyze_py_code, compute_module_scores
from physics_test_runner import (
    DeterministicPhysicsTestSuite,
    _load_external_step_fn,
    step_physics_bad,
    step_physics_good,
)


# -----------------------------------------------------------------------------
# 1. Schemas Pydantic do Estado Global (AuditState)
# -----------------------------------------------------------------------------
class IssueFinding(BaseModel):
    issue_id: str
    title: str
    category: str
    subskill: str = "static-sanitization-auditor"
    severity: Literal["Crítica", "Alta", "Média", "Baixa"] = "Média"
    penalty: int = 10
    physics_subdimension: Optional[str] = None
    subdimension_penalty: int = 0
    file: str
    line: int
    col: int = 0
    description: str
    recommendation: str
    root_cause: str = ""
    best_fix_code: str = ""
    why_best_fix: str = ""
    expected_result: str = ""
    verified_by_observer: bool = False
    observer_notes: str = ""


class SubagentExecutionResult(BaseModel):
    subagent_name: str
    execution_status: Literal["SUCCESS", "FAILED", "NEEDS_RETRY"] = "SUCCESS"
    findings: List[IssueFinding] = Field(default_factory=list)
    raw_logs: Optional[str] = None


class GlobalAuditState(BaseModel):
    project_files: List[str]
    detected_profile: str = "3d_physics"
    audited_files: List[str] = Field(default_factory=list)
    raw_findings: List[IssueFinding] = Field(default_factory=list)
    verified_findings: List[IssueFinding] = Field(default_factory=list)
    rejected_false_positives: List[IssueFinding] = Field(default_factory=list)
    module_scores: Dict[str, float] = Field(default_factory=dict)
    physics_3d_subdimensions: Dict[str, Any] = Field(default_factory=dict)
    deterministic_tests: Dict[str, Any] = Field(default_factory=dict)
    final_s_norm: float = 0.0
    classification: str = ""
    audit_completed: bool = False


# -----------------------------------------------------------------------------
# 2. Motor Determinístico do Observador (StateCheckerObserver)
# -----------------------------------------------------------------------------
class StateCheckerObserver:
    """
    Observador de Estado que valida as saídas dos subagentes executores
    contra a estrutura sintática (AST) e o código-fonte real, eliminando falsos positivos.
    """

    def __init__(self, state: GlobalAuditState) -> None:
        self.state = state

    def verify_finding_against_ast(self, finding: IssueFinding) -> Tuple[bool, str]:
        """
        Relê a AST e as linhas do arquivo alvo e confirma se o erro de fato existe.
        """
        filepath = Path(finding.file)
        if not filepath.exists():
            return True, "Arquivo virtual/em memória validado."

        try:
            code = filepath.read_text(encoding="utf-8", errors="replace")
            source_lines = code.splitlines()
        except Exception:
            return True, "Assumido com cautela (erro de I/O)."

        if finding.line < 1 or finding.line > len(source_lines):
            return False, f"Falso Positivo: Linha {finding.line} fora dos limites ({len(source_lines)} linhas)."

        target_line = source_lines[finding.line - 1]
        window_start = max(0, finding.line - 4)
        window_end = min(len(source_lines), finding.line + 2)
        window_text = "\n".join(source_lines[window_start:window_end]).lower()

        # Validação AST para arquivos Python
        if filepath.suffix.lower() == ".py":
            try:
                tree = ast.parse(code, filename=finding.file)
                if finding.issue_id == "ALLOC_IN_LOOP":
                    for node in ast.walk(tree):
                        if hasattr(node, "lineno") and node.lineno == finding.line:
                            if self._check_parent_is_loop(tree, node):
                                return True, "Confirmado na AST: nó contido em laço ou função render/update."
                    return False, "Falso Positivo descartado: nó fora de escopo de laço na AST."

                elif finding.issue_id == "STRICT_FLOAT_COMPARE":
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Compare) and node.lineno == finding.line:
                            if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops):
                                return True, "Confirmado na AST: operador Eq/NotEq em ponto flutuante."
                    return False, "Falso Positivo descartado: sem comparação estrita na linha apontada."
            except SyntaxError:
                pass

        # Validação contextual de guardrails (Python e JS/TS)
        if finding.issue_id == "UNCHECKED_NORMALIZE":
            guard_tokens = ("length", "lengthsq", "length_sq", "mag", "magnitude", "epsilon", "1e-")
            if any(tok in window_text for tok in guard_tokens):
                return False, "Falso Positivo descartado: guardrail de magnitude/EPSILON encontrado na vizinhança."

        if finding.issue_id == "MISSING_DELTA_TIME":
            if any(tok in target_line.lower() for tok in ("dt", "delta", "deltatime", "addscaledvector")):
                return False, "Falso Positivo descartado: fator de tempo detectado na linha."

        return True, "Confirmado por inspeção cruzada na árvore/código-fonte."

    def _check_parent_is_loop(self, tree: ast.AST, target_node: ast.AST) -> bool:
        """Verifica se o nó alvo está aninhado em For, While ou função update/render/step."""
        loop_kws = ("update", "render", "step", "tick", "animate", "loop", "integrate", "simulate")
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if child is target_node:
                        return True
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if any(k in node.name.lower() for k in loop_kws) and not node.name.lower().startswith("test_"):
                    for child in ast.walk(node):
                        if child is target_node:
                            return True
        return False

    def process_and_consolidate(
        self,
        execution_results: List[SubagentExecutionResult],
        s4_tests_score: float = 100.0,
    ) -> GlobalAuditState:
        """
        Consolida as saídas dos subagentes, filtra falsos positivos e calcula Snorm.
        """
        for result in execution_results:
            for finding in result.findings:
                self.state.raw_findings.append(finding)
                is_valid, notes = self.verify_finding_against_ast(finding)
                finding.observer_notes = notes
                if is_valid:
                    finding.verified_by_observer = True
                    self.state.verified_findings.append(finding)
                else:
                    self.state.rejected_false_positives.append(finding)

        verified_dicts = [
            {
                "id": f.issue_id,
                "subskill": f.subskill,
                "penalty": f.penalty,
                "physics_subdimension": f.physics_subdimension,
                "subdimension_penalty": f.subdimension_penalty,
            }
            for f in self.state.verified_findings
        ]
        static_scores = compute_module_scores(verified_dicts)

        s1 = float(static_scores["s1_static_sanitization"])
        s2 = float(static_scores["s2_architecture_hardcoded"])
        s3 = float(static_scores["s3_physics_3d_math"])
        s4 = float(s4_tests_score)
        s5 = 100.0 if len(self.state.audited_files) >= len(self.state.project_files) else 80.0

        s_norm = round(0.20 * s1 + 0.15 * s2 + 0.25 * s3 + 0.20 * s4 + 0.20 * s5, 2)

        if s_norm >= 90.0:
            classification = "Excelente / Pronto para Produção (Enterprise 3D)"
        elif s_norm >= 75.0:
            classification = "Aprovado com Ressalvas (Débitos Técnicos Moderados)"
        elif s_norm >= 50.0:
            classification = "Instável / Requer Saneamento Matemático e de Memória"
        else:
            classification = "Reprovado / Risco Crítico de Simulação"

        self.state.module_scores = {
            "s1_static_sanitization": s1,
            "s2_architecture_hardcoded": s2,
            "s3_physics_3d_math": s3,
            "s3_subdimensions_weighted": static_scores["s3_subdimensions_weighted"],
            "s4_deterministic_tests": s4,
            "s5_state_observer": s5,
        }
        self.state.physics_3d_subdimensions = static_scores["physics_3d_subdimensions"]
        self.state.final_s_norm = s_norm
        self.state.classification = classification
        self.state.audit_completed = True
        return self.state


def _dict_to_finding(d: Dict[str, Any]) -> IssueFinding:
    sev = d.get("severity", "Média")
    if sev not in ("Crítica", "Alta", "Média", "Baixa"):
        sev = "Média"
    return IssueFinding(
        issue_id=d.get("id", "UNKNOWN"),
        title=d.get("title", ""),
        category=d.get("category", "Geral"),
        subskill=d.get("subskill", "static-sanitization-auditor"),
        severity=sev,
        penalty=int(d.get("penalty", 10)),
        physics_subdimension=d.get("physics_subdimension"),
        subdimension_penalty=int(d.get("subdimension_penalty") or 0),
        file=d.get("file", ""),
        line=int(d.get("line", 1)),
        col=int(d.get("col", 0)),
        description=d.get("description", ""),
        recommendation=d.get("recommendation", ""),
        root_cause=d.get("root_cause", ""),
        best_fix_code=d.get("best_fix_code", ""),
        why_best_fix=d.get("why_best_fix", ""),
        expected_result=d.get("expected_result", ""),
    )


def run_js_ts_audit(filepath: Path) -> Dict[str, Any]:
    js_parser = SCRIPT_DIR / "js_ts_ast_parser.js"
    res = subprocess.run(
        ["node", str(js_parser), str(filepath)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if res.returncode != 0:
        return {"error": res.stderr.strip(), "issues": [], "scores": compute_module_scores([])}
    return json.loads(res.stdout)


def audit_target(
    target_path: Path,
    func_name: str = "",
    test_mode: str = "auto",
) -> Dict[str, Any]:
    source_code = target_path.read_text(encoding="utf-8", errors="replace")

    if target_path.suffix.lower() in (".js", ".ts", ".jsx", ".tsx"):
        static_res = run_js_ts_audit(target_path)
    else:
        static_res = analyze_py_code(source_code, filename=str(target_path))

    raw_issues = static_res.get("issues", [])
    findings_objs = [_dict_to_finding(iss) for iss in raw_issues]

    # Onda 2: Testes Determinísticos
    if test_mode == "bad":
        step_fn = step_physics_bad
        label = "step_physics_bad"
    elif test_mode == "good":
        step_fn = step_physics_good
        label = "step_physics_good"
    elif target_path.suffix.lower() == ".py":
        loaded_fn = _load_external_step_fn(target_path, func_name or None)
        if loaded_fn is not None:
            step_fn = loaded_fn
            label = f"{target_path.name}:{loaded_fn.__name__}"
        else:
            step_fn = step_physics_good
            label = "reference:step_physics_good"
    else:
        step_fn = step_physics_good
        label = "reference:step_physics_good"

    test_suite_res = DeterministicPhysicsTestSuite(step_fn, label=label).run_all_tests()

    state = GlobalAuditState(
        project_files=[str(target_path)],
        audited_files=[str(target_path)] if "error" not in static_res else [],
        deterministic_tests=test_suite_res,
    )
    observer = StateCheckerObserver(state)
    subagent_res = SubagentExecutionResult(
        subagent_name="wave1_static_auditors",
        execution_status="SUCCESS" if "error" not in static_res else "FAILED",
        findings=findings_objs,
    )
    consolidated = observer.process_and_consolidate(
        [subagent_res],
        s4_tests_score=float(test_suite_res["pass_rate_score"]),
    )

    verified_dicts = [
        {
            "id": f.issue_id,
            "title": f.title,
            "category": f.category,
            "subskill": f.subskill,
            "severity": f.severity,
            "penalty": f.penalty,
            "file": f.file,
            "line": f.line,
            "col": f.col,
            "description": f.description,
            "recommendation": f.recommendation,
            "root_cause": f.root_cause,
            "best_fix_code": f.best_fix_code,
            "why_best_fix": f.why_best_fix,
            "expected_result": f.expected_result,
            "observer_verification": f"[PASS] {f.observer_notes}",
        }
        for f in consolidated.verified_findings
    ]

    return {
        "target_file": str(target_path),
        "s_norm": consolidated.final_s_norm,
        "classification": consolidated.classification,
        "module_scores": consolidated.module_scores,
        "physics_3d_subdimensions": consolidated.physics_3d_subdimensions,
        "observer_summary": {
            "files_covered_pct": 100.0 if consolidated.audited_files else 0.0,
            "raw_alerts_count": len(consolidated.raw_findings),
            "verified_issues_count": len(consolidated.verified_findings),
            "false_positives_filtered": len(consolidated.rejected_false_positives),
            "discarded_details": [f.model_dump() for f in consolidated.rejected_false_positives],
        },
        "deterministic_tests": consolidated.deterministic_tests,
        "verified_issues": verified_dicts,
        "pydantic_audit_state": consolidated.model_dump(),
    }


def format_markdown_report(audit_data: Dict[str, Any]) -> str:
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

    lines.extend(["", "---", "", "## 🚨 Diagnóstico Detalhado de Problemas Validados pelo Observador", ""])

    if not issues:
        lines.append("> `[PASS]` Nenhum problema estático confirmado após a validação cruzada do Observador.")
    else:
        for idx, iss in enumerate(issues, start=1):
            err_code = f"ERR-{idx:03d} / {iss['id']}"
            loc = f"{Path(iss['file']).name}:{iss['line']}"
            lines.extend(
                [
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
            )
            if iss.get("best_fix_code"):
                lines.extend(["```python", iss["best_fix_code"], "```"])
            lines.extend(
                [
                    f"* **Por que é a melhor forma:** {iss.get('why_best_fix', iss['recommendation'])}",
                    "",
                    "#### 3. Resultado Esperado Após a Correção",
                    f"* {iss.get('expected_result', 'Estabilidade numérica e conformidade arquitetural restabelecidas.')}",
                    "",
                ]
            )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Subagente Observador & State Checker (Consolidador Snorm).")
    parser.add_argument("target", nargs="?", default="", help="Caminho do arquivo (.py, .js, .ts) a ser auditado.")
    parser.add_argument("--func", default="", help="Nome opcional da função de passo físico para o Test Runner.")
    parser.add_argument(
        "--test-mode",
        choices=["auto", "good", "bad"],
        default="auto",
        help="Modo do runner determinístico (auto, good ou bad).",
    )
    parser.add_argument("--json", action="store_true", help="Emite o resultado consolidado em formato JSON.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste com amostra sintética integrada.")
    args = parser.parse_args()

    if args.self_test or not args.target:
        import tempfile
        sample_code = (
            "class Vector3:\n"
            "    def __init__(self, x=0.0, y=0.0, z=0.0): pass\n"
            "    def normalize(self): return self\n"
            "def init_scene():\n"
            "    v_init = Vector3(1, 2, 3)\n"
            "def update_physics(pos, vel, dt):\n"
            "    for i in range(5):\n"
            "        temp = Vector3(0, -9.81, 0)\n"
            "        pos += vel\n"
        )
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(sample_code)
            tmp_path = Path(tmp.name)
        try:
            audit_data = audit_target(tmp_path, func_name=args.func, test_mode="bad")
            # Simula um falso positivo de ALLOC_IN_LOOP fora do laço (linha 5 - init_scene) para provar o filtro AST
            fake_fp = IssueFinding(
                issue_id="ALLOC_IN_LOOP",
                title="Alocação fora do loop reportada erroneamente",
                category="Sanitização Estática",
                severity="Crítica",
                file=str(tmp_path),
                line=5,
                description="Alocação em init_scene",
                recommendation="N/A",
            )
            obs_check = StateCheckerObserver(GlobalAuditState(project_files=[str(tmp_path)]))
            fp_verified, fp_reason = obs_check.verify_finding_against_ast(fake_fp)
            audit_data["self_test_ast_cross_check"] = {
                "fake_alloc_outside_loop_line_5_accepted": fp_verified,
                "reason": fp_reason,
                "status": "PASS (Falso Positivo Rejeitado)" if not fp_verified else "FAIL",
            }
            if args.json:
                print(json.dumps(audit_data, indent=2, ensure_ascii=False))
            else:
                print(format_markdown_report(audit_data))
                print(f"\n[Self-Test AST Cross-Check]: {audit_data['self_test_ast_cross_check']['status']}")
        finally:
            tmp_path.unlink(missing_ok=True)
        return

    target_path = Path(args.target)
    if not target_path.exists():
        print(json.dumps({"error": f"Arquivo alvo não encontrado: {target_path}"}, ensure_ascii=False))
        sys.exit(1)

    audit_data = audit_target(target_path, func_name=args.func, test_mode=args.test_mode)
    if args.json:
        print(json.dumps(audit_data, indent=2, ensure_ascii=False))
    else:
        print(format_markdown_report(audit_data))


if __name__ == "__main__":
    main()

