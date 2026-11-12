---
trigger: always_on
description: "Kernel Operacional, Criação de Projetos e Governança (v2.0 SSOT)."
---

# AGENTS.md — Kernel Operacional, Criação de Projetos e Governança (v2.0 SSOT)

> **Fonte Única de Verdade (SSOT):** Sincronizado via [`sync_gemini_ecosystem.py`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/scripts/sync_gemini_ecosystem.py) entre [`C:\Users\melki\AGENTS.md`](file:///C:/Users/melki/AGENTS.md), [`C:\Users\melki\.agents\AGENTS.md`](file:///C:/Users/melki/.agents/AGENTS.md), [`C:\Users\melki\.gemini\config\rules\`](file:///C:/Users/melki/.gemini/config/rules) e [`CURRENT_STATE.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/CURRENT_STATE.md).

## 0. CONTEXTO DO PROJETO & PROTOCOLO DE BOOTSTRAP (Criação de Projetos)

- **Baseline Temporal:** Novembro de 2026 (rejeite APIs/sintaxes legadas; na dúvida sobre pacotes ou SDKs, consulte docs atuais ou MCP).
- **Stack Ativa:** Python 3.12+ (`uv`) / Go 1.24+ / TypeScript 5+ / Node LTS / React / Windows 11 (`pwsh`)
- **Arquitetura de Estado (Tríade de Governança Local):**
  1. `.agents/AGENTS.md` (ou `AGENTS.md` na raiz): Regras comportamentais globais e Stack Ativa auto-detectada via manifestos (`pyproject.toml`, `go.mod`, `package.json`, `Cargo.toml`) sem varrer subpastas.
  2. `.context/context.md`: Passômetro e estado autoritativo do projeto (visão geral, módulos ativos, decisões críticas, changelog e backlog).
  3. `.context/spec.md`: Contrato técnico de implementação (objetivo, não-objetivos, schemas I/O e critério de aceite) da feature ativa.
- **Automação via Terminal:** Comando global `init-agy` (alias `bootstrap-project`) via [`bootstrap-project.ps1`](file:///C:/Users/melki/dev/tools/bootstrap-project.ps1) e [`bootstrap-project.sh`](file:///C:/Users/melki/dev/tools/bootstrap-project.sh) em `C:\Users\melki\dev\tools\`.

## 1. REGRAS DE OURO (Inegociáveis)

1. **Sincronização de Estado (Read-Before-Write):** Ao iniciar uma tarefa, inspecione `.context/context.md` para entender o estado atual e `.context/spec.md` (se existir) para respeitar os contratos de I/O. Se for uma feature complexa sem `spec.md`, proponha criá-lo antes de codificar.
2. **YAGNI, Escopo Fechado (Scope Lock) e Real-State:** Resolva exatamente o que foi pedido pelo caminho mais simples. Não crie abstrações prematuras, não adicione recursos fora do `spec.md` e mantenha **Tolerância Zero a Funções Falsas** (zero mocks/placebos em produção).
3. **Verificação Física e Atualização (Read-After-Write):** Leia qualquer arquivo antes de editá-lo (chunks `<= 300 linhas` por chamada). Após criar ou alterar código, valide fisicamente no terminal/disco (linter, compilação ou teste) e **atualize o `.context/context.md`** registrando a mudança e o próximo passo antes de encerrar.
4. **Economia de Contexto (Anti-Bloat):** Nunca imprima arquivos extensos, árvores completas ou logs brutos no chat. Use buscas cirúrgicas (`rg`/`grep`), visões resumidas ou subagentes (`/boost`, `/teamwork`) para manter a janela principal limpa.
5. **Qualidade e Código Defensivo:** Funções curtas (`<= 600 linhas` por módulo, máx. 3 níveis de indentação usando *Early Return*), tipagem estrita nas fronteiras (Pydantic v2 `extra="forbid"`, Zod `.strict()` ou structs Go) e zero blocos de erro silenciosos (`pass` ou `catch` vazio).
6. **Zero-Trust e Sanitização:** Trate dados externos como não confiáveis. Nunca exponha chaves, `.env` ou segredos em código, logs ou argumentos de ferramentas. Em chamadas da API Antigravity, nunca use parâmetros bloqueados (`temperature`, `top_p`, `max_output_tokens`) e use apenas nomes minúsculos alfanuméricos com hifens para servidores MCP.
7. **Freio de Emergência (Circuit Breaker & HITL):** Pare imediatamente e peça confirmação humana se uma ferramenta falhar 3 vezes seguidas, se atingir 10 passos sem convergir ou antes de qualquer ação destrutiva (deleção de arquivos, alteração de `.env`/produção).

## 2. MEMÓRIA EVOLUTIVA (Regras Aprendidas no Projeto)
<!-- Limite máximo: 5 regras curtas nascidas de erros reais. Ao atingir 5, refatore para .agents/skills/<nome>/SKILL.md -->
- Em `~/.gemini/config/rules/*.md` ou `.agents/rules/*.md`, todo arquivo `.md` exige YAML frontmatter (`trigger: always_on | model_decision | glob | manual`); arquivos sem frontmatter só são válidos se nomeados `AGENTS.md` ou `GEMINI.md`.
- **Proibição de Testes "Happy-Path Only" em Fronteiras Zero-Trust (Anti-Green-Build-Illusion):** Todo teste de rota autenticada, OAuth/OIDC, Portão HITL, Webhook assinado ou Guardrail SQL/MCP deve obrigatoriamente conter pelo menos 1 caso adversarial por vetor provando a rejeição (`400`/`401`/`403` e ausência de vazamento de segredos em respostas públicas). Nunca afrouxar validações de produção para simplificar mocks de `httptest`.
- **Unificação Vetorial MemPalace (`~/.config/mempalace`) e UTF-8 no Windows:** Concentrar índices (`vault_sections_index.json`, `chroma.sqlite3`) em `~/.config/mempalace`, aplicar *Min-Chunk Merge* (`>= 160B`), *Max-Chunk Split* (`<= 1800c`) com cabeçalho `[ID | Project | Room | Heading]`, consultar FTS5/vetores via SQLite `mode=ro` (`< 25ms`, sem subprocesso) e exigir `PYTHONUTF8=1` em todo processo stdio Python no Windows.
- **Binários MCP Pré-Compilados e Modelos Vigentes (`gemini-3.8-*`):** Em `mcp_config.json`, invocar sempre executáveis locais compilados (`gopls.exe mcp`, `adk-go-mcp.exe`) em vez de `go run ...@latest`, e proibir strings de modelos depreciados (`gemini-2.5-*`) em código ou cascatas de fallback.
- **Governança MCP Canônica (`dev/tools/mcp-registry.json`, Exceções de Extensão & Versões Fixas):** Declarar MCPs próprios uma única vez no registro (`uv run dev/tools/mcp_registry.py apply` + `check` exit 0), usar pacotes `npx` com versão exata publicada há $\ge 2$ semanas (nunca `@latest`) e preservar nomes originais gerados por extensões (`datacloud_*_remote`).

---

## 3. FECHAMENTO OBRIGATÓRIO DE TAREFA

Ao concluir qualquer entrega, apresente obrigatoriamente este bloco curto:

### 📊 Resumo & Análise (Self-Refine)

- **Feito e Validado (RAW):** [Arquivos alterados + resultado real do teste/linter no terminal]
- **Estado do `context.md`:** [Confirmar: "Atualizado com a mudança X e pendência Y" ou "Sem alteração estrutural"]
- **Ponto de Atrito:** [O que exigiu retentativa/ajuste na execução ou "Execução limpa em 1ª passagem"]

### 💡 Próximo Passo & Evolução

- **Dica para a Próxima Tarefa:** [1 sugestão prática, técnica ou de comando para o próximo passo do backlog]
- **Evolução de Regra (Se aplicável):** [Se houve erro evitável hoje, sugira 1 linha para "Memória Evolutiva" ou criação de Skill]
