---
name: aprimoramento-expansibilidade-agentes-skills
description: >-
  Arquiteto de sistemas multiagentes em código (Google ADK Go/Python/TS, MCP Spec 2026-07-28, Protocolo A2A, Envelope Pattern, Context Forking, Theranostic Confidence Gate, Provenance HMAC e Memória em 3 Camadas). Use quando o usuário pedir para projetar, escalar ou otimizar a arquitetura de agentes de software, pipelines determinísticos (Gate Chain / Sandbox Go), roteadores híbridos ou suítes de avaliação de agentes (Pass@k, FNR < 0.001, GEPA). Não use para criar ou refatorar arquivos SKILL.md do catálogo de skills (use evoluir-skills ou skill-auditor-refatorador-skills).
license: MIT
metadata:
  version: "2.1.0"
  author: "SkillCraft & Melki"
  category: "Arquitetura, Expansibilidade e Avaliação de Agentes"
  updated_at: "2026-10-17"
  tags:
    - "arquitetura-agentes"
    - "google-adk"
    - "mcp-a2a"
    - "theranostic-pipeline"
    - "pass-at-k"
    - "envelope-pattern"
    - "context-forking"
version: 2.1.0
updated_at: 2026-10-17
author: SkillCraft & Melki
category: Arquitetura, Expansibilidade e Avaliação de Agentes
---

# Arquitetura, Expansibilidade e Engenharia de Sistemas Multiagentes (`v2.1.0`) 🧠

Skill de arquitetura de **Agentes de Software em Código** (**Google ADK Go v2**, **ADK Python/TypeScript**, **MCP 2026-07-28** e **A2A**).

> [!NOTE]
> **Fronteira Limpa:** Esta skill projeta **sistemas agênticos e harnesses de código** (`go_agent/`, `py_agent/`, `ts-agent/`). Para criar ou evoluir pacotes `SKILL.md`, use **`evoluir-skills`**; para auditar ou enxugar skills existentes, use **`skill-auditor-refatorador-skills`**.
> Para fórmulas matemáticas completas ($\text{Pass}@k$, $\text{FNR}$, $S_{\text{norm}}$, Softmax) e schemas Pydantic, consulte [`references/guia_expansibilidade_e_metricas_2026.md`](references/guia_expansibilidade_e_metricas_2026.md).

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Projetar ou escalar agentes em **Google ADK (Go, Python ou TypeScript)**, definindo topologias sequenciais, paralelas, em loop ou roteadores híbridos (`HybridDispatcher`).
- Implementar padrões avançados de **Harness & Context Engineering**:
  - **AI-Ready Multimodal Data Pipeline** (higienização Unicode NFC, chunking com overlap de 10–15% e atribuição SHA-256).
  - **Declarative YAML Agent Spec com MCP** (`agent_spec.yaml` + Circuit Breaker determinístico).
  - **Cryptographic Content Provenance Guardrail** (manifesto assinado via `HMAC-SHA256` + verificação `compare_digest`).
  - **Theranostic Diagnostic-to-Action Pipeline** (Agente Analisador Read-Only $\rightarrow$ `ConfidenceGate >= 0.95` $\rightarrow$ Agente Intervencionista assinado).
  - **Cluster Determinístico A2A + MCP JSON-RPC 2.0 (`AgyCalcCluster`)** (separação estrita entre extração cognitiva e execução matemática Zero-LLM em Go com OTel Ledger).
- Desenhar suítes de avaliação estatística de agentes ($\text{Pass}@k$, Paired $t$-test, Token Efficiency Index $\text{TEI}$, $\text{FNR} < 0.001$ e `adk optimize` / GEPA).

## 🚫 Quando NÃO Usar
- **Não usar** para criar pastas `.agents/skills/<slug>/` ou redigir `SKILL.md` (use `evoluir-skills`).
- **Não usar** para auditar ou refatorar skills do catálogo (use `skill-auditor-refatorador-skills`).
- **Não usar** para auditoria visual de interfaces frontend (use `analise-design-tatil-frontend`).

---

## 📥 Entradas Obrigatórias e Pré-requisitos
- `target_system` (obrigatório): Repositório ou módulo do agente (ex.: `go_agent/`, `py_agent/`, `ts-agent/`, `epic-volta/`).
- `scaling_vector` (obrigatório): Padrão arquitetural desejado (`MultimodalDataPipeline`, `DeclarativeAgentSpec`, `ProvenanceGuardrail`, `TheranosticPipeline`, `AgyCalcCluster` ou `EvalHarness`).

---

## ⚙️ Os 3 Pilares da Arquitetura de Agentes (Padrão 2026)

### Pilar 1: Topologia de Execução, Isolamento e Interoperabilidade (`ADK` + `MCP` + `A2A`)
1. **Separação entre Julgamento Cognitivo e Trabalho Determinístico**:
   - O LLM nunca calcula, nunca faz parsing mecânico pesado e nunca decide permissões de segurança sozinho.
   - Use **Subagente Diagnóstico (Extrator JSON)** $\rightarrow$ **Gate Chain Determinístico** $\rightarrow$ **Executor Sandbox Go/Python (Zero-LLM)** $\rightarrow$ **Subagente Observador/Crítico** (`AgyCalcCluster`).
2. **Padrão Envelope (*Action Routing*) e Context Forking**:
   - Exponha interfaces polimórficas mestre (`action` + `params`) para evitar dezenas de tools granulares diluindo a atenção Softmax ($\text{Softmax}(QK^T/\sqrt{d_k})$).
   - Tarefas pesadas rodam em subagentes com fatia de estado isolada (*Context Slicing*), devolvendo apenas o artefato assinado.
3. **Declarative YAML Spec & Circuit Breaker**:
   - Centralize modelo (`gemini-3.8-flash` / fallback `gemini-3.5-flash-lite`), `ThinkingLevel`, servidores MCP, `allowed_tools` e limites de disjuntor (`CLOSED -> OPEN -> HALF_OPEN`) em manifesto YAML auditável (`agent_spec.yaml`).

### Pilar 2: Segurança, Proveniência e Apoio à Decisão Crítica
1. **Theranostic Diagnostic-to-Action Pipeline**:
   - **Estágio 1 (Read-Only Analyzer)**: Bloqueia ferramentas mutáveis em código (`ReadOnlyViolationError`) e emite laudo com `confidence_score` e diagnósticos diferenciais.
   - **Estágio 2 (Confidence Gate)**: Se `confidence_score < 0.95`, congela a esteira em `FROZEN_FOR_HUMAN_VALIDATION` (HITL obrigatório).
   - **Estágio 3 (Action Agent)**: Disparado exclusivamente após aprovação do portão.
2. **Cryptographic Content Provenance (`HMAC-SHA256`)**:
   - Toda saída crítica ou intervenção recebe `ProvenanceManifest` (`model_id`, `output_sha256`, `operator_id`, `timestamp_utc`) assinado com chave privada e verificável em tempo constante.
3. **Memória em 3 Camadas**:
   - *Camada 1*: Scratchpad transitório da tarefa.
   - *Camada 2*: Sessão transacional em SQLite WAL (`adk_sessions.db` / `.context/CURRENT_STATE.md`).
   - *Camada 3*: Longo prazo no Cofre Obsidian + MemPalace com chunks higienizados e hash SHA-256.

### Pilar 3: Engenharia de Avaliação Concorrente (*Eval Harness A vs B*)
1. **Métricas Determinísticas Obrigatórias**:
   - Compare **Estratégia A (Baseline)** vs. **Estratégia B (Candidate)** concorrentemente com múltiplas seeds:
     - $\text{Pass}@1$ e $\text{Pass}@k$ não enviesado.
     - Teste $t$ pareado (*Paired t-Stat*) para significância estatística.
     - **TEI (*Token Efficiency Index*)**: razão entre taxa de sucesso e consumo de tokens.
   - Para guardrails de segurança, exija **Taxa de Falsos Negativos $\text{FNR} < 0.001$**.

---

## 📤 Modelo de Saída
1. **Diagrama e Contrato Arquitetural**: Topologia dos agentes, fatias de estado (*Context Slices*), protocolo (`MCP` / `A2A`) e portas de segurança (`ConfidenceGate`, `CircuitBreaker`, `GateChain`).
2. **Implementação Modular (`<= 300` linhas por arquivo)**: Código tipado em Go, Python ou TypeScript pronto para execução.
3. **Verificação Empírica**: Testes unitários + execução do Eval Harness (`npm run local:gate`).
