#!/usr/bin/env python3
"""
validate_skills.py
Validador determinístico de integridade estrutural, contratual e semântica
do catálogo de skills do Franklin Quebra-Galho (Padrão 2026).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.tools.frontmatter_parser import parse_frontmatter

REQUIRED_SECTIONS: List[Tuple[str, str]] = [
    (
        r"(#|##)\s+.*(Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao|Visão Geral|Visao Geral|Objetivo)",
        "Gatilhos / Quando Usar / Objetivo",
    ),
    (
        r"(#|##)\s+.*(Entradas|Pr[eé]-requisitos|Par[aâ]metros|Contexto|Configura[cç][aã]o|Insumos)",
        "Entradas / Pré-requisitos",
    ),
    (
        r"(#|##)\s+.*(Processamento|Passo a Passo|Fluxo|Execução|Execucao|Arquitetura|M[oó]dulos|Como Funciona)",
        "Processamento / Fluxo / Arquitetura",
    ),
    (
        r"(#|##)\s+.*(Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida|Formato|Relat[oó]rio)",
        "Saídas / Entregáveis",
    ),
    (
        r"(#|##)\s+.*(Exceções|Excecoes|Limites|Quando N[AÃ]O Usar|Restri[cç][oõ]es|Guardrails)",
        "Exceções / Limites / Guardrails",
    ),
]


def _validate_frontmatter_fields(meta: Dict[str, Any], dir_name: str, errors: List[str]) -> None:
    """Valida os campos obrigatórios e limites de tamanho do frontmatter YAML."""
    if not meta:
        errors.append("[FAIL] Frontmatter YAML ausente ou malformado")
    for req in ("name", "description", "version"):
        if not meta.get(req):
            errors.append(f"[FAIL] Campo obrigatório '{req}' ausente no frontmatter")

    name_val = meta.get("name")
    is_template = dir_name == "_template" and name_val == "template-skill"
    if name_val and name_val != dir_name and not is_template:
        errors.append(f"[FAIL] Nome no frontmatter ('{name_val}') difere da pasta ('{dir_name}')")

    desc = str(meta.get("description", ""))
    if desc and len(desc) > 420:
        errors.append(f"[FAIL] Descrição excede o orçamento de contexto de 420 caracteres ({len(desc)} chars)")
    if desc and len(desc) < 30:
        errors.append(f"[FAIL] Descrição muito curta ou rasa ({len(desc)} chars)")


def _validate_evals_file(skill_dir: Path, errors: List[str]) -> None:
    """Valida a estrutura e sintaxe JSON de evals/evals.json quando presente."""
    evals_file = skill_dir / "evals" / "evals.json"
    if not evals_file.exists():
        return
    try:
        evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"[FAIL] Erro de sintaxe JSON em evals/evals.json: {exc}")
        return

    evals_list = (
        evals_data.get("evals", [])
        if isinstance(evals_data, dict)
        else (evals_data if isinstance(evals_data, list) else [])
    )
    if not isinstance(evals_list, list) or not evals_list:
        errors.append("[FAIL] evals.json deve conter uma lista não-vazia de testes")
        return

    for idx, tc in enumerate(evals_list):
        if not isinstance(tc, dict) or ("eval_id" not in tc and "id" not in tc):
            errors.append(f"[FAIL] Test case #{idx} em evals.json requer 'eval_id' (ou 'id')")


def _validate_rules_and_references(skill_dir: Path, errors: List[str]) -> None:
    """Valida marcadores determinísticos em rules/criterios_auditoria.md e JSONs em references/."""
    rules_file = skill_dir / "rules" / "criterios_auditoria.md"
    if rules_file.exists():
        rules_text = rules_file.read_text(encoding="utf-8")
        if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
            errors.append("[FAIL] rules/criterios_auditoria.md deve conter marcadores determinísticos [PASS] e [FAIL]")

    ref_dir = skill_dir / "references"
    if not ref_dir.is_dir():
        return
    for json_ref in ref_dir.glob("*.json"):
        try:
            json.loads(json_ref.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"[FAIL] Erro no JSON de referência {json_ref.name}: {exc}")


def validate_skill_dir(skill_dir: Path) -> List[str]:
    """Valida uma pasta de skill individual."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"[FAIL] Arquivo SKILL.md inexistente em {skill_dir.name}"]

    try:
        content = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"[FAIL] Erro ao ler SKILL.md: {exc}"]

    errors: List[str] = []
    meta, body = parse_frontmatter(content)
    _validate_frontmatter_fields(meta, skill_dir.name, errors)

    for sec_pattern, sec_name in REQUIRED_SECTIONS:
        if not re.search(sec_pattern, body, re.IGNORECASE):
            errors.append(f"[FAIL] Seção essencial ausente: {sec_name}")

    _validate_evals_file(skill_dir, errors)
    _validate_rules_and_references(skill_dir, errors)
    return errors


def _resolve_skill_dirs(agents_skills: Path, targets_arg: str | None) -> List[Path]:
    """Resolve a lista de diretórios de skills a inspecionar."""
    if not targets_arg:
        return sorted(d for d in agents_skills.iterdir() if d.is_dir())
    targets = [t.strip() for t in targets_arg.split(",") if t.strip()]
    return [agents_skills / t for t in targets if (agents_skills / t).is_dir()]


def main() -> int:
    """Ponto de entrada CLI do validador determinístico de skills."""
    parser = argparse.ArgumentParser(description="Validador determinístico de integridade de skills.")
    parser.add_argument("--targets", type=str, help="Nomes das skills separadas por vírgula para validação pontual.")
    args = parser.parse_args()

    root_path = Path(__file__).resolve().parent.parent
    agents_skills = root_path / "skills"
    if not agents_skills.exists():
        agents_skills = root_path / ".agents" / "skills"
    if not agents_skills.exists():
        print(f"[ERROR] Diretório skills não encontrado em {agents_skills}")
        return 1

    print("=== INICIANDO AUDITORIA DETERMINISTICA DE SKILLS ===")
    print(f"Diretório Raiz: {agents_skills}")
    print("-" * 65)

    skill_dirs = _resolve_skill_dirs(agents_skills, args.targets)
    passed_skills = 0
    failures: Dict[str, List[str]] = {}

    for s_dir in skill_dirs:
        errs = validate_skill_dir(s_dir)
        if errs:
            failures[s_dir.name] = errs
            print(f"[FAIL] {s_dir.name:<45}")
            for err in errs:
                print(f"   ↳ {err}")
        else:
            passed_skills += 1
            print(f"[PASS] {s_dir.name:<45}")

    print("-" * 65)
    print(f"Resultado Consolidado: {passed_skills}/{len(skill_dirs)} skills aprovadas.")
    if failures:
        print(f"Status Final: REPROVADO ({len(failures)} skills com inconformidade)")
        return 1

    print("Status Final: APROVADO COM 100% DE CONFORMIDADE DETERMINISTICA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
