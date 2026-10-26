# Critérios Determinísticos de Auditoria (`nav-x-func` v4.0.0)

Este documento define as regras booleanas falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar entregas da skill `nav-x-func`.

---

## 1. Regras de Corte Estrutural, Navegação Real e Suficiência Funcional

### Regra 1: Desacoplamento de Cores vs. Invariantes Estruturais
- **`[PASS]`**: A especificação arquitetural foca nos módulos funcionais (Navegabilidade Real, Ilhas Funcionais, Crítica Severa de MVP `CLAREZA/CREATE`, Suficiência Funcional TIF, Zero Hardcode/SRP e Tipografia Linear), delegando paletas cromáticas para `DESIGN.md` e usando cores no diagrama exclusivamente para semântica de diff (`V1 -> V2`).
- **`[FAIL: POLUICAO_COSMETICA_NO_CONTRATO]`**: A arquitetura mistura dezenas de hexadecimais de temas cosméticos com regras de negócio, diluindo o contrato estrutural.

### Regra 2: Navegabilidade Real (`Clicar em X ativa Y?`), Dead Ends, Regra dos 3 Cliques e 4 Estados (`INE`)
- **`[PASS]`**: Todas as ações de valor primário exigem $\le 3$ cliques a partir da entrada, possuem atalho global `Ctrl+K`/`Cmd+K` sem `alert()`/`confirm()` nativo, cada botão dispara ação real com *loading/debounce* (`X ativa Y`), toda tela interna possui caminho de retorno explícito (`Voltar`/`Esc`), há grafo Mermaid comentado nó a nó e mapeamento dos 4 estados (`Empty`, `Loading`, `Success`, `Error`).
- **`[FAIL: ROTA_ORFA_DEAD_END_OU_BOTAO_INERTE]`**: Presença de becos sem saída (*dead-ends*), botões inertes (`TODO`, `console.log`, `pass`, `"Em breve"`), profundidade $> 3$ cliques sem justificativa ou omissão dos 4 estados de UI.

### Regra 3: Aglomeração Funcional por Ilha, Purga de Pseudo-Complexidade e Isolamento Data/Render (`ICI`)
- **`[PASS]`**: Ferramentas de mesma micro-intenção estão agrupadas em Ilhas Funcionais autocontidas ($\le 2$ domínios e $\le 7$ controles interativos primários por ilha), elementos puramente cosméticos são cortados (Lei de Hick-Hyman), há separação estrita entre *data tools* e *render tools* e blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap`).
- **`[FAIL: ILHA_SOBRECARREGADA_OU_PSEUDO_COMPLEXIDADE]`**: Botões da mesma tarefa espalhados em extremidades opostas da tela, excesso de ornamentos sem função real ou componentes de UI executando queries/fetch direto sem camada de serviço.

### Regra 4: Crítica Severa de MVP (`CLAREZA/CREATE`) e Zero Hardcode (`IRM` & `IPC`)
- **`[PASS]`**: Funcionalidades não essenciais para validar a hipótese da Semana 1 são cortadas explicitamente como `[CORTE OBRIGATÓRIO - FASE 2]`, e zero strings de configuração, URLs ou magic numbers estão chumbados na camada de UI.
- **`[FAIL: BLOAT_MVP_OU_HARDCODE]`**: Aprovação passiva de escopo inchado na Fase 1 ou presença de valores mágicos/URLs hardcoded em componentes visuais.

### Regra 5: Suficiência Funcional — Meios Implementados vs. Fins Prometidos (`TIF`)
- **`[PASS]`**: A Tabela de Integridade Funcional (TIF) comprova que o sistema possui os meios técnicos e operacionais necessários para cumprir a categoria prometida (déficit de suficiência $\le 50\%$).
- **`[FAIL: ALUCINACAO_FUNCIONAL_DO_PROJETO]`**: Distância entre os meios implementados e os meios essenciais exigidos pela categoria prometida superior a $50\%$ sem reposicionamento de escopo ou plano imediato de implementação.

### Regra 6: Tipografia Linear e Cálculo Determinístico Sem Placebo (`ICTE` & `SGA`)
- **`[PASS]`**: Escala tipográfica fluida via `clamp()` com pareamento em 3 camadas (Display + Body $\le 65\text{ch}$ + Monospace `tabular-nums`) e cálculo aberto do `SGA` (`INE`, `ICI`, `IPC`, `IRM`, `ICTE`) via `deterministic_scorer.py` (mais relatório HTML `V1 vs V2` com `<meta>` tags quando em Modo de Resolução).
- **`[FAIL: SCORE_PLACEBO_OU_TIPOGRAFIA_FIXA]`**: Atribuição de nota inventada sem memória de cálculo determinística ou ausência dos metadados obrigatórios no HTML de resolução.
