# 🔐 Especificação Técnica das Regras AST e Regex (`security_rules_spec.md`)

Especificação de engenharia para detecção determinística das regras `SEC001`, `SEC002`, `SEC003`, `ERR001`..`ERR003`, `TYP001`..`TYP002` e `ARCH001`.

---

## 1. Inspeção de Segurança (`SEC001` – `SEC003`)

### `SEC001` — Execução Dinâmica (`eval` / `exec`)
- **Nó AST**: `ast.Call`
- **Condição**: `isinstance(node.func, ast.Name)` com `node.func.id in {"eval", "exec"}` ou `isinstance(node.func, ast.Attribute)` com `node.func.attr in {"eval", "exec"}` quando o objeto base é `builtins`.
- **Exclusão Segura**: `ast.literal_eval` é permitido e não dispara alerta.

### `SEC002` — Injeção de Comando (`shell=True` / `os.system`)
- **Nó AST**: `ast.Call`
- **Condição A**: Chamada a `subprocess.{run, Popen, call, check_call, check_output}` contendo `ast.keyword(arg="shell", value=ast.Constant(value=True))`.
- **Condição B**: Chamada direta a `os.system(...)` ou `os.popen(...)`.

### `SEC003` — Vazamento de Credenciais e Chaves Secretas
- **Inspeção Híbrida (AST + Regex)**:
  1. **AST (`ast.Assign`, `ast.AnnAssign`, `ast.Dict`)**: Identificadores que casam com `(api[_-]?key|secret|password|passwd|pwd|access[_-]?token|auth[_-]?token|private[_-]?key|client[_-]?secret|jwt[_-]?secret)` atribuídos a constantes `str` não-vazias (`len >= 6`) que não sejam placeholders (`YOUR_...`, `<...>`, `changeme`, `dummy`, `example`, `none`, `null`, `todo`).
  2. **Regex de Assinatura de Tokens**: Detecta prefixos conhecidos em literais de string:
     - `sk-[A-Za-z0-9_-]{16,}` (OpenAI / API Secret Key)
     - `gh[pousr]_[A-Za-z0-9]{20,}` (GitHub Personal/Server Token)
     - `AIza[0-9A-Za-z_-]{20,}` (Google Cloud / Gemini API Key)
     - `AKIA[0-9A-Z]{16}` (AWS Access Key ID)
     - `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}` (JWT literal)

---

## 2. Inspeção de Tratamento de Exceções (`ERR001` – `ERR003`)

- **`ERR001` (`except:` nu)**: `isinstance(node, ast.ExceptHandler)` com `node.type is None`.
- **`ERR002` (`except Exception:`)**: `node.type` é `ast.Name(id="Exception" | "BaseException")` ou tupla contendo `Exception`/`BaseException`.
- **`ERR003` (Exceção Silenciada)**: O corpo `node.body` (descontando docstring literal inicial) contém exclusivamente nós `ast.Pass`, `ast.Continue` ou `ast.Expr(value=ast.Constant(value=Ellipsis))`.

---

## 3. Inspeção de Tipagem e Modularidade (`TYP001`, `TYP002`, `ARCH001`)

- **`TYP001`**: Verifica `args.posonlyargs`, `args.args`, `args.kwonlyargs`, `args.vararg` e `args.kwarg`. Ignora `self` e `cls`.
- **`TYP002`**: Verifica `node.returns is None` em `FunctionDef` e `AsyncFunctionDef`. Ignora `__init__` caso os argumentos já estejam tipados ou exige `-> None` quando configurado em modo estrito.
- **`ARCH001`**: Calcula `span = (node.end_lineno or node.lineno) - node.lineno + 1`. Dispara quando `span > 60`.
