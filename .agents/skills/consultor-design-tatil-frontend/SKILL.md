---
name: consultor-design-tatil-frontend
description: >-
  Analisa e mapeia interfaces frontend via agent-browser, avalia conformidade com o Design System Tátil Melki (profundidade de sombras, cards mais claros que o fundo, rim light e paleta mineral anti-cobalto), oferece opções interativas de melhorias visuais e funcionais com formulários de múltipla escolha ou mockups de referência, audita discrepâncias determinísticas e gera o documento canônico DESIGN.md.
license: MIT
metadata:
  version: "1.2.0"
  author: "FrontCraftMaster & Melki"
  category: "Consultoria de Design Tátil e UX"
  updated_at: "2026-10-14"
  tags:
    - "consultoria-ux"
    - "design-tatil"
    - "paleta-mineral"
    - "design-md"
    - "multidimensional-2026"
version: 1.2.0
updated_at: 2026-10-14
author: FrontCraftMaster & Melki
category: Consultoria de Design Tátil e UX
---

# 1. NOME DA SKILL
`consultor-design-tatil-frontend` (Consultor e Mapeador de Frontend com Agent Web, Motor Multidimensional 2026, Relevo Tátil, Opções de Preferências e Gerador de DESIGN.md).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Carregue e execute esta skill sempre que:
- O usuário solicitar: "analise a interface deste app / frontend com agent-browser", "mapeie o frontend e me dê opções de melhorias no meu estilo", "audite a UI deste projeto e aponte discrepâncias com minhas preferências", "aplique meu design system tátil".
- Como etapa complementar após a execução de `auditoria-projetos-sistema`, quando for necessário conceber, refinar ou formalizar o arquivo `DESIGN.md` do projeto.
- Quando for preciso avaliar a ergonomia visual, hierarquia de sombras multicamada, contraste de cores e separação física entre cards e fundo.
- Para gerar formulários interativos de múltipla escolha (`ask_question`) ou mockups HTML de referência comparando a versão atual contra o padrão tátil.

### Quando NÃO Usar
- Para auditoria genérica de repositório focada exclusivamente em `.gitignore` ou código backend sem interface (utilize `auditoria-projetos-sistema`).
- Para tarefas simples de correção de bugs de sintaxe isolados sem impacto visual.
- Para aplicar mutações destrutivas em arquivos de código sem aprovação explícita do usuário (Human-in-the-Loop).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_url_or_path` (obrigatório): URL da aplicação web em execução (ex.: `http://localhost:3000`, `http://localhost:5173`) ou caminho absoluto de arquivo HTML local (ex.: `file:///C:/Users/melki/dev/repos/frontcraft-studio/index.html`).
- `project_root_path` (opcional): Diretório raiz do projeto para gravação do `DESIGN.md` resultante (padrão: diretório do projeto alvo).
- `archetype_preference` (opcional): Arquétipo visual dentre os **22 temas do FrontCraft Studio (`v2.6.0-2026`)**:
  * **7 Estúdio**: `tactile-matte` (Padrão Melki), `phantom-4k`, `luxury-deepblue`, `gilded-navy`, `polar-sand`, `emerald-terminal`, `monokai-tactile`.
  * **5 Trends 2026**: `warm-editorial-paper`, `quiet-luxury-titanium`, `neo-swiss-grid`, `biophilic-matcha-stone`, `tactile-carbon-2026`.
  * **10 Canônicas Melki**: `steadfast-stainless`, `window-tide`, `cotton-dandelions`, `ocean-window`, `mermaid-lagoon`, `nightfall-ambiance`, `sky-balloons`, `grained-memories`, `living-a-dream`, `van-goghs-dream`.
- `feedback_mode` (opcional): Mecanismo de interação com o usuário (`interactive_form` para formulário de múltipla escolha via `ask_question`, `html_mockup` para geração de artefato HTML de referência, ou `both`). Padrão: `both`.

---

## 4. DIRETRIZES TÉCNICAS E MÓDULOS DE DESIGN (PADRÃO MELKI `v2.6.0-2026`)

### 4.1. Módulo de Paleta de Cores Canônica & Motor Multidimensional

A paleta oficial do ecossistema prioriza tons minerais, superfícies de ardósia e contrastes equilibrados (WCAG AA/AAA), sincronizados com **4 Pares Tipográficos (`TYPOGRAPHY_PRESETS`)** e **5 Escalas de Curvatura (`GEOMETRY_PRESETS`)**:

| Função Semântica | Token CSS | Valor HEX | Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **Canvas Escuro (Fundo)** | `--bg-canvas` | `#090B10` / `#060709` | Fundo principal da aplicação no tema escuro |
| **Superfície Card Escuro** | `--bg-card` | `#141824` / `#11141D` | Superfície elevada dos cartões no tema escuro |
| **Superfície Modais / Menus** | `--bg-surface-2` | `#1D2436` / `#1B2130` | Painéis flutuantes, tooltips e flyouts |
| **Canvas Claro (Fundo)** | `--bg-canvas-light`| `#EEF2F6` / `#EFECE6` | Fundo suave Polar Sand / Editorial Paper |
| **Superfície Card Claro** | `--bg-card-light` | `#FFFFFF` / `#FCFBF8` | Branco puro ou marfim algodão elevado |
| **Acento Primário Sóbrio** | `--accent-primary` | `#3B82F6` / `#345E7D` | Safira Fosca / Slate Navy |
| **Acento Editorial / Titanium** | `--accent-2026` | `#9A3412` / `#C5A880` | Terracota Editorial / Ouro Titânio Anodizado |
| **Acento Suíço / Matcha** | `--accent-trend` | `#BE123C` / `#2E6F40` | Carmesim Suíço / Verde Matcha Botânico |
| **Acento Ouro Champanhe** | `--accent-gold` | `#D4AF37` / `#C5A059` | Destaques nobres, planos e badges executivas |
| **Acento Sage Clínico** | `--accent-sage` | `#10B981` / `#274472` | Sucesso, métricas positivas e saúde clínica |
| **Acento Amber / Violet** | `--accent-amber` | `#F59E0B` / `#8B5CF6` | Avisos, telemetria e AI Studio Dark Craft |

- ❌ **Banimento Categórico de Cores Agressivas (Anti-Cobalto):**
  - Proibido o uso de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`, `#0000FF`).
  - Proibido o uso de cores fluorescentes de saturação 100% desbalanceadas que causem estresse visual prolongado.

### 4.2. Módulo de Design Tátil e Composição Visual (Tactile Matte 4K + DNA 2026)

1. **Filosofia Anti-Glassmorphism & Primazia das Sombras:**
   - Proibido o uso de fundos de vidro com desfoque excessivo (`backdrop-filter: blur`), gradientes plásticos reflexivos e contornos neon brilhantes.
   - O relevo físico, os micro-chanfros e a oclusão volumétrica guiam a tridimensionalidade da interface.
2. **Regra de Ouro da Profundidade (Cards Lighter than Canvas):**
   - No tema escuro, os cartões e elementos interativos **DEVEM ser visivelmente mais claros que o canvas de fundo** (`L_card > L_canvas`).
   - Isso garante o contraste positivo necessário para que a projeção de sombra externa seja perceptível ao olho humano.
3. **Sistema de Sombras Físicas Multicamadas:**
   - Toda superfície elevada deve empregar no mínimo duas camadas complementares:
     * *Camada de Contato Curta:* `0 4px 10px rgba(0, 0, 0, 0.35)` (oclusão próxima).
     * *Camada de Projeção Difusa:* `0 16px 36px -4px rgba(0, 0, 0, 0.65)` (volume espacial).
     * *Micro-chanfro óptico:* `inset 0 1px 0 rgba(255, 255, 255, 0.1)`.
4. **Fio de Luz Superior Mineral (Rim Light Zenital) & Física 3D (`calculateCardTilt`):**
   - Cartões, botões e modais devem possuir acabamento superior refletindo luz zenital (`border-top: 1px solid rgba(255, 255, 255, 0.14);`) e inclinação 3D opcional limitada a $\pm 5.5^\circ$ (com desativação automática sob `prefers-reduced-motion`).
5. **Resiliência de Conteúdo (Anti-Squish):**
   - Botões de ação, badges e tags de status devem incluir obrigatoriamente `flex-shrink: 0;` e `white-space: nowrap;`, impedindo categoricamente quebras verticais de texto ("C o p i a r").
   - Caminhos de arquivo e URLs longas devem usar truncamento inteligente (`text-overflow: ellipsis; white-space: nowrap; overflow: hidden; min-width: 0;`) com atributo `title="..."`.
6. **Grid Responsivo & Ergonomia Cognitiva (Suporte TDAH):**
   - Largura mínima de coluna de `350px` em grids (`gap: 1.5rem`), evitando compactação de títulos.
   - Todo app deve conter atalho de busca rápida centralizada (`Ctrl + K` / `⌘K`).
   - Feedbacks cinestésicos físicos instantâneos em botões: `active:scale-95` ou `translateY(1px)`.
   - Proibido o uso de caixas de diálogo nativas bloqueantes (`alert()`, `confirm()`); utilizar toasts in-page ou modais contextuais.

### 4.3. Módulo de Opções Baseadas nas Preferências do Desenvolvedor

Sempre que a interface for avaliada ou concebida, a skill formula alternativas prontas alinhadas com as preferências do Melki:

1. **Apresentação Estruturada de Opções:**
   - Uso da ferramenta `ask_question` para permitir ao usuário escolher o arquétipo e as melhorias com 1 clique dentre os **22 temas** (7 Estúdio, 5 Trends 2026, 10 Canônicas Melki), os **4 Pares Tipográficos** (`humanist-tech`, `editorial-serif`, `swiss-grotesk`, `classic-garamond`) e as **5 Geometrias de Borda** (`6px`, `12px`, `16px`, `20px`, `24px`).
2. **Ecosistema de Componentes Open Source Autorizado (Padrão shadcn/ui):**
   - Priorizar componentes de código aberto "copy-paste" (desacoplados no projeto, sem pacotes "caixa-preta"): **shadcn/ui**, **Radix UI**, **Tailwind UI / Catalyst**, **Lucide Icons** e **Geist Design**.
3. **Geração de Mockup HTML Interativo:**
   - Criação de artefato `mockup_tatil_referencia.html` demonstrando a tela refatorada com as preferências aplicadas lado a lado com a versão original.

### 4.4. Módulo de Auditoria de Discrepâncias com as Preferências

O subagente confronta ativamente a interface inspecionada contra as preferências do desenvolvedor e gera uma tabela determinística de discrepâncias com status booleano:

| Código da Regra | Requisito de Preferência Melki | Status | Discrepância Detectada | Ação Corretiva Recomendada |
| :--- | :--- | :---: | :--- | :--- |
| **DISC-01: COR** | Ausência de azul cobalto ofuscante ou neon puro (`#0044FF`, `#233DFF`, `#1D4ED8`) | `[PASS] / [FAIL]` | Identifica hexadecimais saturados na folha de estilos | Substituir por Slate Navy (`#203657`) ou Petroleum Blue (`#2B4C7E`) |
| **DISC-02: DARK-LUM** | Cartão mais claro que o canvas no dark mode (`L_card > L_canvas`) | `[PASS] / [FAIL]` | Cartões pretos ou no mesmo tom do canvas (`#000` sobre `#000`) | Elevar o card para `#141B2D` ou `#162033` sobre canvas `#0B101B` |
| **DISC-03: SOMBRA** | Presença de sombras físicas multicamadas (contato + projeção difusa) | `[PASS] / [FAIL]` | Interface ultra-flat sem sombras ou sombra única rígida | Aplicar fórmula `--elevation-card` multicamada |
| **DISC-04: RIM-LIGHT** | Fio de luz superior zenital mineral em cartões e botões elevados | `[PASS] / [FAIL]` | Bordas uniformes sem simulação de luz zenital | Inserir `border-top: 1px solid rgba(255,255,255,0.14)` |
| **DISC-05: GLASS** | Anti-Glassmorphism (sem vidros borrados ou reflexos plásticos excessivos) | `[PASS] / [FAIL]` | Uso de `backdrop-filter: blur()` excessivo com caixas transparentes | Substituir vidro por superfície ardósia sólida fosca |
| **DISC-06: SQUISH** | Anti-squish em botões e badges (`flex-shrink: 0; white-space: nowrap;`) | `[PASS] / [FAIL]` | Botões com texto quebrado verticalmente | Aplicar classes `shrink-0 whitespace-nowrap` |
| **DISC-07: TDAH-UX** | Ergonomia cognitiva: busca rápida (`Ctrl+K`), sem alerts bloqueantes | `[PASS] / [FAIL]` | Uso de `window.alert()` nativo ou ausência de busca rápida | Implementar command bar rápida e toasts contextuais |
| **DISC-08: SUPPLY** | Componentes modulares copy-paste (padrão shadcn/ui) em vez de pacotes opacos | `[PASS] / [FAIL]` | Dependência de frameworks pesados caixa-preta | Adotar componentes Tailwind/Radix desacoplados |

---

## 5. PROCESSAMENTO PASSO A PASSO (FLUXO EXECUTIVO COM AGENT-BROWSER)

```text
[1. Conexão & Navegação via agent-browser]
               │
               ▼
[2. Mapeamento Estrutural do DOM & Nós Interativos]
               │
               ▼
[3. Diagnóstico nos 4 Módulos de Design & Preferências]
               │
               ▼
[4. Compilação da Matriz de Discrepâncias ([PASS]/[FAIL])]
               │
               ▼
[5. Consulta Interativa ao Usuário (ask_question / HTML Mockup)]
               │
               ▼
[6. Emissão e Gravação Canônica do DESIGN.md]
```

### Passo 1: Conexão e Navegação via agent-browser
1. Configurar o executável do navegador corporativo se necessário:
   ```powershell
   $env:AGENT_BROWSER_EXECUTABLE_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
   ```
2. Abrir a aplicação alvo com o `agent-browser`:
   ```powershell
   agent-browser open "[URL_DO_APP]"
   agent-browser wait 1500
   ```

### Passo 2: Mapeamento Estrutural do DOM e Nós Interativos
1. Obter o snapshot interativo da árvore de acessibilidade:
   ```powershell
   agent-browser snapshot -i
   ```
2. Capturar telas nos modos escuro e claro para análise de contraste e oclusão:
   ```powershell
   agent-browser --color-scheme dark screenshot --annotate
   agent-browser --color-scheme light screenshot
   ```
3. Mapear alvos de clique, formulários, botões e campos de inserção para validar tamanhos mínimos (>= 40x40px).

### Passo 3: Diagnóstico nos 4 Módulos de Design & Preferências
Executar a inspeção detalhada conforme:
- **Paleta de Cores:** Avaliar conformidade cromática, extrair valores hexadecimais e verificar ausência de azul cobalto neon.
- **Design Tátil:** Medir luminância relativa (`L_card > L_canvas`), presença de sombras multicamadas, rim light e classes anti-squish.
- **Opções das Preferências:** Identificar qual dos 5 arquétipos canônicos melhor equilibra o objetivo do software.
- **Detecção de Discrepâncias:** Atribuir status booleano (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) a cada regra da Matriz de Discrepâncias.

### Passo 4: Compilação da Matriz de Discrepâncias
Sintetizar as falhas e sucessos encontrados em uma tabela de auditoria clara, destacando o impacto visual e a solução em CSS/Tailwind.

### Passo 5: Consulta Interativa ao Usuário
Oferecer as melhorias através de:
1. **Formulário Interativo de Múltipla Escolha:** Acionar a ferramenta `ask_question` com opções pré-configuradas baseadas nos arquétipos do Melki.
2. **Artefato HTML de Referência:** Gerar um mockup executável (`mockup_tatil_referencia.html`) demonstrando o componente refinado com as melhorias aplicadas.

### Passo 6: Emissão e Gravação Canônica do `DESIGN.md`
Após a decisão do usuário (ou quando invocada para formalização pós-auditoria), gravar na raiz do projeto o arquivo `DESIGN.md` contendo:
- Metadados do projeto e arquétipo visual escolhido.
- Tabela completa de cores (HEX, sRGB, papéis semânticos e status WCAG).
- Fórmulas CSS de sombra, elevação, rim-light e raios de curvatura.
- Catálogo de componentes base e padrões de micro-interação.
- Matriz resolvida de discrepâncias auditadas.
- Lista de anti-padrões proibidos (regras negativas).

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A skill entrega:
1. **Relatório de Mapeamento Heurístico e Matriz de Discrepâncias:**
   - Tabela determinística com marcadores `[PASS]`, `[FAIL]` e `[UNVERIFIED]` para cada um dos 8 critérios de preferência.
2. **Pacote de Opções de Melhorias:**
   - Alternativas estruturadas de arquétipo visual e componentes (shadcn/ui e Lucide).
3. **Mecanismo Interativo de Validação:**
   - Pergunta interativa via `ask_question` e/ou link para o artefato `mockup_tatil_referencia.html`.
4. **Documento Canônico `DESIGN.md`:**
   - Especificação técnica consolidada gravada na raiz do projeto.

---

## 7. EXCEÇÕES, LIMITES E ANTI-PADRÕES (QUANDO NÃO USAR)

- NUNCA inventar dados de contraste ou propriedades CSS que não foram extraídos do DOM real ou inspecionados no código.
- NUNCA aplicar azul cobalto saturado (#0044FF) ou cores neon que violem a paleta mineral do Melki.
- NUNCA modificar arquivos de código fonte do projeto sem antes apresentar as opções e colher a confirmação do usuário.
- Se a URL do app estiver inacessível via `agent-browser` (ex.: porta fechada ou processo encerrado), a skill DEVE cair em fallback seguro: inspecionar o arquivo HTML/CSS estático localmente no disco e sinalizar `[UNVERIFIED]` nas asserções que dependerem de renderização dinâmica de viewport.
