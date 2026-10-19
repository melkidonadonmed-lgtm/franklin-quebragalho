---
name: aprimoramento-expansibilidade-agentes-skills
description: >-
  Arquiteto de sistemas agênticos, seleção de frameworks, contratos de tools Pydantic/MCP 2026-07-28, despacho polimórfico (Envelope Pattern) e auditoria matemática (Pass@k, D_cos, FNR<0.001, Snorm, TEI). Use para projetar agentes de software, escolher frameworks ou rodar auditoria matemática; não use para editar SKILL.md do catálogo (use evoluir-skills ou skill-auditor-refatorador-skills).
license: MIT
metadata:
  version: "2.2.0"
  author: "SkillCraft & Melki"
  category: "Arquitetura, Expansibilidade e Avaliação de Agentes"
  updated_at: "2026-10-19"
  tags:
    - "arquitetura-agentes"
    - "google-adk"
    - "mcp-2026-07-28"
    - "pass-at-k"
    - "tei-score"
    - "envelope-pattern"
    - "context-forking"
version: 2.2.0
updated_at: 2026-10-19
author: SkillCraft & Melki
category: "Arquitetura, Expansibilidade e Avaliação de Agentes"
---

# Arquitetura de Sistemas Agênticos, Frameworks, Tools, MCP & Auditoria Matemática (`v2.2.0`) 🧠

Fonte Única de Verdade (SSOT) para engenharia de **Agentes em Código**, **Seleção de Frameworks**, **Contratos Determinísticos de Tools (`Pydantic` / `MCP 2026-07-28`)** e **Auditoria Matemática (`Pass@k`, `D_cos`, `FNR`, `S_norm`, `TEI`)**.

> [!NOTE]
> **Fronteira Limpa (Zero Redundância):**
> - Esta skill governa **sistemas agênticos, runtimes, tools e métricas matemáticas**.
> - Para criar ou evoluir pacotes `SKILL.md`, use **`evoluir-skills`**.
> - Para auditar ou enxugar skills existentes contra o Checklist Mestre, use **`skill-auditor-refatorador-skills`**.
> - Consulte os **5 Módulos Técnicos Completos** em [`references/guia_expansibilidade_e_metricas_2026.md`](references/guia_expansibilidade_e_metricas_2026.md).

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Escolher entre **Prompt/Schema**, **Skill**, **Tool**, **Workflow Determinístico**, **Agente Único** ou **Multiagente**, e selecionar o framework ideal (`SDK direto`, `LangChain`, `LangGraph`, `LlamaIndex`, `CrewAI`, `AutoGen v0.4`, `Semantic Kernel`, `Microsoft Agent Framework` ou `Google ADK 2.x`).
- Implementar contratos seguros de **Tools e Despacho Polimórfico** (`Pydantic v2` com `ConfigDict(extra="forbid")` $\rightarrow$ `JSON Schema 2020-12` $\rightarrow$ `PolyExtensibleSkillEngine` com injeção dinâmica de sub-schemas e `recovery_hint`) ou servidores **MCP Python SDK 2.x** (`stdio` / `Streamable HTTP` com `OAuth 2.1` e `Resource Indicators`).
- Projetar o **Loop Cognitivo em 8 Passos**, **5 Camadas de Memória**, **11 Modos de Falha e Controles**, **Theranostic Gate (`Confidence >= 0.95`)** e **Proveniência Criptográfica (`HMAC-SHA256`)**.
- Executar a suíte de **Auditoria Matemática de Agentes** via `scripts/agentic_math_and_engine_auditor.py` ($\text{Pass}@k$ iterativo estável, Distância de Cosseno $D_{\cos} \le 0.18$, Matriz de Confusão $\text{FNR} < 0.001$, Juiz Sintético $S_{\text{norm}} \in [0,100]$ e Índice de Eficiência de Tokens $\text{TEI}$).

## 🚫 Quando NÃO Usar
- **Não usar** para criar pastas `skills/<slug>/` ou redigir `SKILL.md` do zero (use `evoluir-skills`).
- **Não usar** para auditar ou desacoplar skills do catálogo (use `skill-auditor-refatorador-skills`).
- **Não usar** para auditoria visual de interfaces frontend (use `analise-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `target_system` (obrigatório): Sistema, módulo do agente ou conjunto de métricas a projetar/auditar.
- `architecture_module` (opcional): Módulo específico a acionar (`Módulo A: Frameworks & Ontologia`, `Módulo B: Loop Cognitivo & Memória`, `Módulo C: Tools, Envelope & MCP`, `Módulo D: Zero-Trust & Theranostic Gate`, `Módulo E: Auditoria Matemática`).

---

## ⚙️ Fluxo Arquitetural por Módulo (5 Módulos Canônicos)

### Módulo A: Distinção Ontológica e Escolha de Framework
1. **Regra do Gargalo Dominante**:
   - Se os passos já são conhecidos $\rightarrow$ **Workflow Determinístico** (Python/SQL/Grafo).
   - Se a IA esquece o procedimento $\rightarrow$ **Skill** (`SKILL.md`).
   - Se a IA precisa ler/alterar sistema externo $\rightarrow$ **Tool Tipada / MCP**.
   - Se exige observar resultados e adaptar o plano $\rightarrow$ **Agente Único Limitado** (só escale para **Multiagente** após benchmark comprovar ganho real sem cascata de erros).
2. Consulte a **Matriz de Frameworks (Notas 0–3)** e a **Sequência de Maturidade (Níveis 0 a 7)** na Seção 1 de [`references/guia_expansibilidade_e_metricas_2026.md`](references/guia_expansibilidade_e_metricas_2026.md).

### Módulo B: Loop Cognitivo em 8 Passos e 5 Camadas de Memória
1. **Loop Cognitivo**: *(1) Percepção $\rightarrow$ (2) Construção de Contexto $\rightarrow$ (3) Planejamento/Política $\rightarrow$ (4) Validação Pré-Ação $\rightarrow$ (5) Execução no Runtime $\rightarrow$ (6) Observação Normalizada $\rightarrow$ (7) Avaliação de Pós-Condição $\rightarrow$ (8) Persistência Seletiva*.
2. **Separação Estrita de Memória**: Nunca trate a memória do agente (*Turno, Trabalho, Curto Prazo, Longo Prazo*) como **Fonte de Verdade**; releia dados críticos (pedidos, agenda, prontuário, saldo) diretamente do banco/API transacional antes de decidir ou escrever.

### Módulo C: Contratos de Tools, Envelope Polimórfico e MCP 2026-07-28
1. **Despacho Polimórfico (`PolyExtensibleSkillEngine`)**:
   - Exponha uma interface mestre (`action`, `organization_id`/`target`, `parameters`) para evitar dezenas de tools granulares diluindo a atenção Softmax ($\text{softmax}(QK^T/\sqrt{d_k})V$).
   - Valide sub-schemas dinamicamente com `ConfigDict(extra="forbid")` e devolva `expected_schema` + `recovery_hint` em caso de `ValidationError`.
2. **Protocolo MCP (`2026-07-28`)**:
   - Núcleo *stateless*: estado de tarefas longas trafega por identificadores explícitos (`job_handle`, `cursor`).
   - Autorização HTTP via **OAuth 2.1 com Resource Indicators e Audience Binding**; em `stdio`, credenciais vêm do ambiente e **nenhum log pode ir para `stdout`**.

### Módulo D: Defesa Zero-Trust, `Context Forking` e `Theranostic Gate`
1. **Carregador Declarativo (`scripts/agent_spec_loader.py`)**: Instancia manifestos YAML com defaults seguros de modelo, guardrails e servidores MCP.
2. **Theranostic Pipeline & Proveniência**: Subagente Read-Only $\rightarrow$ `ConfidenceGate >= 0.95` (abaixo disso congela em `FROZEN_FOR_HUMAN_VALIDATION`) $\rightarrow$ Subagente Executor assinado com `HMAC-SHA256`.

### Módulo E: Auditoria Matemática Determinística (`scripts/agentic_math_and_engine_auditor.py`)
Execute o motor matemático para validar qualquer arquitetura agêntica:
```powershell
uv run python skills/aprimoramento-expansibilidade-agentes-skills/scripts/agentic_math_and_engine_auditor.py --self-test
```
Calcula deterministicamente: $\text{Pass}@k$ iterativo sem overflow, Distância de Cosseno ($D_{\cos} \le 0.18$), Matriz de Confusão ($\text{FNR} < 0.001$), Juiz Sintético Ponderado ($S_{\text{norm}} \in [0, 100]$) e Índice de Eficiência de Tokens ($\text{TEI}$).

---

## 🛡️ Orçamento Operacional, Limites e Armadilhas (*Gotchas*)

### Orçamento Operacional Padrão de Produção
```yaml
max_steps: 12
max_tool_calls: 20
max_parallel_calls: 4
deadline_seconds: 90
max_retries_per_operation: 2
fnr_security_threshold: 0.001
semantic_drift_threshold_tau: 0.18
```

### Armadilhas Conhecidas (*Gotchas*)
- **Efeito Duplicado em Retries**: Nunca repita chamadas de escrita sem `idempotency_key` e verificação *read-after-write*; erros de schema pedem correção de argumento, não backoff cego.
- **Colapso *Lost-in-the-Middle***: Posicione invariantes determinísticas e contratos de saída imediatamente antes da barreira final de predição, delimitados por tags XML assimétricas.
- **MCP não é Barramento de Memória**: O MCP padroniza conexão e descoberta (`tools/list`, `tools/call`); a persistência e resolução de conflitos temporais pertencem ao Store/DB da aplicação.

---

## 📤 Modelo de Saída
1. **Decisão Arquitetural e Topologia**: Escolha justificada do artefato (Workflow vs Tool vs Skill vs Agente), framework, camadas de memória e orçamento operacional.
2. **Implementação Executável (`<= 300` linhas/arquivo)**: Código tipado (`Pydantic v2` / `MCP` / `ADK`) com registro fechado de tools e erros acionáveis.
3. **Laudo Matemático Determinístico**: Resultados verificados de $\text{Pass}@k$, $D_{\cos}$, $\text{FNR}$, $S_{\text{norm}}$ e $\text{TEI}$.
