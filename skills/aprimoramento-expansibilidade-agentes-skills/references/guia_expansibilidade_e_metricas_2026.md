# Guia Canônico de Engenharia de Agentes, Frameworks, MCP e Auditoria Matemática (Padrão 2026)

Este documento constitui o **Tier 3 (Referência Sob Demanda)** da skill `aprimoramento-expansibilidade-agentes-skills` (`v2.2.0`), consolidando em **5 Módulos** a ontologia de agentes, a matriz de decisão de frameworks, o loop cognitivo de 8 passos, os contratos determinísticos de tools/MCP e as formulações matemáticas de auditoria.

---

## Módulo A: Ontologia, Determinismo vs. Estocástico e Matriz de Frameworks

### A.1. Diferenciação Ontológica: Skill vs. Tool vs. Agente vs. Workflow

| Elemento | Natureza Arquitetural | Decide? | Executa Efeito Externo? | Estado Próprio? | Quando Construir Primeiro |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Prompt + Schema** | Diretriz e contrato de saída | Não | Não | Turno único | Quando precisa apenas de resposta estruturada consistente |
| **Skill (`SKILL.md`)** | Procedimento operacional padrão | Orienta | Não (salvo via tools/scripts autorizados) | Não | Quando a IA esquece como executar um procedimento recorrente |
| **Tool** | Função tipada com contrato | Não | Sim, conforme backend | Explícito nos argumentos | Quando a IA precisa consultar ou alterar um sistema real |
| **Workflow** | Grafo determinístico de etapas | Regras / nós | Por etapas previsíveis | Checkpoint de execução | Quando a sequência de passos (`extrair -> validar -> gravar`) já é conhecida |
| **Agente** | Loop decisório adaptativo | Sim (probabilístico) | Por meio de tools | Memória de trabalho e sessão | Quando o caminho depende de observar resultados intermediários |
| **Servidor MCP** | Protocolo aberto (`JSON-RPC 2.0`) | Não | Expõe `tools`, `resources`, `prompts` | *Stateless* no protocolo (`2026-07-28`) | Quando múltiplos hosts/agentes precisam descobrir o mesmo catálogo |

### A.2. Fronteira Determinístico vs. Estocástico

| Tipo de Etapa | Exemplos Práticos | Implementação Preferida | Justificativa Técnica |
| :--- | :--- | :--- | :--- |
| **Determinística** | Validar CPF/CNPJ, calcular dose/EBITDA/WACC, transformar schema, calcular hash | Função Python/Go, SQL, script em `scripts/` | Previsível, testável em microssegundos e custo zero de tokens |
| **Semiestruturada** | Classificar intenção, extrair campos de texto livre, escolher entre poucas rotas | *Structured Output* + `Pydantic` + regra de validação | Flexibilidade semântica com fronteira sintática rígida |
| **Agentiva** | Investigar causa-raiz (RCA), encadear buscas dinâmicas, adaptar plano após erro | Loop de agente com `max_steps` e `deadline` | Caminho exato não é conhecido antecipadamente |
| **Alto Risco** | Excluir registros, pagar, enviar e-mail externo, prescrever, publicar em produção | Regra determinística + `--dry-run` + Portão **HITL** | O LLM nunca deve ser a única barreira de proteção |

### A.3. Matriz Comparativa de Frameworks (Escala 0 a 3)

| Opção / Framework | Simplicidade Inicial | Grafo & Durabilidade | RAG & Docs | Multiagente | Ecossistema Enterprise | Melhor Caso de Uso Dominante |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **API / SDK Direto + Pydantic** | **3** | 1 | 1 | 1 | 2 | Funções simples com 1–5 tools e controle total sem abstrações |
| **Google ADK 2.x (Go/Py/TS)** | 2 | **3** | 2 | **3** | **3** | Arquitetura code-first Zero-Trust, Cloud Run/GKE, KMS, gVisor e A2A |
| **LangGraph** | 1 | **3** | 2 | **3** | **3** | Grafos híbridos cíclicos, pausa/retomada, *checkpointers* e *time-travel* |
| **LangChain (`create_agent`)** | 2 | 2 | 2 | 2 | 2 | Harness rápido de modelo + tools + middlewares |
| **LlamaIndex** | 2 | 2 | **3** | 2 | 2 | Agentes e workflows centrados em ingestão documental e RAG complexo |
| **Microsoft Agent Framework** | 2 | **3** | 2 | **3** | **3** | Sucessor unificado (2026) de AutoGen e Semantic Kernel para .NET/Python |
| **CrewAI (`Flow` + `Crew`)** | 2 | 2 | 1 | **3** | 2 | Equipes de papéis acionadas dentro de um `Flow` determinístico |
| **AutoGen v0.4 / Semantic Kernel** | 1–2 | 2 | 1–2 | 2–3 | 2–3 | Manutenção de bases legadas existentes (novos projetos: migrar para Agent Framework) |

### A.4. Sequência Recomendada de Maturidade (Níveis 0 a 7)
- **Nível 0 — Chat**: Prompt claro, sem execução externa.
- **Nível 1 — Saída Estruturada**: JSON Schema / Pydantic e validação sintática.
- **Nível 2 — Tool Única**: Somente leitura, contrato estreito (`extra="forbid"`) e logs sem segredos.
- **Nível 3 — Workflow Híbrido**: Grafo determinístico externo com decisões do LLM restritas a nós específicos.
- **Nível 4 — Agente Limitado**: Seleção dinâmica de tools com orçamento (`max_steps`, `deadline`) e pós-condição verificável.
- **Nível 5 — Integrações Interoperáveis**: MCP `2026-07-28`, scopes OAuth 2.1 por operação e catálogo dinâmico (*tool search*).
- **Nível 6 — Multiagente**: Somente após benchmark provar ganho sobre agente único, com isolamento (`context: fork`) e contratos anti-cascata.
- **Nível 7 — Autonomia Gradual**: Permissões expandidas por evidência estatística ($\text{Pass}@k$, $\text{FNR} < 0.001$) e rollback/circuit breaker.

---

## Módulo B: Loop Cognitivo em 8 Passos, 5 Camadas de Memória e 11 Modos de Falha

### B.1. As 5 Camadas de Memória (E Por Que Memória $\neq$ Fonte de Verdade)

| Camada | Escopo Temporal | Conteúdo Típico | Implementação Recomendada | Risco Principal e Mitigação |
| :--- | :--- | :--- | :--- | :--- |
| **1. Contexto do Turno** | 1 chamada | Instruções ativas, pergunta, evidências filtradas e schemas | Janela de atenção do modelo | Diluição Softmax $\rightarrow$ Podar ruído e limitar tools expostas |
| **2. Memória de Trabalho** | 1 execução (run) | Plano atual, pendências, scratchpad transitório | Estado do workflow / `scratch/` | Inconsistência após retry $\rightarrow$ Estado imutável por passo |
| **3. Curto Prazo** | 1 sessão / thread | Histórico recente e resumo compactado | `Checkpointer` / `.context/SESSION_LOG.md` | Explosão de tokens $\rightarrow$ Compaction e resumo verificável |
| **4. Longo Prazo** | Múltiplas sessões | Preferências perenes, decisões e fatos homologados | Cofre Obsidian + MemPalace / Store | Fato obsoleto ou envenenado $\rightarrow$ Proveniência, data ISO e TTL |
| **5. Fonte de Verdade** | Sistema de negócio | Pedido, prontuário, agenda, estoque, financeiro | Banco transacional / API autoritativa | **Nunca usar Camadas 1–4 como substitutas da Camada 5** |

### B.2. Matriz dos 11 Modos de Falha e Controles Determinísticos

| # | Modo de Falha | Sinal Observável no Trace | Controle Determinístico Obrigatório |
| :---: | :--- | :--- | :--- |
| 1 | **Tool Inexistente** | Chamada de função fora do registro | `REGISTRY` fechado (*allowlist*) + rejeição imediata |
| 2 | **Argumento Inválido** | `ValidationError` repetido | `Pydantic extra="forbid"` + retorno de `expected_schema` e `recovery_hint` |
| 3 | **Loop Sem Progresso** | Mesmas chamadas e argumentos em sequência | `max_steps: 12`, detector de repetição de hash de chamada e `deadline_seconds: 90` |
| 4 | **Explosão de Tokens** | Latência e custo crescentes a cada turno | Compaction, truncamento seguro de saída de tool e paginação |
| 5 | **Perda *Lost-in-the-Middle*** | Esquecimento de restrições posicionadas no meio | Delimitadores XML assimétricos e invariantes posicionadas no final do prompt |
| 6 | **Memória Obsoleta** | Conflito entre memória antiga e estado real | Releitura obrigatória da Fonte de Verdade antes de escritas |
| 7 | **Prompt Injection (OWASP LLM01)** | Dado externo tenta comandar o agente | Envelopes `<untrusted_user_input>`, `SemanticGuard` e policy gate |
| 8 | **Efeito Duplicado** | Retry repete cobrança, envio ou inserção | `idempotency_key` obrigatório em tools de escrita + *read-after-write* |
| 9 | **Privilégio Excessivo** | Token/tool com escopo amplo demais | Menor privilégio, credenciais injetadas no runtime e *step-up auth* |
| 10 | **Cascata Multiagente** | Alucinação do Agente A vira `[FATO]` no Agente B | Validação de schema e proveniência (`HMAC-SHA256`) na fronteira entre agentes |
| 11 | **Parada Prematura** | Resposta textual afirma sucesso sem execução | Verificador determinístico de pós-condição antes de encerrar o loop |

---

## Módulo C: Contratos de Tools, Despacho Polimórfico e MCP 2026-07-28

### C.1. Contrato Canônico de Tool (`Pydantic v2` $\rightarrow$ `JSON Schema 2020-12` $\rightarrow$ `REGISTRY`)
1. **Verbo Estreito e Semântico**: `buscar_pedido` (somente leitura) separado de `cancelar_pedido` (escrita destrutiva com `idempotency_key`).
2. **Proibição de Campos Fantasmas**: Sempre declarar `model_config = ConfigDict(extra="forbid")`.
3. **Despacho Polimórfico (*Envelope Pattern*)**: Quando uma skill possui múltiplas suboperações (ex.: `AUDIT_BALANCE`, `VALUATION_DCF`, `TAX_RECONCILIATION`), exponha um único envelope mestre (`MasterSkillInvocation`) e valide os parâmetros contra o sub-schema especializado em tempo de execução (implementado em [`scripts/agentic_math_and_engine_auditor.py`](../scripts/agentic_math_and_engine_auditor.py)).

### C.2. Requisitos MCP (`Specification 2026-07-28` & Python SDK 2.x)
- **Stateless Core**: Não dependa de sessão oculta na conexão; passe `job_handle` e `cursor` explicitamente nos argumentos.
- **Descoberta e Cache**: `tools/list` é paginado, determinístico e respeita `ttlMs` e `cacheScope`, podendo variar conforme a autorização do request.
- **Segurança `stdio` vs `HTTP`**:
  - Em `stdio`: obtenha credenciais do ambiente e **jamais escreva logs em `stdout`** (use `stderr`).
  - Em `Streamable HTTP`: utilize **OAuth 2.1**, exija *Resource Indicators* (audience binding) e nunca repasse tokens recebidos para outros serviços downstream.

---

## Módulo D: Densidade de Atenção (Softmax), `Context Forking` e `Theranostic Gate`

### D.1. Física da Atenção Softmax
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V, \quad \alpha_{ij} = \frac{\exp(q_i \cdot k_j / \sqrt{d_k})}{\sum_{l=1}^{N} \exp(q_i \cdot k_l / \sqrt{d_k})}$$
- Expandir $N$ com dezenas de schemas de ferramentas inúteis ou históricos brutos infla o denominador exponencial, reduzindo logaritmicamente a atenção $\alpha_{ij}$ dedicada às restrições de segurança.
- **Solução Tripla**: (1) Divulgação Progressiva em 3 Tiers; (2) *Envelope Pattern* polimórfico; (3) *Context Forking* (`context: fork` / `invoke_subagent`) para isolar subtarefas pesadas e retornar apenas o resumo assinado (`< 500` tokens).

### D.2. Theranostic Diagnostic-to-Action Pipeline
- **Estágio 1 (Read-Only Analyzer)**: Bloqueia tools mutáveis em nível de código (`ReadOnlyViolationError`) e emite diagnóstico estruturado com `confidence_score`.
- **Estágio 2 (`ConfidenceGate >= 0.95`)**: Se `confidence_score < 0.95`, congela em `FROZEN_FOR_HUMAN_VALIDATION`.
- **Estágio 3 (Action Executor + `HMAC-SHA256`)**: Executa a mutação autorizada e emite `ProvenanceManifest` verificável via `hmac.compare_digest`.

---

## Módulo E: Formulação Matemática Completa de Auditoria

Implementação executável disponível em [`scripts/agentic_math_and_engine_auditor.py`](../scripts/agentic_math_and_engine_auditor.py):

1. **Estimador Não Enviesado Estável de $\text{Pass}@k$ (Chen et al., HumanEval)**:
   $$\text{Pass}@k = \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right] = 1 - \prod_{i=1}^{k} \left(1 - \frac{c}{n - k + i}\right)$$
   *(O produto iterativo evita overflow fatorial para $n$ grande).*

2. **Fidelidade Factual e Grounding Vetorial ($D_{\cos}$)**:
   $$\text{Sim}_{\cos}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}, \quad D_{\cos}(\mathbf{u}, \mathbf{v}) = 1 - \text{Sim}_{\cos}(\mathbf{u}, \mathbf{v})$$
   - Limiar canônico de deriva semântica / alucinação: **$D_{\cos}(\mathbf{u}, \mathbf{v}) > \tau_{\text{limiar}} = 0.18$**.

3. **Matriz de Confusão para Guardrails ($\text{FNR} < 0.001$)**:
   $$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = \frac{2TP}{2TP + FP + FN}, \quad \text{FNR} = \frac{FN}{FN + TP} = 1 - \text{Recall}$$
   - Tolerância máxima para fuga de prompt injection / mutação indevida em produção: **$\text{FNR} < 0.001$**.

4. **Normalização Ponderada Multicritério (`LLM-as-a-Judge` $S_{\text{norm}}$)**:
   $$S_{\text{norm}} = \left[ \frac{\sum_{j=1}^{M} w_j \cdot \left(\frac{s_j - s_{\min,j}}{s_{\max,j} - s_{\min,j}}\right)}{\sum_{j=1}^{M} w_j} \right] \times 100 \in [0, 100]$$

5. **Índice de Eficiência de Tokens ($\text{TEI}$)**:
   $$\text{TEI} = \frac{S_{\text{norm}} \cdot \mathbb{I}(\text{Sucesso})}{C_{\text{USD}} \cdot \ln\left(T_{\text{in}} + \beta \cdot T_{\text{out}} + e\right)}, \quad C_{\text{USD}} = T_{\text{in}} P_{\text{in}} + T_{\text{out}} P_{\text{out}}$$
   *(Onde $\beta \ge 1.0$, tipicamente $\beta = 2.0$, penaliza o custo térmico e de latência sequencial da KV-cache na geração de saída).*
