# Critérios Determinísticos de Auditoria — `frontend-code-architect` (`v4.0.0`)

- `[PASS]` Estrutura modular `src/` dividida em `components/ui/`, `components/bento/`, `components/layout/`, `config/` (`tokens.ts` + `DESIGN.md`), `styles/` (`globals.css` + `theme.css`) e `types/` com arquivos $\le 300$ linhas.
- `[FAIL]` Componentes monolíticos na raiz ou ausência de separação em 5 camadas de Design Atômico.
- `[PASS]` Uso estrito da regra 60-30-10 tonal (`surface-canvas`, `surface-raised`, `surface-inset`, `surface-contrast`) com iluminação direcional dupla a 135° e acento Cerulean/Ocean Sapphire (`#0284C7` / `#1E6091`).
- `[FAIL]` Presença de `backdrop-filter: blur()`, bordas neon, bordas duras de 1px ou azul cobalto (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`).
- `[PASS]` Componentes tipados em TypeScript estrito (zero `any`) com suporte a estados FSM (`isLoading`, `error`) e atributos WAI-ARIA (`aria-label`, `aria-busy`, `role="status"`, `role="alert"`).
