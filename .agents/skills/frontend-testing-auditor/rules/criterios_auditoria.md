# Critérios Determinísticos de Auditoria — `frontend-testing-auditor` (`v2.5.0`)

- `[PASS]` Suíte de testes contém os identificadores explícitos `AUDIT-A11Y-01`, `AUDIT-A11Y-02`, `AUDIT-VIS-01`, `AUDIT-STATE-01`, `AUDIT-STATE-02` e `AUDIT-SEC-01`.
- `[FAIL]` Testes superficiais que apenas verificam renderização básica sem auditar `jest-axe`, `backdropFilter`, máquina de estados (`FSM`) ou injeção XSS.
- `[PASS]` Verifica explicitamente `expect(computedStyle.backdropFilter).not.toContain('blur')` e presença da classe `.ui-card-soft` sem azul cobalto.
- `[FAIL]` Ausência de verificação anti-glassmorphism ou falta do cálculo da rubrica ponderada $\text{Score} = 0.35\cdot\text{A11y} + 0.30\cdot\text{FSM} + 0.20\cdot\text{Tokens} + 0.15\cdot\text{Sec}$.
