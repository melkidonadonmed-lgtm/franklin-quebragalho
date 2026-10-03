# Critérios Determinísticos de Auditoria e Design Tátil (Padrão Melki)

Este arquivo define os critérios objetivos, booleanos e falsificáveis aplicados na auditoria visual e consultoria de frontend. Todo item avaliado deve obrigatoriamente receber um dos seguintes marcadores determinísticos:
- `[PASS]`: Requisito plenamente satisfeito com evidência mensurável.
- `[FAIL]`: Requisito violado com causa raiz identificada.
- `[UNVERIFIED]`: Não foi possível validar por ausência de insumo ou página inacessível.

---

## REGRA 1: Separação de Luminância no Tema Escuro (Regra de Ouro)
- **Definição:** No tema escuro, a luminância relativa do cartão de superfície deve ser estritamente superior à luminância do canvas de fundo (`L_card > L_canvas`).
- `[PASS]`: O fundo do card é perceptivelmente mais claro que o canvas (ex.: `#141B2D` sobre `#090B10`), permitindo que a sombra projetada seja visível e gere volume.
- `[FAIL]`: O card e o canvas possuem a mesma cor ou o card é mais escuro que o canvas no dark mode, achatando a interface e tornando as sombras invisíveis.

---

## REGRA 2: Relevo Físico e Sombras Multicamadas
- **Definição:** Elementos de superfície devem utilizar pelo menos 2 camadas de sombra complementares: uma sombra de contato curta e intensa (`0 2px 4px`) e uma sombra de projeção difusa ampla (`0 12px 28px -4px`).
- `[PASS]`: A classe ou variável CSS aplica sombra multicamada com dispersão calibrada (ex.: `--elevation-card` ou `--shadow-card`).
- `[FAIL]`: Interface inteiramente "flat" sem sombras, ou uso exclusivo de uma única sombra genérica sem camadas de contato.

---

## REGRA 3: Fio de Luz Mineral Superior (Rim Light)
- **Definição:** Cartões e botões elevados devem possuir uma borda superior translúcida ou gradiente linear horizontal que simule o reflexo óptico de luz de topo.
- `[PASS]`: Presença de `border-top: 1px solid rgba(255, 255, 255, alpha)` ou pseudo-elemento `::after` com gradiente reflexivo.
- `[FAIL]`: Ausência de qualquer acabamento de micro-bisel ou rim-light no topo de componentes elevados.

---

## REGRA 4: Banimento de Azul Cobalto e Cores Ácidas
- **Definição:** Nenhuma superfície interativa ou de destaque pode utilizar azul cobalto ofuscante puro (`#0044FF`, `#1D4ED8`) ou tons neons de saturação máxima desbalanceada.
- `[PASS]`: Acentos visuais utilizam paleta mineral atenuada (Petroleum Blue, Slate Navy, Amber Matte, Sage, Indigo, Champagne Gold ou Ciano Céu sóbrio).
- `[FAIL]`: Uso de `#0044FF`, `#1D4ED8` ou outros azuis fluorescentes que causem cansaço visual.

---

## REGRA 5: Acessibilidade e Contraste WCAG 2.1 (AA / AAA)
- **Definição:** Todo texto sobre superfície deve atender a razão matemática mínima de contraste de 4.5:1 para texto padrão e 3.0:1 para elementos de UI e textos grandes.
- `[PASS]`: Razão de contraste comprovada >= 4.5:1 (Nível AA) ou >= 7.0:1 (Nível AAA).
- `[FAIL]`: Razão de contraste inferior a 4.5:1 em textos normais de leitura.

---

## REGRA 6: Alvos Táteis e Interatividade sem Bloqueios
- **Definição:** Alvos de clique devem ter dimensões mínimas confortáveis (40x40px), feedback cinestésico tátil no hover/active (`active:scale-95` ou `translateY(1px)`) e ausência de alerts nativos.
- `[PASS]`: Botões com transições físicas suaves, áreas confortáveis de clique e modais contextuais in-page.
- `[FAIL]`: Presença de chamadas a `alert()` ou `confirm()` nativos, ou botões sem feedback visual de clique.

---

## REGRA 7: Emissão Estruturada do DESIGN.md
- **Definição:** Ao ser acionada para consolidar a auditoria, a skill deve gerar o arquivo `DESIGN.md` completo com tokens, variáveis CSS, classes Tailwind e guia de componentes.
- `[PASS]`: Arquivo `DESIGN.md` criado na raiz do projeto com todas as seções canônicas preenchidas.
- `[FAIL]`: Ausência do arquivo `DESIGN.md` ou arquivo com placeholders genéricos não resolvidos.
