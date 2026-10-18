# Critérios Determinísticos de Auditoria — `design-md` (`v4.5.0`)

- `[PASS]` O arquivo `DESIGN.md` gerado contém o frontmatter YAML `version: "4.5-soft"` com as camadas tonais (`surface-canvas`, `surface-raised`, `surface-inset`, `surface-contrast`) e iluminação direcional a 135°.
- `[FAIL]` Ausência de tokens de superfície tátil ou uso de bordas duras de 1px sem relevo tonal.
- `[PASS]` Paleta 100% livre de azul cobalto elétrico (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`), adotando Cerulean Sapphire (`#0284C7`), Ocean Sapphire (`#1E6091`), Moss (`#174930`) ou Mineral Ice (`#38BDF8`).
- `[FAIL]` Presença de qualquer código hexadecimal de azul cobalto, neon ou `backdrop-filter: blur()`.
- `[PASS]` Integração explícita com `frontend-code-architect` (`v4.0.0`) e `frontend-testing-auditor` (`v2.5.0`).
