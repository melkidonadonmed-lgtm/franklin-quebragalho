# Compêndio Completo (All-in-One): `minimal-impact-ui` (Ex Umbris Ad Lucem + WinUI 3 Gallery)

Este documento reúne em um único arquivo Markdown autocontido todas as diretrizes operacionais, regras tipográficas de alta nitidez, tokens CSS/JS dos 3 temas, 6 arquétipos de composição de página e o catálogo de 28 efeitos de superfície, layout, movimento e controles interativos para uso direto no **Antigravity**.

## 1. Visão Geral e Filosofia Central

Esta skill aplica a arquitetura visual **Ex Umbris Ad Lucem** (*Das Sombras para a Luz* — Minimalismo de Impacto e Complexidade da Simplicidade) combinada ao vocabulário espacial e cinemático do **WinUI 3 Gallery**:

- **Proporção Cromática 98% / 2% (Efeito de Isolamento de Von Restorff):** 98% da interface é construída em tons neutros arquitetônicos (cinza monolítico `#57545d`, grafite `#49464f`, branco editorial `#F3F3F5` e preto obsidiana `#070709`). Apenas **2% da tela** recebe uma única cor pontual calibrada por objetivo, transformando o ponto focal em um ímã retiniano imediato.
- **Nitidez Tipográfica Absoluta (Zero Letras Vermelhas Embaçadas):** Proíbe o uso de letras vermelhas puras (`color: #e13535`) ou fontes serifadas finas sobre fundos cinza/escuros (que sofrem de baixo contraste 2.1:1 e aberração cromática ocular). Todo destaque sobre fundo cinza ou preto usa **texto branco puro (`#FFFFFF`) em Semibold (`font-weight: 600`)** ancorado por um **sublinhado cirúrgico de `2px`** (em títulos) ou **borda lateral esquerda de `2.5px solid var(--punctual-accent)`** (em badges e tags).
- **Menus Nítidos de Alto Contraste:** Proíbe letras brancas lavadas sobre barras de navegação claras ou acinzentadas (`#8e8999`). Os links do menu usam tinta grafite escura (`#16151A`) dentro de contêineres em pílula (`rounded-full`), invertendo para fundo escuro sólido (`#1E1C22`) e texto claro (`#F5F4F8`) no item ativo ou em hover.

## 2. Matriz dos 3 Temas Oficiais e das 4 Cores Pontuais (2%)

### 2.1. Os 3 Temas Obrigatórios (Alternância Ao Vivo + `localStorage`)

| Token CSS / Atributo | 1. Cinza Monolítico (`data-theme="gray"` — Padrão) | 2. Claro Editorial (`data-theme="light"` — Ad Lucem) | 3. Preto Terminal IBM (`data-theme="dark"`) |
| :--- | :--- | :--- | :--- |
| **Fundo Principal (`--bg-canvas`)** | `#57545d` | `#F3F3F5` | `#070709` |
| **Superfície de Card (`--bg-surface`)** | `#49464f` | `#FFFFFF` | `#101014` |
| **Superfície Elevada (`--bg-elevated`)** | `#635f6a` | `#E6E6EA` | `#18181E` |
| **Card de Contraste (`--bg-contrast-card`)** | `#232127` (texto `#F4F3F7`) | `#18181C` (texto `#F4F4F6`) | `#1D1D24` (texto `#FAFAFA`) |
| **Barra de Menu (`--nav-shell-bg`)** | `#8e8999` (tinta `#16151A`) | `rgba(255, 255, 255, 0.92)` (tinta `#18181B`) | `rgba(16, 16, 20, 0.92)` (tinta `#E4E4E7`) |
| **Texto Primário (`--ink-primary`)** | `#F7F6F9` | `#111115` | `#F4F4F6` |
| **Texto Secundário (`--ink-secondary`)** | `#DFDDE4` | `#3F3F46` | `#B4B4BE` |
| **Texto Silenciado (`--ink-muted`)** | `#BDB9C6` | `#686873` | `#7D7D8A` |
| **Texto de Acento (`--punctual-text`)** | `#FFFFFF` (com filete/borda 2.5px) | `#991B1B` (escuro nítido) | `#FFFFFF` (com filete/borda 2.5px) |
| **Tipografia Base (`--font-sans`)** | `Inter`, `Plus Jakarta Sans` | `Inter`, `Plus Jakarta Sans` | `IBM Plex Sans` + títulos `IBM Plex Mono` |

### 2.2. As 4 Cores Pontuais Calibradas por Objetivo (Regra dos 2%)

| Domínio / Objetivo do Projeto | Cor Pontual (`--punctual-accent`) | Fundo Suave (`--punctual-soft`) | Brilho (`--punctual-glow`) | Texto no Botão (`--punctual-btn-ink`) |
| :--- | :--- | :--- | :--- | :--- |
| **Design, Editorial, Produtividade & Foco (Padrão)** | `#e13535` (Carmim Selo) | `rgba(225, 53, 53, 0.12)` | `rgba(225, 53, 53, 0.35)` | `#FFFFFF` |
| **IA, Engenharia de Dados, SaaS & Telemetria** | `#35acd8` (Azul Cerúleo) | `rgba(53, 172, 216, 0.14)` | `rgba(53, 172, 216, 0.38)` | `#091318` (Grafite Escuro) |
| **MedTech, Clínica, Calculadoras & SUS** | `#10B981` (Esmeralda Clínico) | `rgba(16, 185, 129, 0.13)` | `rgba(16, 185, 129, 0.35)` | `#062016` (Verde-Preto Escuro) |
| **FinTech, Jurídico, Patrimônio & Alertas** | `#D97706` (Âmbar Imperial) | `rgba(217, 119, 6, 0.13)` | `rgba(217, 119, 6, 0.35)` | `#FFFFFF` |

## 3. Boilerplate Completo de Produção (HTML Head + CSS + JS)

```html
<!-- 1. HEAD: Tailwind CSS + Fontes de Alta Nitidez (Inter, Plus Jakarta Sans, JetBrains Mono, IBM Plex) -->
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root, [data-theme="light"] {
    --bg-canvas: #F3F3F5;
    --bg-surface: #FFFFFF;
    --bg-elevated: #E6E6EA;
    --bg-contrast-card: #18181C;
    --ink-contrast-card: #F4F4F6;

    --nav-shell-bg: rgba(255, 255, 255, 0.92);
    --nav-pill-bg: #EAEAEF;
    --nav-ink: #18181B;
    --nav-ink-muted: #52525B;
    --nav-active-bg: #18181B;
    --nav-active-ink: #FFFFFF;

    --ink-primary: #111115;
    --ink-secondary: #3F3F46;
    --ink-muted: #686873;
    --ink-subtle: #A1A1AA;

    --border-hairline: rgba(24, 24, 27, 0.10);
    --border-strong: rgba(24, 24, 27, 0.24);
    --rim-light: rgba(255, 255, 255, 0.95);

    --shadow-sculpted: 
        0 1px 2px rgba(17, 17, 21, 0.04),
        0 10px 28px -6px rgba(17, 17, 21, 0.08),
        0 28px 56px -14px rgba(17, 17, 21, 0.10),
        inset 0 1px 0 0 rgba(255, 255, 255, 1);

    --font-sans: 'Inter', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;

    --punctual-accent: #e13535;
    --punctual-text: #991B1B;
    --punctual-soft: rgba(225, 53, 53, 0.12);
    --punctual-glow: rgba(225, 53, 53, 0.32);
    --punctual-btn-ink: #FFFFFF;
}

[data-theme="gray"] {
    --bg-canvas: #57545d;
    --bg-surface: #49464f;
    --bg-elevated: #635f6a;
    --bg-contrast-card: #232127;
    --ink-contrast-card: #F4F3F7;

    --nav-shell-bg: #8e8999;
    --nav-pill-bg: rgba(35, 33, 39, 0.12);
    --nav-ink: #16151A;
    --nav-ink-muted: #2E2C35;
    --nav-active-bg: #1E1C22;
    --nav-active-ink: #F5F4F8;

    --ink-primary: #F7F6F9;
    --ink-secondary: #DFDDE4;
    --ink-muted: #BDB9C6;
    --ink-subtle: #8e8999;

    --border-hairline: rgba(255, 255, 255, 0.14);
    --border-strong: rgba(255, 255, 255, 0.28);
    --rim-light: rgba(255, 255, 255, 0.22);

    --shadow-sculpted: 
        0 2px 6px rgba(15, 14, 18, 0.35),
        0 16px 36px -6px rgba(15, 14, 18, 0.50),
        0 32px 64px -14px rgba(15, 14, 18, 0.65),
        inset 0 1px 0 0 var(--rim-light);

    --font-sans: 'Inter', 'Plus Jakarta Sans', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;
    --punctual-text: #FFFFFF;
}

[data-theme="dark"] {
    --bg-canvas: #070709;
    --bg-surface: #101014;
    --bg-elevated: #18181E;
    --bg-contrast-card: #1D1D24;
    --ink-contrast-card: #FAFAFA;

    --nav-shell-bg: rgba(16, 16, 20, 0.92);
    --nav-pill-bg: #18181F;
    --nav-ink: #E4E4E7;
    --nav-ink-muted: #A1A1AA;
    --nav-active-bg: #FAFAFA;
    --nav-active-ink: #09090B;

    --ink-primary: #F4F4F6;
    --ink-secondary: #B4B4BE;
    --ink-muted: #7D7D8A;
    --ink-subtle: #3F3F48;

    --border-hairline: rgba(255, 255, 255, 0.09);
    --border-strong: rgba(255, 255, 255, 0.22);
    --rim-light: rgba(255, 255, 255, 0.13);

    --shadow-sculpted: 
        0 2px 4px rgba(0, 0, 0, 0.65),
        0 16px 36px -6px rgba(0, 0, 0, 0.82),
        0 36px 72px -16px rgba(0, 0, 0, 0.95),
        inset 0 1px 0 0 var(--rim-light);

    --font-sans: 'IBM Plex Sans', sans-serif;
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', monospace;
    --punctual-text: #FFFFFF;
}

body {
    background-color: var(--bg-canvas);
    color: var(--ink-primary);
    font-family: var(--font-sans);
    transition: background-color 0.45s cubic-bezier(0.16, 1, 0.3, 1), color 0.3s ease;
    overflow-x: hidden;
}

[data-theme="dark"] h1,
[data-theme="dark"] h2,
[data-theme="dark"] h3,
[data-theme="dark"] .ibm-terminal-heading {
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: -0.03em;
}

/* Destaque geométrico nítido em títulos com sublinhado cirúrgico de 2px (Zero serifa fina embaçada) */
.highlight-surgical, .font-serif-editorial {
    font-family: var(--font-sans);
    font-style: normal;
    font-weight: 600;
    letter-spacing: -0.02em;
    text-decoration: underline;
    text-decoration-color: var(--punctual-accent);
    text-decoration-thickness: 2px;
    text-underline-offset: 6px;
}

.font-mono-tech {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    letter-spacing: 0.01em;
}

.surface-canvas { background-color: var(--bg-canvas); }
.surface-card { background-color: var(--bg-surface); }
.surface-elevated { background-color: var(--bg-elevated); }
.surface-contrast { background-color: var(--bg-contrast-card); color: var(--ink-contrast-card); }

.nav-shell { background-color: var(--nav-shell-bg); color: var(--nav-ink); backdrop-filter: blur(16px); }
.nav-pill-container { background-color: var(--nav-pill-bg); border: 1px solid var(--border-hairline); }
.nav-link-item { color: var(--nav-ink); font-weight: 500; letter-spacing: 0.02em; transition: all 0.2s ease; white-space: nowrap; }
.nav-link-item:hover, .theme-pill-btn.active { background-color: var(--nav-active-bg); color: var(--nav-active-ink); }
.theme-pill-btn { color: var(--nav-ink); font-weight: 500; transition: all 0.2s ease; }

.ink-primary { color: var(--ink-primary); }
.ink-secondary { color: var(--ink-secondary); }
.ink-muted { color: var(--ink-muted); }
.ink-subtle { color: var(--ink-subtle); }

.border-hair { border-color: var(--border-hairline); }
.border-strong { border-color: var(--border-strong); }

.accent-bg {
    background-color: var(--punctual-accent);
    color: var(--punctual-btn-ink);
    font-weight: 600;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.18);
}

/* Tag/Badge de acento de altíssimo contraste (Zero letras vermelhas soltas sobre cinza) */
.accent-text {
    color: var(--punctual-text);
    font-weight: 600;
    background-color: var(--punctual-soft);
    padding: 0.1rem 0.45rem;
    border-radius: 5px;
    border-left: 2.5px solid var(--punctual-accent);
    display: inline-block;
    line-height: 1.35;
}
h1 .accent-text, h2 .accent-text {
    background-color: transparent;
    border-left: none;
    padding: 0;
    border-radius: 0;
    color: var(--ink-primary);
    font-weight: 600;
}

.accent-soft { background-color: var(--punctual-soft); }
.accent-border { border-color: var(--punctual-accent); }
.accent-glow { box-shadow: 0 0 18px var(--punctual-glow); }

.shadow-architectural { box-shadow: var(--shadow-sculpted); }
.terrixa-card { position: relative; border-radius: 14px; }
.architectural-grid {
    background-size: 64px 64px;
    background-image: 
        linear-gradient(to right, var(--border-hairline) 1px, transparent 1px),
        linear-gradient(to bottom, var(--border-hairline) 1px, transparent 1px);
}

/* Inputs, Selects e Textareas */
.input-ex-umbris {
    background-color: var(--bg-elevated);
    color: var(--ink-primary);
    border: 1px solid var(--border-hairline);
    border-radius: 10px;
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    outline: none;
}
.input-ex-umbris::placeholder { color: var(--ink-muted); opacity: 0.75; }
.input-ex-umbris:focus, button:focus-visible, a:focus-visible {
    border-color: var(--punctual-accent);
    box-shadow: 0 0 0 3px var(--punctual-soft);
    outline: none;
}

/* Tabelas Arquitetônicas */
.table-ex-umbris { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.table-ex-umbris th {
    font-family: var(--font-mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--ink-muted);
    text-align: left;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-strong);
}
.table-ex-umbris td {
    padding: 0.85rem 1rem;
    font-size: 0.8125rem;
    color: var(--ink-secondary);
    border-bottom: 1px solid var(--border-hairline);
}
.table-ex-umbris tr:hover td { background-color: var(--bg-elevated); color: var(--ink-primary); }

.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}

@media print {
    :root, [data-theme="gray"], [data-theme="dark"], [data-theme="light"] {
        --bg-canvas: #FFFFFF !important;
        --bg-surface: #FFFFFF !important;
        --bg-elevated: #F4F4F6 !important;
        --ink-primary: #111115 !important;
        --ink-secondary: #3F3F46 !important;
        --ink-muted: #52525B !important;
        --border-hairline: rgba(0, 0, 0, 0.15) !important;
        --shadow-sculpted: none !important;
    }
    .no-print, header.nav-shell { display: none !important; }
    body { background: #FFFFFF !important; color: #111115 !important; }
}
</style>

<script>
const ACCENT_PRESETS = {
    red:   { hex: '#e13535', soft: 'rgba(225,53,53,0.12)',  glow: 'rgba(225,53,53,0.35)',  ink: '#FFFFFF' },
    blue:  { hex: '#35acd8', soft: 'rgba(53,172,216,0.14)', glow: 'rgba(53,172,216,0.38)', ink: '#091318' },
    green: { hex: '#10B981', soft: 'rgba(16,185,129,0.13)', glow: 'rgba(16,185,129,0.35)', ink: '#062016' },
    amber: { hex: '#D97706', soft: 'rgba(217,119,6,0.13)',  glow: 'rgba(217,119,6,0.35)',  ink: '#FFFFFF' }
};

function setThemeMode(mode) {
    document.documentElement.setAttribute('data-theme', mode);
    try { localStorage.setItem('ex-umbris-theme', mode); } catch (e) {}
    ['Light', 'Gray', 'Dark'].forEach(t => {
        const btn = document.getElementById('themeBtn' + t);
        if (btn) btn.classList.toggle('active', t.toLowerCase() === mode);
    });
}

function setAccentPreset(key) {
    const p = ACCENT_PRESETS[key] || ACCENT_PRESETS.red;
    const root = document.documentElement.style;
    root.setProperty('--punctual-accent', p.hex);
    root.setProperty('--punctual-soft', p.soft);
    root.setProperty('--punctual-glow', p.glow);
    root.setProperty('--punctual-btn-ink', p.ink);
}
</script>
```

## 4. Os 6 Arquétipos de Página (Além de Formulários e Gráficos Comuns)

| # | Arquétipo de Página | Estrutura Espacial | Quando Usar (Exemplos Reais) | Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Split-Screen Live Workbench** | Painel esquerdo (`col-span-5`) com pílulas de inserção rápida e campos compactos + Painel direito (`col-span-7`) com folha A4 / preview ao vivo. | Geradores de Evolução Médica, APAC/LME/SISREG, editores de prompts/skills e laudos estruturados. | Telas exclusivamente mobile sem converter o painel direito em aba ou modal rápido. |
| **02** | **Linha do Tempo Cronológica (Timeline)** | Eixo vertical contínuo (`border-l-2 border-strong`) com nós numerados (`D1`, `D2`, `D3`), cards expansíveis e ponto de 2% no marco atual. | Evolução hospitalar dia a dia, histórico comparativo de exames, linha de cuidado ou roadmaps. | Catálogos de itens sem relação temporal ou cronológica. |
| **03** | **Quadro Kanban Operacional** | 3 a 4 colunas de estágio (`Pendente`, `Em Análise`, `Concluído`) com contadores no topo e cartões compactos com filete lateral. | Gestão de pacientes do turno, acompanhamento de processos SUS ou quadro de tarefas (Anti-TDAH). | Mais de 5 colunas simultâneas ou centenas de registros sem filtro. |
| **04** | **Canvas Espacial de Nós (Árvore de Decisão)** | Nós clicáveis sobre malha arquitetônica (`64x64px`) que iluminam o caminho escolhido (`Sim / Não`) com borda `--punctual-accent`. | Diretrizes clínicas (sepse, dor torácica, regulação SUS), algoritmos diagnósticos e fluxos de IA. | Cadastros tabulares simples de preenchimento linear. |
| **05** | **Wizard Modo Foco Anti-TDAH** | Monólito centralizado exibindo apenas 1 decisão/etapa por tela com barra de progresso superior em `JetBrains Mono` e botões grandes. | Processos complexos onde exibir 30 ou 40 campos de uma vez causa paralisia ou fadiga cognitiva. | Edição rápida de apenas 1 campo isolado em uma ficha já concluída. |
| **06** | **Catálogo Interativo (WinUI Gallery)** | `SelectorBar` em pílulas no topo + busca instantânea por palavra-chave + grade de cartões com `Expander` de código/copiar em cada item. | Bulário pessoal, biblioteca de protocolos clínicos, cofre de prompts e documentação interativa. | Entrada sequencial de dados de um único atendimento. |

## 5. Catálogo Completo de 28 Efeitos, Layouts, Motion & Controles (WinUI 3 + Ex Umbris)

### 5.1. Materiais, Luz & Atmosfera (6 Efeitos)

| # | Nome Técnico / Comando | O que é | Variação Técnica para Ficar Bonito | Quando Usar vs. Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **AcrylicBrush (Vidro Acromático)** | Material translúcido com `backdrop-filter: blur(16px)` para painéis flutuantes. | Opacidade entre `85%` e `92%` + borda de `1px` (`--border-hairline`). Nunca deixe transparente demais. | **Usar:** Navbar fixa, popovers, Command Palette.<br>**Evitar:** Tabelas longas e textos de leitura densa. |
| **02** | **SystemBackdrop / Superfície Mica** | Material base opaco e aveludado (`#57545d` canvas, `#49464f` card, `#635f6a` elevado). | Diferença sutil de luminosidade (`6%` a `10%`) entre fundo, card e input elevado. | **Usar:** Estrutura principal (85%+ da tela) para longas sessões sem fadiga.<br>**Evitar:** Misturar mais de 3 tons neutros na mesma seção. |
| **03** | **ThemeShadow + Luz Especular (Rim Light)** | Sombra física em 3 camadas (umbra, penumbra e difusão) + `1px` de luz interna no topo. | O segredo no fundo cinza/preto é o `inset 0 1px 0 0 var(--rim-light)` na borda superior. | **Usar:** Cards principais, modais e monólitos.<br>**Evitar:** Células individuais de tabelas ou listas longas. |
| **04** | **ContentIsland & Contraste Alternado** | Ilhas modulares que alternam superfície padrão (`#49464f`) e bloco escuro (`#232127`). | Em grades de 4 cards (`01–04`), alterne cards normais (`01, 03`) e escuros (`02, 04`) com raio de `14px`. | **Usar:** Resumos executivos e aberturas de sistemas.<br>**Evitar:** Textos longos de mais de 3 parágrafos invertidos. |
| **05** | **Compact Sizing (Alta Densidade)** | Redução calibrada de paddings (`py-1.5 px-2.5`) para exibir 40% mais dados sem rolar. | Combine com `JetBrains Mono` em `tabular-nums` (números alinhados verticalmente) e linhas de `1px`. | **Usar:** Exames laboratoriais, tabelas SIGTAP/CID e logs.<br>**Evitar:** Landing pages editoriais ou modo foco. |
| **06** | **Grade Arquitetônica (Blueprint)** | Malha geométrica de `64x64px` desenhada com linhas de `1px` (`--border-hairline`). | Opacidade entre `40%` e `60%` com `pointer-events: none` no fundo de seções Hero e palcos. | **Usar:** Aberturas, simuladores e árvores de decisão.<br>**Evitar:** Atrás de textos longos ou tabelas densas. |

### 5.2. Arquitetura de Layout & Espaço (8 Estruturas)

| # | Nome Técnico / Comando | O que é | Variação Técnica para Ficar Bonito | Quando Usar vs. Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **07** | **Grid & VariableSizedWrapGrid (Bento)** | Grade onde o card prioritário ocupa `col-span-2` e os secundários ocupam `col-span-1`. | Concentre a cor pontual de 2% apenas no bloco expandido (`2x1`); mantenha os demais em grafite. | **Usar:** Painéis com 4 a 7 blocos de pesos diferentes.<br>**Evitar:** Listas onde todos os itens têm peso igual. |
| **08** | **SplitView (Master-Detail)** | Divide a tela em 2 áreas coordenadas (lista/entrada à esquerda e detalhe/preview à direita). | Borda divisória fina (`border-r border-hair`) e colapso automático em telas menores. | **Usar:** Prontuários, editores ao vivo e catálogos.<br>**Evitar:** Páginas simples de leitura linear única. |
| **09** | **Expander (Revelação Progressiva)** | Acordeão retrátil que esconde os 80% técnicos/código-fonte até ser clicado. | Exiba um resumo curto já no cabeçalho fechado (ex: `Critérios · 4 itens`). | **Usar:** Essencial contra sobrecarga visual no TDAH.<br>**Evitar:** Esconder o botão principal de salvar dentro dele. |
| **10** | **Canvas (Camadas Top, Left, Z-Index)** | Palco de coordenadas absolutas para sobrepor camadas, HUDs ou marcadores. | Aplique `ThemeShadow` e `AcrylicBrush` nas camadas de maior `Z-Index`. | **Usar:** Mapas anatômicos, diagramas e quadros espaciais.<br>**Evitar:** Layout geral de formulários (quebra no mobile). |
| **11** | **SelectorBar & TabView em Pílula** | Alternância instantânea de contexto usando pílulas arredondadas (`rounded-full`). | Tinta escura `#16151A` sobre `#8e8999` nas abas inativas; fundo `#1E1C22` com texto claro na ativa. | **Usar:** Alternar entre 2 a 6 módulos na mesma página.<br>**Evitar:** Mais de 7 categorias (use `SplitView` ou `Ctrl+K`). |
| **12** | **Viewbox & Folha A4 Proporcional** | Contêiner que preserva a proporção exata de uma folha A4 (`210x297mm`) para impressão. | Folha branca (`#FFFFFF`) com sombra esculpida sobre o palco cinza (`#57545d`). | **Usar:** Formulários SUS (APAC, LME), receitas e laudos.<br>**Evitar:** Interfaces exclusivas para tela de celular. |
| **13** | **StackPanel & WrapPanel (Chips)** | Fila inteligente que quebra linha para acomodar pílulas clicáveis de sintomas, CIDs ou tags. | Pílulas em `--bg-elevated`; quando selecionada, recebe `border: 1.5px solid var(--punctual-accent)`. | **Usar:** Substituir `select multiple` por cliques rápidos.<br>**Evitar:** Mais de 25 chips soltos sem agrupamento. |
| **14** | **Border & Molduras Hairline** | Divisórias estruturais ultrafinas de `1px` (`--border-hairline` e `--border-strong`). | Bordas externas firmes (`28%`) no card e divisórias internas suaves (`14%`) entre cabeçalho e corpo. | **Usar:** Em toda a estrutura para precisão geométrica.<br>**Evitar:** Bordas grossas (`3px+`) em todos os lados. |

### 5.3. Motion, Cinemática & Transições (6 Mecânicas)

| # | Nome Técnico / Comando | O que é | Variação Técnica para Ficar Bonito | Quando Usar vs. Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **15** | **Implicit Transitions** | Interpolação automática suave quando qualquer propriedade (largura, filtro, ordem) muda. | `transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1)` nos cartões dinâmicos. | **Usar:** Filtros de catálogo e alternância de densidade.<br>**Evitar:** Elementos arrastados pelo mouse em tempo real. |
| **16** | **Connected Animation** | O próprio card clicado se expande no lugar para mostrar os detalhes sem corte seco de tela. | Mantenha o título ancorado durante a expansão para preservar a memória espacial (Anti-TDAH). | **Usar:** Abrir detalhes de um protocolo, paciente ou tarefa.<br>**Evitar:** Quando é preciso comparar 2 itens lado a lado. |
| **17** | **Easing Functions Físicas** | Curvas de velocidade com desaceleração natural (`Quint Out`) ou micro-elasticidade (`Spring`). | `cubic-bezier(0.16, 1, 0.3, 1)` (`250ms–450ms`) para painéis; `cubic-bezier(0.34, 1.56, 0.64, 1)` para badges. | **Usar:** Em 100% das transições da interface.<br>**Evitar:** Transições `linear` robóticas ou acima de `600ms`. |
| **18** | **Theme Transitions** | Metamorfose sincronizada de `450ms` ao alternar entre Claro, Cinza `#57545d` e Preto IBM. | Transicione `background-color` (`0.45s`) e `color` (`0.3s`) suavemente no `body`. | **Usar:** Sempre que houver o seletor triplo de temas.<br>**Evitar:** Desativar automaticamente no `@media print`. |
| **19** | **Page Transitions (Stagger)** | Entrada escalonada curta (`translateY(10px) -> 0`) com `40ms` de intervalo entre cards. | Deslocamento discreto (`8px` a `12px`) e duração rápida (`300ms`). | **Usar:** Carga inicial ou troca de aba principal.<br>**Evitar:** Atrasos longos que façam o usuário esperar. |
| **20** | **ParallaxView Sutil** | Deslocamento diferencial leve (`10%–15%`) apenas na grade arquitetônica de fundo ao rolar. | Mantenha todos os textos e cartões de leitura 100% firmes no eixo principal. | **Usar:** Aberturas editoriais e portfólios.<br>**Evitar:** Calculadoras clínicas e tabelas operacionais. |

### 5.4. Controles Avançados, Feedback & Fluxo Anti-TDAH (8 Controles)

| # | Nome Técnico / Comando | O que é | Variação Técnica para Ficar Bonito | Quando Usar vs. Quando Evitar |
| :--- | :--- | :--- | :--- | :--- |
| **21** | **Command Palette (`Ctrl+K`)** | Busca universal flutuante para achar qualquer função, código SIGTAP/CID ou tema em 3 letras. | Fundo `AcrylicBrush`, navegação por setas e atalhos em `JetBrains Mono`. | **Usar:** Qualquer app com mais de 5 funções (Anti-TDAH).<br>**Evitar:** Páginas mínimas de função única. |
| **22** | **App Notifications (Toasts) & Badges** | Avisos discretos no canto inferior direito (`✓ Copiado!`) e contadores nas pílulas de menu. | Card `.surface-contrast` com ponto de `8px` na cor pontual. Nunca use alerta nativo do navegador. | **Usar:** Confirmar cópia, salvamento ou exportação.<br>**Evitar:** Erros críticos que exigem leitura longa. |
| **23** | **Popup & Popover Contextual** | Micro-painel ancorado que mostra doses ou valores de referência sem sair da tela atual. | Superfície elevada, `--shadow-sculpted` e fechamento ao clicar fora ou apertar `Esc`. | **Usar:** Consultas rápidas de apoio à decisão.<br>**Evitar:** Textos extensos (use `SplitView`). |
| **24** | **Botão Pílula Direcional (`↘`)** | CTA principal `rounded-full` na cor pontual com círculo interno (`w-6 h-6`) e seta `↘`. | Contraste obrigatório: texto branco em `#e13535`/`#D97706` e texto escuro em `#35acd8`/`#10B981`. | **Usar:** Apenas 1 ou 2 por tela (ação principal).<br>**Evitar:** Botões secundários (`Limpar`, `Cancelar`). |
| **25** | **RichEditBox com Templates** | Editor de texto assistido por barra de pílulas que inserem frases/exame físico com 1 clique. | Auto-save em `localStorage` + contador de palavras + botão de copiar formatado. | **Usar:** Evoluções médicas, laudos e notas estruturadas.<br>**Evitar:** Campos puramente numéricos. |
| **26** | **Storage Dropzone Tátil** | Zona tracejada para arrastar PDFs/exames/JSON ou colar imagens da área de transferência (`Ctrl+V`). | No `dragover`, muda a borda para `--punctual-accent` e o fundo para `--punctual-soft`. | **Usar:** Importação de exames, fotos ou backups.<br>**Evitar:** Ocupar metade da tela após o upload concluir. |
| **27** | **InkCanvas (Desenho & Marcação)** | Superfície `<canvas>` para desenhar à mão livre, assinar ou marcar diagramas anatômicos. | 3 espessuras de traço, botão `Desfazer` e cores restritas ao grafite e `--punctual-accent`. | **Usar:** Mapa de dor/lesões e assinatura rápida.<br>**Evitar:** Quando botões pré-mapeados forem mais rápidos. |
| **28** | **Squint Test & Modo Foco** | Desfoque de auditoria (`filter: blur(5px)`) e escurecimento de barras periféricas. | Botão reversível em 1 clique na barra superior para testar se os 2% de cor guiam o olho. | **Usar:** Auditoria visual de hierarquia e foco profundo.<br>**Evitar:** Nunca iniciar ativado por padrão. |
