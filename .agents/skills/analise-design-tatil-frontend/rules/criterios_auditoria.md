# Critérios Determinísticos de Auditoria: analise-design-tatil-frontend

Validações booleanas aplicadas para emissão do relatório comparativo:

- `[PASS]` **Critério 01 (Anti-Compactação):** Menus e links possuem espaçamento mínimo de `gap >= 12px` e padding confortável.
- `[FAIL]` **Critério 01:** Menus colapsados, espremidos ou claustrofóbicos (`gap < 8px` ou padding insuficiente).

- `[PASS]` **Critério 02 (Sidebar Estável):** Largura no estado expandido `>= 240px` sem truncamento forçado de rótulos.
- `[FAIL]` **Critério 02:** Sidebar inferior a 240px ou com quebra/reticências excessivas em labels essenciais.

- `[PASS]` **Critério 03 (Tipografia Nobre):** Famílias tipográficas refinadas (Inter, Geist Sans, JetBrains Mono ou calibradas).
- `[FAIL]` **Critério 03:** Uso de fontes padrão genéricas sem estilização (Arial crua, Times) ou fontes com problemas de kerning.

- `[PASS]` **Critério 04 (Ícones Uniformes):** Stroke padronizado (1.5px a 2.0px) e caixas de delimitação consistentes (Lucide Icons).
- `[FAIL]` **Critério 04:** Mistura de ícones de traços desiguais, preenchidos e contornados sem coerência de espessura.

- `[PASS]` **Critério 05 (Ergonomia de Botões):** Altura `>= 40px`, com classes `shrink-0` e `whitespace-nowrap` (anti-squish).
- `[FAIL]` **Critério 05:** Botões pequenos (`height < 36px`) ou que permitem quebra vertical de rótulo.

- `[PASS]` **Critério 06 (Cinestesia e Transições):** Elementos interativos possuem micro-interação ao clique (`active:scale-95`) e transições rápidas (150ms).
- `[FAIL]` **Critério 06:** Elementos estáticos sem feedback tátil ao clique ou transições lentas (>300ms).

- `[PASS]` **Critério 07 (Profundidade Dark Mode):** No tema escuro, os cartões são mais claros que o canvas (`L_card > L_canvas`) com sombras multicamadas.
- `[FAIL]` **Critério 07:** Cartões pretos no mesmo tom do canvas de fundo, eliminando a percepção de volume físico.

- `[PASS]` **Critério 08 (Banimento Anti-Cobalto):** Ausência total de azul cobalto neon (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes agressivas.
- `[FAIL]` **Critério 08:** Presença de azuis saturados de alta fluorescência que causam fadiga visual.
