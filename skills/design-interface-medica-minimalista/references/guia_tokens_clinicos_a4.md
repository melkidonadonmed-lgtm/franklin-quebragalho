# Guia de Tokens Clínicos, Calculadoras Determinísticas e Folha Vetorial A4 (`v4.0.0`)

Referência de Tier 3 para implementação de interfaces médicas sob `design-interface-medica-minimalista` alinhada ao SSOT de Física da Luz Zenital (90°–120°), Sombras Multi-Camadas e Folha Vetorial A4.

---

## 1. Tokens Semânticos Clínicos (`globals.css`)

```css
html, body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-optical-sizing: auto;
  font-synthesis: none;
}

:root,
[data-theme="clinical-day"] {
  --surface-canvas: #F4F6F8;
  --surface-sunken: #ECEFF3;
  --surface-card: #FFFFFF;
  --surface-elevated: #FFFFFF;
  --surface-glass: rgba(255, 255, 255, 0.84);

  --ink-primary: #0F172A;
  --ink-secondary: #334155;
  --ink-muted: #64748B;

  --cta-bg: #0F172A;
  --cta-ink: #F8FAFC;

  --status-ok: #059669;
  --status-warn: #D97706;
  --status-danger: #DC2626;
  --status-info: #0284C7;

  --border-hairline: rgba(15, 23, 42, 0.08);
  --catch-light: inset 0 1px 0 0 rgba(255, 255, 255, 0.85);
  --recess-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);

  --elevation-1:
    0 1px 2px -1px rgba(0, 0, 0, 0.08),
    0 2px 4px 0 rgba(0, 0, 0, 0.04),
    var(--catch-light);
  --elevation-2:
    0 4px 6px -2px rgba(0, 0, 0, 0.12),
    0 10px 15px -3px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.06),
    var(--catch-light);
  --elevation-3:
    0 12px 24px -6px rgba(0, 0, 0, 0.18),
    0 24px 48px -12px rgba(0, 0, 0, 0.14),
    0 0 0 1px rgba(128, 128, 128, 0.12),
    var(--catch-light);

  --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', 'JetBrains Mono', monospace;
}

[data-theme="clinical-night"] {
  --surface-canvas: #0B0E14;
  --surface-sunken: #07090D;
  --surface-card: #121721;
  --surface-elevated: #181F2C;
  --surface-glass: rgba(18, 23, 33, 0.82);

  --ink-primary: #F1F5F9;
  --ink-secondary: #CBD5E1;
  --ink-muted: #94A3B8;

  --cta-bg: #F8FAFC;
  --cta-ink: #0F172A;

  --border-hairline: rgba(255, 255, 255, 0.08);
  --catch-light: inset 0 1px 0 0 rgba(255, 255, 255, 0.12);
}

.clinical-unit {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  flex-shrink: 0;
}

.a4-sheet {
  width: 210mm;
  min-height: 297mm;
  background: #FFFFFF;
  color: #0F172A;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 12px;
  padding: 15mm;
  box-shadow: var(--elevation-2);
}

@media print {
  @page {
    size: A4 portrait;
    margin: 12mm;
  }
  body {
    background: #FFFFFF !important;
    color: #000000 !important;
  }
  .no-print, nav, aside {
    display: none !important;
  }
  .a4-sheet, .surface-card {
    box-shadow: none !important;
    border: 1px solid #CBD5E1 !important;
    page-break-inside: avoid;
  }
}
```
