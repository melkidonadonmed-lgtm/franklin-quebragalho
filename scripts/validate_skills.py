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


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extrai frontmatter YAML (com suporte a metadata aninhado) e corpo do documento."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    raw_yaml, body = match.group(1), match.group(2)
    meta: Dict[str, Any] = {}

    try:
        import yaml
        parsed = yaml.safe_load(raw_yaml)
        if isinstance(parsed, dict):
            meta = parsed
            if "metadata" in meta and isinstance(meta["metadata"], dict):
                for k, v in meta["metadata"].items():
                    if k not in meta:
                        meta[k] = v
            return meta, body
    except ImportError:
        pass

    # Parser determinístico fallback sem dependências
    current_key = None
    multiline_val: List[str] = []
    in_metadata = False
    metadata_dict: Dict[str, Any] = {}

    for line in raw_yaml.splitlines():
        if re.match(r"^\s+", line) and current_key:
            multiline_val.append(line.strip())
            continue

        if current_key and multiline_val:
            val_joined = " ".join(multiline_val)
            if in_metadata:
                metadata_dict[current_key] = val_joined
            else:
                meta[current_key] = val_joined
            multiline_val = []
            current_key = None

        if re.match(r"^metadata:\s*$", line):
            in_metadata = True
            continue

        if in_metadata and re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line):
            m = re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip().strip("'\"")
                if v in (">-", ">", "|", "|-"):
                    current_key = k
                    multiline_val = []
                else:
                    metadata_dict[k] = v
            continue

        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            in_metadata = False
            key, val = kv_match.group(1), kv_match.group(2).strip()
            if val in (">-", ">", "|", "|-"):
                current_key = key
                multiline_val = []
            else:
                val = val.strip("'\"")
                meta[key] = val
                current_key = None

    if current_key and multiline_val:
        val_joined = " ".join(multiline_val)
        if in_metadata:
            metadata_dict[current_key] = val_joined
        else:
            meta[current_key] = val_joined

    if metadata_dict:
        meta["metadata"] = metadata_dict
        for k, v in metadata_dict.items():
            if k not in meta:
                meta[k] = v

    return meta, body


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

    # Checagem de seções essenciais no corpo
    required_sections = [
        (r"(#|##)\s+.*(Gatilhos|Quando Usar|Propósito|Proposito|Missão|Missao)", "Gatilhos / Quando Usar"),
        (r"(#|##)\s+.*(Entradas|Pr[eé]-requisitos|Par[aâ]metros)", "Entradas / Pré-requisitos"),
        (r"(#|##)\s+.*(Processamento|Passo a Passo|Fluxo|Execução|Execucao)", "Processamento / Fluxo"),
        (r"(#|##)\s+.*(Saídas|Saidas|Entregáveis|Entregaveis|Modelo de Saída|Modelo de Saida)", "Saídas / Entregáveis"),
        (r"(#|##)\s+.*(Exceções|Excecoes|Limites|Quando N[AÃ]O Usar)", "Exceções / Limites"),
    ]

    for sec_pattern, sec_name in required_sections:
        if not re.search(sec_pattern, body, re.IGNORECASE):
            errors.append(f"[FAIL] Seção obrigatória ausente: {sec_name}")

    # Checagem de evals/evals.json se existir
    evals_file = skill_dir / "evals" / "evals.json"
    if evals_file.exists():
        try:
            evals_data = json.loads(evals_file.read_text(encoding="utf-8"))
            if not isinstance(evals_data, list) or len(evals_data) == 0:
                errors.append("[FAIL] evals.json deve ser uma lista não-vazia de testes")
            else:
                for idx, tc in enumerate(evals_data):
                    if not isinstance(tc, dict) or "eval_id" not in tc or "expected_behavior" not in tc:
                        errors.append(f"[FAIL] Test case #{idx} em evals.json malformado (requer eval_id e expected_behavior)")
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
    agents_skills = root_path / ".agents" / "skills"

    if not agents_skills.exists():
        print(f"[ERROR] Diretório .agents/skills não encontrado em {agents_skills}")
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
