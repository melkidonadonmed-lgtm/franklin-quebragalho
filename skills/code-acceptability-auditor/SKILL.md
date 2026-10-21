---
name: code-acceptability-auditor
description: >-
  Audita estaticamente arquivos Python via AST contra falhas de segurança (segredos hardcoded, eval/exec, shell=True), ausência de type hints, except silencioso e funções longas (>60 linhas). Use antes de commits/PRs para calcular o Quality Score (0-100) e validar critérios de aceite.
license: MIT
compatibility: Python 3.11+, Pydantic 2.x, Git
metadata:
  author: "Gemini Notebook AI Engineering & Melki"
  version: "1.1.0"
  category: "Auditoria e Qualidade de Código"
  updated_at: "2026-10-21"
  tags:
    - "ast"
    - "python-audit"
    - "security"
    - "type-hints"
    - "pre-commit"
    - "quality-gate"
    - "cyclomatic-complexity"
version: 1.1.0
updated_at: 2026-10-21
author: Gemini Notebook AI Engineering & Melki
category: Auditoria e Qualidade de Código
---

# 🛡️ Code Acceptability Auditor (`code-acceptability-auditor` v1.1.0)

## 1. Visão Geral e Objetivo
Esta Skill fornece um procedimento automatizado e determinístico para auditoria estática de código-fonte Python. Ela mapeia o código utilizando o analisador **AST** (*Abstract Syntax Tree*) e valida se os artefatos atendem aos **critérios de aceite institucionais**, prevenindo o vazamento de credenciais, falhas de tipagem e exceções silenciadas sem necessidade de executar scripts não confiáveis.

---

## 2. Quando Usar (Gatilhos de Ativação)

### ✅ Gatilhos Positivos (Quando usar)
- O usuário ou agente pede para "auditar", "verificar a qualidade" ou "validar o código" de scripts ou módulos Python.
- Antes de realizar `git commit` ou criar um *Pull Request* (PR) na esteira CI/CD para checar critérios de aceite.
- Após a criação ou refatoração de novos scripts Python, garantindo zero regressões de tipagem, segurança e modularidade.
- Para verificar a presença de chaves secretas, tokens de API hardcodeados, chamadas `eval()`/`exec()` ou `subprocess` com `shell=True`.

### ❌ Quando NÃO Usar e Fronteira da Esteira de 3 Portões (`2026-10-21`)
- **Fronteira na Esteira de Qualidade e Convergência (3 Portões)**:
  1. **Portão 1 — Código de Produção (`code-acceptability-auditor` `v1.1.0` — Esta Skill)**: Audita estaticamente módulos e scripts Python via AST/Pydantic (`12` regras: `SEC001..003`, `SYN001`, `ERR001..003`, `TYP001..002`, `ARCH001..003`, `Score >= 75.0`).
  2. **Portão 2 — Suítes de Testes & Evals (`test-quality-auditor` `v1.2.0`)**: Para auditar qualidade, falsificabilidade AAA e determinismo de suítes de testes (`pytest`, `vitest`, `*_test.go`, `MCP JSON-RPC` e `Harness`), delegue para `test-quality-auditor`.
  3. **Portão 3 — RCA & Convergência Spec-to-Code (`gap-analyzer-auditor` `v2.1.0`)**: Para análise de causa-raiz em falhas de runtime, violações reportadas pelos Portões 1/2 ou convergência `SPEC.md`/`tasks.md` (`/speckit-converge`), delegue para `gap-analyzer-auditor`.
- **Não usar** para explicar conceitos teóricos de Python (ex: como funciona `try/except` ou diferenças entre Python e TypeScript).
- **Não usar** para criar scripts do zero ou refatorar algoritmos sem pedido de auditoria de aceite.
- **Não usar** para auditoria matemática de motores de Física 3D/WebGL — delegue para `code-quality-audit-3d-physics`.

---

## 3. Entradas e Pré-requisitos
- **Alvo da Auditoria**: Caminho de um arquivo Python (`--file caminho/arquivo.py`) ou diretório de projeto (`--dir caminho/projeto`).
- **Parâmetros de Portão (Quality Gate)**:
  - `min_quality_score`: Pontuação mínima exigida (padrão: `75.0`).
  - `max_critical_violations`: Limite máximo de violações críticas toleradas (padrão: `0`).
- **Ambiente**: Python `3.11+` com `pydantic>=2.0`.

---

## 4. Processamento, Fluxo de Execução e Matriz de Regras

### 4.1. Matriz de Regras de Auditoria e Severidade

| Regra ID | Categoria | Severidade | Penalidade | Descrição do Problema | Ação / Recomendação |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`SEC001`** | Segurança | **CRÍTICO** | `-25.0` | Chamada para funções perigosas `eval()` ou `exec()`. | Substituir por `ast.literal_eval` ou parsing estruturado. |
| **`SEC002`** | Segurança | **CRÍTICO** | `-25.0` | Subprocesso executado com `shell=True`. | Definir `shell=False` e passar argumentos em lista. |
| **`SEC003`** | Segurança | **CRÍTICO** | `-25.0` | Suspeita de chave secreta, token JWT ou senha hardcodeada. | Mover credenciais para variáveis de ambiente (`.env`). |
| **`SYN001`** | Sintaxe | **CRÍTICO** | `-25.0` | Erro de sintaxe Python (*SyntaxError*). | Corrigir a sintaxe antes de qualquer execução. |
| **`ERR001`** | Tratamento de Erros | **ALTO** | `-10.0` | Captura de exceção genérica (`except:` sem classe). | Especificar a exceção exata (ex: `except ValueError:`). |
| **`ERR002`** | Tratamento de Erros | **MÉDIO** | `-5.0` | Captura ampla (`except Exception:` ou `BaseException`). | Restringir à classe de erro específica do domínio. |
| **`ERR003`** | Tratamento de Erros | **CRÍTICO** | `-25.0` | Exceção ignorada silenciosamente com `pass`, `...` ou `continue`. | Adicionar log estruturado, tratamento explícito ou `raise`. |
| **`TYP001`** | Tipagem | **MÉDIO** | `-5.0` | Parâmetro de função sem anotação de tipo (*Type Hint*). | Adicionar anotações de tipo explícitas nos argumentos. |
| **`TYP002`** | Tipagem | **MÉDIO** | `-5.0` | Função sem indicação do tipo de retorno (`-> Type`). | Declarar o tipo de retorno explicitamente na assinatura. |
| **`ARCH001`** | Arquitetura | **BAIXO** | `-2.0` | Função muito longa (`> 60` linhas de código). | Refatorar dividindo responsabilidades (Princípio SRP). |
| **`ARCH002`** | Complexidade Cognitiva | **MÉDIO** | `-5.0` | Aninhamento de controle (`if/for/while`) `> 3` níveis. | Aplicar *Early Return* (*Guard Clauses*) ou extrair subfunções. |
| **`ARCH003`** | Complexidade Ciclomática | **MÉDIO** | `-5.0` | Complexidade ciclomática McCabe $M = E - N + 2P > 10$. | Reduzir ramificações ($M \le 10$) com despacho por dicionário ou helpers. |

### 4.2. Algoritmo de Avaliação e Quality Gate
A pontuação de qualidade (**Quality Score**) é calculada deterministicamente a partir de um valor base de **100.0**, subtraindo penalidades acumuladas:

$$\text{Quality Score} = \max\left(0.0, 100.0 - \sum \text{Penalidades}\right)$$

**Critério de Aprovação (`APPROVED`)**:
1. **Zero Violações Críticas**: Nenhuma violação com severidade `CRÍTICO` (`critical_count == 0`).
2. **Quality Score Mínimo**: Pontuação global $\ge 75.0 / 100.0$.
3. **Validação Sintática**: `passed_syntax == True`.

Caso qualquer condição falhe, o arquivo recebe status **`REJECTED`** e o pré-commit/PR é bloqueado.

### 4.3. Modos de Execução (`pwsh`)
```powershell
# 1. Auditar um arquivo específico via CLI
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file caminho/do/arquivo.py

# 2. Auditar um diretório inteiro em formato JSON
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared --json

# 3. Executar auto-teste determinístico (Self-Test)
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --self-test

# 4. Executar suíte de Trigger Evals (20 queries: treino + validação, F1 = 1.0)
uv run python skills/code-acceptability-auditor/scripts/trigger_eval_runner.py

# 5. Executar auditoria de modos de falha e benchmark A vs B
uv run python skills/code-acceptability-auditor/scripts/skill_failure_auditor.py

# 6. Instalar Git Hook local (.git/hooks/pre-commit)
uv run python skills/code-acceptability-auditor/scripts/install_pre_commit_hook.py --repo-root .
```

---

## 5. Saídas e Entregáveis Esperados
A execução retorna um relatório estruturado validado via Pydantic v2 (`FileAuditReport` / `DirectoryAuditSummary`) contendo:
- `status`: `"APPROVED"` ou `"REJECTED"`.
- `quality_score`: Nota numérica de `0.0` a `100.0`.
- `passed_syntax`: Booleano indicando integridade da árvore AST.
- `violations`: Lista detalhada com `rule_id`, `category`, `severity`, `penalty`, `line`, `symbol`, `message` e `recommendation`.
- `criterios_auditoria`: Marcadores determinísticos `[PASS]` ou `[FAIL: <RULE_ID>]`.

---

## 6. Estrutura de Arquivos da Skill

```text
code-acceptability-auditor/
├── SKILL.md                                   # Manifesto e instruções operacionais (Tiers 1 e 2)
├── rules/
│   └── criterios_auditoria.md                 # Regras determinísticas falsificáveis ([PASS]/[FAIL])
├── scripts/
│   ├── code_acceptability_auditor.py          # Motor AST + Regex com modelos Pydantic v2
│   ├── trigger_eval_runner.py                 # Runner e métricas da matriz de gatilhos (TRIG-01..20)
│   ├── skill_failure_auditor.py               # Auditor de falhas, fallbacks e delta Baseline vs Skill
│   ├── install_pre_commit_hook.py             # Instalador do Git Hook pre-commit
│   └── test_code_acceptability_auditor.py     # Suíte de testes unitários automatizados (pytest)
├── references/
│   ├── criterios_de_aceite.md                 # Tabela detalhada de critérios institucionais
│   ├── security_rules_spec.md                 # Especificação técnica das regras AST e Regex
│   ├── trigger_matrix_queries.json            # Dataset canônico TRIG-01..20 (train/validation)
│   └── trigger_eval_report_baseline.json      # Relatório consolidado de precisão/recall/F1 (100%)
├── evals/
│   └── evals.json                             # Casos funcionais + trigger_eval_queries para o Harness Go
└── assets/
    └── .github/workflows/ci.yml               # Workflow de CI/CD para GitHub Actions
```

---

## 7. Guardrails e Armadilhas Comuns (*Gotchas*)
- **`except:` vs `except Exception:`**: O analisador AST distingue `except:` nu (`ERR001`, severidade `ALTO`, `-10`) de `except Exception:` (`ERR002`, severidade `MÉDIO`, `-5`). Ambos se tornam `ERR003` (`CRÍTICO`, `-25`) se o bloco contiver apenas `pass`, `...` ou `continue`.
- **Falsos Positivos de Segredos (`SEC003`)**: A inspeção ignora leituras legítimas de variáveis de ambiente (`os.getenv`, `os.environ.get`), strings vazias e placeholders óbvios (`YOUR_API_KEY`, `<token>`, `changeme`, `example`).
- **Parâmetros de Instância/Classe**: Os argumentos `self` e `cls` são automaticamente isentos da exigência de Type Hints (`TYP001`), e métodos `__init__` sem anotação de retorno explícita ou anotados com `-> None` são tratados sem falsos positivos.
