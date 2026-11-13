---
name: code-acceptability-auditor
description: "Audita estaticamente arquivos Python via AST contra eval/exec, shell=True, ausência de type hints e funções longas >60 linhas. Use para calcular o Quality Score; não use para dúvidas teóricas."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "1.1.0"
  updated_at: "2026-11-13"
  author: "Gemini Notebook AI Engineering & Melki"
  category: "Auditoria e Qualidade de Código"
  tags: ["ast", "python-audit", "security", "type-hints", "pre-commit", "quality-gate", "cyclomatic-complexity"]
---

# Code Acceptability Auditor (`code-acceptability-auditor`)

## 1. Propósito e Gatilhos (Portão 1 da Esteira de Qualidade)

Audita estaticamente módulos/scripts Python via **AST** (*Abstract Syntax Tree*) contra segurança, tipagem, tratamento de erros e complexidade sem executar código não confiável:

- Validar arquivos/diretórios Python antes de `git commit` ou PR (`eval`/`exec`, `shell=True`, segredos, type hints, `<= 60` linhas, aninhamento `<= 3`, McCabe $M \le 10$).
- Calcular o **Quality Score** (`0.0` a `100.0`) exigindo aprovação (`Score >= 75.0`, zero críticos).

## 2. Entradas e Pré-requisitos

- **`--file` / `--dir` (obrigatório):** Arquivo Python ou diretório raiz sob auditoria.
- **`min_quality_score` (padrão `75.0`) e `max_critical_violations` (`0`).**
- **Ambiente:** Python `3.12+` + `pydantic>=2.0`.

## 3. Processamento, Regras e Quality Gate

Consulte a tabela das 12 regras (`SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`) e os 7 modos CLI em [`references/matriz_12_regras_e_cli.md`](references/matriz_12_regras_e_cli.md):

$$\text{Quality Score} = \max\left(0.0, 100.0 - \sum \text{Penalidades}\right)$$

- **Aprovação (`APPROVED`):** `critical_count == 0`, `quality_score >= 75.0` e `passed_syntax == True`; qualquer desvio gera `REJECTED`.

```powershell
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared --json
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --self-test
```

**Gotchas do Parser:** `except:` (`ERR001`, `-10`) difere de `except Exception:` (`ERR002`, `-5`), ambos viram `ERR003` (`-25`) com `pass`/`...`/`continue`; `SEC003` isenta `os.getenv`/`os.environ.get` e placeholders (`YOUR_API_KEY`); `self`/`cls` são isentos em `TYP001` e `__init__` em `TYP002`.

## 4. Saídas e Entregáveis

Relatório Pydantic (`FileAuditReport` / `DirectoryAuditSummary`, ver [`references/criterios_de_aceite.md`](references/criterios_de_aceite.md), [`references/security_rules_spec.md`](references/security_rules_spec.md) e [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)): `status`, `quality_score`, `passed_syntax`, `violations` e `[PASS]`/`[FAIL: <RULE_ID>]`.

## 5. Exceções, Limites e Quando NÃO Usar

- **Portão 2 (Testes & Evals):** Para `pytest`, `vitest`, `*_test.go`, MCP e Harness AAA, use `test-quality-auditor`.
- **Portão 3 (RCA & Convergência):** Para causa raiz em runtime e `/speckit-converge`, use `gap-analyzer-auditor`.
- **Teoria / Scaffolding / Física 3D:** Não use para dúvidas conceituais Python, criação do zero ou motores WebGL/3D (`code-quality-audit-3d-physics`).
