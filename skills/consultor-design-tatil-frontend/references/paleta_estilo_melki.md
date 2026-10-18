# Diretrizes do Design System Tátil, Minimalist Impact & Multidimensional Melki (`DESIGN.md v4.5-soft`)

Este documento contém o cânone visual consolidado do **Minimalist Impact & Soft Tactile Architecture (`DESIGN.md v4.5-soft`)**: a Regra 60-30-10 Tonal, a Pilha de 4+1 Camadas com Iluminação Direcional a 135°, os **4 Presets Soft UI (Zero Cobalto)**, os **8 Kits de Componentes Soft UI** e o catálogo de **22 temas minerais homologados**.

---

## 1. Arquitetura Minimalist Impact & Soft Tactile (`DESIGN.md v4.5-soft`)

### 1.1. Economia Tonal 60-30-10 & Pilha de 4+1 Camadas (135° Directional Light)
- **Layer 0 (`60%` `surface-canvas`)**: Fundo neutro contínuo sem branco estourado (`#F1F4F8` em Nexus Slate; `#F4F3EC` em Moss; `#F5F4EE` em Soft Sapphire; `#12151B` / `#090B10` em Obsidian Dark).
- **Layer 1 (`surface-inset`)**: Cavidade física escavada (`#E5E9F0` com `inset 4px 4px 10px rgba(166,180,200,0.45), inset -4px -4px 10px rgba(255,255,255,0.85)`) para campos de busca, inputs, trilhos de switches/sliders e o **berço deslizante do ícone ativo na Sidebar (`#sidebar-active-tracker`)**.
- **Layer 2 (`surface-flat`)**: Placa intermediária de agrupamento (`#E9EEF5`) sem bordas duras de `1px`.
- **Layer 3 (`30%` `surface-raised` / `.ui-card-soft` / `.bento-card-soft`)**: Cards Bento esculpidos com iluminação direcional dupla a **135°** (`8px 8px 20px rgba(166,180,200,0.42), -8px -8px 20px rgba(255,255,255,0.95)`) e zero bordas duras. No modo escuro, respeita obrigatoriamente $L_{\text{card}} > L_{\text{canvas}}$.
- **Layer 4 (`surface-contrast` / `.terrixa-notched`)**: Âncora de inversão tonal monocromática (`#1E293B` / `#1A2E22` com recorte chanfrado opcional `clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 0 100%)`) para destacar cards críticos sem recorrer a neons.
- **Acento Focal Único (`10%` `--accent-point` — Zero Cobalto)**: Reservado exclusivamente para CTAs primários, barra vertical de `4px` da sidebar ativa e indicadores focais.

### 1.2. Os 4 Presets Soft UI (`DESIGN.md v4.5-soft` — Anti-Cobalto)
| Preset (`data-theme`) | Canvas (60%) | Raised / Inset (30%) | Contrast Anchor | Accent Focal (10% — Zero Cobalto) | Aplicação Principal |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`slate` (Nexus v4.5 Slate)** | `#F1F4F8` | `#F1F4F8` / `#E5E9F0` | `#1E293B` | **Cerulean Sapphire** (`#0284C7`) + `#7DD3FC` | Centros de operações agênticas, Bento Dashboards e SaaS |
| **`moss` (Moss & Calm System)** | `#F4F3EC` | `#F8F7F2` / `#E8E5DC` | `#1A2E22` | **Forest Moss** (`#174930`) + `#B7D3C0` | Saúde serena, escrita reflexiva e leitura longa sem fadiga |
| **`sapphire` (Soft Sapphire)** | `#F5F4EE` | `#FAF9F5` / `#E6E5DD` | `#1E293B` | **Ocean Sapphire** (`#1E6091`) + `#69ADC6` | Interfaces executivas, prontuários clínicos e sistemas diurnos |
| **`obsidian` (Obsidian Dark)** | `#12151B` | `#181D26` / `#0D1016` | `#F1F4F8` | **Mineral Ice** (`#38BDF8`) + `#10B981` | Plantões noturnos, IDEs, terminais e monitoramento 4K |

### 1.3. Motor Multidimensional de Temas (`TYPOGRAPHY_PRESETS` & `GEOMETRY_PRESETS`)
1. **Pareamento Tipográfico (`TYPOGRAPHY_PRESETS`)**:
   - `nexus-sans` / `humanist-tech`: **Public Sans** / **Plus Jakarta Sans** + **JetBrains Mono** (`line-height: 1.6`, `tracking: -0.025em`)
   - `editorial-serif`: **Instrument Serif** + **Public Sans** / **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
   - `swiss-grotesk`: **Space Grotesk** + **Inter** + **JetBrains Mono** (`tracking: -0.03em`)
   - `classic-garamond`: **Cormorant Garamond** + **Plus Jakarta Sans** + **JetBrains Mono** (`tracking: -0.015em`)
2. **Geometria Estrutural de Curvatura (`GEOMETRY_PRESETS`)**:
   - `sharp`: **6px** | `editorial`: **12px** | `technical`: **16px** | `tactile`: **20px** | `organic` / `soft-lg`: **24px** (`--rounded-pill: 9999px`)

---

## 2. Banimento Estrito de Cores Agressivas (Anti-Cobalto & Anti-Glassmorphism)

- ❌ **TERMINANTEMENTE PROIBIDO (`AUDIT-VIS-01`):** Tons de azul cobalto ofuscante ou neon elétrico puro (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`, `#0000FF`, `#00E5FF`).
- ❌ **TERMINANTEMENTE PROIBIDO (`AUDIT-VIS-01`):** Glassmorphism / vidro fosco com `backdrop-filter: blur()`, bordas neon ou bordas duras de `1px` em containers Bento.
- ✅ **ACENTOS MINERAIS E SAFIRA AUTORIZADOS:** Cerulean Sapphire (`#0284C7`), Ocean Sapphire (`#1E6091`), Mineral Ice (`#38BDF8`), Safira Fosco (`#3B82F6`), Slate Navy (`#345E7D`), Glacial Navy (`#274472`), Forest Moss (`#174930`), Clinical Emerald (`#059669`), Ouro Champanhe (`#D4AF37`), Titânio Anodizado (`#C5A880`) e Terracota Editorial (`#9A3412`).

---

## 3. Catálogo Oficial dos 22 Temas Minerais Homologados (`DESIGN.md v4.5-soft`)

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
| 16 | **Tactile Matte Minimalist** | `#090B10` | `#141824` | `#3B82F6` | Plus Jakarta + JetBrains • `20px` | **Padrão Dark Melki**: Painéis e cockpits |
| 17 | **Phantom Obsidian 4K** | `#060709` | `#11141D` | `#38BDF8` | Space Grotesk + Inter • `16px` | Monitores 4K/OLED e centros de comando |
| 18 | **Luxury Deep Blue & Mineral** | `#070C18` | `#121C31` | `#60A5FA` | Instrument Serif + Jakarta • `20px` | Relatórios executivos e softwares premium |
| 19 | **Gilded Navy Heritage** | `#05070D` | `#0E1424` | `#D4AF37` | Cormorant Garamond + Jakarta • `12px` | Private banking e relatórios patrimoniais |
| 20 | **Polar Sand Light** | `#EEF2F6` | `#FFFFFF` | `#0284C7` | Plus Jakarta + JetBrains • `20px` | Sistemas diurnos com Cerulean Sapphire |
| 21 | **Emerald Terminal & Bio-OS** | `#070F0B` | `#0F1E17` | `#10B981` | Space Grotesk + Inter • `16px` | Telemetria de sensores e terminais de segurança |
| 22 | **Monokai Tactile / Amber** | `#0A0D12` | `#151B26` | `#F59E0B` | Space Grotesk + Inter • `16px` | Compiladores, debuggers e consoles técnicos |

---

## 4. Fórmulas Canônicas de Sombra e Elevação CSS (`v4.5-soft`)

```css
:root {
  /* Camadas Tonais 60-30-10 (Nexus Slate Cerulean — Zero Cobalto) */
  --surface-canvas: #F1F4F8;
  --surface-flat: #E9EEF5;
  --surface-raised: #F1F4F8;
  --surface-inset: #E5E9F0;
  --surface-contrast: #1E293B;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --accent-point: #0284C7;
  --accent-sapphire: #1E6091;

  /* Iluminação Direcional 135° (Soft Neumorphism) */
  --soft-shadow-main: 8px 8px 20px rgba(166, 180, 200, 0.42);
  --soft-shadow-light: -8px -8px 20px rgba(255, 255, 255, 0.95);
  --soft-shadow-inset: inset 4px 4px 10px rgba(166, 180, 200, 0.45),
                       inset -4px -4px 10px rgba(255, 255, 255, 0.85);

  /* Geometria e Spring Physics */
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}
```
