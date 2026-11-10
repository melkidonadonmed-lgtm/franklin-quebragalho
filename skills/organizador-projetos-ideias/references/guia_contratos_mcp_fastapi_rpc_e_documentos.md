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

---

## 4. Templates Canônicos da Tríade de Governança v2.0 (`.agents/AGENTS.md`, `.context/context.md`, `.context/spec.md`)

Ao criar ou fazer bootstrap de qualquer projeto novo ou existente (ou via `C:\Users\melki\dev\tools\bootstrap-project.ps1`), gere fisicamente os 3 arquivos abaixo:

### 4.1. `.agents/AGENTS.md` (Kernel Operacional v2.0)

```markdown
# AGENTS.md — Kernel Operacional e Governança (v2.0)

## 0. CONTEXTO DO PROJETO (Auto-detectado)
- **Baseline Temporal:** Novembro de 2026 (rejeite APIs/sintaxes legadas; na dúvida sobre pacotes ou SDKs, consulte docs atuais ou MCP).
- **Stack Ativa:** [Ex: Python 3.12+ / Go 1.22+ / TypeScript 5+ / React — preencher no init via manifestos da raiz]
- **Arquitetura de Estado:**
  - `.agents/AGENTS.md`: Regras comportamentais globais (carregado no boot).
  - `.context/context.md`: Passômetro e estado autoritativo do projeto (leitura/escrita sob demanda).
  - `.context/spec.md`: Contrato técnico e limites da feature ativa (quando aplicável).

## 1. REGRAS DE OURO (Inegociáveis)
1. **Sincronização de Estado (Read-Before-Write):** Ao iniciar uma tarefa, inspecione `.context/context.md` para entender o estado atual e `.context/spec.md` (se existir) para respeitar os contratos de I/O. Se for uma feature complexa sem `spec.md`, proponha criá-lo antes de codificar.
2. **YAGNI & Escopo Fechado (Scope Lock):** Resolva exatamente o que foi pedido pelo caminho mais simples. Não crie abstrações prematuras nem adicione recursos fora do `spec.md`.
3. **Verificação Física e Atualização (Read-After-Write):** Leia qualquer arquivo antes de editá-lo. Após criar ou alterar código, valide fisicamente no terminal/disco (linter, compilação ou teste) e **atualize o `.context/context.md`** registrando a mudança e o próximo passo antes de encerrar.
4. **Economia de Contexto (Anti-Bloat):** Nunca imprima arquivos extensos, árvores completas ou logs brutos no chat. Use buscas cirúrgicas (`rg`/`grep`), visões resumidas ou subagentes (`/boost`, `/teamwork`) para manter a janela principal limpa.
5. **Qualidade e Código Defensivo:** Funções curtas (máx. 3 níveis de indentação usando *Early Return*), tipagem estrita nas fronteiras (Pydantic v2 `extra="forbid"`, Zod ou structs Go) e zero blocos de erro silenciosos (`pass` ou `catch` vazio).
6. **Zero-Trust e Sanitização:** Trate dados externos como não confiáveis. Nunca exponha chaves, `.env` ou segredos em código, logs ou argumentos de ferramentas. Em chamadas da API Antigravity, nunca use parâmetros bloqueados (`temperature`, `top_p`, `max_output_tokens`) e use apenas nomes minúsculos alfanuméricos para servidores MCP.
7. **Freio de Emergência (Circuit Breaker & HITL):** Pare imediatamente e peça confirmação humana se uma ferramenta falhar 3 vezes seguidas, se atingir 10 passos sem convergir ou antes de qualquer ação destrutiva (deleção de arquivos, alteração de `.env`/produção).

## 2. MEMÓRIA EVOLUTIVA (Regras Aprendidas no Projeto)
<!-- Limite máximo: 5 regras curtas nascidas de erros reais. Ao atingir 5, refatore para .agents/skills/<nome>/SKILL.md -->
- [Vazio no init — aguardando aprendizados práticos]
```

### 4.2. `.context/context.md` (Passômetro e Estado Autoritativo)

```markdown
# CONTEXT.MD — Estado Autoritativo do Projeto
> **Última Atualização:** 2026-11-06 | **Status:** `ACTIVE`

## 1. Visão Geral & Arquitetura Atual
- **Propósito:** [1 frase sobre o que o sistema faz]
- **Stack & Runtime:** [Ex: Go 1.22 + SQLite WAL + React/Tailwind]
- **Módulos Ativos:** [Lista rápida dos serviços/pastas principais que já estão prontos]

## 2. Decisões Técnicas Críticas (Não Violar)
- [Ex: Autenticação usa JWT stateless; Banco usa sempre queries parametrizadas sem ORM pesado]

## 3. Últimas Alterações (Changelog Recente)
- `[2026-11-06]` Estrutura inicial criada e regras globais configuradas.

## 4. Backlog & Próximos Passos (Fila de Execução)
- [ ] `TASK-01`: [Próxima tarefa prioritária]
- [ ] `TASK-02`: [Tarefa seguinte]
```

### 4.3. `.context/spec.md` (Contrato de Implementação)

```markdown
# SPEC.MD — Contrato de Implementação: [Nome da Feature]

## 1. Objetivo e Fronteiras (Scope Lock)
- **O que construir:** [Descrição direta da funcionalidade]
- **Não-Objetivos (Proibido fazer):** [Ex: Não alterar a tabela de usuários existente; não instalar novas libs de UI]

## 2. Contratos de Dados e Interfaces (I/O)
- **Entrada esperada / Schema:** [Ex: Payload JSON / Struct Go / Modelo Pydantic]
- **Saída esperada / Efeito:** [Ex: Status 201 + gravação no SQLite]

## 3. Critério de Aceite e Parada (Definition of Done)
- [ ] Passar no linter/typecheck sem erros (`mypy --strict` / `go vet` / `tsc`).
- [ ] Teste unitário ou comando de verificação executando com sucesso no terminal.
```
