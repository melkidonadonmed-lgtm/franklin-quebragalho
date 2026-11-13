# Matriz das 12 Regras AST e Modos CLI — Code Acceptability Auditor

Referência completa de penalidades e comandos usada por [`../SKILL.md`](../SKILL.md), complementando [`criterios_de_aceite.md`](criterios_de_aceite.md) e [`security_rules_spec.md`](security_rules_spec.md).

## Matriz das 12 Regras AST

| Regra ID | Categoria | Severidade | Penalidade | Descrição do Problema | Ação / Recomendação |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`SEC001`** | Segurança | **CRÍTICO** | `-25.0` | Chamada para `eval()` ou `exec()`. | Usar `ast.literal_eval` ou parsing estruturado. |
| **`SEC002`** | Segurança | **CRÍTICO** | `-25.0` | Subprocesso com `shell=True`. | Definir `shell=False` e passar lista de args. |
| **`SEC003`** | Segurança | **CRÍTICO** | `-25.0` | Suspeita de chave/JWT/senha hardcoded. | Mover credenciais para `.env`/ambiente. |
| **`SYN001`** | Sintaxe | **CRÍTICO** | `-25.0` | Erro de sintaxe Python (*SyntaxError*). | Corrigir a sintaxe antes de executar. |
| **`ERR001`** | Tratamento de Erros | **ALTO** | `-10.0` | Captura genérica (`except:` nu). | Especificar exceção exata (`except ValueError:`). |
| **`ERR002`** | Tratamento de Erros | **MÉDIO** | `-5.0` | Captura ampla (`except Exception:`/`BaseException`). | Restringir à classe específica do domínio. |
| **`ERR003`** | Tratamento de Erros | **CRÍTICO** | `-25.0` | Exceção silenciada com `pass`, `...` ou `continue`. | Logar, tratar explicitamente ou usar `raise`. |
| **`TYP001`** | Tipagem | **MÉDIO** | `-5.0` | Parâmetro sem Type Hint (`self`/`cls` isentos). | Adicionar anotações de tipo nos argumentos. |
| **`TYP002`** | Tipagem | **MÉDIO** | `-5.0` | Função sem retorno anotado (`__init__` isento). | Declarar `-> Type` explicitamente. |
| **`ARCH001`** | Arquitetura | **BAIXO** | `-2.0` | Função muito longa (`> 60` linhas). | Dividir responsabilidades (SRP). |
| **`ARCH002`** | Complexidade Cognitiva | **MÉDIO** | `-5.0` | Aninhamento `> 3` níveis. | Usar *Early Return* / subfunções. |
| **`ARCH003`** | Complexidade Ciclomática | **MÉDIO** | `-5.0` | McCabe $M = E - N + 2P > 10$. | Reduzir ramificações ($M \le 10$) via despacho/helpers. |

## Modos de Execução CLI (`pwsh`)

```powershell
# 1. Auditar arquivo único
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --file caminho/do/arquivo.py

# 2. Auditar diretório em JSON
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared --json

# 3. Auto-teste determinístico
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --self-test

# 4. Trigger Evals (F1 = 1.0)
uv run python skills/code-acceptability-auditor/scripts/trigger_eval_runner.py

# 5. Benchmark A vs B / Failure Auditor
uv run python skills/code-acceptability-auditor/scripts/skill_failure_auditor.py

# 6. Instalar hook .git/hooks/pre-commit
uv run python skills/code-acceptability-auditor/scripts/install_pre_commit_hook.py --repo-root .

# 7. Portão Combinado (AST + Pytest)
uv run python skills/code-acceptability-auditor/scripts/code_acceptability_auditor.py --dir shared; uv run pytest -q
```
