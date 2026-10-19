# Critérios Determinísticos de Auditoria — `frontend-testing-auditor` (`v3.0.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para o gatekeeper determinístico de testes de frontend (`scripts/audit_tactile_ui.py` + Jest/Vitest + Axe-Core).

---

## 1. Execução Zero-LLM de `scripts/audit_tactile_ui.py` (`[AUDIT-GATE-01]`)
- **`[PASS]`**: O script `scripts/audit_tactile_ui.py` executa sem dependências externas de rede, remove comentários (`//` e `/* */`) antes da análise estática e exige `Readiness Score >= 90.0`, `S_Tokens >= 85.0` e `S_FSM >= 85.0` para emitir `Verdict: PASS`.
- **`[FAIL: AUDITORIA_SIMULADA]`**: Emissão de nota visual subjetiva sem executar `audit_tactile_ui.py` ou aprovação com `Readiness Score < 90.0`.
- **`[UNVERIFIED]`**: Nenhum arquivo `.tsx`, `.jsx`, `.vue`, `.html` ou `.css` encontrado no diretório alvo.

## 2. Cobertura das 4 Suítes Determinísticas e Rubrica Ponderada (`[AUDIT-GATE-02]`)
- **`[PASS]`**: Calcula exatamente $\text{Score} = (0.35 \cdot S_{\text{A11y}}) + (0.30 \cdot S_{\text{FSM}}) + (0.20 \cdot S_{\text{Tokens}}) + (0.15 \cdot S_{\text{Sec}})$ cobrindo:
  - `AUDIT-A11Y-01/02` (35%): `jest-axe` 0 violações WCAG 2.1 AA, `:focus-visible`, `aria-live`, `tabular-nums` e `prefers-reduced-motion`.
  - `AUDIT-STATE-01/02` (30%): Máquina de estados finitos executável (`data-state`, `data-theme`, `aria-busy`, `role="alert"` / `role="status"`).
  - `AUDIT-VIS-01` (20%): Famílias de tokens semânticos alinhadas ao propósito (`--bg-canvas`/`--bg-surface`/`--ink-primary`, `--surface-canvas`/`--surface-primary` ou `--surface-raised`), camadas esculpidas (`--shadow-sculpted`, `--rim-light`, `.sculpted-card`) e ausência de componentes órfãos (`SurfaceCard`/`SoftCard`).
  - `AUDIT-SEC-01` (15%): Bloqueio de `dangerouslySetInnerHTML` sem `DOMPurify` e `eval()`.
- **`[FAIL: SUITE_INCOMPLETA]`**: Omissão de qualquer uma das 4 dimensões ponderadas ou ausência de asserções anti-XSS.

## 3. Detecção Anti-Placebo e Anti-Comment-Gaming (`[AUDIT-GATE-03]`)
- **`[PASS]`**: Reprova automaticamente (`-25 pts`) comentários artificiais `// empty | loading | success | error` e componentes de card criados em `src/components/ui/` mas órfãos nas views (`-25 pts`).
- **`[FAIL: FALSO_POSITIVO_GAMING]`**: Aceitação de comentários estáticos como evidência de máquina de estados.
