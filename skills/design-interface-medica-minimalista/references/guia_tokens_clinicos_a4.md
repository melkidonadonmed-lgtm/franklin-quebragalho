# Guia de Tokens Clínicos `OKLCH`, Calculadoras Determinísticas e Folha Vetorial A4 (`v5.0.0`)

Referência de Tier 3 para implementação de interfaces médicas sob `design-interface-medica-minimalista`, alinhada ao SSOT de Cores Perceptuais `OKLCH` + `light-dark()`, Luz Zenital (90°–120°), Sombras Multi-Camadas sem `!important` (via `@layer`) e Folha Vetorial A4.

---

## 1. Tokens Semânticos Clínicos em `OKLCH` (`globals.css`)

```css
@layer reset, tokens, base, layouts, components, print;

@layer base {
  html, body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    font-optical-sizing: auto;
    font-synthesis: none;
  }
}

@layer tokens {
  :root {
    color-scheme: light dark;

    --surface-canvas: light-dark(oklch(0.97 0.005 245), oklch(0.16 0.015 255));
    --surface-sunken: light-dark(oklch(0.95 0.006 245), oklch(0.13 0.015 255));
    --surface-card: light-dark(oklch(1 0 0), oklch(0.21 0.018 255));
    --surface-elevated: light-dark(oklch(1 0 0), oklch(0.26 0.020 255));
    --surface-glass: light-dark(oklch(1 0 0 / 0.84), oklch(0.21 0.018 255 / 0.82));

    --ink-primary: light-dark(oklch(0.18 0.02 255), oklch(0.96 0.005 245));
    --ink-secondary: light-dark(oklch(0.38 0.02 255), oklch(0.82 0.012 250));
    --ink-muted: light-dark(oklch(0.52 0.02 255), oklch(0.68 0.015 250));

    --cta-bg: light-dark(oklch(0.18 0.02 255), oklch(0.97 0.005 245));
    --cta-ink: light-dark(oklch(0.97 0.005 245), oklch(0.18 0.02 255));

    --status-ok: oklch(0.60 0.15 162);
    --status-warn: oklch(0.68 0.16 70);
    --status-danger: oklch(0.58 0.20 25);
    --status-info: oklch(0.60 0.15 240);

    --border-hairline: light-dark(oklch(0.18 0.02 255 / 0.08), oklch(1 0 0 / 0.10));
    --catch-light: inset 0 1px 0 0 light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.12));
    --shadow-inset:
      inset 0 2px 4px 0 light-dark(oklch(0 0 0 / 0.06), oklch(0 0 0 / 0.45)),
      inset 0 0 0 1px light-dark(oklch(0 0 0 / 0.04), oklch(1 0 0 / 0.05));
    --shadow-inset-sunken: var(--shadow-inset);

    --shadow-layer-sm:
      0 1px 2px -1px light-dark(oklch(0.18 0.02 255 / 0.08), oklch(0 0 0 / 0.45)),
      0 2px 4px -1px light-dark(oklch(0.18 0.02 255 / 0.04), oklch(0 0 0 / 0.35)),
      var(--catch-light);
    --shadow-layer-md:
      0 4px 8px -2px light-dark(oklch(0.18 0.02 255 / 0.10), oklch(0 0 0 / 0.55)),
      0 12px 20px -4px light-dark(oklch(0.18 0.02 255 / 0.07), oklch(0 0 0 / 0.50)),
      var(--catch-light);
    --shadow-layer-lg:
      0 8px 16px -4px light-dark(oklch(0.18 0.02 255 / 0.12), oklch(0 0 0 / 0.65)),
      0 24px 48px -8px light-dark(oklch(0.18 0.02 255 / 0.14), oklch(0 0 0 / 0.60)),
      var(--catch-light);

    --shadow-elevation-1: var(--shadow-layer-sm);
    --shadow-elevation-2: var(--shadow-layer-md);
    --shadow-elevation-3: var(--shadow-layer-lg);
    --shadow-elevation-low: var(--shadow-elevation-1);
    --shadow-elevation-medium: var(--shadow-elevation-2);
    --shadow-elevation-high: var(--shadow-elevation-3);

    --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
    --font-mono: 'IBM Plex Mono', 'JetBrains Mono', monospace;
  }

  [data-theme="clinical-day"] { color-scheme: light; }
  [data-theme="clinical-night"] { color-scheme: dark; }
}

@layer components {
  .clinical-unit {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .a4-sheet, .sus-grid {
    inline-size: 210mm;
    min-block-size: 297mm;
    background: oklch(1 0 0);
    color: oklch(0.18 0.02 255);
    display: grid;
    grid-template-rows: auto 1fr auto;
    gap: 12px;
    padding: 15mm;
    box-shadow: var(--shadow-elevation-2);
  }
}

@layer print {
  @media print {
    @page { size: A4 portrait; margin: 12mm; }
    body { background: oklch(1 0 0); color: oklch(0.12 0 0); }
    .no-print, nav, aside { display: none; }
    .a4-sheet, .sus-grid, .surface-card {
      box-shadow: none;
      border: 1px solid oklch(0.85 0.01 250);
      break-inside: avoid;
    }
  }
}
```
