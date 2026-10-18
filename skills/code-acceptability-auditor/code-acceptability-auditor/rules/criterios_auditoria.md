# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`code-acceptability-auditor` v1.0.0)

Toda auditoria executada por esta skill deve emitir marcadores determinísticos baseados em evidências reais extraídas da Árvore Sintática Abstrata (AST) do Python e de padrões léxicos de segurança:
- `[PASS]`: Requisito sintático, de segurança, tratamento de erros, tipagem e modularidade comprovado sem violações bloqueantes.
- `[FAIL]`: Violação confirmada pelo analisador AST/Regex com apontamento exato de `arquivo:linha`, `rule_id` e penalidade aplicada.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência do arquivo alvo no disco ou caminho inválido.

---

### Regra 1: Integridade Sintática da Árvore AST (`SYN001`)
- **Critério**: O arquivo Python deve ser parseável por `ast.parse()` sem levantar `SyntaxError`.
- **Verificação Determinística**:
  - Falha no `ast.parse()` com `SyntaxError` -> `[FAIL: SYN001]` (Severidade: `CRÍTICO` | Penalidade: `-25.0` | `passed_syntax = False` | Rejeição imediata `REJECTED`).
  - Árvore AST construída com sucesso -> `[PASS]`.

### Regra 2: Proibição de Execução Dinâmica Arbitrária (`SEC001`)
- **Critério**: Nenhum módulo deve invocar `eval()` ou `exec()` sobre strings ou expressões dinâmicas.
- **Verificação Determinística**:
  - Nó `ast.Call` cujo `func` é `Name(id="eval")` ou `Name(id="exec")` (ou `builtins.eval`/`builtins.exec`) -> `[FAIL: SEC001]` (Severidade: `CRÍTICO` | Penalidade: `-25.0` | `REJECTED`).
  - Ausência de chamadas `eval`/`exec` (ou uso seguro de `ast.literal_eval`) -> `[PASS]`.

### Regra 3: Proibição de Subprocessos com `shell=True` (`SEC002`)
- **Critério**: Chamadas a `subprocess.run`, `subprocess.Popen`, `subprocess.call`, `subprocess.check_call`, `subprocess.check_output` ou `os.system` não devem habilitar `shell=True`.
- **Verificação Determinística**:
  - Nó `ast.Call` de `subprocess.*` com keyword `shell=Constant(value=True)` ou chamada direta a `os.system(...)` -> `[FAIL: SEC002]` (Severidade: `CRÍTICO` | Penalidade: `-25.0` | `REJECTED`).
  - Execução de subprocessos com argumentos em lista e `shell=False` (ou omitido) -> `[PASS]`.

### Regra 4: Proteção Contra Credenciais e Segredos Hardcodeados (`SEC003`)
- **Critério**: Nenhuma variável, constante ou chave de dicionário associada a segredos (`api_key`, `secret`, `password`, `passwd`, `token`, `private_key`, `access_key`, `jwt`) ou padrões de token (`sk-...`, `ghp_...`, `AIza...`, `Bearer eyJ...`) deve ter valor literal não-vazio hardcodeado no código-fonte.
- **Verificação Determinística**:
  - Atribuição literal de segredo ou match de padrão de chave de API em código ativo -> `[FAIL: SEC003]` (Severidade: `CRÍTICO` | Penalidade: `-25.0` | `REJECTED`).
  - Leitura via `os.getenv(...)`, `os.environ[...]`, `pydantic_settings` ou placeholders de documentação -> `[PASS]`.

### Regra 5: Proibição de Exceções Silenciadas ou Genéricas (`ERR001`, `ERR002`, `ERR003`)
- **Critério**: Blocos `except` devem declarar classes de exceção específicas e nunca engolir falhas silenciosamente com `pass`, `...` ou `continue`.
- **Verificação Determinística**:
  - Bloco `ast.ExceptHandler` cujo corpo efetivo (ignorando docstrings) contém apenas `ast.Pass`, `ast.Continue` ou `ast.Constant(value=Ellipsis)` -> `[FAIL: ERR003]` (Severidade: `CRÍTICO` | Penalidade: `-25.0` | `REJECTED`).
  - Bloco `ast.ExceptHandler` com `type is None` (`except:` nu) -> `[FAIL: ERR001]` (Severidade: `ALTO` | Penalidade: `-10.0`).
  - Bloco `ast.ExceptHandler` capturando `Exception` ou `BaseException` genérico -> `[FAIL: ERR002]` (Severidade: `MÉDIO` | Penalidade: `-5.0`).
  - Tratamento explícito com exceções específicas e ação corretiva/logging/raise -> `[PASS]`.

### Regra 6: Tipagem Explícita em Assinaturas de Funções (`TYP001`, `TYP002`)
- **Critério**: Todas as funções e métodos (`FunctionDef` e `AsyncFunctionDef`) devem possuir anotações de tipo nos parâmetros (exceto `self` e `cls`) e anotação de tipo de retorno (`-> Type`).
- **Verificação Determinística**:
  - Argumento (exceto `self`/`cls`) com `arg.annotation is None` -> `[FAIL: TYP001]` (Severidade: `MÉDIO` | Penalidade: `-5.0`).
  - Função/método (exceto `__init__`) com `node.returns is None` -> `[FAIL: TYP002]` (Severidade: `MÉDIO` | Penalidade: `-5.0`).
  - Assinatura 100% anotada com Type Hints -> `[PASS]`.

### Regra 7: Modularidade e Limite de Linhas por Função (`ARCH001`)
- **Critério**: Funções e métodos devem respeitar o Princípio da Responsabilidade Única (SRP), não excedendo `60` linhas de código (`end_lineno - lineno + 1 <= 60`).
- **Verificação Determinística**:
  - Função com extensão `> 60` linhas -> `[FAIL: ARCH001]` (Severidade: `BAIXO` | Penalidade: `-2.0`).
  - Todas as funções com `<= 60` linhas -> `[PASS]`.

### Regra 8: Portão Final de Qualidade (`Quality Gate`)
- **Critério**: O arquivo só é aprovado (`APPROVED`) se obtiver simultaneamente `passed_syntax == True`, `critical_violations == 0` e `quality_score >= 75.0`.
- **Verificação Determinística**:
  - `not passed_syntax` ou `critical_violations > 0` ou `quality_score < 75.0` -> `[FAIL: QUALITY_GATE_REJECTED]`.
  - Todos os 3 critérios atendidos -> `[PASS]`.
