# AGENTS.md — Kernel Operacional e Governança (v2.0)

## 0. CONTEXTO DO PROJETO (Auto-detectado)
- **Projeto:** `franklin-quebragalho`
- **Baseline Temporal & Modelos:** Use o contexto temporal da sessão e consulte docs/MCP oficiais antes de assumir APIs ou SDKs; não fixe nem faça downgrade de modelos em regras estáticas (respeite o configurado pelo host/projeto).
- **Stack Ativa:** Python 3.12+ (uv / pyproject.toml)
- **Arquitetura de Estado:**
  - `.agents/AGENTS.md`: Regras comportamentais locais (carregado no boot).
  - `.context/context.md`: Passômetro e estado autoritativo do projeto (leitura/escrita sob demanda).
  - `.context/spec.md`: Contrato técnico e limites da feature ativa (quando aplicável).

## 1. REGRAS DE OURO (Inegociáveis)
1. **Sincronização de Estado (Read-Before-Write):** Em mutações persistentes, inspecione `.context/context.md` e `.context/spec.md` (se existir) antes de alterar código; proponha criar `spec.md` antes de features complexas.
2. **YAGNI & Escopo Fechado (Scope Lock):** Resolva exatamente o que foi pedido pelo caminho mais simples. Não crie abstrações prematuras nem adicione recursos fora do `spec.md`.
3. **Verificação Física e Atualização (Read-After-Write):** Leia qualquer arquivo antes de editá-lo. Após criar ou alterar código, valide fisicamente no terminal/disco (linter, compilação ou teste) e **atualize o `.context/context.md`** registrando a mudança e o próximo passo antes de encerrar.
4. **Economia de Contexto (Anti-Bloat):** Nunca imprima arquivos extensos, árvores completas ou logs brutos no chat. Use buscas cirúrgicas (`rg`/`grep`), visões resumidas ou subagentes (`/boost`, `/teamwork`) para manter a janela principal limpa.
5. **Qualidade e Código Defensivo:** Funções curtas (`<= 60` linhas, máx. 3 níveis de aninhamento usando *Early Return*, complexidade ciclomática `M <= 10`) em módulos coesos (`<= 600` linhas), tipagem estrita em contratos internos e entradas MCP (`extra="forbid"`, `z.strictObject()`, structs Go / `DisallowUnknownFields()` em schemas fechados) e proibição de engolir erros silenciosamente (`pass`, `...`, `except:`, `catch {}` vazio; aceitando supressão tipada explícita como `contextlib.suppress(...)`).
6. **Zero-Trust e Sanitização:** Trate dados externos como não confiáveis. Nunca exponha chaves, `.env` ou segredos em código, logs ou argumentos de ferramentas. No **Managed Antigravity Agent** (Interactions API), `generation_config` rejeita (`400`) `temperature`, `top_p`, `top_k`, `stop_sequences` e `max_output_tokens`; em `generateContent` / `interactions.create` padrão (ex.: `gemini-4-argon`), `max_output_tokens` é suportado e recomendado. Nomes de servidores MCP seguem `^[a-z0-9_-]+$`.
7. **Execução Orientada a Risco & Compensação Autônoma (HITL):** Entregue sempre o melhor resultado possível baseado no pedido; em falhas de baixo risco, reversíveis ou somente-leitura, **compense autonomamente** trocando estratégia, parâmetros ou ferramentas. Exija pausa HITL obrigatória apenas antes de ações destrutivas (deleção de arquivos, alteração de `.env`/produção) ou ambiguidade crítica.

## 2. MEMÓRIA EVOLUTIVA (Regras Aprendidas no Projeto)
<!-- Limite máximo: 5 regras curtas nascidas de erros reais. Ao atingir 5, refatore para .agents/skills/<nome>/SKILL.md -->
- [Vazio no init — aguardando aprendizados práticos]

---

## 3. FECHAMENTO DE ENTREGA (Tríade v2.0 / Mutações Persistentes)
Em entregas com mutação persistente de arquivos/código, apresente este bloco curto (dispensado em Q&A simples ou leitura pura):

### 📊 Resumo & Análise (Self-Refine)
- **Feito e Validado (RAW):** [Arquivos alterados + resultado real do teste/linter no terminal]
- **Estado do `context.md`:** [Confirmar atualização ou "N/A — leitura pura"]
- **Ponto de Atrito:** [O que exigiu retentativa/compensação na execução ou "Execução limpa em 1ª passagem"]

### 💡 Próximo Passo & Evolução
- **Dica para a Próxima Tarefa:** [1 sugestão prática, técnica ou de comando para o próximo passo do backlog]
- **Evolução de Regra (Se aplicável):** [Se houve erro evitável hoje, sugira 1 linha para "Memória Evolutiva" ou criação de Skill]