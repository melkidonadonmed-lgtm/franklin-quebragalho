---
name: frontend-ui-ux-auditor
description: >-
  Audita com precisão matemática navegabilidade UI/UX, densidade DOM, fidelidade a Design Tokens (DESIGN.md), ícones, tipografia mobile, contraste WCAG 2.1 AA, física da luz (135°) e elevação por sombras. Use para diagnóstico visual e ergonômico de frontend; não use para testes de backend.
version: "1.0.0"
license: MIT
metadata:
  version: "1.0.0"
  author: "UI-Architect & Melki"
  category: "Frontend UI/UX Mathematical Auditing"
---

# Skill: Auditor de UI/UX, Navegabilidade e Design Systems Frontend

## 1. Objetivo, Propósito e Quando Usar (Gatilhos)

Esta Skill estabelece a esteira de auditoria técnica para inspecionar componentes e layouts frontend, garantindo acabamento estético de elite, acessibilidade estrita e conformidade com Design Tokens. A arquitetura segue a separação estrita de responsabilidades: o modelo cognitivo atua na análise contextual e decisões de refinamento, enquanto o script Python (`scripts/ui_ux_frontend_auditor.py`) executa cálculos determinísticos de contraste WCAG, contagem de nós no DOM e detecção de classes arbitrárias fora da escala.

### Gatilhos Positivos (Quando Usar):
- Solicitação de auditoria ou inspeção visual de telas, interfaces, menus e layouts.
- Verificação de Design Tokens, variáveis CSS e conformidade com o `DESIGN.md` (escala modular de 8px).
- Avaliação de renderização móvel, nitidez tipográfica e responsividade desktop-mobile.
- Auditoria de acessibilidade (contraste WCAG 2.1 AA, luminância relativa W3C e touch targets $\ge 44 \times 44\text{ px}$).

### Gatilhos Negativos (Exceções e Limites — Quando NÃO Usar):
- Revisão de regras de negócio puramente backend (queries SQL, rotas gRPC isoladas).
- Testes unitários de algoritmos computacionais sem relação com a camada visual.

---

## 2. Entradas e Pré-requisitos

1. **Alvo da Auditoria:** Arquivo `.html`, `.css`, `.jsx`, `.tsx`, `.vue` ou diretório raiz do frontend.
2. **Motor Determinístico:** `scripts/ui_ux_frontend_auditor.py`, executável via CLI (`python scripts/ui_ux_frontend_auditor.py --target <caminho>`) ou MCP (`franklin_run_skill_script`).
3. **Contrato de Design (Opcional):** `DESIGN.md` na raiz do projeto definindo variáveis semânticas (`--border-muted`, `--accent`, etc.).

---

## 3. Processamento e Fluxo: As 8 Dimensões Invioláveis da Auditoria Frontend UI/UX

### 3.1. Inventário, Densidade de Componentes e Árvore DOM
O auditor decompõe a interface nas quatro camadas do **Design Atômico** para evitar proliferação de nós órfãos:
- **Átomos:** Botões (`<button>`), campos (`<input>`), etiquetas (`<label>`), badges e ícones SVG isolados.
- **Moléculas:** Inputs compostos com ícone integrado, cards de métricas simples e chips de filtro.
- **Organismos:** Navbars, Sidebars colapsáveis, Bento Grids estruturais, modais de confirmação e tabelas de dados.
- **Templates e Layout:** Grids responsivos de 12 colunas e contêineres mestre.

**Limites de Densidade Estrutural:**
- **Teto de Profundidade:** Profundidade máxima da árvore DOM limitada a **$\le 12$ níveis** para prevenir gargalos de pintura e recálculo de estilo.
- **Divsoup Ratio:** A razão entre tags genéricas e o total de nós ($\frac{\text{tags } \langle\text{div}\rangle}{\text{total de tags}}$) deve ser mantida **$\le 0.45$**, exigindo o emprego universal de HTML5 semântico (`<main>`, `<header>`, `<nav>`, `<aside>`, `<section>`, `<article>`).

### 3.2. Design Tokens e Escala Modular de 8px (`DESIGN.md`)
Os Design Tokens funcionam como a fonte normativa única de verdade para espaçamentos, bordas e cores:
- **Grade de Espaçamento Base 8px:** Todo `padding`, `margin` e `gap` deve obrigatoriamente derivar da progressão canônica: `4px (0.5), 8px (1), 12px (1.5), 16px (2), 24px (3), 32px (4), 48px (6), 64px (8)`.
- **Detecção de Valores Arbitrários:** O auditor sinaliza e rejeita qualquer declaração pontual fora do catálogo do sistema (ex.: `p-[13px]`, `w-[37px]`, `gap-[7px]`, `margin: 11px`).
- **Espessamento de Tokens de Borda:**
  - Bordas estruturais em superfícies de repouso: estritamente `1px solid var(--border-muted)`.
  - Bordas de destaque ou foco ativo: padronizadas em `2px solid var(--accent)`.
  - É proibido mesclar espessuras aleatórias entre componentes da mesma hierarquia.

### 3.3. Navegabilidade Estrutural (Sidebar, Topbar, Menus e Acessibilidade)
A navegação deve manter previsibilidade tanto no Desktop quanto no Mobile:
- **Barra Lateral (Sidebar):**
  - **Desktop:** Largura fixa previsível (`240px` a `280px`), colapsabilidade com persistência de estado e transição suave.
  - **Mobile:** Conversão automática para Drawer/Menu Hambúrguer flutuante com camada de desfoque/escurecimento de fundo (*backdrop overlay*), suporte a fechamento pela tecla `Escape` e bloqueio de rolagem do body quando aberto.
- **Acessibilidade de Navegação por Teclado:**
  - Anéis de foco visíveis e destacados em todos os elementos acionáveis via `:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }`.
  - Mapeamento explícito da página ativa através do atributo semântico `aria-current="page"`.
  - Ordem sequencial lógica de `tabindex` correspondente à leitura visual.

### 3.4. Iconografia e Consistência Geométrica
Ícones comunicam função semântica e não devem sofrer distorções ou discrepâncias estilísticas:
- **Bounding Box Padronizado:**
  - Ícones em linhas de texto / badges: **$16 \times 16\text{ px}$** (`w-4 h-4`).
  - Ícones em botões e menus de navegação: **$20 \times 20\text{ px}$** (`w-5 h-5`).
  - Ícones de cabeçalho de seção e cartões de destaque: **$24 \times 24\text{ px}$** (`w-6 h-6`).
  - **Proporção Obrigatória 1:1:** O auditor reprova ícones com caixas assimétricas (ex.: `width="22"` e `height="18"`).
- **Consistência de Traço e Família:**
  - Emprego de uma única biblioteca vetorial (ex.: Lucide ou Heroicons), banindo a coexistência de pacotes visuais concorrentes.
  - Espessura de traço (*stroke-width*) padronizada (`1.5px`, `1.75px` ou `2.0px`) em todo o sistema.

### 3.5. Tipografia, Escala Modular e Nitidez Mobile (Anti-Embaçamento)
A tipografia define a hierarquia visual e não pode sofrer artefatos de renderização:
- **Escala Tipográfica Proporcional:** Estruturada sob razão modular (ex.: Major Second `1.125` ou Minor Third `1.20`):
  - `Display / H1`: 32px – 48px | `line-height: 1.15` | `font-weight: 700`
  - `H2`: 24px – 30px | `line-height: 1.25` | `font-weight: 600`
  - `Body`: 14px – 16px | `line-height: 1.5` a `1.6` | `font-weight: 400`
  - `Label / Caps`: 11px – 12px | `letter-spacing: 0.05em` | `font-weight: 500`
- **Mitigação de Fontes Embaçadas no Mobile:**
  - Em telas OLED e de alta densidade de pixels (Retina), exige-se a ativação de renderização subpixel nítida:
    ```css
    body {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
    }
    ```
  - Configuração obrigatória da meta tag no cabeçalho do documento:
    ```html
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ```
  - Proibição de textos corridos com tamanho inferior a **12px**.

### 3.6. Acessibilidade Cromática e Contraste WCAG 2.1 AA
O cálculo de contraste é executado deterministicamente com base na luminância relativa da norma W3C:

$$L = 0.2126 \cdot R' + 0.7152 \cdot G' + 0.0722 \cdot B'$$

Onde cada canal $C \in \{R, G, B\}$ em escala sRGB de 8 bits é normalizado por:

$$C' = \begin{cases} \frac{C/255}{12.92}, & \frac{C}{255} \le 0.04045 \\ \left(\frac{C/255 + 0.055}{1.055}\right)^{2.4}, & \frac{C}{255} > 0.04045 \end{cases}$$

A razão de contraste ($CR$) entre a cor de primeiro plano e a cor de fundo deve satisfazer:

$$CR = \frac{L_{\text{mais claro}} + 0.05}{L_{\text{mais escuro}} + 0.05}$$

- **Texto Normal (< 18pt regular ou < 14pt negrito):** **$CR \ge 4.5:1$** (Conformidade AA obrigatória).
- **Texto Grande e Componentes de Interface:** **$CR \ge 3.0:1$**.
- **Touch Targets no Mobile:** Área física clicável de no mínimo **$44 \times 44\text{ px}$** para impedir erros de acionamento em telas de toque.

### 3.7. Física da Luz (Eixo 135° / Chanfro Especular), Elevação Tátil e Bordas Reflexivas
Interfaces modernas de alto padrão aplicam regras de iluminação física (detalhadas em [`references/tactile_elevation_and_shadows.md`](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/frontend-ui-ux-auditor/references/tactile_elevation_and_shadows.md)) para produzir profundidade atmosférica sem poluição visual:
- **Chanfro Especular Superior (*Specular Micro-Bevel*) ou Eixo 135°:** Todo elemento de superfície elevada (botões, cards, modais) recebe destaque interno sutil de `1px` no topo (`--specular-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.75)` no Light Mode; `0.14` a `0.22` no Dark Mode) ou borda superior reflexiva (`border-top: 1px solid rgba(255, 255, 255, 0.15)`), combinado com bordas perimetrais translúcidas (`1px solid var(--border-subtle)` / `rgba(15, 23, 42, 0.08)`).
- **Elevação em Camadas (*Multi-Layered Shadows* — proibido sombra única pesada/preta pura no Light Mode):**
  1. *Oclusão de Contato (Ambient Occlusion):* deslocamento curto (`1px` a `2px`), desfoque mínimo e opacidade baixa (`4%` a `6%`) ancorando à base.
  2. *Difusão Direcional (Key Light):* projeção descendente no eixo Y com desfoque progressivo (`4px` a `32px`) e tom derivado da superfície (`rgba(15, 23, 42, 0.04..0.10)` no Light Mode):
     - **Baixa (`--elevation-low` / `tactile-low`):** `0 1px 2px -1px rgba(15,23,42,0.06), 0 2px 4px 0 rgba(15,23,42,0.04)`
     - **Média (`--elevation-medium` / `tactile-md`):** `0 2px 4px -1px rgba(15,23,42,0.06), 0 6px 14px -2px rgba(15,23,42,0.08)`
     - **Alta (`--elevation-high` / `tactile-lg`):** `0 4px 8px -2px rgba(15,23,42,0.05), 0 16px 32px -4px rgba(15,23,42,0.10)`
     - **Comprimida (`--elevation-pressed` / `tactile-pressed`):** `0 1px 1px 0 rgba(15,23,42,0.08), inset 0 1px 2px rgba(15,23,42,0.12)`
- **Glassmorphism com Desfoque Otimizado:** `backdrop-filter: blur(12px)` a `blur(16px)` acompanhado de fundo semi-transparente (`rgba(15, 23, 42, 0.75)`).

### 3.8. Transições, Dinâmica Tátil (`Hover` / `Active`) e Prevenção de Reflow
- **Zero Reflow (Aceleração Exclusiva por GPU):** Animar estritamente `transform`, `box-shadow`, `background-color` e `opacity`. Reprovação imediata ao animar `width`, `height`, `padding`, `margin`, `top` ou `left` (*layout thrashing*).
- **Microdinâmica Mecânica de Mola:**
  - *Hover:* Ascensão suave (`transform: translateY(-1px)` em botões, `translateY(-2px)` em cards interativos) com expansão para `--elevation-medium` (`--motion-release: 160ms cubic-bezier(0.2, 0, 0, 1)`).
  - *Active / Pressed:* Amortecimento físico nítido (`transform: translateY(1px) scale(0.99)` e `--elevation-pressed`) com transição rápida (`--motion-press: 100ms cubic-bezier(0.2, 0.8, 0.2, 1)`).
- **Acessibilidade a Movimento:** Respeito obrigatório à preferência `@media (prefers-reduced-motion: reduce)`.

---

## 4. Saídas e Entregáveis: Rubrica Matemática, Checklist e Relatório

A nota global da interface ($\text{Score}_{\text{UI/UX}} \in [0, 100]$) é calculada por combinação linear ponderada:

$$\text{Score}_{\text{UI/UX}} = \sum_{j=1}^{6} W_j \cdot S_j$$

| Dimensão Auditada | Peso ($W_j$) | Critério Central de Avaliação |
| :--- | :---: | :--- |
| **Design Tokens** | **0.20 (20%)** | Taxa de aderência à escala de 8px e ausência de valores arbitrários. |
| **Tipografia & Mobile** | **0.20 (20%)** | Legibilidade mobile, `antialiased`, entrelinha, meta viewport e contraste WCAG AA. |
| **Estrutura & Semântica** | **0.15 (15%)** | HTML5 semântico, `divsoup ratio` $\le 0.45$ e profundidade DOM $\le 12$. |
| **Iconografia** | **0.15 (15%)** | Proporção 1:1, bounding box padronizado (16/20/24px) e stroke uniforme. |
| **Física da Luz & Elevação** | **0.15 (15%)** | Aresta superior reflexiva 135° e sombras de elevação difusas. |
| **Movimento & Transições** | **0.15 (15%)** | Zero reflow (GPU), curvas Bézier e suporte a `prefers-reduced-motion`. |

### Checklist Silencioso de Liberação (Self-Refine)
- [ ] O contraste de texto em relação ao fundo atende ao mínimo de $4.5:1$ da WCAG 2.1 AA?
- [ ] Todos os alvos de clique no mobile possuem dimensão mínima de $44 \times 44\text{ px}$?
- [ ] A tag `<meta name="viewport" content="width=device-width, initial-scale=1.0">` está configurada?
- [ ] As regras de suavização de fonte (`antialiased` e `optimizeLegibility`) estão ativas?
- [ ] Nenhum elemento interativo anima propriedades de layout geométrico (`width`, `height`, `margin`)?
- [ ] Todos os ícones possuem formato quadrado (1:1) e derivam de uma família vetorial única?
- [ ] As superfícies elevadas possuem a borda reflexiva de refração do eixo de luz 135°?
- [ ] A barra lateral (sidebar) fecha e abre sem provocar transbordamento horizontal (*horizontal scroll*) no mobile?

### Execução do Motor Determinístico (`scripts/ui_ux_frontend_auditor.py`)
```powershell
uv run python skills/frontend-ui-ux-auditor/scripts/ui_ux_frontend_auditor.py --target "<arquivo_ou_diretorio>"
```
