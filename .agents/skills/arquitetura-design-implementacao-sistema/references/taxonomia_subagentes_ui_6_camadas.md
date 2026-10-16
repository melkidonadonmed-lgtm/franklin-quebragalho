# Taxonomia dos 6 Módulos de UI e Orquestração de Subagentes (`Topologia 3+1`)

Referência canônica de **Tier 3** da skill `arquitetura-design-implementacao-sistema` (sob a persona **`FrontCraftMaster`**). Consolida as 6 especialidades de engenharia visual em **3 Subagentes Construtores + 1 Coordenador Determinístico (`3+1`)**, eliminando colisões de DOM/CSS e integrando a execução em ondas via **Franklin MCP + Epic-Volta DAG**.

---

## 1. Mapa de Roteamento: 6 Especialidades ➔ 4 Subagentes (`agents/*.md`)

| Onda DAG | Subagente (`agents/`) | Módulos Cobertos | Responsabilidade Estrutural |
| :---: | :--- | :--- | :--- |
| **Onda 1** | [`ui-shell-navigator`](../../../agents/ui-shell-navigator.md) | **1. Arquitetura Visual e Layout**<br/>**2. Navegação e Menus** | *UI Islands* (Micro-Frontends / Server-Driven UI), `GridView`/`StackPanel`/`SplitView`/`ViewBox`/`VariableSizedWrapGrid`, `AppWindow` multitela, `Border`/`Shadow DOM`, `MenuBar`/`SelectorBar`/`TabView` lazy, `TreeView` assíncrono, `SemanticZoom` e `Ctrl+K`. |
| **Onda 2A** | [`ui-controls-data`](../../../agents/ui-controls-data.md) | **3. Componentes de Entrada e Ações**<br/>**4. Exibição de Dados e Feedback** | `Button`/`SplitButton`/`CheckBox`/`ToggleSwitch`/`Slider` ($\ge 44\times44\text{px}$, anti-squish, Regra 1+2), `RichEditBox`/`CalendarDatePicker`/`StoragePicker` (WAI-ARIA inline), `ListView`/`ItemsView` virtualizados a $60\text{fps}$, `InfoBar`/`TeachingTips` (`aria-live`) e `IconElement`/`Hyperlink` WCAG AA/AAA. |
| **Onda 2B** | [`ui-motion-interaction`](../../../agents/ui-motion-interaction.md) | **5.1 Efeitos Visuais e Transições**<br/>**5.2 Gestos e Interações** | `ConnectedAnimation`, `ImplicitTransition` e `ThemeTransitions` aceleradas por GPU (`transform`/`opacity`), proteção vestibular `prefers-reduced-motion`, gestos multi-input (`Touch`, `Pen`, `Mouse`, `Keyboard`) e `PullToRefresh`. |
| **Onda 3** | [`ui-deterministic-observer`](../../../agents/ui-deterministic-observer.md) | **5.3 Coordenador Determinístico**<br/>**6. Diretrizes e Boas Práticas** | *State Bus* orientado a eventos, fila determinística de renderização, auditoria WCAG 2.1 AA/AAA ($4.5:1$ / $3:1$), Core Web Vitals ($\text{LCP} < 2.5\text{s}$, $\text{INP} < 200\text{ms}$, $\text{CLS} < 0.1$), Web Workers, Tipagem Estrita + DI (**Hilt**), Cobertura de Testes e **Fidelidade Física de Luz e Sombra**. |

---

## 2. Protocolo do Barramento de Estado (*State Bus*) e Contratos `upstream_mapping`

A comunicação entre as 3 ondas no motor DAG do `epic-volta` ocorre sem compartilhar texto bruto desnecessário, projetando apenas chaves determinísticas via *dot-notation*:

1. **Saída da Onda 1 (`ui_shell_navigator`)**:
   - `ui_shell_navigator.layout_contract`: Regiões de *UI Islands*, grid breakpoints, reservas anti-CLS e fronteiras `Shadow DOM`.
   - `ui_shell_navigator.navigation_contract`: Árvore de rotas, atalhos globais (`Ctrl+K`), slots de `TabView`/`SplitView` e mapa de foco ortogonal.
2. **Saídas Paralelas da Onda 2 (`ui_controls_data` + `ui_motion_interaction`)**:
   - `ui_controls_data.controls_contract`: Alvos $44\times44\text{px}$, anti-squish, Regra 1+2 e validação inline WAI-ARIA.
   - `ui_controls_data.data_feedback_contract`: Virtualização `DOM recycling` a $60\text{fps}$ e regiões `aria-live`.
   - `ui_motion_interaction.motion_contract`: Pipeline GPU (`ConnectedAnimation`, `ImplicitTransition`) e fallback `prefers-reduced-motion`.
   - `ui_motion_interaction.interaction_contract`: Eventos `Touch/Pen/Mouse/Keyboard` e `PullToRefresh`.
3. **Veredito da Onda 3 (`ui_deterministic_observer`)**:
   - Consome todos os 6 contratos acima via `upstream_mapping`, recalcula a fila de renderização no *State Bus* e emite o checklist `[AUDIT-01]` a `[AUDIT-09]`.

---

## 3. Como Acionar na Prática

### Modo A: Modo Nativo Antigravity (`invoke_subagent` / `define_subagent`)
Os 4 subagentes de UI (`ui-shell-navigator`, `ui-controls-data`, `ui-motion-interaction`, `ui-deterministic-observer`) são registrados nativamente em `<subagents>` (`Available subagents`) pelo plugin `franklin-skills` (com `enable_write_tools: true` e `enable_mcp_tools: true`). Para orquestrar as 3 ondas diretamente no Antigravity IDE/CLI:
1. **Onda 1 (Estrutura e Navegação)**: Chame `invoke_subagent(TypeName="ui-shell-navigator", Task="...")` para produzir `layout_contract` e `navigation_contract`.
2. **Onda 2 (Paralela — Controles/Dados e Motion/Gestos)**: Chame em paralelo `invoke_subagent(TypeName="ui-controls-data", Task="...")` e `invoke_subagent(TypeName="ui-motion-interaction", Task="...")` consumindo as regiões da Onda 1.
3. **Onda 3 (Gatekeeper Determinístico)**: Chame `invoke_subagent(TypeName="ui-deterministic-observer", Task="...")` para auditar CWV, WCAG AA/AAA, DI/Tipagem e Física de Luz/Sombra (`[AUDIT-01]` a `[AUDIT-09]`).
4. *Opcional*: Caso deseje instanciar um subagente customizado em tempo de execução com permissões explícitas de escrita, utilize `define_subagent(..., enable_write_tools=True, enable_mcp_tools=True)` antes de `invoke_subagent`.

### Modo B: Modo Motor DAG Assíncrono (`franklin_execute_dag` / `franklin_get_agents` / `epic-volta`)
Para execução assíncrona em ondas com persistência SQLite WAL ou inspeção declarativa dos contratos:
- **Via MCP (`franklin-skills`)**:
  - `franklin_get_agents(agent_name="ui")` (ou individualmente `franklin_get_agents(agent_name="ui-shell-navigator")`) e `agent_spec_loader.py` para carregar os contratos declarativos.
  - `franklin_execute_dag(plan_path_or_json="plans/ui_composition_dag.json", run_id="ui-comp-01")` (ou pelo alias curto `franklin_execute_dag(plan_path_or_json="ui")`).
- **Via CLI do Epic-Volta**:
  ```powershell
  uv --directory C:\Users\melki\dev\repos\epic-volta run python -m orchestrator.cli C:\Users\melki\dev\repos\franklin-quebragalho\plans\ui_composition_dag.json --run-id ui-comp-01
  ```
