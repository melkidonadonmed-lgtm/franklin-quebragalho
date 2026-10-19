# Guia de Tokens Clínicos, Calculadoras Determinísticas e Folha A4 (`v3.0.0`)

Referência de Tier 3 para implementação de interfaces médicas sob `design-interface-medica-minimalista`.

---

## 1. Tokens Semânticos Clínicos (`globals.css`)

```css
:root,
[data-theme="clinical-day"] {
  --bg-canvas: #F4F6F8;
  --bg-surface: #FFFFFF;
  --bg-elevated: #E8ECEF;
  --bg-contrast-card: #0F172A;
  --contrast-card-ink: #F8FAFC;

  --ink-primary: #0F172A;
  --ink-secondary: #334155;
  --ink-muted: #64748B;
  --ink-subtle: #94A3B8;

  --punctual-accent: #0284C7;
  --clinical-emerald: #059669;
  --clinical-amber: #D97706;
  --clinical-danger: #DC2626;

  --border-hairline: rgba(15, 23, 42, 0.08);
  --rim-light: rgba(255, 255, 255, 0.9);
  --shadow-sculpted:
    0 1px 2px rgba(15, 23, 42, 0.04),
    0 8px 20px -4px rgba(15, 23, 42, 0.05),
    inset 0 1px 0 0 var(--rim-light);

  --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', 'JetBrains Mono', monospace;
}

[data-theme="clinical-night"] {
  --bg-canvas: #0B0E14;
  --bg-surface: #121721;
  --bg-elevated: #1A2130;
  --bg-contrast-card: #F4F6F8;
  --contrast-card-ink: #0F172A;
  --ink-primary: #F1F5F9;
  --ink-secondary: #CBD5E1;
  --ink-muted: #94A3B8;
  --punctual-accent: #38BDF8;
  --border-hairline: rgba(255, 255, 255, 0.08);
  --rim-light: rgba(255, 255, 255, 0.07);
}

.clinical-unit {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  flex-shrink: 0;
}

@media print {
  @page {
    size: A4 portrait;
    margin: 15mm;
  }
  body {
    background: #FFFFFF !important;
    color: #000000 !important;
  }
  .no-print, nav, aside {
    display: none !important;
  }
  .sculpted-card {
    box-shadow: none !important;
    border: 1px solid #CBD5E1 !important;
    page-break-inside: avoid;
  }
}
```
