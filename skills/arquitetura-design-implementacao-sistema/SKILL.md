---
name: arquitetura-design-implementacao-sistema
description: >-
  Executa diagnóstico severo de MVP, arquitetura de navegabilidade comentada, aglomeração funcional por ilhas (Island UI/UX), especificação tipográfica linear, alinhamento de atmosfera ao propósito do sistema, auditoria anti-hardcode e plano de implementação modular com score determinístico e histórico comparativo V1 vs V2 em HTML com metadados.
license: MIT
metadata:
  author: "Franklin-Main & Melki"
  version: "3.0.0"
  category: "Arquitetura de Sistemas, Navegabilidade Funcional & Auditoria Determinística"
  updated_at: "2026-10-19"
  tags:
    - "system-architecture"
    - "island-architecture"
    - "mvp-critique"
    - "deterministic-audit"
    - "typography-scale"
version: 3.0.0
updated_at: 2026-10-19
author: Franklin-Main & Melki
category: Arquitetura de Sistemas, Navegabilidade Funcional & Auditoria Determinística
---

# Arquitetura de Sistemas, Navegabilidade Comentada, Ilhas Funcionais e Implementação Determinística (`v3.0.0`)

Transforma requisitos de produto ou sistemas existentes (`V1`) em uma **Arquitetura Modular de Alta Coesão (`V2`)**, validada por **cálculo determinístico de prontidão** e **histórico comparativo auditável em HTML**. A escolha estética de atmosfera e estilo nunca usa paletas fixas engessadas: ela deriva do **propósito do sistema** via `DESIGN.md` e [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md).

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Projetar a arquitetura completa de um sistema antes de codificar, exigindo **crítica severa de MVP** (corte de excessos) e **aglomeração funcional por ilhas**.
- Diagnosticar e refatorar um sistema existente (`V1 -> V2`) com **relatório HTML autocontido** contendo metadados auditáveis e **diagrama de diff estrutural**.
- Auditar navegabilidade (Regra dos $\le 3$ cliques, `Ctrl+K`, 4 estados de tela), desacoplamento zero-hardcode e hierarquia tipográfica linear (`clamp()`, `tabular-nums`).

### 🚫 Quando NÃO Usar (Fronteira Estrita)
- Para escolher apenas temas ou tokens CSS isolados sem escopo de arquitetura de sistema (use **`design-md`**).
- Para auditar exclusivamente higiene de Git e arquivos órfãos (use **`auditoria-projetos-sistema`**).

---

## 📥 Entradas Esperadas
1. **`escopo_ou_codigo_fonte` (Obrigatório):** Ideia bruta, PRD, árvore de arquivos ou código da versão atual (`V1`).
2. **`modo_operacao` (Opcional, padrão: `arquitetura_nova`):**
   - `arquitetura_nova`: Crítica de MVP + Ilhas Funcionais + Plano de Implementação Modular + Score Determinístico.
   - `resolucao_v1_v2`: Diagnóstico comparativo `V1 vs V2` + Score Determinístico de Evolução ($\Delta$) + Relatório HTML com `<meta>` tags e diagrama de diff.
3. **`restricoes_stack` (Opcional):** Stack alvo (ex.: Next.js/React + TypeScript, Python FastAPI/ADK, Go, SQLite/Postgres).

---

## ⚙️ Fluxo de Execução (5 Módulos Estruturais)

### Passo 1: Crítica Severa de MVP e Alinhamento ao Propósito (`IRM` — Peso 20%)
1. Identifique a **Hipótese Central de Valor** e o **Propósito Cognitivo do Sistema** (*Conversão/SaaS*, *Editorial*, *FinTech*, *IA Nativa*, *MedTech* ou *DevTools/Terminal IBM*).
2. Classifique cada funcionalidade em:
   - `[ESSENCIAL - SEMANA 1]`: Indispensável para o fluxo primário funcionar de ponta a ponta.
   - `[CORTE OBRIGATÓRIO - FASE 2]`: Complexidade prematura que deve ser removida do MVP.
   - `[RISCO ARQUITETURAL]`: Acoplamento oculto, falta de idempotência ou gargalo de estado.

### Passo 2: Aglomeração Funcional por Ilhas — *Island Architecture* (`ICI` — Peso 25%)
Consulte os contratos detalhados em [`references/protocolo_ilhas_tipografia_e_resolucao_html.md`](references/protocolo_ilhas_tipografia_e_resolucao_html.md):
- **Proximidade Semântica (Lei de Fitts):** Ferramentas que operam sobre o mesmo objeto de domínio residem na **mesma Ilha Funcional autocontida** ($\le 2$ domínios e $\le 7$ controles interativos por ilha).
- **Isolamento de Estado e Falha:** Cada ilha gerencia seus 4 estados (`Empty`, `Loading`, `Success`, `Error`) de forma independente, com blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap`, alvos $\ge 44\times44\text{px}$).
- **Separação Data vs. Render:** Ações de mutação/busca (*data tools*) nunca ficam misturadas com lógica de apresentação (*render tools*).

### Passo 3: Arquitetura de Navegabilidade Comentada (`INE` — Peso 25%)
- **Regra dos $\le 3$ Cliques e Atalho Global (`Ctrl+K` / `Cmd+K`):** Nenhuma ação primária pode exigir mais de 3 cliques a partir da entrada. Proibido usar `window.alert()` ou `window.confirm()` bloqueantes.
- **Grafo Mermaid Comentado Nó a Nó:** Todo fluxo de navegação deve ser acompanhado de uma **Tabela de Diagnóstico por Nó** explicando responsabilidade, gatilho de entrada, saída e tratamento de falha.

### Passo 4: Tipografia Linear, Espaçamento, Camadas e Pureza Anti-Hardcode (`IPC` 15% + `ICTE` 15%)
- **Escala Tipográfica Linear e Hierarquia (`ICTE`):**
  - **Camada 1 — Display / H1-H2:** `clamp()` fluido, `letter-spacing: -0.03em`, `line-height: 1.1`.
  - **Camada 2 — Body / Leitura:** `1rem` (`16px`), `line-height: 1.6`, largura máxima de linha travada em **`60ch–70ch`**.
  - **Camada 3 — Telemetria / Dados / Atalhos:** Fonte monoespaçada (`IBM Plex Mono` / `JetBrains Mono`) com **`font-variant-numeric: tabular-nums` obrigatório** em preços, contadores, tabelas, IDs e timestamps.
- **Pureza Arquitetural e Zero Hardcode (`IPC`):** Proibido chumbar URLs, limites de paginação, textos de domínio ou chaves de configuração dentro de componentes visuais. Cada módulo respeita o **Princípio da Responsabilidade Única (SRP)**.

### Passo 5: Cálculo Determinístico (`SGA`) e Modo de Resolução HTML (`V1 -> V2`)
Execute [`scripts/deterministic_scorer.py`](scripts/deterministic_scorer.py) para calcular o **Score Global de Arquitetura (`SGA`)**:

$$\text{SGA} = 0.25 \cdot \text{INE} + 0.25 \cdot \text{ICI} + 0.20 \cdot \text{IRM} + 0.15 \cdot \text{IPC} + 0.15 \cdot \text{ICTE}$$

Quando em **`modo_operacao="resolucao_v1_v2"`**, gere também o artefato HTML autocontido seguindo o template de [`references/protocolo_ilhas_tipografia_e_resolucao_html.md`](references/protocolo_ilhas_tipografia_e_resolucao_html.md).

---

## 📤 Saídas e Entregáveis
Emitir o **Dossiê de Arquitetura e Implementação Modular** e validar cada entrega contra [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md). Para orquestração de subagentes de interface, consulte [`references/taxonomia_subagentes_ui_6_camadas.md`](references/taxonomia_subagentes_ui_6_camadas.md).
