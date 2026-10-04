---
name: analise-design-tatil-frontend
description: >-
  Inspeciona e audita interfaces frontend (via agent-browser ou codigo estatico), analisa menus, sidebar, tipografia, fontes, icones, tamanho dos botoes, transicoes, layout e profundidade tatil, emitindo um Relatorio Comparativo deterministico confrontando o estado atual contra as preferencias canônicas do Melki.
version: 1.0.0
updated_at: 2026-10-03
author: FrontCraftMaster & Melki
category: Diagnóstico Visual e Auditoria Frontend
---

# 1. NOME DA SKILL
`analise-design-tatil-frontend` (Diagnóstico Estrutural de Frontend, Inspeção Visual e Relatório Comparativo de Preferências).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative esta skill sempre que:
- O usuário solicitar: "analise o frontend deste projeto", "compare o design atual com minhas preferências", "mapeie menus, botões e fontes", "audite a interface do app sem alterar o código".
- Antes de iniciar qualquer refatoração de frontend, para levantar o baseline exato do projeto.
- Para verificar se uma interface respeita o espaçamento nobre de menus, alvos de clique ergonômicos, fontes adequadas e o banimento de azul cobalto neon.
- Quando for necessário inspecionar uma aplicação em execução via `agent-browser` ou código HTML/CSS estático gerando um relatório em tabela determinística (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).

### Quando NÃO Usar
- Para aplicar alterações, mutações ou correções de código CSS/JS (utilize `refatoracao-design-tatil-frontend`).
- Para auditorias genéricas de repositório Git ou checagem de backend sem interface (utilize `auditoria-projetos-sistema`).
- Para tarefas de infraestrutura ou pipelines de dados.

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `target_url_or_path` (obrigatório): URL ativa da aplicação (ex.: `http://localhost:5173`) ou caminho do arquivo HTML local (ex.: `C:\Users\melki\Projetos\frontcraft-studio\index.html`).
- `inspection_mode` (opcional): `live_browser` (via `agent-browser`) ou `static_code` (análise de arquivos em disco). Padrão: detecção automática (se URL acessível, `live_browser`; se arquivo estático, `static_code`).
- `output_report_path` (opcional): Caminho para salvar o relatório Markdown gerado (padrão: `.context/RELATORIO_ANALISE_FRONTEND.md` no projeto alvo).

---

## 4. DIRETRIZES DE INSPEÇÃO PONTO A PONTO (PREFERÊNCIAS MELKI)

A análise avalia rigorosamente os 8 pontos críticos do Design System Tátil:

### 4.1. Menus e Navegação
- **Anti-Compactação:** Proibição de menus colapsados ou espremidos com padding claustrofóbico.
- **Espaçamento Nobre:** Espaçamento mínimo entre itens de navegação (`gap >= 0.75rem` / `12px`), padding interno respirável (`padding >= 0.6rem 1rem`).
- **Respiro e Legibilidade:** Títulos de menu sem quebra forçada de linha e rótulos claros.

### 4.2. Sidebar (Barra Lateral)
- **Largura Mínima Operacional:** No estado expandido, a sidebar deve possuir largura de no mínimo `240px` a `280px` para acomodar rótulos completos e badges sem truncamento.
- **Hierarquia:** Separação semântica nítida entre seções de navegação, ações de rodapé e perfil de usuário.

### 4.3. Tipografia e Fontes
- **Famílias Autorizadas:** Valida se o projeto utiliza fontes profissionais refinadas (ex.: **Inter**, **Geist Sans**, **system-ui** bem calibrado e **JetBrains Mono** para dados/código).
- **Banimento de Fontes Genéricas:** Reprovação de fontes descalibradas (Arial crua, Times New Roman, Comic Sans ou fontes com kerning irregular).
- **Escala e Line-Height:** `line-height` relaxado (`1.4` a `1.6`), contrastes tipográficos WCAG AA mínimos (4.5:1).

### 4.4. Ícones
- **Padronização:** Adoção recomendada de **Lucide Icons** ou biblioteca equivalente de traço linear limpo.
- **Consistência de Stroke e Escala:** Espessura de traço consistente (`1.5px` a `2px`), caixas de delimitação uniformes (`16px`, `20px` ou `24px`).
- **Alinhamento Óptico:** Centralização vertical perfeita com o texto adjacente (`inline-flex items-center gap-2`).

### 4.5. Tamanho dos Botões e Alvos de Clique
- **Altura Ergonômica:** Altura mínima de `40px` (preferencialmente `44px`) para alvos de clique confortáveis.
- **Anti-Squish Obrigatório:** Presença de `flex-shrink: 0;` e `white-space: nowrap;` em botões de ação e tags, eliminando quebras verticais ("C o p i a r").
- **Padding Interno:** Mínimo horizontal de `1rem` (16px) em botões principais.

### 4.6. Transições e Micro-interações
- **Feedback Tátil Cinestésico:** Existência de resposta visual imediata no clique (`active:scale-95` ou `translateY(1px)`).
- **Curva e Tempo de Transição:** Animações rápidas e orgânicas (`150ms` a `200ms`, `cubic-bezier(0.16, 1, 0.3, 1)`).
- **Ausência de Rigidez:** Reprovação de elementos interativos que não ofereçam mudança perceptível de estado no hover/active.

### 4.7. Layout e Grids
- **Largura Mínima de Colunas:** Colunas em grids de dashboards devem respeitar largura mínima de `350px`, evitando quebras agressivas em telas médias.
- **Respiro Geral:** `gap` consistente entre cartões (`1.5rem` / `24px`).
- **Comando Rápido:** Presença ou ausência de barra de comando rápido (`Ctrl+K`).

### 4.8. Cores e Profundidade Tátil
- **Banimento Anti-Cobalto:** Reprovação expressa de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes ácidas.
- **Regra da Luminância no Dark Mode:** Cartões e painéis devem ser visivelmente mais claros que o canvas de fundo (`L_card > L_canvas`), garantindo o contraste necessário para projeção da sombra.
- **Sombras Multicamadas:** Presença de sombra de contato curta combinada com projeção difusa ampla.
- **Fio de Luz Superior (Rim Light):** Borda superior com micro-chanfro zenital mineral (`border-top: 1px solid rgba(255, 255, 255, 0.14)`).
- **Anti-Glassmorphism:** Reprovação de caixas de vidro transparentes com blur excessivo e reflexos plásticos.

---

## 5. PROCESSO PASSO A PASSO (INSPEÇÃO E COMPARAÇÃO)

### Passo 1: Varredura de Ambiente e DOM
1. Se URL acessível, abrir a página e capturar a árvore de acessibilidade via `agent-browser`:
   ```powershell
   agent-browser open "[URL]"
   agent-browser wait 1500
   agent-browser snapshot -i
   ```
2. Capturar telas em dark mode e light mode para inspeção de oclusão e contraste:
   ```powershell
   agent-browser --color-scheme dark screenshot --annotate
   ```
3. Se arquivos estáticos, inspecionar folhas de estilo (`globals.css`, `tailwind.config.js`) e componentes principais.

### Passo 2: Extração dos Parâmetros Reais
Mapear os valores reais em uso:
- Altura dos botões (`computedStyle.height`).
- Font-family dos títulos e parágrafos.
- Hexadecimais de fundo e cartões.
- Existência de classes `shrink-0`, `whitespace-nowrap`, `active:scale-95`.
- Espaçamento de itens da sidebar e navbar.

### Passo 3: Confronto com a Tabela Canônica de Preferências
Atribuir status determinístico para cada um dos 8 critérios:
- `[PASS]`: Atende integralmente à preferência do Melki.
- `[FAIL]`: Viola a diretriz ou apresenta defeito visual/ergonômico.
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

## 2. Matriz de Conformidade com as Preferências Melki

| Ponto de Análise | Estado Atual Detectado | Preferência Melki | Status | Discrepância / Diagnóstico |
| :--- | :--- | :--- | :---: | :--- |
| **1. Menus & Navegação** | [Ex: Espaço 4px, compactado] | Espaçamento nobre (gap >= 12px, padding relaxado) | `[FAIL]` | Menus espremidos gerando sensação claustrofóbica |
| **2. Sidebar** | [Ex: 180px de largura] | Mínimo 240px a 280px com labels completas | `[FAIL]` | Nomes de itens truncados |
| **3. Tipografia & Fontes** | [Ex: Arial / Roboto genérica] | Inter / Geist Sans / JetBrains Mono | `[FAIL]` | Tipografia padrão sem requinte visual |
| **4. Ícones** | [Ex: Ícones mistos sem padrão] | Lucide Icons com stroke uniforme (1.5-2px) | `[FAIL]` | Traços e tamanhos desiguais |
| **5. Botões & Anti-Squish** | [Ex: Altura 32px, quebra de linha] | Altura >= 40px, shrink-0, whitespace-nowrap | `[FAIL]` | Alvo pequeno e texto suscetível a squish |
| **6. Transições & Feedback**| [Ex: Sem efeito de clique] | active:scale-95, transição tátil 150ms | `[FAIL]` | Elementos estáticos sem cinestesia |
| **7. Layout & Grids** | [Ex: Coluna de 260px] | Colunas >= 350px, respiro generoso | `[PASS]` | Distribuição espacial adequada |
| **8. Cores & Relevo Tátil** | [Ex: Fundo preto e card preto] | L_card > L_canvas, sombras multicamadas, rim-light | `[FAIL]` | Sem percepção de profundidade física |

## 3. Recomendações Técnicas para Refatoração
[Lista de classes Tailwind / CSS sugeridas para alimentar a skill de refatoração]
```

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- **Read-Only Rigoroso:** Esta skill NUNCA modifica arquivos de código nem executa comandos de mutação.
- **Falsificabilidade:** NUNCA emitir `[PASS]` sem evidência comprovada extraída do DOM ou do CSS.
- **Fallback Estático:** Se a porta local estiver inacessível, inspecione os arquivos estáticos e marque itens que dependam de renderização como `[UNVERIFIED]`.
