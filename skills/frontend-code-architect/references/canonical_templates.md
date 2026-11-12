# Templates Base Canônicos (`frontend-code-architect` v7.0.0)

## A. Fundação CSS: Tokens OKLCH em 3 Camadas, Sombras, `@container` e Breadcrumbs (`src/styles/globals.css`)

```css
@layer tokens, reset, layouts, components, utilities;

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  font-optical-sizing: auto;
  font-synthesis: none;
}

:root {
  color-scheme: light dark;

  /* 1. TOKENS PRIMITIVOS */
  --primitive-blue-500: oklch(0.62 0.21 258);
  --primitive-emerald-500: oklch(0.70 0.17 160);
  --primitive-neutral-50: oklch(0.985 0.004 255);
  --primitive-neutral-100: oklch(0.955 0.008 255);
  --primitive-neutral-800: oklch(0.22 0.025 260);
  --primitive-neutral-900: oklch(0.16 0.02 260);

  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;

  --step--1: clamp(0.8125rem, 0.78rem + 0.16vw, 0.9rem);
  --step-0:  clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --step-1:  clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --step-2:  clamp(1.5625rem, 1.4rem + 0.8vw, 2rem);

  /* 2. TOKENS SEMÂNTICOS (Aliases duplos --bg-*/--surface-* e --text-*/--ink-*) */
  --brand-primary: var(--primitive-blue-500);
  --brand-accent: var(--primitive-emerald-500);

  --bg-canvas: light-dark(var(--primitive-neutral-50), var(--primitive-neutral-900));
  --bg-surface-1: light-dark(oklch(1 0 0), var(--primitive-neutral-800));
  --bg-surface-2: light-dark(
    var(--primitive-neutral-100),
    oklch(from var(--primitive-neutral-800) calc(l + 0.05) c h)
  );
  --surface-canvas: var(--bg-canvas);
  --surface-sunken: var(--bg-surface-2);
  --surface-card: var(--bg-surface-1);
  --surface-elevated: var(--bg-surface-2);
  --surface-glass: oklch(from var(--bg-surface-1) l c h / 0.72);

  --text-primary: light-dark(
    color-mix(in oklab, var(--brand-primary) 15%, oklch(0.15 0.02 255)),
    oklch(0.96 0.01 255)
  );
  --text-secondary: light-dark(oklch(0.45 0.03 255), oklch(0.74 0.02 255));
  --text-muted: light-dark(oklch(0.52 0.02 255), oklch(0.66 0.02 255));
  --ink-primary: var(--text-primary);
  --ink-secondary: var(--text-secondary);
  --ink-muted: var(--text-muted);

  --border-subtle: light-dark(oklch(0.2 0.02 255 / 0.08), oklch(1 0 0 / 0.12));
  --catch-light: inset 0px 1px 0px 0px light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.12));

  --shadow-elevation-1:
    0px 1px 2px 0px oklch(0.2 0.03 255 / 0.05),
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.04),
    var(--catch-light);
  --shadow-elevation-2:
    0px 2px 4px -1px oklch(0.2 0.03 255 / 0.06),
    0px 6px 12px -2px oklch(0.2 0.03 255 / 0.08),
    0px 14px 24px -4px oklch(0.2 0.03 255 / 0.05);
  --shadow-elevation-3:
    0px 4px 8px -2px oklch(0.2 0.03 255 / 0.06),
    0px 16px 24px -4px oklch(0.2 0.03 255 / 0.10),
    0px 32px 48px -8px oklch(0.2 0.03 255 / 0.14);
  --shadow-inset:
    inset 0px 2px 4px 0px oklch(0.15 0.02 255 / 0.08),
    inset 0px 0px 0px 1px oklch(0.15 0.02 255 / 0.05);

  --elevation-1: var(--shadow-elevation-1);
  --elevation-2: var(--shadow-elevation-2);
  --elevation-3: var(--shadow-elevation-3);
  --sunken-recess: var(--shadow-inset);

  --font-sans: 'Inter', 'Plus Jakarta Sans', 'Geist', 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'Geist Mono', monospace;
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-fast: cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="light"] { color-scheme: light; }
[data-theme="dark"]  { color-scheme: dark; }

.section-wrapper { display: flow-root; }
.prose > * + * { margin-block-start: var(--flow-space, 1.25em); }

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
  gap: var(--space-6);
}

.sculpted-card {
  container-type: inline-size;
  container-name: card;
  background-color: var(--bg-surface-1);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: clamp(1rem, 4cqi, 1.75rem);
  box-shadow: var(--shadow-elevation-1);
  transition: transform 220ms var(--ease-spring), box-shadow 220ms var(--ease-spring), border-color 200ms ease;
}

.sculpted-card[data-variant="outlined"] { box-shadow: none; }
.sculpted-card[data-variant="subtle"] { background-color: var(--bg-surface-2); border-color: transparent; box-shadow: none; }
.sculpted-card[data-variant="elevated"]:hover, .sculpted-card[data-interactive="true"]:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-elevation-2);
  border-color: oklch(from var(--brand-primary) l c h / 0.35);
}
.sculpted-card[data-interactive="true"]:active {
  transform: translateY(0px);
  box-shadow: var(--shadow-elevation-1);
  transition-duration: 150ms;
  transition-timing-function: var(--ease-fast);
}
.sculpted-card:focus-visible, .sculpted-card:focus-within {
  outline: 2px solid var(--brand-primary);
  outline-offset: 3px;
}

.breadcrumbs ol { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; list-style: none; font-size: var(--step--1); }
.breadcrumbs li + li::before { content: "›"; margin-inline-end: 0.5rem; color: var(--text-secondary); pointer-events: none; }
.breadcrumbs a[aria-current="page"] { color: var(--text-primary); font-weight: 600; text-decoration: none; }

.tabular-metric { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }

@media (display-mode: standalone), (display-mode: minimal-ui) {
  .install-pwa-banner { display: none; }
  nav, button, .app-header { user-select: none; -webkit-user-select: none; }
}
@media (pointer: coarse) {
  button, .btn-action { min-block-size: 44px; min-inline-size: 44px; padding-inline: 1.25rem; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms; transition-duration: 0.01ms; transform: none; }
}
```

## B. Componente Polimórfico de Superfície com 4 Variantes e FSM (`src/components/ui/SurfaceCard.tsx`)

```tsx
import React, { useState } from 'react';

export type UIState = 'idle' | 'loading' | 'empty' | 'error' | 'pressed';
export type CardVariant = 'elevated' | 'outlined' | 'subtle' | 'card' | 'sunken';

export interface SurfaceCardProps extends React.HTMLAttributes<HTMLElement> {
  as?: 'article' | 'section' | 'div';
  title: string;
  eyebrow?: string;
  variant?: CardVariant;
  interactive?: boolean;
  isLoading?: boolean;
  isEmpty?: boolean;
  emptyActionLabel?: string;
  onEmptyAction?: () => void;
  error?: string | null;
}

export const SurfaceCard: React.FC<SurfaceCardProps> = ({
  as: Component = 'article',
  title,
  eyebrow,
  variant = 'elevated',
  interactive = false,
  isLoading = false,
  isEmpty = false,
  emptyActionLabel = 'Restaurar dados',
  onEmptyAction,
  error = null,
  className = '',
  children,
  ...props
}) => {
  const [isPressed, setIsPressed] = useState(false);
  const currentState: UIState = error
    ? 'error'
    : isLoading
      ? 'loading'
      : isEmpty
        ? 'empty'
        : isPressed
          ? 'pressed'
          : 'idle';

  return (
    <Component
      className={`sculpted-card ${className}`.trim()}
      data-variant={variant}
      data-interactive={interactive ? 'true' : 'false'}
      data-state={currentState}
      tabIndex={interactive ? 0 : undefined}
      aria-label={title}
      aria-busy={isLoading}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      {...props}
    >
      <header className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold tracking-tight">{title}</h3>
        {eyebrow && <span className="text-xs font-mono uppercase tracking-wider">{eyebrow}</span>}
      </header>
      {isLoading ? (
        <div role="status" aria-busy="true" aria-live="polite" className="p-4 rounded-lg">
          Sincronizando estado...
        </div>
      ) : error ? (
        <div role="alert" aria-live="assertive" className="p-4 rounded-lg font-medium">
          {error}
        </div>
      ) : isEmpty ? (
        <div className="p-4 rounded-lg flex items-center justify-between">
          <span>Nenhum registro encontrado para o filtro atual.</span>
          {onEmptyAction && (
            <button type="button" className="btn-action" onClick={onEmptyAction}>
              {emptyActionLabel}
            </button>
          )}
        </div>
      ) : (
        <div className="card-body">{children}</div>
      )}
    </Component>
  );
};
```
