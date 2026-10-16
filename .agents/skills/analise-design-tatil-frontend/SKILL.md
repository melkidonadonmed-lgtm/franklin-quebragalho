---
name: analise-design-tatil-frontend
description: >-
  Inspeciona e audita interfaces frontend (via agent-browser ou codigo estatico), orquestra os 4 subagentes de UI (Topologia 3+1: ui-shell-navigator, ui-controls-data, ui-motion-interaction, ui-deterministic-observer), analisa menus, sidebar, tipografia, fontes, icones, tamanho dos botoes, transicoes, layout, profundidade tatil e conformidade estrita com o Google HTML/CSS Style Guide e Google JSON Guide, emitindo um Relatorio Comparativo deterministico.
license: MIT
metadata:
  version: "1.2.0"
  author: "FrontCraftMaster & Melki"
  category: "Design System Tátil e Frontend"
  updated_at: "2026-10-16"
  tags:
    - "design-tatil"
    - "auditoria-ui"
    - "anti-cobalto"
    - "ergonomia"
    - "multidimensional-2026"
    - "subagentes-ui-3+1"
version: 1.2.0
updated_at: 2026-10-16
author: FrontCraftMaster & Melki
category: Design System Tátil e Frontend
---

# 1. NOME DA SKILL
`analise-design-tatil-frontend` (Diagnóstico Estrutural de Frontend, Inspeção Visual, Motor Multidimensional 2026, Auditoria Google Style Guides e Relatório Comparativo de Preferências).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative esta skill sempre que:
- O usuário solicitar: "analise o frontend deste projeto", "compare o design atual com minhas preferências", "mapeie menus, botões e fontes", "audite a interface do app sem alterar o código", "verifique a conformidade com o Google Style Guide no frontend".
- Antes de iniciar qualquer refatoração de frontend, para levantar o baseline exato do projeto.
- Para verificar se uma interface respeita o espaçamento nobre de menus, alvos de clique ergonômicos, fontes adequadas, banimento de azul cobalto neon e regras do Google HTML/CSS.
- Quando for necessário inspecionar uma aplicação em execução via `agent-browser` ou código HTML/CSS estático gerando um relatório em tabela determinística (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).

### Quando NÃO Usar
- Para aplicar alterações, mutações ou correções de código CSS/JS (utilize `refatoracao-design-tatil-frontend`).
- Para auditorias genéricas de repositório Git ou checagem de backend sem interface (utilize `auditoria-projetos-sistema`).
- Para tarefas de infraestrutura ou pipelines de dados.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_url_or_path` (obrigatório): URL ativa da aplicação (ex.: `http://localhost:3000`, `http://localhost:5173`) ou caminho do arquivo HTML local (ex.: `C:\Users\melki\dev\repos\frontcraft-studio\index.html`).
- `inspection_mode` (opcional): `live_browser` (via `agent-browser`) ou `static_code` (análise de arquivos em disco). Padrão: detecção automática (se URL acessível, `live_browser`; se arquivo estático, `static_code`).
- `output_report_path` (opcional): Caminho para salvar o relatório Markdown gerado (padrão: `.context/RELATORIO_ANALISE_FRONTEND.md` no projeto alvo).

---

## 4. DIRETRIZES DE INSPEÇÃO PONTO A PONTO (PREFERÊNCIAS MELKI & GOOGLE)

A análise avalia rigorosamente os 10 pontos críticos de design tátil, motor multidimensional `v2.6.0-2026` e padrões de código:

### 4.1. Menus e Navegação
- **Anti-Compactação:** Proibição de menus colapsados ou espremidos com padding claustrofóbico.
- **Espaçamento Nobre:** Espaçamento mínimo entre itens de navegação (`gap >= 0.75rem` / `12px`), padding interno respirável (`padding >= 0.6rem 1rem`).
- **Respiro e Legibilidade:** Títulos de menu sem quebra forçada de linha e rótulos claros.

### 4.2. Sidebar (Barra Lateral)
- **Largura Mínima Operacional:** No estado expandido, a sidebar deve possuir largura de no mínimo `240px` a `280px` para acomodar rótulos completos e badges sem truncamento.
- **Hierarquia:** Separação semântica nítida entre seções de navegação, ações de rodapé e perfil de usuário.

### 4.3. Tipografia e Pareamento Multidimensional (`TYPOGRAPHY_PRESETS`)
- **Famílias e Pares Autorizados (Padrão 2026):** Valida se o projeto utiliza um dos 4 pareamentos canônicos:
  * `humanist-tech`: **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.025em`)
  * `editorial-serif`: **Instrument Serif** + **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
  * `swiss-grotesk`: **Space Grotesk** + **Inter** + **JetBrains Mono** (`tracking: -0.03em`)
  * `classic-garamond`: **Cormorant Garamond** + **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
- **Banimento de Fontes Genéricas:** Reprovação de fontes descalibradas (Arial crua, Times New Roman, Comic Sans ou fontes com kerning irregular).
- **Escala e Line-Height:** `line-height` relaxado (`1.4` a `1.6`), contrastes tipográficos WCAG AA mínimos (4.5:1; ideal AAA $\ge$ 7.0:1).

### 4.4. Ícones
- **Padronização:** Adoção recomendada de **Lucide Icons** ou biblioteca equivalente de traço linear limpo.
- **Consistência de Stroke e Escala:** Espessura de traço consistente (`1.5px` a `2px`), caixas de delimitação uniformes (`16px`, `20px` ou `24px`).
- **Alinhamento Óptico:** Centralização vertical perfeita com o texto adjacente (`inline-flex items-center gap-2`).

### 4.5. Tamanho dos Botões e Alvos de Clique
- **Altura Ergonômica:** Altura mínima de `40px` (preferencialmente `44px`) para alvos de clique confortáveis.
- **Anti-Squish Obrigatório:** Presença de `flex-shrink: 0;` e `white-space: nowrap;` em botões de ação e tags, eliminando quebras verticais ("C o p i a r").
- **Padding Interno:** Mínimo horizontal de `1rem` (16px) em botões principais.

### 4.6. Transições, Micro-interações e Física 3D (`calculateCardTilt`)
- **Feedback Tátil Cinestésico:** Existência de resposta visual imediata no clique (`active:scale-95` ou `translateY(1px)`).
- **Curva e Tempo de Transição:** Animações rápidas e orgânicas (`150ms` a `200ms`, `cubic-bezier(0.16, 1, 0.3, 1)`).
- **Física 3D Opcional Resiliente:** Quando houver inclinação 3D em cartões (`.tactile-card-interactive`), deve respeitar limite angular de $\pm 5.5^\circ$ e desativar transformações sob `@media (prefers-reduced-motion: reduce)`.

### 4.7. Layout, Grids e Geometria Estrutural (`GEOMETRY_PRESETS`)
- **Largura Mínima de Colunas:** Colunas em grids de dashboards devem respeitar largura mínima de `350px`, evitando quebras agressivas em telas médias.
- **Geometria Coerente de Borda:** Raios calibrados conforme o preset do tema: `sharp` (`6px`), `editorial` (`12px`), `technical` (`16px`), `tactile` (`20px`) ou `organic` (`24px`).
- **Comando Rápido:** Presença ou ausência de barra de comando rápido (`Ctrl+K` / `⌘K`).

### 4.8. Cores, 22 Temas Homologados e Profundidade Tátil
- **Banimento Anti-Cobalto:** Reprovação expressa de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes ácidas.
- **Catálogo de 22 Temas (`v2.6.0-2026`):** Suporte às 10 Paletas Canônicas Melki (`steadfast-stainless`, `window-tide`, `cotton-dandelions`, `ocean-window`, `mermaid-lagoon`, `nightfall-ambiance`, `sky-balloons`, `grained-memories`, `living-a-dream`, `van-goghs-dream`), 5 Trends 2026 (`warm-editorial-paper`, `quiet-luxury-titanium`, `neo-swiss-grid`, `biophilic-matcha-stone`, `tactile-carbon-2026`) e 7 Temas de Estúdio (`tactile-matte`, `phantom-4k`, `luxury-deepblue`, `gilded-navy`, `polar-sand`, `emerald-terminal`, `monokai-tactile`), cada um com 6 swatches únicos.
- **Regra da Luminância no Dark Mode:** Cartões e painéis devem ser visivelmente mais claros que o canvas de fundo (`L_card > L_canvas`), garantindo o contraste necessário para projeção da sombra.
- **Sombras Multicamadas & Rim Light:** Presença de sombra de contato curta combinada com projeção difusa ampla e borda superior com micro-chanfro zenital mineral (`border-top: 1px solid rgba(255, 255, 255, 0.14)`).
- **Anti-Glassmorphism:** Reprovação de caixas de vidro transparentes com blur excessivo e reflexos plásticos.

### 4.9. Sintaxe HTML5 Semântica (Google HTML/CSS Style Guide)
- **Tags e Atributos:** Todas as tags e atributos em minúsculas (`<div class="...">`).
- **Ausência de Trailing Slash em Void Elements:** Reprovação de `<br />`, `<img ... />` ou `<meta ... />` em documentos HTML5; exigir `<br>`, `<img>`, `<meta>`.
- **Omissão de Tipos Redundantes:** Reprovação de `type="text/javascript"` em `<script>` e `type="text/css"` em `<link>`.
- **Protocolos Limpos:** URLs externas com HTTPS explícito ou protocolo relativo (`//`).

### 4.10. Formatação CSS e Nomenclatura (Google Style Guide)
- **Nomenclatura em Kebab-case:** Classes e identificadores obrigatoriamente no padrão `kebab-case` (`.user-card`, `.btn-action`). Reprovação de `camelCase` em classes CSS.
- **Omissão de Unidade Zero:** Reprovação de `0px`, `0em`, `0%` onde deve ser apenas `0` (`margin: 0;`).
- **Indentação e Espaçamento:** Indentação consistente de 2 espaços por nível de bloco CSS.
- **Uso de IDs para Estilo:** Reprovação do uso de seletores `#id` para estilização (usar exclusivamente classes).

### 4.11. Orquestração do Esquadrão de Subagentes de UI (`Topologia 3+1`)
Para auditorias completas ou interfaces complexas, esta skill aciona os **4 Subagentes Especialistas de UI** (`agents/ui-*.md`) em **3 Ondas determinísticas** via **Modo Nativo Antigravity (`invoke_subagent`)** ou **Modo Motor DAG Assíncrono (`franklin_execute_dag` / `franklin_get_agents` / `epic-volta`)**:
1. **Onda 1 — [`ui-shell-navigator`](../../agents/ui-shell-navigator.md)**: Inspeciona Módulos 1 e 2 (*UI Islands*, Grid/SplitView, `Shadow DOM`, reservas anti-CLS $< 0.1$, `MenuBar`, `TabView` lazy, `TreeView` assíncrono e `Ctrl+K`), emitindo `layout_contract` e `navigation_contract`.
2. **Onda 2A — [`ui-controls-data`](../../agents/ui-controls-data.md)**: Inspeciona Módulos 3 e 4 (alvos $\ge 44\times44\text{px}$, anti-squish, Regra 1+2, validação WAI-ARIA inline, virtualização de listas a $60\text{fps}$ e regiões `aria-live`), emitindo `controls_contract` e `data_feedback_contract`.
3. **Onda 2B — [`ui-motion-interaction`](../../agents/ui-motion-interaction.md)**: Inspeciona Módulos 5.1 e 5.2 (animações GPU `transform`/`opacity`, `ConnectedAnimation`, proteção `prefers-reduced-motion` e paridade multi-input `Touch/Pen/Mouse/Keyboard`), emitindo `motion_contract` e `interaction_contract`.
4. **Onda 3 (Gatekeeper) — [`ui-deterministic-observer`](../../agents/ui-deterministic-observer.md)**: Consome os contratos das Ondas 1 e 2 via `upstream_mapping` e audita os 9 itens determinísticos (`[AUDIT-01: SHELL-CLS]` a `[AUDIT-09: LIGHT-SHADOW]`).

**Como invocar os subagentes na prática:**
- **Modo Nativo Antigravity (`invoke_subagent`)**: invocação direta dos subagentes registrados pelo plugin `franklin-skills` em `<subagents>` (`Available subagents`) em 3 ondas:
  - **Onda 1**: `invoke_subagent(TypeName="ui-shell-navigator", Task="...")`
  - **Onda 2 (Paralela)**: `invoke_subagent(TypeName="ui-controls-data", Task="...")` e `invoke_subagent(TypeName="ui-motion-interaction", Task="...")`
  - **Onda 3 (Gatekeeper)**: `invoke_subagent(TypeName="ui-deterministic-observer", Task="...")`
- **Modo Motor DAG Assíncrono (`franklin_execute_dag` / `franklin_get_agents` / `epic-volta`)**:
  - `franklin_get_agents(agent_name="ui")` (carrega os contratos dos 4 subagentes de UI) ou `franklin_get_agents(agent_name="ui-deterministic-observer")`.
  - `franklin_execute_dag(plan_path_or_json="plans/ui_composition_dag.json", run_id="ui-audit-01")` (ou alias curto `franklin_execute_dag(plan_path_or_json="ui")`).
  - Terminal (Epic-Volta CLI):
    ```powershell
    uv --directory C:\Users\melki\dev\repos\epic-volta run python -m orchestrator.cli C:\Users\melki\dev\repos\franklin-quebragalho\plans\ui_composition_dag.json --run-id ui-audit-01
    ```

---

## 5. PROCESSO PASSO A PASSO (INSPEÇÃO E COMPARAÇÃO)

### Passo 1: Varredura de Ambiente, DOM e Subagentes (`Topologia 3+1`)
1. Acionar os 4 subagentes em 3 ondas via `invoke_subagent` (`TypeName="ui-shell-navigator"` ➔ `ui-controls-data` + `ui-motion-interaction` ➔ `ui-deterministic-observer`), ou carregar os contratos (`franklin_get_agents(agent_name="ui")`) / disparar a esteira DAG (`franklin_execute_dag(plan_path_or_json="ui")`) quando a análise abranger múltiplos módulos de UI.
2. Se URL acessível, abrir a página e capturar a árvore de acessibilidade via `agent-browser`:
   ```powershell
   agent-browser open "[URL]"
   agent-browser wait 1500
   agent-browser snapshot -i
   ```
3. Capturar telas em dark mode e light mode para inspeção de oclusão e contraste:
   ```powershell
   agent-browser --color-scheme dark screenshot --annotate
   ```
4. Se arquivos estáticos, inspecionar folhas de estilo (`globals.css`, `tailwind.config.js`) e arquivos HTML/JSX/TSX.

### Passo 2: Extração dos Parâmetros Reais
Mapear os valores reais em uso:
- Altura dos botões (`computedStyle.height`).
- Font-family dos títulos e parágrafos.
- Hexadecimais de fundo e cartões.
- Presença de tags void com autofechamento XML (`<br/>`, `/>`).
- Nomenclatura das classes CSS (`kebab-case` vs `camelCase`).
- Existência de classes `shrink-0`, `whitespace-nowrap`, `active:scale-95`.
- Espaçamento de itens da sidebar e navbar.

### Passo 3: Confronto com a Tabela Canônica de Preferências e Checklist `[AUDIT-01..09]`
Atribuir status determinístico para cada um dos 10 critérios e consolidar o veredito do `ui-deterministic-observer`:
- `[PASS]`: Atende integralmente à diretriz.
- `[FAIL]`: Viola a diretriz ou apresenta defeito visual/ergonômico/sintático.
- `[UNVERIFIED]`: Não foi possível testar dinamicamente no momento da análise.

### Passo 4: Emissão do Relatório Comparativo
Gravar o relatório estruturado contendo a comparação detalhada e soluções recomendadas.

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega o relatório com este modelo:

```markdown
# 📊 Relatório de Diagnóstico Frontend e Análise Comparativa

## 1. Visão Geral da Interface
- **Alvo Analisado:** [URL ou Arquivo]
- **Tema Base Identificado:** [Dark Mode / Light Mode / Misto]
- **Framework Detectado:** [React / Tailwind / HTML Puro / Outro]

## 2. Matriz de Conformidade com as Preferências Melki e Google Style Guides

| Ponto de Análise | Estado Atual Detectado | Padrão Esperado | Status | Discrepância / Diagnóstico |
| :--- | :--- | :--- | :---: | :--- |
| **1. Menus & Navegação** | [Ex: Espaço 4px, compactado] | Espaçamento nobre (gap >= 12px, padding relaxado) | `[FAIL]` | Menus espremidos gerando sensação claustrofóbica |
| **2. Sidebar** | [Ex: 180px de largura] | Mínimo 240px a 280px com labels completas | `[FAIL]` | Nomes de itens truncados |
| **3. Tipografia & Fontes** | [Ex: Arial / Roboto genérica] | Inter / Geist Sans / JetBrains Mono | `[FAIL]` | Tipografia padrão sem requinte visual |
| **4. Ícones** | [Ex: Ícones mistos sem padrão] | Lucide Icons com stroke uniforme (1.5-2px) | `[FAIL]` | Traços e tamanhos desiguais |
| **5. Botões & Anti-Squish** | [Ex: Altura 32px, quebra de linha] | Altura >= 40px, shrink-0, whitespace-nowrap | `[FAIL]` | Alvo pequeno e texto suscetível a squish |
| **6. Transições & Feedback**| [Ex: Sem efeito de clique] | active:scale-95, transição tátil 150ms | `[FAIL]` | Elementos estáticos sem cinestesia |
| **7. Layout & Grids** | [Ex: Coluna de 260px] | Colunas >= 350px, respiro generoso | `[PASS]` | Distribuição espacial adequada |
| **8. Cores & Relevo Tátil** | [Ex: Fundo preto e card preto] | L_card > L_canvas, sombras multicamadas, rim-light | `[FAIL]` | Sem percepção de profundidade física |
| **9. Sintaxe HTML5 (Google)**| [Ex: Tags <br/> e type redundante] | Tags void sem barra, omitir type em script/css | `[FAIL]` | Presença de sintaxe XML obsoleta em HTML5 |
| **10. CSS & Classes (Google)**| [Ex: Classes em camelCase e 0px] | Classes kebab-case, 2 espaços, zero sem unidade | `[FAIL]` | Classes fora do padrão e unidades em valor 0 |

## 3. Recomendações Técnicas para Refatoração
[Lista de classes Tailwind / CSS e correções sugeridas para alimentar a skill de refatoração]
```

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- **Read-Only Rigoroso:** Esta skill NUNCA modifica arquivos de código nem executa comandos de mutação.
- **Falsificabilidade:** NUNCA emitir `[PASS]` sem evidência comprovada extraída do DOM ou do CSS.
- **Fallback Estático:** Se a porta local estiver inacessível, inspecione os arquivos estáticos e marque itens que dependam de renderização como `[UNVERIFIED]`.
