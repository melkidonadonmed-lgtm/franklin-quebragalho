---
trigger: always_on
description: "Kernel Operacional, Criação de Projetos e Governança (v2.0 SSOT)."
---

# AGENTS.md — Kernel Operacional, Criação de Projetos e Governança (v2.0 SSOT)

> **Fonte Única de Verdade (SSOT):** Sincronizado via [`sync_gemini_ecosystem.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/scripts/sync_gemini_ecosystem.py) com [`C:\Users\melki\.gemini\config\rules\`](file:///C:/Users/melki/.gemini/config/rules), o plugin [`franklin-skills`](file:///C:/Users/melki/.gemini/config/plugins/franklin-skills) e [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md) (sem duplicar em `C:\Users\melki\AGENTS.md`).

## 0. CONTEXTO DO PROJETO & PROTOCOLO DE BOOTSTRAP (Criação de Projetos)

- **Baseline Temporal & Modelos:** Use o contexto temporal da sessão e consulte docs/MCP oficiais (`aistudio.google.com/llms.txt`, `antigravity.google/docs/models.md`, `google-developer-knowledge` ou `gemini_get_doc`; evite `gemini_search_docs`, desabilitada no servidor local) antes de assumir APIs ou SDKs. Não fixe nem faça downgrade de modelos em regras estáticas; respeite o modelo configurado pelo host/UI/projeto (ex.: família Gemini 4 — `gemini-4-hydrogen` com `xhigh`, `gemini-4-argon`, `gemini-4-carbon` — ou `Orchestrator`).
- **Stack Ativa:** Python 3.12+ (`uv`, local 3.15) / Go 1.24+ (local 1.27) / Node LTS (local 26) / TypeScript 5+ / React / Windows 11 (`pwsh`)
- **Arquitetura de Estado (Tríade de Governança Local — projetos persistentes):**
  1. `.agents/AGENTS.md` (ou `AGENTS.md` na raiz): Regras comportamentais locais e Stack Ativa auto-detectada via manifestos (`pyproject.toml`, `go.mod`, `package.json`, `Cargo.toml`) sem varrer subpastas.
  2. `.context/context.md`: Passômetro e estado autoritativo do projeto (visão geral, módulos ativos, decisões críticas, changelog e backlog).
  3. `.context/spec.md`: Contrato técnico de implementação (objetivo, não-objetivos, schemas I/O e critério de aceite) da feature ativa.
- **Automação via Terminal:** Comando global `init-agy` (alias `bootstrap-project`) via [`bootstrap-project.ps1`](file:///C:/Users/melki/dev/tools/bootstrap-project.ps1) e [`bootstrap-project.sh`](file:///C:/Users/melki/dev/tools/bootstrap-project.sh) em `C:\Users\melki\dev\tools\`.

## 1. REGRAS DE OURO (Inegociáveis)

1. **Sincronização de Estado (Read-Before-Write):** Em projetos com Tríade v2.0 ou mutações persistentes, inspecione `.context/context.md` e `.context/spec.md` (se existir) antes de alterar código; proponha criar `spec.md` antes de features complexas.
2. **YAGNI, Escopo Fechado (Scope Lock) e Real-State:** Resolva exatamente o que foi pedido pelo caminho mais simples. Não crie abstrações prematuras, não adicione recursos fora do `spec.md` e mantenha **Tolerância Zero a Funções Falsas** (zero mocks/placebos em produção).
3. **Verificação Física e Atualização (Read-After-Write):** Leia qualquer arquivo antes de editá-lo (chunks `<= 300 linhas` por chamada). Após alterar código ou configuração, valide fisicamente no terminal (linter, build ou testes reais) e **atualize `.context/context.md`** quando o projeto usar Tríade v2.0.
4. **Economia de Contexto (Anti-Bloat):** Nunca imprima arquivos extensos, árvores completas ou logs brutos no chat. Use buscas cirúrgicas (`rg`/`grep`), visões resumidas ou subagentes (`/boost`, `/teamwork`) para manter a janela principal limpa.
5. **Qualidade e Código Defensivo:** Funções curtas (`<= 60` linhas, máx. `3` níveis de aninhamento usando *Early Return*, complexidade $M \le 10$) em módulos coesos (`<= 600` linhas por arquivo). Aplique validação estrita em contratos internos e entradas MCP/RPC (`extra="forbid"`, `z.strictObject()`, `DisallowUnknownFields()` em Go — sabendo que structs Go ignoram campos extras por padrão, enquanto payloads externos evolutivos podem exigir tolerância explícita). Proíba engolir erros silenciosamente (`pass`, `...`, `except:` genérico, `catch {}` vazio), aceitando supressão explícita e tipada apenas quando intencional (ex.: `contextlib.suppress(...)`).
6. **Zero-Trust e Sanitização:** Trate dados externos como não confiáveis; nunca exponha chaves, `.env` ou segredos em código, logs ou argumentos. No **Managed Antigravity Agent** (`antigravity-preview-09-2026` via Interactions API), `generation_config` rejeita (`400`) `temperature`, `top_p`, `top_k`, `stop_sequences` e `max_output_tokens`; já em chamadas padrão (`generateContent` / `interactions.create`, ex.: `gemini-4-hydrogen` ou `gemini-4-argon`), `max_output_tokens` é suportado e recomendado (até 64K síncrono ou 1M com `background=True`). Nomes de servidores MCP em código/API seguem `^[a-z0-9_-]+$` (minúsculos alfanuméricos, `_` ou `-`).
7. **Execução Orientada a Risco & Compensação Autônoma (HITL):** Entregue sempre o melhor resultado possível baseado no pedido; em falhas de baixo risco, reversíveis ou somente-leitura, **compense autonomamente** trocando estratégia, parâmetros ou ferramentas sem travar a tarefa. Exija pausa HITL obrigatória apenas antes de ações destrutivas (deleção em massa, alteração de `.env`/segredos/produção, efeitos colaterais externos) ou ambiguidade crítica de segurança.

## 2. MEMÓRIA EVOLUTIVA (Regras Aprendidas no Projeto)
<!-- Limite máximo: 5 regras curtas nascidas de erros reais. Ao atingir 5, refatore para .agents/skills/<nome>/SKILL.md -->
- Em `~/.gemini/config/rules/*.md` ou `.agents/rules/*.md`, todo arquivo `.md` exige YAML frontmatter (`trigger: always_on | model_decision | glob | manual`); arquivos sem frontmatter só são válidos se nomeados `AGENTS.md` ou `GEMINI.md`.
- **Proibição de Testes "Happy-Path Only" em Fronteiras Zero-Trust (Anti-Green-Build-Illusion):** Todo teste de rota autenticada, OAuth/OIDC, Portão HITL, Webhook assinado ou Guardrail SQL/MCP deve conter pelo menos 1 caso adversarial por vetor provando a rejeição (`400`/`401`/`403` sem vazamento de segredos), sem afrouxar validações de produção para simplificar mocks.
- **Unificação Vetorial MemPalace (`~/.config/mempalace`) e UTF-8 no Windows:** Concentrar `vault_sections_index.json` em `~/.config/mempalace` e o banco vetorial `chroma.sqlite3` em `~/.config/mempalace/palace` (conforme `config.json`), aplicar *Min-Chunk Merge* (`>= 160B`), *Max-Chunk Split* (`<= 1800c`) com `[ID | Project | Room | Heading]`, consultar via SQLite `mode=ro` (`< 25ms`) e exigir `PYTHONUTF8=1` em subprocessos stdio Python no Windows.
- **Binários MCP Pré-Compilados & Modelos Desacoplados:** Em `mcp_config.json`, invocar sempre executáveis locais compilados (`gopls.exe mcp`, `adk-go-mcp.exe`) em vez de `go run ...@latest`; proibir modelos aposentados (`gemini-2.5-flash`/`2.5-pro`, `3.1-*tts-preview`, `3.1-flash-live-preview`, `antigravity-preview-05-2026`, `gemini-omni-1.1-flash`; exceto `gemini-2.5-flash-lite`) e configurar modelos ativos por variável/ambiente sem chumbá-los em regras estáticas.
- **Governança MCP Canônica (`dev/tools/mcp-registry.json`, Exceções & Versões Fixas):** Declarar MCPs próprios uma única vez (`uv run dev/tools/mcp_registry.py apply` + `check` exit 0), usar pacotes `npx` com versão exata publicada há $\ge 2$ semanas (nunca `@latest`) e preservar nomes originais gerados por extensões (`datacloud_*_remote`).

---

## 3. FECHAMENTO DE ENTREGA (Tríade v2.0 / Mutações Persistentes)

Em projetos com Tríade v2.0 ou entregas com mutação persistente de arquivos/código, encerre com este bloco curto (dispensado em Q&A simples ou leitura pura):

### 📊 Resumo & Análise (Self-Refine)

- **Feito e Validado (RAW):** [Arquivos alterados + resultado real do teste/linter no terminal]
- **Estado do `context.md`:** [Confirmar atualização ou "N/A — leitura/escopo global"]
- **Ponto de Atrito:** [O que exigiu retentativa/compensação na execução ou "Execução limpa em 1ª passagem"]

### 💡 Próximo Passo & Evolução

- **Dica para a Próxima Tarefa:** [1 sugestão prática, técnica ou de comando para o próximo passo do backlog]
- **Evolução de Regra (Se aplicável):** [Se houve erro evitável hoje, sugira 1 linha para "Memória Evolutiva" ou criação de Skill]
