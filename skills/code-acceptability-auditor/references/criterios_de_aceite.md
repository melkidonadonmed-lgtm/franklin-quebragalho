# 📋 Critérios Institucionais de Aceite de Código Python (`code-acceptability-auditor` v1.1.0)

Este documento detalha os critérios técnicos obrigatórios para aprovação de scripts e módulos Python antes de qualquer `git commit`, *Pull Request* ou publicação em produção.

---

## 1. Tabela de Regras e Penalidades Determinísticas (12 Regras)

| Regra ID | Categoria | Severidade | Penalidade | Condição de Disparo | Remediação Exigida |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **`SYN001`** | Sintaxe | `CRÍTICO` | `-25.0` | Falha no `ast.parse()` por erro sintático. | Corrigir a sintaxe antes de submeter o arquivo. |
| **`SEC001`** | Segurança | `CRÍTICO` | `-25.0` | Uso de `eval()` ou `exec()` na árvore AST. | Usar `ast.literal_eval()` ou deserialização tipada (Pydantic). |
| **`SEC002`** | Segurança | `CRÍTICO` | `-25.0` | Uso de `subprocess.*(..., shell=True)` ou `os.system()`. | Passar lista de argumentos com `shell=False`. |
| **`SEC003`** | Segurança | `CRÍTICO` | `-25.0` | Segredo, senha, chave de API ou token JWT hardcodeado. | Carregar de variáveis de ambiente (`os.getenv` / `.env`). |
| **`ERR001`** | Erros | `ALTO` | `-10.0` | Cláusula `except:` nua sem especificar classe de erro. | Capturar exceção específica (ex.: `except ValueError:`). |
| **`ERR002`** | Erros | `MÉDIO` | `-5.0` | Captura excessivamente ampla (`except Exception:`). | Restringir à exceção esperada ou relançar após log. |
| **`ERR003`** | Erros | `CRÍTICO` | `-25.0` | Bloco `except` silenciado com `pass`, `...` ou `continue`. | Registrar erro com `logging` ou relançar a exceção. |
| **`TYP001`** | Tipagem | `MÉDIO` | `-5.0` | Parâmetro de função sem *Type Hint* (exceto `self`/`cls`). | Anotar todos os parâmetros da assinatura. |
| **`TYP002`** | Tipagem | `MÉDIO` | `-5.0` | Função ou método (exceto `__init__`) sem retorno `-> Type`. | Declarar explicitamente o tipo de retorno. |
| **`ARCH001`** | Arquitetura | `BAIXO` | `-2.0` | Função/método com mais de `60` linhas (`end_lineno - lineno + 1 > 60`). | Extrair funções auxiliares coesas (SRP). |
| **`ARCH002`** | Complexidade Cognitiva | `MÉDIO` | `-5.0` | Aninhamento de controle (`if/for/while`) `> 3` níveis (tratando `elif` no mesmo nível). | Aplicar *Early Return* (*Guard Clauses*) ou extrair subfunções. |
| **`ARCH003`** | Complexidade Ciclomática | `MÉDIO` | `-5.0` | Complexidade ciclomática McCabe $M = E - N + 2P > 10$. | Reduzir ramificações ($M \le 10$) via despacho por dicionário ou subfunções. |

---

## 2. Fórmula do Quality Score e Portão de Aprovação

$$\text{Quality Score} = \max\left(0.0, 100.0 - \sum_{i=1}^{n} \text{Penalidade}_i\right)$$

Um artefato Python recebe o veredito **`APPROVED`** se, e somente se:
1. `passed_syntax is True`
2. `critical_violations == 0`
3. `quality_score >= 75.0`
