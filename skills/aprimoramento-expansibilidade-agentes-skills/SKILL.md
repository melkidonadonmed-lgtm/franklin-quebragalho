---
name: aprimoramento-expansibilidade-agentes-skills
description: >-
  Motor consultivo de arquitetura, expansibilidade (3 Tiers, Envelope Pattern, Context Forking, Memória em 3 Camadas, MCP/A2A) e ciclo de qualidade orientado a dados (Eval-Driven Iteration, Pass@k, FNR < 0.001, LLM-as-a-Judge Snorm, Trigger Optimization, GEPA/ADK e Densidade de Atenção Softmax) para Agentes de IA e SKILL.md. Use quando consultada pela evoluir-skills ou quando o usuário solicitar conversão de agente monolítico em multiagente, escalabilidade em Níveis 1 a 4, despoluição de janela de contexto ou engenharia de métricas de avaliação. Não use para criar pasta física de skill do zero sem passar pela evoluir-skills.
license: MIT
metadata:
  version: "2.0.0"
  author: "SkillCraft & Melki"
  category: "Arquitetura, Expansibilidade e Avaliação de Agentes"
  updated_at: "2026-10-14"
  tags:
    - "expansibilidade"
    - "eval-driven"
    - "pass-at-k"
    - "envelope-pattern"
    - "context-forking"
    - "mcp-a2a"
    - "progressive-disclosure"
version: 2.0.0
updated_at: 2026-10-14
author: SkillCraft & Melki
category: Arquitetura, Expansibilidade e Avaliação de Agentes
---

# Aprimoramento, Expansibilidade e Avaliação de Agentes & Skills (`v2.0.0`) 🧠

Skill consultiva de engenharia de sistemas agênticos (Estágio 2 do pipeline `evoluir-skills` e arquiteta de expansão para **Google ADK**, **Antigravity**, **MCP** e **A2A**). Substitui impressões subjetivas por métricas formais, divulgação progressiva em 3 camadas e desacoplamento estrutural.

> [!TIP]
> **Referência Técnica Completa (Tier 3):** Para fórmulas matemáticas ($\text{Pass}@k$, $\text{FNR}$, $S_{\text{norm}}$, Softmax), schemas Pydantic do *Envelope Pattern* e a tabela completa dos 4 Níveis de Maturidade, consulte [`references/guia_expansibilidade_e_metricas_2026.md`](references/guia_expansibilidade_e_metricas_2026.md).

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Como **Estágio 2 Consultivo** invocado automaticamente pela `evoluir-skills` ao projetar ou evoluir qualquer habilidade do catálogo.
- Quando o usuário solicitar migração de um **Prompt Monolítico (Nível 1/2)** para uma arquitetura de **Context & Intent Engineering (Nível 3)** ou **Specification Engineering Corporativo (Nível 4)**.
- Para diagnosticar degradação de atenção (*Context Drift* em 20–50 passos), excesso de regras (*over-constraining*), loops de ferramentas em `transcript.jsonl` ou falsos positivos/negativos de ativação.
- Na implementação de **Google ADK** (`adk optimize` / GEPA), **Padrão Envelope**, **Context Forking (`context: fork`)**, **Memória em 3 Camadas** ou interoperabilidade **MCP / A2A**.

---

## 🚫 Limites, Exceções e Quando NÃO Usar
- **Não usar** isoladamente para scaffolding físico de diretórios e atualização do `MY_SKILLS.md` sem o fluxo mestre da `evoluir-skills`.
- **Não usar** para expandir prompts simples de turno único que não envolvam arquitetura de agentes ou skills (use `expansao-contexto-adaptativa`).
- **Não usar** para auditoria cosmética/visual de frontend (use `analise-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Alvo da Consultoria**: Definição atual do agente (Python/TS/ADK) ou contrato `SKILL.md` (ou escopo expandido vindo do Estágio 1).
2. **Vetor de Escala ou Gargalo**: Otimização de contexto/latência, adição de ferramentas via Envelope/MCP, isolamento de subagentes ou desenho de suíte de avaliação (`evals.json`).
3. **Nível de Maturidade Alvo**: Nível 3 (*Context & Intent Engineering*) ou Nível 4 (*Specification Engineering Corporativo*).

---

## ⚙️ Processamento Passo a Passo: Os 2 Eixos de Engenharia

### Eixo 1: Critérios de Expansibilidade e Arquitetura Extensível (*Extensibility & Scaling*)

```text
+-----------------------------------------------------------------------------------+
|                        DIVULGAÇÃO PROGRESSIVA (3 TIERS)                           |
+-----------------------------------------------------------------------------------+
| Tier 1: Catálogo (Início)        --> name + description (~50-100 tokens)          |
| Tier 2: Ativação (Match)         --> Corpo SKILL.md (<5000 tokens / <500 linhas)  |
| Tier 3: Execução (Sob demanda)   --> references/, scripts/, schemas Pydantic      |
+-----------------------------------------------------------------------------------+
                                        │
                                        ▼
+-----------------------------------------------------------------------------------+
|                     ARQUITETURA DE EXECUÇÃO E ORQUESTRAÇÃO                        |
+-----------------------------------------------------------------------------------+
| • Envelope Pattern (Action Routing)   --> Interface polimórfica mestre            |
| • Context Forking (context: fork)     --> Subagentes isolados para tarefas longas |
| • Barramento MCP + A2A (JSON-RPC 2.0) --> Desacoplamento de tools e Agent Cards   |
| • Memória em 3 Camadas                --> Scratchpad | Sessão | Memory Bank (TTL) |
+-----------------------------------------------------------------------------------+
```

1. **Divulgação Progressiva Estrita (3 Tiers)**:
   - **Tier 1 (Catálogo)**: Carrega apenas `name` e `description` (~50–100 tokens).
   - **Tier 2 (Ativação)**: Injeta o corpo do `SKILL.md` ($< 5.000$ tokens / $< 500$ linhas) somente quando a skill é ativada.
   - **Tier 3 (Execução sob demanda)**: `references/`, `scripts/`, `assets/` e schemas JSON/Pydantic só são lidos quando o passo ativo exigir.
2. **Descentralização Modular e Padrão Envelope (*Envelope Pattern*)**:
   - Abandone o prompt monolítico ("Parede de Complexidade").
   - Em vez de dezenas de tools granulares poluindo o catálogo, exponha uma única interface mestre (**Envelope**) com `action: Literal[...]` e `params: dict`, despachando internamente para sub-esquemas Pydantic em tempo de execução.
3. **Bifurcação de Contexto (`context: fork`) e Controle de Fronteira**:
   - Tarefas longas de pesquisa, depuração ou tentativa-e-erro devem rodar em subagente isolado (`invoke_subagent` / `context: fork`), retornando ao orquestrador apenas o payload final assinado.
   - O roteador de intenção opera sem acesso direto a ferramentas destrutivas (*boundary control*).
4. **Arquitetura de Memória em 3 Camadas**:
   - **Camada 1 (Scratchpad Transitório)**: Buffer Markdown para raciocínio imediato (CoT/ReAct).
   - **Camada 2 (Estado de Sessão)**: Contexto transacional ativo da thread (`.context/CURRENT_STATE.md` / cache rápido).
   - **Camada 3 (Memory Bank de Longo Prazo)**: Cofre Obsidian + MemPalace / banco vetorial/grafo com proveniência, TTL e integridade SHA-256.
5. **Interoperabilidade (`MCP` + `A2A`) e Governança (`HITL`)**:
   - Ferramentas desacopladas em servidores **MCP** (JSON-RPC 2.0 via stdio ou Streamable HTTP) e colaboração entre agentes via **A2A** (`/.well-known/agent-card.json`).
   - Resolução determinística de colisão (`Escopo de Projeto > Escopo de Usuário`) e **Policy Gates HITL** obrigatórios para mutações destrutivas ou externas irreversíveis.

---

### Eixo 2: Critérios de Aprimoramento e Ciclo de Qualidade (*Refinement & Evaluation*)

1. **Avaliação Estruturada (*Eval-Driven Iteration*) e Métricas Formais**:
   - **Baseline vs. Treatment**: Executar `evals/evals.json` com a skill ativada vs. desativada (ou versão anterior), medindo o ganho real ($\Delta\text{Pass Rate}$) contra o custo de latência e tokens.
   - **Estimador Não Enviesado $\text{Pass}@k$**: Medir a probabilidade de gerar ao menos 1 solução funcionalmente correta em $k$ amostras independentes.
   - **Matriz de Confusão para Guardrails**: Em filtros de segurança/injeção com acesso de escrita, calibrar Precisão, Recall e exigir **Taxa de Falsos Negativos $\text{FNR} < 0.001$**.
   - **Juízes `LLM-as-a-Judge` Normalizados ($S_{\text{norm}} \in [0, 100]$)**: Avaliar estrutura, tom e aderência com rubricas ortogonais ponderadas usando modelo de família distinta do gerador para evitar viés de autoavaliação.
2. **Diagnóstico de Trajetórias (`transcript.jsonl`) e *Lean Instructions***:
   - Inspecionar os logs passo a passo da sessão para detectar chamadas improdutivas ou loops.
   - **Instruções baseadas no "Porquê"**: Substituir listas de regras rígidas ("SEMPRE faça X") por explicações causais enxutas, removendo restrições redundantes quando o pass rate estagnar (*over-constraining*).
   - **Empacotamento em `scripts/`**: Extrair qualquer lógica ou parser que o agente reescreva repetidamente em runtime para scripts determinísticos na pasta `scripts/`.
3. **Otimização do Gatilho de Ativação (*Trigger Optimization*)**:
   - Construir matriz de consultas `should-trigger` (variando formalidade, erros de digitação, caminhos e complexidade) e `should-not-trigger` com **casos limítrofes (*near-misses*)** semanticamente próximos.
   - Separar consultas em conjuntos de **Treino e Validação** com múltiplas execuções (*trigger rate*) para impedir overfitting da `description`.
4. **Otimização Programática (`GEPA` / `adk optimize`) e Simulação Multiturno**:
   - Utilizar otimizadores automáticos de prompt/descrição (como o algoritmo **GEPA** via `adk optimize` no Google ADK) guiados pelos relatórios de falha.
   - Empregar simulação sintética de usuário multiturno com personas adversariais para testar recuperação de falhas.
5. **Densidade de Atenção na Janela de Contexto (Softmax)**:
   - Como a autoatenção distribui pesos via $\text{Softmax}(QK^T/\sqrt{d_k})$, tokens irrelevantes inflam a soma exponencial do denominador e diluem o foco nos guardrails. Elimine ruído para manter alta densidade informacional em jornadas de 20 a 50 passos.

---

## 📊 Matriz Resumo de Maturidade (Níveis 1 a 4)

| Dimensão | Nível 1: Monolítico | Nível 2: Produto | Nível 3: Context & Intent Eng. | Nível 4: Specification Eng. |
| :--- | :--- | :--- | :--- | :--- |
| **Arquitetura** | Tudo no System Prompt | Instruções fixas do app | Perfil enxuto + `SKILL.md` + Tools | Grafo Multiagente + Spec Corpus |
| **Contexto** | Envia tudo a cada turno | Janela estática com logs | **Divulgação Progressiva (3 Tiers)** | Filtros semânticos + Roteamento dinâmico |
| **Qualidade** | Empírico ("parece bom") | Testes manuais avulsos | **Evals Baseline/Treatment + Pass@k** | CI/CD Contínuo + LLM-as-a-Judge ($S_{\text{norm}}$) |
| **Integração** | Funções ad-hoc acopladas | Conectores proprietários | **Servidores MCP + SDKs padrão** | Barramento MCP + Protocolo A2A + Registry |

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
1. **Diagnóstico de Maturidade e Gargalos**: Classificação atual (Nível 1 a 4), análise de densidade atencional (Softmax) e falhas de trajetória/gatilho.
2. **Arquitetura de Expansão Recomendada**: Divisão exata em **Tier 1 / Tier 2 / Tier 3**, especificação de **Envelope Pattern**, **Context Forking** e extração para `scripts/`.
3. **Plano de Avaliação Empírica (`evals.json`)**: Definição do protocolo *Baseline vs. Treatment*, matriz de gatilhos (`should-trigger` vs `near-misses`) e metas de $\text{Pass}@k$ / $\text{FNR}$.
4. **Artefato Refatorado (`SKILL.md` ou Código ADK/MCP)**: Implementação modular tipada pronta para homologação no Estágio 3/4 da `evoluir-skills`.
