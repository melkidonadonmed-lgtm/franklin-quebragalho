#!/usr/bin/env python3
"""
validate_skills.py
Validador determinístico de integridade estrutural, contratual e semântica
do catálogo de skills do Franklin Quebra-Galho (Padrão 2026).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Blindagem de codificação para consoles Windows (PowerShell/CMD)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.tools.frontmatter_parser import parse_frontmatter


def validate_skill_dir(skill_dir: Path) -> List[str]:
    """Valida uma pasta de skill individual."""
    errors = []
    skill_file = skill_dir / "SKILL.md"

    if not skill_file.exists():
        return [f"[FAIL] Arquivo SKILL.md inexistente em {skill_dir.name}"]

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"[FAIL] Erro ao ler SKILL.md: {e}"]

    meta, body = parse_frontmatter(content)
    if not meta:
        errors.append("[FAIL] Frontmatter YAML ausente ou malformado")

    # Checagem de campos vitais
    for req in ["name", "description", "version"]:
        if req not in meta or not meta[req]:
            errors.append(f"[FAIL] Campo obrigatório '{req}' ausente no frontmatter")

    if "name" in meta and meta["name"] != skill_dir.name:
        # Se for _template, permitir template-skill
        if not (skill_dir.name == "_template" and meta["name"] == "template-skill"):
            errors.append(f"[FAIL] Nome no frontmatter ('{meta['name']}') difere da pasta ('{skill_dir.name}')")

    if "description" in meta:
        desc = meta["description"]
        if len(desc) > 1024:
            errors.append(f"[FAIL] Descrição excede 1024 caracteres ({len(desc)} chars)")
        if len(desc) < 30:
            errors.append(f"[FAIL] Descrição muito curta ou rasa ({len(desc)} chars)")

    # Checagem de seções essenciais no corpo (aceitando sinônimos naturais sem engessar)
    required_sections = [
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

    for sec_pattern, sec_name in required_sections:
        if not re.search(sec_pattern, body, re.IGNORECASE):
            errors.append(f"[FAIL] Seção essencial ausente: {sec_name}")

    # Checagem de evals/evals.json se existir (aceita lista direta [...] ou objeto {"evals": [...]})
    evals_file = skill_dir / "evals" / "evals.json"
    if evals_file.exists():
        try:
            evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
            if isinstance(evals_data, dict) and "evals" in evals_data:
                evals_list = evals_data["evals"]
            elif isinstance(evals_data, list):
                evals_list = evals_data
            else:
                evals_list = []

            if not isinstance(evals_list, list) or len(evals_list) == 0:
                errors.append("[FAIL] evals.json deve conter uma lista não-vazia de testes")
            else:
                for idx, tc in enumerate(evals_list):
                    if not isinstance(tc, dict) or ("eval_id" not in tc and "id" not in tc):
                        errors.append(f"[FAIL] Test case #{idx} em evals.json requer 'eval_id' (ou 'id')")
        except Exception as e:
            errors.append(f"[FAIL] Erro de sintaxe JSON em evals/evals.json: {e}")

    # Checagem de rules/criterios_auditoria.md se existir
    rules_file = skill_dir / "rules" / "criterios_auditoria.md"
    if rules_file.exists():
        rules_text = rules_file.read_text(encoding="utf-8")
        if "[PASS]" not in rules_text or ("[FAIL]" not in rules_text and "[FAIL:" not in rules_text):
            errors.append("[FAIL] rules/criterios_auditoria.md deve conter marcadores determinísticos [PASS] e [FAIL]")

    # Checagem de referências JSON se existirem
    ref_dir = skill_dir / "references"
    if ref_dir.exists() and ref_dir.is_dir():
        for json_ref in ref_dir.glob("*.json"):
            try:
                json.loads(json_ref.read_text(encoding="utf-8"))
            except Exception as e:
                errors.append(f"[FAIL] Erro no JSON de referência {json_ref.name}: {e}")

    return errors


def main() -> int:
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

    if args.targets:
        targets = [t.strip() for t in args.targets.split(",")]
        skill_dirs = [agents_skills / t for t in targets if (agents_skills / t).is_dir()]
    else:
        skill_dirs = sorted([d for d in agents_skills.iterdir() if d.is_dir()])

    total_skills = 0
    passed_skills = 0
    failures: Dict[str, List[str]] = {}

    for s_dir in skill_dirs:
        total_skills += 1
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
    print(f"Resultado Consolidado: {passed_skills}/{total_skills} skills aprovadas.")

    if failures:
        print(f"Status Final: REPROVADO ({len(failures)} skills com inconformidade)")
        return 1

    print("Status Final: APROVADO COM 100% DE CONFORMIDADE DETERMINISTICA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
