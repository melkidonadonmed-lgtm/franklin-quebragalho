# Critérios Determinísticos de Auditoria: refatoracao-design-tatil-frontend

Validações booleanas aplicadas para a entrega da refatoração de código:

- `[PASS]` **Critério 01 (Menus Descompactados):** Código refatorado aplica espaçamento mínimo de `gap: 12px` (ou `gap-3`/`gap-4`) e padding relaxado na navegação.
- `[FAIL]` **Critério 01:** Menus mantêm elementos compactados, sem respiro ou com texto truncado forçadamente.

- `[PASS]` **Critério 02 (Anti-Squish em Botões):** Botões de ação possuem obrigatoriamente `shrink-0 whitespace-nowrap` (ou equivalente CSS).
- `[FAIL]` **Critério 02:** Botões refatorados continuam permitindo quebra vertical de texto sob compressão de tela.

- `[PASS]` **Critério 03 (Altura Ergonômica de Botões):** Altura mínima de `40px` (classe `h-10` ou `h-11` no Tailwind) garantida em botões principais.
- `[FAIL]` **Critério 03:** Botões com altura inferior a 36px ou área de toque insuficiente.

- `[PASS]` **Critério 04 (Ícones Lucide Padronizados):** Ícones convertidos para Lucide com espessura uniforme (`stroke-width` entre 1.5 e 2px).
- `[FAIL]` **Critério 04:** Persistência de ícones heterogêneos de diferentes pacotes com espessuras de traço incompatíveis.

- `[PASS]` **Critério 05 (Profundidade e Rim-Light):** Injeção de sombras multicamadas e fio de luz superior (`border-top: 1px solid rgba(255,255,255,0.14)` ou equivalente) em cards.
- `[FAIL]` **Critério 05:** Cards sem relevo físico ou com sombra única dura sem oclusão de contato.

- `[PASS]` **Critério 06 (Ausência de Cobalto Neon):** Zero ocorrências de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) nos arquivos refatorados.
- `[FAIL]` **Critério 06:** Presença de classes ou estilos com azul cobalto saturado.

- `[PASS]` **Critério 07 (Preservação Funcional):** Callbacks, eventos e IDs funcionais do código original são preservados integralmente no diff.
- `[FAIL]` **Critério 07:** Remoção inadvertida de funções, hooks ou manipuladores de clique durante a refatoração visual.
