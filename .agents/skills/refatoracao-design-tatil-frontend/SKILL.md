---
name: refatoracao-design-tatil-frontend
description: >-
  Executa a refatoracao e implementacao pratica de frontend por framework modular (React, Tailwind, HTML5/CSS, Vue), aplicando navegabilidade de alto padrao, menus descompactados com espacamento nobre, botoes ergonomicos com anti-squish, icones Lucide, tipografia refinada, elevacao tatil mineral e conformidade estrita com o Google HTML/CSS Style Guide e Google JSON Guide.
license: MIT
metadata:
  version: "1.1.0"
  author: "FrontCraftMaster & Melki"
  category: "Implementação e Refatoração Frontend"
  updated_at: "2026-10-04"
  tags:
    - "frontend"
    - "design-tatil"
    - "tailwind"
    - "refatoracao"
    - "anti-cobalto"
version: 1.1.0
updated_at: 2026-10-04
author: FrontCraftMaster & Melki
category: Implementação e Refatoração Frontend
---

# 1. NOME DA SKILL
`refatoracao-design-tatil-frontend` (Refatoração de Frontend Modular, Navegação de Alto Padrão, Injeção do Design System Tátil Melki e Conformidade Google Style Guides).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "refatore o frontend deste app", "aplique meu design system tátil no código", "reestruture menus e botões no padrão alto padrão", "corrija os botões espremidos e menus compactados", "troque o tema para o meu padrão mineral", "alinhe o HTML/CSS com o Google Style Guide".
- Como etapa sequencial após a execução de `analise-design-tatil-frontend` ou de uma auditoria com apontamentos em UI/UX.
- Quando for necessário injetar classes Tailwind, tokens CSS, componentes modulares ou reestruturar arquivos de estilo e JSX/TSX/HTML.
- Para eliminar menus claustrofóbicos, botões pequenos (`< 40px`), quebras de linha em botões ("C o p i a r"), azul cobalto e vidros borrados.
- Para higienizar código HTML/CSS expurgando tags vazias com autofechamento XML (`<br/>`), atributos redundantes (`type="text/javascript"`), classes fora de `kebab-case` e unidades inválidas em valores zero (`0px`).

### Quando NÃO Usar
- Para apenas inspecionar e relatar sem aplicar alterações de código (utilize `analise-design-tatil-frontend`).
- Para alterações em APIs puras de backend ou banco de dados que não toquem em templates ou estilização visual.
- Para realizar mudanças destrutivas ou apagar componentes funcionais sem aprovação prévia.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `project_root_path` (obrigatório): Caminho absoluto da raiz do projeto frontend a ser refatorado.
- `framework_target` (opcional): `react_tailwind`, `html_css_vanilla`, `vue_tailwind` ou `detect` (padrão: `detect` automático inspecionando `package.json` ou arquivos de código).
- `archetype` (opcional): Arquétipo visual desejado (`tactile_matte`, `phantom_obsidian`, `polar_sand`). Padrão: `tactile_matte` (Padrão Melki).
- `analysis_report_path` (opcional): Caminho do relatório comparativo gerado pela skill de análise.

---

## 4. MÓDULOS DE REFATORAÇÃO POR FRAMEWORK

A refatoração opera via módulos desacoplados de acordo com a stack técnica do projeto:

### 4.1. Módulo React / Next.js / Vite com Tailwind CSS
- **Tokens no Tailwind:** Configurar no `tailwind.config.js` ou `:root` em `globals.css` as superfícies minerais:
  ```css
  :root {
    --bg-canvas: #090B10;
    --bg-card: #141B2D;
    --bg-surface-2: #1E2B45;
    --accent-primary: #3B82F6;
    --rim-light: rgba(255, 255, 255, 0.14);
  }
  ```
- **Componentes Copy-Paste (Padrão shadcn/ui):** Manter componentes desacoplados na pasta `components/ui/` do projeto, sem pacotes externos fechados.

### 4.2. Módulo HTML5 Semântico / CSS Puro / Vanilla JS
- **Variáveis Nativas:** Injetar tokens no topo da folha de estilos principal (`style.css` ou `main.css`).
- **Classes Utilitárias Táteis:** Injetar classes reutilizáveis em `kebab-case`:
  * `.btn-tactile`: `height: 44px; display: inline-flex; align-items: center; justify-content: center; padding: 0 1.25rem; font-weight: 500; border-radius: 8px; flex-shrink: 0; white-space: nowrap; transition: all 150ms cubic-bezier(0.16, 1, 0.3, 1);`
  * `.card-tactile`: `background: var(--bg-card); border: 1px solid rgba(255, 255, 255, 0.08); border-top: 1px solid var(--rim-light); box-shadow: 0 2px 4px rgba(0,0,0,0.4), 0 10px 25px -4px rgba(0,0,0,0.65); border-radius: 12px;`

---

## 5. DIRETRIZES DE ALTO PADRÃO E GOOGLE STYLE GUIDES

Toda refatoração deve aplicar os 6 mandamentos de ergonomia tátil somados às regras oficiais do Google:

### 5.1. Conformidade Estrita com Google HTML/CSS Style Guide
- **Sintaxe HTML5 Semântica:**
  - Tags e atributos rigorosamente em caixa baixa (`<div class="card">`).
  - Indentação de 2 espaços por nível de aninhamento.
  - Proibição de autofechamento XML em tags void HTML5: usar `<br>`, `<img>`, `<hr>`, `<meta>`, `<link>`, `<input>` (NUNCA `<br />` ou `<img ... />`).
  - Omissão de atributos redundantes: omitir `type="text/css"` em `<link rel="stylesheet">` e `type="text/javascript"` em `<script>`.
  - Links com HTTPS explícito ou protocolo omitido (`//fonts.googleapis.com/...`).
- **Formatação CSS Canônica do Google:**
  - Classes e IDs exclusivamente em `kebab-case` (`.menu-item`, `.card-header`). Proibido `camelCase` em classes CSS.
  - Indentação de 2 espaços em blocos CSS.
  - Omissão de unidades em valores zero: `margin: 0;` (NUNCA `margin: 0px;`).
  - Espaço obrigatório após `:` e ponto e vírgula obrigatório ao final de cada declaração.
  - Uso de propriedades shorthand concisas (`padding: 8px 16px;`).

### 5.2. Conformidade com Google JSON Style Guide (`jsoncguide`)
- Em estados frontend, mocks e consumo de APIs:
  - Propriedades de objetos JSON obrigatoriamente em `camelCase` (`userId`, `profileImage`).
  - Estruturação de respostas simuladas com envelopes canônicos (`data`, `error`).

### 5.3. Menus Nobres (Não Compactar)
- **Espaçamento e Respiro:** Substituir layouts claustrofóbicos por espaçamentos generosos:
  * Container de navegação: `gap: 0.75rem` a `1rem` (12px a 16px).
  * Links e itens de menu: `padding: 0.625rem 1rem`, `border-radius: 8px`, texto legível com peso 500.
- **Sidebar Estável:** Largura mínima fixa de `260px` no desktop, impedindo que os itens fiquem comprimidos.

### 5.4. Tipografia e Fontes
- **Injeção de Fontes Autorizadas:** Configurar importação limpa de **Inter**, **Geist Sans** ou **JetBrains Mono** (para dados/código).
- **Hierarquia:**
  * `h1`: 1.75rem a 2.25rem, font-weight 600, tracking-tight.
  * `h2` / `h3`: 1.25rem a 1.5rem, font-weight 600.
  * Rótulos / Menus: 0.875rem a 0.9375rem, font-weight 500.
  * `line-height`: 1.5 para textos corridos.

### 5.5. Ícones Padronizados
- **Substituição por Lucide Icons:** Trocar ícones heterogêneos por componentes Lucide (`lucide-react` ou SVG/sprites Lucide nativos).
- **Proporções:** Tamanho fixo de `18px` a `20px` com `stroke-width: 1.75px` ou `2px`.

### 5.6. Botões Ergonômicos e Anti-Squish
- **Dimensão e Área de Toque:** `min-height: 40px` (preferência `44px`), padding lateral mínimo de `1rem`.
- **Blindagem Anti-Squish:** Adicionar obrigatoriamente `flex-shrink: 0; white-space: nowrap;` (Tailwind: `shrink-0 whitespace-nowrap`).
- **Relevo Físico Convexo:** Borda sutil, gradiente de 1 grau imperceptível ou rim-light no topo.

### 5.7. Transições e Micro-interações
- **Feedback Tátil:** Adicionar `active:scale-95` ou `translateY(1px)` em botões e cards clicáveis.
- **Tempo de Transição:** `transition: all 150ms cubic-bezier(0.16, 1, 0.3, 1)`.

### 5.8. Paleta Mineral e Eliminação de Anti-Padrões
- **Banimento Total:** Substituir qualquer `#0044FF`, `#233DFF`, `#1D4ED8` por Petroleum Blue (`#2B4C7E` / `#3B82F6`) ou Slate Navy (`#203657`).
- **Eliminação de Vidro Borrado:** Remover `backdrop-filter: blur` excessivo e fundos translúcidos de plástico, substituindo por ardósia fosca sólida.
- **Regra de Ouro da Luminância:** No Dark Mode, cartões devem ser mais claros que o fundo (`L_card > L_canvas`), com projeção de sombra física visível e rim-light no topo.

---

## 6. PROCESSO PASSO A PASSO (EXECUÇÃO DE REFATORAÇÃO)

```text
[1. Inspeção do Projeto & Seleção do Módulo de Framework]
                          │
                          ▼
[2. Injeção de Tokens de Cor, Sombra e Tipografia]
                          │
                          ▼
[3. Refatoração de Sintaxe HTML/CSS (Google Style Guides)]
                          │
                          ▼
[4. Refatoração da Navegação (Menus Descompactados & Sidebar)]
                          │
                          ▼
[5. Refatoração de Componentes (Botões Anti-Squish & Lucide)]
                          │
                          ▼
[6. Validação com Teste de Sanidade Visual (agent-browser)]
```

### Passo 1: Inspeção do Projeto
Detectar estrutura de arquivos (`package.json`, `tailwind.config.js`, `index.html`, `src/`).

### Passo 2: Injeção de Tokens
Atualizar ou criar variáveis CSS no arquivo de estilos central com o arquétipo mineral escolhido.

### Passo 3: Higienização de Sintaxe Google HTML/CSS
Remover autofechamentos XML de tags void (`<br>`, `<img>`), converter classes para `kebab-case` e eliminar unidades em valores zero (`0`).

### Passo 4: Refatoração de Menus e Layout
Ajustar componentes de Navbar e Sidebar para garantir o espaçamento nobre e largura mínima (`260px`).

### Passo 5: Refatoração de Componentes
Percorrer botões e formulários, inserindo classes ergonômicas, anti-squish e ícones Lucide.

### Passo 6: Verificação de Sanidade
Conferir visualmente via `agent-browser` ou abrindo o arquivo local no Chrome/Edge para assegurar que não ocorreram quebras de layout ou regressões visuais.

---

## 7. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill apresenta:
1. **Resumo das Alterações de Frontend:**
   - Arquivos modificados e tokens injetados.
   - Ajustes nos mandamentos de alto padrão e conformidade Google HTML/CSS.
2. **Diff / Código Refatorado:**
   - Trechos exatos alterados com explicação de cada ajuste tátil e de estilo.
3. **Checklist de Validação Determinística:**
   - Tabela com status `[PASS]` comprovando que os menus foram descompactados, botões calibrados, tags void sem barra e o cobalto eliminado.

---

## 8. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA quebrar a lógica de negócio, callbacks de evento (`onClick`, `onSubmit`) ou rotas da aplicação.
- NUNCA aplicar cores fluorescentes ácidas ou azul cobalto saturado.
- NUNCA introduzir dependências pesadas caixa-preta se for possível resolver com CSS/Tailwind e Lucide Icons desacoplados.
