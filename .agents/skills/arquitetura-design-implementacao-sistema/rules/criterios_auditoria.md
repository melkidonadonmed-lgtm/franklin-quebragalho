# Critérios Determinísticos de Auditoria (`arquitetura-design-implementacao-sistema` v2.0.0)

Este documento define as regras booleanas falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar entregas da skill `arquitetura-design-implementacao-sistema`.

---

## 1. Regras de Corte Estrutural e Módulos Funcionais

### Regra 1: Desacoplamento de Cores vs. Invariantes Estruturais
- **`[PASS]`**: A especificação arquitetural foca nos 5 módulos funcionais (Navegabilidade, Ilhas Funcionais, Crítica Severa de MVP, Zero Hardcode/SRP e Tipografia Linear), delegando paletas cromáticas cosméticas para `DESIGN.md` e usando cores no diagrama exclusivamente para semântica de diff (`V1 -> V2`).
- **`[FAIL: POLUICAO_COSMETICA_NO_CONTRATO]`**: A arquitetura mistura dezenas de hexadecimais de temas cosméticos com regras de negócio, diluindo o contrato estrutural.

### Regra 2: Navegabilidade, Regra dos 3 Cliques e 4 Estados de UI (`INE`)
- **`[PASS]`**: Todas as ações de valor primário exigem $\le 3$ cliques a partir do Dashboard, possuem atalho global `Ctrl+K`/`Cmd+K` sem `alert()`/`confirm()` nativo, grafo Mermaid com diagnóstico comentado nó a nó e mapeamento explícito dos 4 estados (`Empty`, `Loading`, `Success`, `Error`).
- **`[FAIL: ROTA_ORFA_OU_ESTADOS_INCOMPLETOS]`**: Presença de becos sem saída (*dead-ends*), profundidade $> 3$ cliques sem justificativa ou omissão dos 4 estados de UI.

### Regra 3: Aglomeração Funcional por Ilha e Isolamento Data/Render (`ICI`)
- **`[PASS]`**: Ferramentas de mesma micro-intenção estão agrupadas em Ilhas Funcionais autocontidas ($\le 2$ domínios e $\le 7$ controles interativos primários por ilha), com separação estrita entre *data tools* e *render tools* e blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap`).
- **`[FAIL: ILHA_SOBRECARREGADA_OU_ACOPLADA]`**: Botões da mesma tarefa espalhados em extremidades opostas da tela ou componentes de UI executando queries/fetch direto sem camada de serviço.

### Regra 4: Crítica Severa de MVP e Zero Hardcode (`IRM` & `IPC`)
- **`[PASS]`**: Funcionalidades não essenciais para validar a hipótese da Semana 1 são cortadas explicitamente como `[CORTE OBRIGATÓRIO - FASE 2]`, e zero strings de configuração, URLs ou magic numbers estão chumbados na camada de UI.
- **`[FAIL: BLOAT_MVP_OU_HARDCODE]`**: Aprovação passiva de escopo inchado na Fase 1 ou presença de valores mágicos/URLs hardcoded em componentes visuais.

### Regra 5: Tipografia Linear e Cálculo Determinístico Sem Placebo (`ICTE` & `SGA`)
- **`[PASS]`**: Escala tipográfica fluida via `clamp()` com pareamento em 3 camadas (Display + Body $\le 65\text{ch}$ + Monospace `tabular-nums`) e cálculo aberto do `SGA` (`INE`, `ICI`, `IPC`, `IRM`, `ICTE`) via `deterministic_scorer.py` ( più relatório HTML `V1 vs V2` com `<meta>` tags quando em Modo de Resolução).
- **`[FAIL: SCORE_PLACEBO_OU_TIPOGRAFIA_FIXA]`**: Atribuição de nota inventada sem memória de cálculo determinística ou ausência dos metadados obrigatórios no HTML de resolução.
