# Guia de Referência: Documentos-Chave, Contratos (`MCP`, `FastAPI`, `RPC`) e Higiene da Raiz (Padrão 2026)

Este guia de referência (Tier 3) apoia a skill `organizador-projetos-ideias` na geração e padronização dos artefatos estruturais de um projeto.

---

## 1. Checklist de Documentos-Chave da Raiz

| Arquivo | Papel Canônico | Verificação de Paridade (Real vs. Descrito) |
| :--- | :--- | :--- |
| **`README.md`** | Porta de entrada do projeto: objetivo, arquitetura real, árvore de diretórios atualizada, setup e comandos reais. | Todos os caminhos, scripts e comandos listados devem existir fisicamente no disco. |
| **`AGENTS.md`** | Topologia de agentes/subagentes, comandos rápidos (`pytest`, linters, builds) e regras de delegação. | Comandos executáveis testados e alinhados ao runtime real (`uv`, `npm`, `go`). |
| **`SPEC.md`** | Especificação funcional e técnica do MVP, requisitos, contratos de entrada/saída e limites de escopo. | Reflete exatamente as funções aprovadas para a versão atual (`v1.0.0` ou `vX.Y.Z`). |
| **`CONTEXT.md`** | Regras de negócio, problema resolvido, estado atual da implementação, decisões tomadas e próximos passos. | Atualizado ao final de cada ciclo de organização junto com a memória ativa. |
| **`DESIGN.md`** | Diretrizes visuais orientadas ao propósito do projeto, paleta/tokens, tipografia, espaçamento e estados de componentes. | Sincronizado com `src/components/` e folhas de estilo (`globals.css`). |
| **`GEMINI.md` / `CLAUDE.md`** | Instruções de sistema locais, restrições de segurança, convenções de código e idioma do workspace. | Alinhado às regras globais do desenvolvedor e ao stack do repositório. |
| **`.env.example` & `.gitignore`** | Proteção de credenciais e isolamento de artefatos gerados (`.env`, `.venv/`, `node_modules/`, `dist/`, `__pycache__/`). | `.env` real nunca é versionado; `.env.example` documenta apenas os nomes das chaves vazias. |

---

## 2. Padronização de Contratos e Métodos (`MCP`, `FastAPI`, `RPC`)

### 2.1. Contrato MCP (`tools.json` / FastMCP)
- Cada ferramenta exposta deve declarar:
  - `name`: Identificador em `snake_case` claro e sem ambiguidade.
  - `description`: Finalidade da ferramenta, quando usar e efeitos colaterais (Read-Only vs. Mutação).
  - `inputSchema`: JSON Schema estrito (`additionalProperties: false`) ou modelo `Pydantic v2` (`ConfigDict(extra="forbid")`).

### 2.2. Conexão FastAPI (REST / OpenAPI)
- Estruturar em `src/api/`:
  - `routes/` ou `routers/`: Endpoints agrupados por domínio com `response_model` explícito.
  - `schemas/`: Modelos `Pydantic v2` de Request/Response validados estritamente.
  - `dependencies.py`: Injeção de dependências, autenticação e conexão com banco/serviços.
  - Endpoint obrigatório de saúde: `GET /health` retornando versão e status do serviço.

### 2.3. Contratos RPC (`JSON-RPC 2.0` / `gRPC`)
- Estruturar em `src/contracts/` (ou `proto/`):
  - Catálogo explícito de **métodos** (`<namespace>/<metodo>`, ex.: `project/organize`, `task/execute`).
  - Definição tipada de `params`, `result` e códigos de erro padronizados (`-32600` Invalid Request, `-32601` Method Not Found, `-32602` Invalid Params, `-32603` Internal Error).

---

## 3. Protocolo de Limpeza Segura da Raiz (Dry-Run)

1. **Permitidos na Raiz:** Documentos-chave (`README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, `GEMINI.md`, `CLAUDE.md`, `LICENSE`), manifestos de pacotes (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`), configurações de controle de versão (`.gitignore`, `.env.example`) e entrypoints estritamente necessários.
2. **Candidatos à Realocação:**
   - Scripts soltos (`*.ps1`, `*.py`, `*.sh` auxiliares) $\rightarrow$ mover para `scripts/`.
   - Testes soltos (`test_*.py`, `*.spec.ts`) $\rightarrow$ mover para `tests/`.
   - Notas, rascunhos e diagramas avulsos $\rightarrow$ mover para `docs/` ou `_arquivo_temporario/`.
3. **Regra de Segurança:** Sempre listar os arquivos detectados fora de escopo e solicitar confirmação antes de mover ou remover.
