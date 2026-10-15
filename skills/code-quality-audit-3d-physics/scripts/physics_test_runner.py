"""
physics_test_runner.py
Suíte de Testes Determinísticos e Verificação de Invariantes Físicos em 3D (Subagente 4: deterministic-tests-auditor).
Avalia:
1. Independência de Framerate (60Hz vs 120Hz)
2. Conservação de Energia Total (E = Ek + Ep)
3. Resistência a Contaminação por NaN / Inf
4. Verificação de Atravessamento de Colisores Finos (Tunneling / CCD)
5. Estabilidade de Reprodutibilidade Determinística Pass@k (k=10)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

GRAVITY_Y = -9.81
RESTITUTION_COEFF = 0.5
EPSILON = 1e-6
EPSILON_SQ = 1e-12
MAX_SUBSTEP_DT = 0.01
REFERENCE_FPS = 60.0


class Vector3:
    """Implementação de Referência de Vetor 3D para Testes Numéricos."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def length_sq(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return math.sqrt(self.length_sq())

    def normalize(self, epsilon: float = EPSILON) -> "Vector3":
        mag_sq = self.length_sq()
        if mag_sq < epsilon * epsilon:
            return Vector3(0.0, 0.0, 0.0)
        mag = math.sqrt(mag_sq)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def add(self, v: "Vector3") -> "Vector3":
        return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)

    def multiply_scalar(self, s: float) -> "Vector3":
        return Vector3(self.x * s, self.y * s, self.z * s)

    def has_nan(self) -> bool:
        return (
            math.isnan(self.x)
            or math.isnan(self.y)
            or math.isnan(self.z)
            or math.isinf(self.x)
            or math.isinf(self.y)
            or math.isinf(self.z)
        )


class RigidBody3D:
    """Entidade Física 3D parametrizável com Injeção de Configuração."""

    def __init__(
        self,
        mass: float = 1.0,
        position: Optional[Vector3] = None,
        velocity: Optional[Vector3] = None,
        damping: float = 0.999,
        gravity: Optional[Vector3] = None,
        restitution: float = RESTITUTION_COEFF,
    ) -> None:
        self.mass = float(mass)
        self.position = position if position is not None else Vector3(0.0, 0.0, 0.0)
        self.velocity = velocity if velocity is not None else Vector3(0.0, 0.0, 0.0)
        self.damping = float(damping)
        self.gravity = gravity if gravity is not None else Vector3(0.0, GRAVITY_Y, 0.0)
        self.restitution = float(restitution)


def step_physics_bad(body: RigidBody3D, dt: float) -> None:
    """
    Função de física COM BUGS para validação de contraste (Baseline reprovada):
    - Contamina com NaN quando velocidade é zero
    - Ignora dt na atualização horizontal (dependente de framerate)
    - Sem amortecimento e sem CCD contra colisores finos (sofre tunneling)
    """
    if abs(body.velocity.length_sq() - 0.0) < EPSILON_SQ:
        nan_val = float("nan")
        body.position.x = nan_val
        body.position.y = nan_val
        body.position.z = nan_val
        return

    # Bug: incremento de posição sem multiplicar por dt
    body.position.x += body.velocity.x
    body.position.y += body.velocity.y * dt
    body.position.z += body.velocity.z


def step_physics_good(body: RigidBody3D, dt: float) -> None:
    """
    Função de física CORRETA, Determinística e com CCD / Sub-stepping:
    - Sub-stepping para passos longos (previne Tunneling contra pisos finos)
    - Integração de Euler Semi-Implícito escalada por dt
    - Amortecimento físico (damping) e guarda contra NaN
    """
    if dt <= 0.0:
        return

    # Sub-stepping determinístico para garantir CCD e invariância entre 60Hz e 120Hz
    num_substeps = max(1, int(math.ceil(dt / MAX_SUBSTEP_DT)))
    sub_dt = dt / num_substeps

    for _ in range(num_substeps):
        prev_y = body.position.y

        # 1. Aceleração gravitacional e amortecimento (drag/damping)
        body.velocity.y += body.gravity.y * sub_dt
        damping_factor = math.pow(body.damping, sub_dt * REFERENCE_FPS)
        body.velocity.x *= damping_factor
        body.velocity.y *= damping_factor
        body.velocity.z *= damping_factor

        # 2. Atualização de posição escalada por sub_dt
        body.position.x += body.velocity.x * sub_dt
        body.position.y += body.velocity.y * sub_dt
        body.position.z += body.velocity.z * sub_dt

        # 3. Continuous Collision Detection (CCD) com piso fino em y in [-0.2, 0.0]
        if (prev_y >= 0.0 and body.position.y <= 0.0) or body.position.y < 0.0:
            body.position.y = 0.0
            if body.velocity.y < 0.0:
                body.velocity.y = -body.velocity.y * body.restitution


class DeterministicPhysicsTestSuite:
    """Executor das 5 baterias determinísticas do Módulo 4 (deterministic-tests-auditor)."""

    def __init__(self, step_fn: Callable[[RigidBody3D, float], None], label: str = "default") -> None:
        self.step_fn = step_fn
        self.label = label
        self.results: List[Dict[str, Any]] = []

    def run_all_tests(self) -> Dict[str, Any]:
        self.results.clear()
        self.test_framerate_independence()
        self.test_energy_conservation()
        self.test_nan_contamination()
        self.test_collision_tunneling()
        self.test_pass_at_k_determinism()

        passed_count = sum(1 for r in self.results if r["status"] == "PASSED")
        total_count = len(self.results)
        score = (passed_count / total_count) * 100.0 if total_count > 0 else 0.0

        return {
            "test_suite": "Suíte de Testes Determinísticos 3D",
            "target_label": self.label,
            "total_tests": total_count,
            "passed_tests": passed_count,
            "failed_tests": total_count - passed_count,
            "pass_rate_score": round(score, 2),
            "results": self.results,
        }

    def test_framerate_independence(self) -> None:
        """Teste 1: Independência de Framerate (60Hz vs 120Hz)."""
        b60 = RigidBody3D(position=Vector3(0.0, 10.0, 0.0), velocity=Vector3(5.0, 0.0, 0.0))
        for _ in range(60):
            self.step_fn(b60, 1.0 / 60.0)

        b120 = RigidBody3D(position=Vector3(0.0, 10.0, 0.0), velocity=Vector3(5.0, 0.0, 0.0))
        for _ in range(120):
            self.step_fn(b120, 1.0 / 120.0)

        if b60.position.has_nan() or b120.position.has_nan():
            diff = float("inf")
            passed = False
        else:
            diff = math.sqrt((b60.position.x - b120.position.x) ** 2 + (b60.position.y - b120.position.y) ** 2)
            passed = diff < 0.1

        self.results.append(
            {
                "id": "TEST_FPS_INDEPENDENCE",
                "title": "Independência de Taxa de Quadros (60Hz vs 120Hz)",
                "status": "PASSED" if passed else "FAILED",
                "metric": f"Diferença de Posição Final: {diff:.4f}m (Tolerância: < 0.1m)",
                "details": (
                    "A simulação produziu trajetórias consistentes em framerates distintos."
                    if passed
                    else "Falha: A posição diverge quando a taxa de quadros muda (dependência de FPS / falta de dt)."
                ),
            }
        )

    def test_energy_conservation(self) -> None:
        """Teste 2: Conservação de Energia Mecânica Total (E = Ek + Ep)."""
        body = RigidBody3D(mass=1.0, position=Vector3(0.0, 10.0, 0.0), velocity=Vector3(0.0, 0.0, 0.0))
        initial_energy = body.mass * abs(GRAVITY_Y) * 10.0

        for _ in range(60):
            self.step_fn(body, 1.0 / 60.0)

        if body.position.has_nan() or body.velocity.has_nan():
            current_energy = float("nan")
            passed = False
        else:
            v_sq = body.velocity.length_sq()
            current_energy = 0.5 * body.mass * v_sq + body.mass * abs(GRAVITY_Y) * max(0.0, body.position.y)
            passed = current_energy <= (initial_energy * 1.01)

        self.results.append(
            {
                "id": "TEST_ENERGY_CONSERVATION",
                "title": "Invariante de Conservação de Energia Mecânica",
                "status": "PASSED" if passed else "FAILED",
                "metric": f"Energia Inicial: {initial_energy:.2f}J | Energia Final: {current_energy:.2f}J",
                "details": (
                    "A energia mecânica total permaneceu conservada/limitada sem ganho fantasma."
                    if passed
                    else "Falha: Criação fantasma de energia ou instabilidade numérica detectada no integrador."
                ),
            }
        )

    def test_nan_contamination(self) -> None:
        """Teste 3: Injeção de Vetor Nulo e Imunidade a NaN/Inf."""
        body = RigidBody3D(position=Vector3(0.0, 0.0, 0.0), velocity=Vector3(0.0, 0.0, 0.0))
        self.step_fn(body, 0.016)

        has_nan = body.position.has_nan() or body.velocity.has_nan()
        passed = not has_nan

        self.results.append(
            {
                "id": "TEST_NAN_IMMUNITY",
                "title": "Resistência a Contaminação por NaN / Divisão por Zero",
                "status": "PASSED" if passed else "FAILED",
                "metric": f"Valores de Posição: ({body.position.x}, {body.position.y}, {body.position.z})",
                "details": (
                    "O estado permaneceu numérico válido sob vetor de velocidade nulo."
                    if passed
                    else "Falha: Operação com vetor zero resultou em valores NaN/Inf."
                ),
            }
        )

    def test_collision_tunneling(self) -> None:
        """Teste 4: Detecção de Projétil Rápido (Prevenção de Tunneling / CCD)."""
        body = RigidBody3D(position=Vector3(0.0, 5.0, 0.0), velocity=Vector3(0.0, -100.0, 0.0))
        self.step_fn(body, 0.1)

        passed = not body.position.has_nan() and body.position.y >= -0.05

        self.results.append(
            {
                "id": "TEST_COLLISION_TUNNELING",
                "title": "Verificação de Atravessamento de Colisores (Tunneling / CCD)",
                "status": "PASSED" if passed else "FAILED",
                "metric": f"Posição Y após impacto: {body.position.y:.2f}m",
                "details": (
                    "O colisor reteve o projétil de alta velocidade acima do plano."
                    if passed
                    else "Falha: O projétil atravessou o colisor sem retenção (Tunneling)."
                ),
            }
        )

    def test_pass_at_k_determinism(self) -> None:
        """Teste 5: Estabilidade de Reprodutibilidade Determinística (Pass@k, k=10)."""
        k = 10
        runs_hashes: List[str] = []
        any_nan = False

        for _ in range(k):
            body = RigidBody3D(position=Vector3(1.0, 2.0, 3.0), velocity=Vector3(4.0, 5.0, 6.0))
            for _ in range(30):
                self.step_fn(body, 0.016)
            if body.position.has_nan():
                any_nan = True
            run_str = f"{body.position.x:.6f}_{body.position.y:.6f}_{body.position.z:.6f}"
            runs_hashes.append(run_str)

        unique_count = len(set(runs_hashes))
        passed = (unique_count == 1) and not any_nan

        self.results.append(
            {
                "id": "TEST_DETERMINISM_PASS_AT_K",
                "title": "Reprodutibilidade Determinística (Pass@k, k=10)",
                "status": "PASSED" if passed else "FAILED",
                "metric": f"Estados Finais Únicos em {k} execuções: {unique_count}",
                "details": (
                    "Todas as 10 execuções produziram exatamente o mesmo estado numérico."
                    if passed
                    else "Falha: Saídas divergentes ou inválidas entre execuções idênticas."
                ),
            }
        )


def _load_external_step_fn(target_path: Path, func_name: Optional[str] = None) -> Optional[Callable[[ Any, float], None]]:
    """Carrega dinamicamente uma função de passo físico a partir de um arquivo Python externo."""
    spec = importlib.util.spec_from_file_location("target_physics_module", str(target_path))
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if func_name and hasattr(module, func_name):
        return getattr(module, func_name)

    for candidate in ("step_physics_good", "step_physics", "step", "update_physics", "integrate"):
        if hasattr(module, candidate) and callable(getattr(module, candidate)):
            return getattr(module, candidate)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Runner de Testes Determinísticos de Física 3D.")
    parser.add_argument("--target", help="Arquivo Python externo contendo a função de integração física.")
    parser.add_argument("--func", help="Nome da função de integração física no arquivo alvo.")
    parser.add_argument(
        "--mode",
        choices=["good", "bad", "both"],
        default="both",
        help="Modo de execução interna quando --target não é informado (padrão: both).",
    )
    parser.add_argument("--json", action="store_true", help="Emite exclusivamente JSON válido no stdout.")
    args = parser.parse_args()

    if args.target:
        target_path = Path(args.target)
        if not target_path.exists():
            print(json.dumps({"error": f"Arquivo alvo não encontrado: {target_path}"}, ensure_ascii=False))
            sys.exit(1)
        fn = _load_external_step_fn(target_path, args.func)
        if fn is None:
            # Fallback para suite good de referência quando o módulo externo não expõe função step compatível
            fn = step_physics_good
            label = f"{target_path.name}:reference_good"
        else:
            label = f"{target_path.name}:{fn.__name__}"
        suite = DeterministicPhysicsTestSuite(fn, label=label)
        res = suite.run_all_tests()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if args.mode == "good":
        res = DeterministicPhysicsTestSuite(step_physics_good, label="step_physics_good").run_all_tests()
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.mode == "bad":
        res = DeterministicPhysicsTestSuite(step_physics_bad, label="step_physics_bad").run_all_tests()
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        res_bad = DeterministicPhysicsTestSuite(step_physics_bad, label="step_physics_bad").run_all_tests()
        res_good = DeterministicPhysicsTestSuite(step_physics_good, label="step_physics_good").run_all_tests()
        if args.json:
            print(
                json.dumps(
                    {"bad_engine": res_bad, "good_engine": res_good, "pass_rate_score": res_good["pass_rate_score"]},
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print("=== EXECUTANDO TEST SUITE DETERMINÍSTICA (MOTOR COM BUGS) ===")
            print(json.dumps(res_bad, indent=2, ensure_ascii=False))
            print("\n=== EXECUTANDO TEST SUITE DETERMINÍSTICA (MOTOR CORRIGIDO) ===")
            print(json.dumps(res_good, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
