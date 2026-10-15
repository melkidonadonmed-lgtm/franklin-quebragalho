# Diretrizes do Design System Tátil & Multidimensional Melki (`v2.6.0-2026`)

Este documento contém o cânone visual, o Motor Multidimensional de Temas (Cores + Tipografia + Geometria + Acabamento), as fórmulas matemáticas de elevação 3D, as variáveis CSS e o catálogo completo de **22 temas homologados** no **FrontCraft Studio (`v2.6.0-2026`)**.

---

## 1. Princípios Fundamentais de Ergonomia Visual & Física 3D

### 1.1. Regra de Ouro da Profundidade Volumétrica (Z-Index Físico)
- **No Tema Escuro (Dark Mode):** Os cartões (`cards`) e superfícies elevadas **DEVEM ser visivelmente mais claros que o plano de fundo (`canvas`)** ($L_{\text{card}} > L_{\text{canvas}}$).
  - Exemplo canônico: Canvas `#090B10` ou `#060709` vs Cartões `#141824` ou `#11141D`.
  - **Causa Raiz:** Em fundos escuros onde o card tem a mesma tonalidade do fundo, as sombras tornam-se invisíveis e a interface perde o relevo físico. A diferença positiva de luminância entre o card e o fundo é o que permite à sombra projetada criar volume palpável.
- **No Tema Claro (Light Mode / Polar Sand):** O canvas adota tom mineral/polar suave (`#EEF2F6`, `#E3EBF2`, `#EFECE6`), enquanto os cards adotam branco puro (`#FFFFFF`) ou marfim elevado (`#FCFBF8`), com sombras de oclusão e contato nítidas (`rgba(11, 19, 43, 0.12)`).

### 1.2. Fio de Luz Superior Mineral (Rim Light) & Física 3D (`calculateCardTilt`)
Todo cartão e botão em relevo deve possuir uma linha de reflexão superior translúcida (micro-chanfro óptico) simulando a incidência de luz zenital, combinada com inclinação 3D opcional limitada a $\pm 5.5^\circ$:
```css
/* Gradiente suave de luz mineral no topo do card */
--rim-light-gradient: linear-gradient(90deg, transparent 5%, rgba(255, 255, 255, 0.18) 50%, transparent 95%);

/* Borda física superior */
border-top: 1px solid rgba(255, 255, 255, 0.14);
```

### 1.3. Motor Multidimensional de Temas (`TYPOGRAPHY_PRESETS` & `GEOMETRY_PRESETS`)
Cada tema reconfigura simultaneamente **4 eixos arquiteturais**:
1. **Pareamento Tipográfico (`TYPOGRAPHY_PRESETS`)**:
   - `humanist-tech`: **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.025em`)
   - `editorial-serif`: **Instrument Serif** + **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
   - `swiss-grotesk`: **Space Grotesk** + **Inter** + **JetBrains Mono** (`tracking: -0.03em`)
   - `classic-garamond`: **Cormorant Garamond** + **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
2. **Geometria Estrutural de Curvatura (`GEOMETRY_PRESETS`)**:
   - `sharp`: **6px** (Brutalista / Grid Suíço)
   - `editorial`: **12px** (Editorial Clássico)
   - `technical`: **16px** (Técnico / Precisão)
   - `tactile`: **20px** (Tátil Melki Padrão)
   - `organic`: **24px** (Orgânico / Cerâmico Biofílico)

---

## 2. Banimento Estrito de Cores Agressivas (Anti-Cobalto Neon)

- ❌ **TERMINANTEMENTE PROIBIDO:** Tons de azul cobalto ofuscante ou neon elétrico puro (`#0044FF`, `#1D4ED8`, `#233DFF`, `#0000FF`, `#00E5FF`).
- ❌ **TERMINANTEMENTE PROIBIDO:** Cores ácidas fluorescentes não balanceadas que agridam a vista em longas sessões de trabalho.
- ✅ **ACENTOS MINERAIS AUTORIZADOS:** Safira Fosco (`#3B82F6`), Slate Navy (`#345E7D`), Glacial Navy (`#274472`), Ouro Champanhe (`#D4AF37`), Titânio Anodizado (`#C5A880`), Terracota Editorial (`#9A3412`), Carmesim Suíço (`#BE123C`), Matcha Botânico (`#2E6F40`) e Violeta Ardósia (`#8B5CF6`).

---

## 3. Catálogo Oficial dos 22 Temas Homologados (`v2.6.0-2026`)

### 3.1. As 10 Paletas Canônicas Oficiais Melki (`canonical`)
| # | Tema | Canvas | Card | Acento | Tipografia & Raio | Aplicação |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| 1 | **Steadfast Stainless** | `#E3EBF2` | `#FFFFFF` | `#345E7D` | Space Grotesk + Inter • `16px` | CLIs web, ferramentas de sistema e DevOps |
| 2 | **Window Tide** | `#F4F8F9` | `#FFFFFF` | `#274472` | Plus Jakarta + JetBrains • `20px` | SaaS médico, prescrições e prontuários |
| 3 | **Cotton Dandelions** | `#E6E7E2` | `#F5F6F3` | `#3D5919` | Instrument Serif + Jakarta • `24px` | Obsidian, notas e leitura reflexiva calma |
| 4 | **Ocean Window** | `#C7CDC0` | `#FFFFFF` | `#21568A` | Space Grotesk + Inter • `16px` | Dashboards analíticos, KPIs e telemetria |
| 5 | **Mermaid Lagoon** | `#EAF3F8` | `#FFFFFF` | `#145DA0` | Plus Jakarta + JetBrains • `20px` | Landing pages e produtos SaaS modernos |
| 6 | **Nightfall Ambiance** | `#000B26` | `#094886` | `#2479DF` | Space Grotesk + Inter • `16px` | Dark Mode nativo para IDEs e monitoramento |
| 7 | **Sky Balloons** | `#F0F8FB` | `#FFFFFF` | `#1848A0` | Plus Jakarta + JetBrains • `20px` | Produtividade diurna e formulários limpos |
| 8 | **Grained Memories** | `#F5F5E9` | `#FFFFFF` | `#266D82` | Instrument Serif + Jakarta • `12px` | Documentação nobre e interfaces analógicas |
| 9 | **Living a Dream** | `#FFFFF6` | `#FFFFFF` | `#69ADC6` | Plus Jakarta + JetBrains • `24px` | Bem-estar, saúde serena e foco sem fadiga |
| 10 | **Van Gogh's Dream** | `#FDFEE9` | `#FFFFFF` | `#042698` | Cormorant Garamond + Jakarta • `12px` | Portais culturais e publicações de prestígio |

### 3.2. Os 5 Temas Tendências 2026 (`trends2026`)
| # | Tema | Canvas | Card | Acento | Tipografia & Raio | Aplicação |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| 11 | **Warm Editorial Paper** | `#EFECE6` | `#FCFBF8` | `#9A3412` | Instrument Serif + Jakarta • `12px` | IA conversacional, ensaios e leitura imersiva |
| 12 | **Quiet Luxury Titanium** | `#0B0C0E` | `#16181D` | `#C5A880` | Space Grotesk + Inter • `16px` | Fintechs de patrimônio e hardware precision |
| 13 | **Neo-Swiss Architectural Grid** | `#E6E9EF` | `#FFFFFF` | `#BE123C` | Space Grotesk + Inter • `6px` | Sistemas de engenharia e design ops suíço |
| 14 | **Biophilic Matcha & Alabaster** | `#E7ECE6` | `#FBFDF9` | `#2E6F40` | Cormorant Garamond + Jakarta • `24px` | Healthtechs clínicas, longevidade e foco |
| 15 | **Tactile Carbon & Violet Slate** | `#07080C` | `#12141E` | `#8B5CF6` | Space Grotesk + Inter • `14px` | Orquestradores de agentes de IA e IDEs 2026 |

### 3.3. Os 7 Temas Arquiteturais do Estúdio (`studio`)
| # | Tema | Canvas | Card | Acento | Tipografia & Raio | Aplicação |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| 16 | **Tactile Matte Minimalist** | `#090B10` | `#141824` | `#3B82F6` | Plus Jakarta + JetBrains • `20px` | **Padrão Oficial Melki**: Painéis e cockpits |
| 17 | **Phantom Obsidian 4K** | `#060709` | `#11141D` | `#38BDF8` | Space Grotesk + Inter • `16px` | Monitores 4K/OLED e centros de comando |
| 18 | **Luxury Deep Blue & Mineral** | `#070C18` | `#121C31` | `#60A5FA` | Instrument Serif + Jakarta • `20px` | Relatórios executivos e softwares premium |
| 19 | **Gilded Navy Heritage** | `#05070D` | `#0E1424` | `#D4AF37` | Cormorant Garamond + Jakarta • `12px` | Private banking e relatórios patrimoniais |
| 20 | **Polar Sand Light** | `#EEF2F6` | `#FFFFFF` | `#0284C7` | Plus Jakarta + JetBrains • `20px` | Sistemas diurnos com barra navy de ancoragem |
| 21 | **Emerald Terminal & Bio-OS** | `#070F0B` | `#0F1E17` | `#10B981` | Space Grotesk + Inter • `16px` | Telemetria de sensores e terminais de segurança |
| 22 | **Monokai Tactile / Amber** | `#0A0D12` | `#151B26` | `#F59E0B` | Space Grotesk + Inter • `16px` | Compiladores, debuggers e consoles técnicos |

---

## 4. Fórmulas Canônicas de Sombra e Elevação CSS

```css
:root {
  /* Tipografia Multidimensional */
  --font-display: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --tracking-display: -0.025em;

  /* Geometria e Curvatura */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;

  /* Elevação Padrão de Card (Multicamada: Contato + Projeção) */
  --shadow-contact: 0 2px 4px rgba(0, 0, 0, 0.45);
  --shadow-card: 0 4px 10px rgba(0, 0, 0, 0.35), 0 16px 36px -4px rgba(0, 0, 0, 0.65);
  --shadow-card-hover: 0 8px 16px rgba(0, 0, 0, 0.4), 0 24px 48px -6px rgba(0, 0, 0, 0.85);
  --shadow-elevated: 0 24px 60px -12px rgba(0, 0, 0, 0.9);
  --shadow-bevel: inset 0 1px 0 rgba(255, 255, 255, 0.1), inset 0 -1px 0 rgba(0, 0, 0, 0.6);
  --shadow-sunken: inset 2px 2px 6px rgba(0, 0, 0, 0.7), inset -1px -1px 3px rgba(255, 255, 255, 0.04);
}
```

---

## 5. Minimalismo, Antipoluição Visual, UI/UX Intuitiva & Suporte a TDAH

### 5.1. Regras Rígidas de UI/UX, Luz/Sombra e Antipoluição Visual (Obrigatórias em 100% dos Projetos)
1. **Destaque por Sombra, Profundidade e Incidência de Luz (NÃO por Cor Hiperdestacada)**:
   - O destaque de botões primários, abas ativas, badges e cartões deve nascer da **incidência de luz zenital** (`radial-gradient` no topo do card, `linear-gradient` nas teclas + `inset 0 1px 0` especular), **cavidades esculpidas** (`sunken wells` para inputs, trilhos de abas e pílulas) e **sombras físicas multicamadas** (oclusão + projeção).
   - **Proibido** usar cores hiperdestacadas, textos/botões pintados de azul/verde vibrante ou neon para chamar atenção. A hierarquia é escultural e luminosa, não cromático-saturada.
2. **Orçamento de Densidade por Card (Regra do 1+2 & Progressive Disclosure)**:
   - Cada cartão deve exibir no máximo **1 ação primária clara** (tecla física iluminada) e **2 ações secundárias discretas**. Ações extras devem ficar recolhidas em um menu popover (`⋯`) ou aparecer sob demanda.
   - Proibido empilhar 5 a 9 botões ou repetir emojis decorativos em cada botão de uma mesma grade.
3. **Zero "Caixa dentro de Caixa" Desnecessária**:
   - Separe metadados dentro do cartão usando tipografia (`font-mono`), espaço em branco (*whitespace* $\ge 30\%$) e divisórias sutis de `1px`. Reserve cavidades (`sunken wells`) para inputs de busca, trilhos de filtro e tags gravadas.
4. **Escaneabilidade em 3 Segundos & Ergonomia TDAH**:
   - Em até 3 segundos o usuário deve identificar: (1) onde está, (2) qual é o dado principal e (3) onde clicar.
   - Busca rápida centralizada (`Ctrl + K` / `⌘K`), feedback físico imediato nos botões (`translateY(1px)`), blindagem anti-squish (`flex-shrink: 0; white-space: nowrap;`) e proibição de `alert()` / `confirm()` nativos (usar toasts silenciosos com `role="status" aria-live="polite"`).

### 5.2. Preferências Flexíveis de Paleta e Temas (NÃO usar como camisa de força)
1. **Autonomia de Materiais e Superfícies por Projeto**:
   - Os 22 temas acima são um **repertório de preferência**, não uma obrigação de deixar todos os sistemas com a mesma cor. Varie as superfícies minerais (ardósia, titânio, basalto, calcário, papel algodão) de acordo com a alma do produto, mantendo sempre baixa saturação e relevo por luz e sombra.
2. **Kit de 5 Temas Integrados com `localStorage` (Para Cockpits, Utilitários e Testes)**:
   - Quando o projeto for um utilitário pessoal, dashboard de controle ou quando múltiplos temas forem desejados, inclua o seletor leve com persistência em `localStorage` contendo os **5 temas favoritos**:
     1. `Tactile Matte`
     2. `Phantom Obsidian 4K`
     3. `Quiet Luxury Titanium`
     4. `Steadfast Stainless`
     5. `Warm Editorial Paper`

