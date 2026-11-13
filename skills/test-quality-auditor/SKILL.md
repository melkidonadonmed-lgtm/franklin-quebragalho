---
name: test-quality-auditor
description: "Audita suítes de testes em 5 módulos (Python, TS, Go, MCP e Harness) detectando Green Build Illusion e falhas AAA. Use para auditar suítes de testes e gerar grading.json; não use para código de produção."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "1.3.0"
  updated_at: "2026-11-13"
  author: "Melki"
  category: "Auditoria de Qualidade de Testes e Engenharia de Evals"
  tags: ["test-quality", "ast-auditor", "go-testing", "mcp-testing", "harness-testing", "mirrored-evals", "aaa-pattern", "mutation-score", "evals", "grading-json", "benchmark-json"]
---
# `test-quality-auditor` — Auditor Determinístico de Testes & Evals (`v1.3.0`)

Motor modular (`<300` linhas/módulo) com espelhamento 1:1 em `evals/modules/*_evals.json` para **5 domínios**: Python (`python_ast_auditor.py`), TS/JS (`ts_js_auditor.py`), Go (`go_test_auditor.py`), MCP/JSON-RPC 2.0 (`mcp_test_auditor.py` alinhado à skill `agent-server-auditor`) e Harness/Evals (`harness_test_auditor.py` + `perfkit_stats.py`). Detalhes dos 7 módulos e Níveis 1–4 constam em [`references/test_quality_7_modulos_espectro.md`](references/test_quality_7_modulos_espectro.md) e nos guias em `references/`.

## 1. Gatilhos de Ativação (Quando Usar)

- Auditar eficácia, padrão AAA e Níveis 1–4 em testes `test_*.py`, `*.test.ts`, `*_test.go`, `test_server.py` e `test_harness_quality.py`.
- Detectar *Green Build Illusion* (`assert True`, erro descartado `_` em Go, `t.Fatal` em goroutine, handshake MCP incompleto ou falta de `pytest.raises(SecurityViolationError)`).
- Rodar módulos espelhados em `evals/modules/*_evals.json` emitindo `grading.json` e `benchmark.json`.

## 2. Limites, Exceções e Esteira de 3 Portões

- **Portões:** Portão 1 (`code-acceptability-auditor` para produção Python AST), **Portão 2 (`test-quality-auditor` — exige Nível 4 `81–100 pts`)**, Portão 3 (`gap-analyzer-auditor` para RCA e `/speckit-converge`).
- **Não Use Para:** Auditoria de Física 3D/WebGL (`code-quality-audit-3d-physics`), build/deploy Cloud Run ou limpeza local/Drive (`manutencao-disco-windows`, `gdrive-auditoria-limpeza`).
- **Regra Crítica:** Nunca aprove uma suíte apenas por cobertura de linhas ou `Exit Code 0` sem checar densidade e rigor adversarial das asserções.

## 3. Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Arquivo/diretório de testes (`tests/`, `go_agent/`) ou manifesto `evals/evals.json`.
- **`domain` (opcional):** `auto` (padrão) | `python` | `ts` | `go` | `mcp` | `harness`.
- **`eval_module` (opcional):** `all` (padrão) | `python` | `ts_js` | `go` | `mcp` | `harness`.

## 4. Processamento nos 7 Módulos & Comandos CLI

```powershell
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py <caminho_alvo> --domain go --markdown
uv run python skills/test-quality-auditor/scripts/test_quality_auditor.py --run-evals --eval-module harness
```

1. **Varredura Modular:** Execute `test_quality_auditor.py` (aciona os 5 auditores + `perfkit_stats.py` para $P_{50}..P_{99.9}$, `stddev` `ddof=1`, `geomean`).
2. **Análise dos 7 Módulos:** (1) Problemática, (2) Montagem AAA, (3) Falha Tautológica, (4) Fatores de Persistência, (5) Espectro Níveis 1–4 (`0–100`), (6) Correção Cirúrgica para Nível 4 + reexecução (`pytest`/`go test`/`node --test`), (7) Evals via [`scripts/eval_harness.py`](scripts/eval_harness.py).

## 5. Saídas e Entregáveis ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md))

1. **Dossiê Executivo nos 7 Módulos** + tabela por teste (Níveis 1–4), refatoração Antes vs. Depois e `grading.json` / `benchmark.json`.
2. **Veredito Determinístico** (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) + links `file:///` clicáveis para arquivos auditados e corrigidos.
