# Google Style Guide Output & Authoring Standards (`google/styleguide`)

Canonical L3 reference distilled from `https://github.com/google/styleguide` and `https://google.github.io/styleguide/go` to ensure uniform, low-variance code and documentation output across the ecosystem.

---

## 1. Python (`pyguide.md` + `ruff` Google Convention)

1. **Docstrings (`[tool.ruff.lint.pydocstyle] convention = "google"`):**
   - Start every public module, class, and function with a 1-line imperative summary ending in a period, followed by a blank line and `Args:`, `Returns:`, and `Raises:` sections when applicable.
2. **Type Annotations & Strictness:**
   - Annotate all public function parameters and return types (`-> None`, `-> dict[str, Any]`).
   - Use Pydantic v2 `ConfigDict(extra="forbid")` on internal and RPC/MCP boundary models.
3. **Exceptions & Control Flow:**
   - Never use bare `except:` or silent `pass`; catch specific exception classes or use `contextlib.suppress(...)` when intentional.
   - Prefer early returns (`<= 3` nesting levels, `<= 60` lines per function).

---

## 2. TypeScript / JavaScript (`tsguide.html` & `jsguide.html`)

1. **Type Safety:**
   - Never use `any`; use `unknown` and narrow explicitly (`instanceof Error`, Zod `.strict()`).
   - Use `import type { ... }` (`verbatimModuleSyntax: true`) for type-only imports.
2. **Modules & Mutability:**
   - Use named exports; avoid `default` exports and TypeScript `namespace` / mutable `enum` (`erasableSyntaxOnly: true` in Node 26 ESM).
   - Default to `const`; use `let` only when reassignment is required, never `var`.

---

## 3. Go (`google.github.io/styleguide/go/decisions`)

1. **Naming & Packages:**
   - Package names are lowercase single words without underscores (`mcpserver`, `memorybridge`); avoid stutter (`memorybridge.Bridge`, not `memorybridge.MemoryBridge`).
   - MixedCaps (`camelCase` / `PascalCase`) for identifiers; initialisms keep uniform case (`URL`, `ID`, `HTTP`, `JSON`, `MCP`).
2. **Error Handling & Boundaries:**
   - Wrap errors with `%w` and actionable context (`fmt.Errorf("load config %s: %w", path, err)`).
   - Enforce `json.NewDecoder(r).DisallowUnknownFields()` at strict internal/RPC boundaries.

---

## 4. Shell (`shellguide.md`) & PowerShell (`pwsh`)

1. **When to Use Shell:**
   - Use Shell/PowerShell only for small utilities and wrapper orchestration (`<= 100` lines); once data structures or complex logic appear, write Python (`uv run`) or Go.
2. **Quoting & Error Safety:**
   - Always quote variable expansions (`"$var"`), validate exit codes, and avoid `eval` / `Invoke-Expression` on untrusted strings.

---

## 5. Markdown & Documentation (`docguide/style.md` & `best_practices.md`)

1. **Minimum Viable Documentation:**
   - Prefer concise, scannable tables and numbered steps over long narrative paragraphs.
   - Keep one blank line around headings, lists, tables, alerts, and fenced code blocks (*Blank-Line Law*).
   - Always declare language tags on fenced code blocks (`python`, `go`, `typescript`, `powershell`, `json`, `yaml`, `mermaid`).
