# Critérios Determinísticos de Auditoria — `plan-uiux`

- `[PASS]` Evidência estática coletada via `analyze_javascript_application` / `inspect_go_binary` e filtrada via `inspect_analysis_view(detail="summary")`.
- `[PASS]` Tokens de cor em `oklch(L C H)` respeitando a proporção 60-30-10, sombras multi-camadas e `@container`.
- `[FAIL]` Ausência de classificação epistêmica (`[FATO OBSERVADO]`, `[INFERÊNCIA TÉCNICA]`, `[INCERTEZA / LACUNA]`) ou falta de bloco `Antes vs. Depois`.
- `[FAIL]` Presença de sombras planas de 1 camada, emojis decorativos em controles ou ausência de `:focus-visible`.
