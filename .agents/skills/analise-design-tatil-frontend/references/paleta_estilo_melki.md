# Diretrizes do Design System Tátil Melki (Padrão 2026)

Este documento contém o cânone visual, as fórmulas matemáticas de elevação, as variáveis CSS e a paleta mineral personalizada do usuário Melki, desenvolvidas no Cockpit Melki e no FrontCraft Studio.

---

## 1. Princípios Fundamentais de Ergonomia Visual

### 1.1. Regra de Ouro da Profundidade Volumétrica (Z-Index Físico)
- **No Tema Escuro (Dark Mode):** Os cartões (cards) e superfícies elevadas **DEVEM ser visivelmente mais claros que o plano de fundo (canvas)**.
  - Exemplo canônico: Canvas `#090B10` ou `#060709` vs Cartões `#141B2D` ou `#11141D`.
  - **Causa Raiz:** Em fundos escuros onde o card tem a mesma tonalidade do fundo, as sombras tornam-se invisíveis e a interface perde o relevo físico. A diferença positiva de luminância entre o card e o fundo é o que permite à sombra projetada criar volume palpável.
- **No Tema Claro (Light Mode / Polar Sand):** O canvas adota tom neutro/polar suave (`#EEF2F6` a `#F4F6FB`), enquanto os cards adotam branco puro (`#FFFFFF`) ou tonalidade elevada, com sombras de oclusão e contato nítidas (`rgba(11, 19, 43, 0.12)`).

### 1.2. Fio de Luz Superior Mineral (Rim Light)
Todo cartão e botão em relevo deve possuir uma linha de reflexão superior translúcida (micro-chanfro óptico) simulando a incidência de luz de topo:
```css
/* Gradiente suave de luz mineral no topo do card */
--rim-light-gradient: linear-gradient(90deg, transparent 5%, rgba(255, 255, 255, 0.18) 50%, transparent 95%);

/* Borda física superior */
border-top: 1px solid rgba(255, 255, 255, 0.14);
```

### 1.3. Primazia da Sombra sobre a Cor (Shadows Over Color)
- Relevo, micro-chanfros e sombras multicamada geram vida e distinção visual; blocos excessivos de cores saturadas geram poluição cognitiva.
- Cores de fundo dos botões secundários e terciários devem reaproveitar a própria cor da superfície (`--bg-surface-1` / `--bg-surface-2`) com chanfro óptico sutil.

---

## 2. Banimento Estrito de Cores Agressivas (Anti-Cobalto Neon)

- ❌ **TERMINANTEMENTE PROIBIDO:** Tons de azul cobalto ofuscante ou neon elétrico puro (`#0044FF`, `#1D4ED8`, `#0000FF`, `#00E5FF`).
- ❌ **TERMINANTEMENTE PROIBIDO:** Cores ácidas fluorescentes não balanceadas que agridam a vista em longas sessões de trabalho.
- ✅ **PALETA MINERAL AUTORIZADA:**
  - **Petroleum Blue / Safira Fosca:** `#2B4C7E` / `#3B82F6` (sempre atenuado ou translúcido)
  - **Slate Navy:** `#4A5B73` / `#1E293B`
  - **Sage Clínico / Esmeralda Mate:** `#2D6A4F` / `#10B981`
  - **Amber Matte / Ocre:** `#925C18` / `#F59E0B`
  - **Indigo Matte:** `#373B6B` / `#6366F1`
  - **Rust / Terracota Atenuado:** `#8A3D3D`
  - **Ouro Champanhe Fosco:** `#D4AF37` / `#C5A059`
  - **Ciano Astronômico:** `#38BDF8` (apenas para detalhes pontuais de foco)

---

## 3. Os 5 Arquétipos Oficiais do Ecossistema

| Arquétipo | Canvas | Card Superfície | Acento Principal | Propósito / Aplicação |
| :--- | :---: | :---: | :---: | :--- |
| **Tactile Matte Minimalist** | `#090B10` | `#141B2D` | `#3B82F6` (sóbrio) | **Padrão Oficial Melki**: Painéis executivos, cockpits e ferramentas diárias. |
| **Phantom Obsidian 4K** | `#060709` | `#11141D` | `#38BDF8` (céu) | Aplicações astronômicas, terminais ultra-dark e interfaces de telemetria. |
| **Luxury Deep Blue** | `#070C18` | `#121C31` | `#60A5FA` (mineral) | Ambientes editoriais, plataformas de conteúdo nobre e tipografia clássica. |
| **Gilded Navy Heritage** | `#05070D` | `#0E1424` | `#D4AF37` (ouro) | Sistemas de alto valor, aplicações financeiras executivas e prestígio. |
| **Polar Sand Light** | `#EEF2F6` | `#FFFFFF` | `#0284C7` (azul profundo) | Ambientes claros de alta luminosidade com barras navy escuras para ancoragem. |

---

## 4. Fórmulas Canônicas de Sombra e Elevação CSS

```css
:root {
  /* Elevação de Botão em Repouso */
  --elevation-button: 0 2px 4px rgba(0, 0, 0, 0.4), 0 1px 0 rgba(255, 255, 255, 0.08) inset;
  --elevation-button-pressed: inset 0 2px 4px rgba(0, 0, 0, 0.6);

  /* Elevação Padrão de Card (Multicamada: Contato + Projeção) */
  --elevation-card: 0 4px 12px rgba(0, 0, 0, 0.45), 0 16px 36px -4px rgba(0, 0, 0, 0.65);
  --elevation-card-hover: 0 8px 18px rgba(0, 0, 0, 0.5), 0 24px 48px -6px rgba(0, 0, 0, 0.85);

  /* Elevação Máxima (Modais e Flyouts) */
  --elevation-modal: 0 24px 60px -12px rgba(0, 0, 0, 0.9);

  /* Chanfros Ópticos */
  --rim-light: inset 0 1px 0 rgba(255, 255, 255, 0.12);
  --rim-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.6);

  /* Input Afundado (Sunken) */
  --shadow-sunken: inset 2px 2px 6px rgba(0, 0, 0, 0.7), inset -1px -1px 2px rgba(255, 255, 255, 0.04);
}
```

---

## 5. Suporte a TDAH e Ergonomia Cognitiva

1. **Agrupamento Semântico e Caixas Delimitadas**: Não deixar informações flutuando sem contorno; cada bloco de dados deve habitar seu próprio cartão tátil.
2. **Busca Rápida Centralizada (`Ctrl + K`)**: O usuário não deve navegar por menus complexos para encontrar uma função; todo app deve ter busca instantânea com revelação de abas.
3. **Feedbacks Físicos Imediatos**: Todo botão deve possuir `active:scale-95` ou `translateY(1px)` para fornecer feedback cinestésico tátil instantâneo.
4. **Proibição de Bloqueios Nativos**: Proibido o uso de `alert()` ou `confirm()` que travam o navegador; usar modais in-page ou toasts automáticos com auto-dismiss.
