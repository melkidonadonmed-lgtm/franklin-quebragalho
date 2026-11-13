# Padrões de Mutação `Antes vs. Depois` (`plan-uiux`)

```tsx
// ANTES ([FATO OBSERVADO]: Estilos genéricos sem suporte a temas, OKLCH ou a11y)
<div className="bg-gray-100 p-4 shadow">
  <button onClick={handleClick}>Enviar</button>
</div>

// DEPOIS ([INFERÊNCIA TÉCNICA]: Tokens em OKLCH, 60-30-10, área tátil min 48px)
<div className="surface-card">
  <button className="btn-primary" type="button" onClick={handleClick}>
    Enviar
  </button>
</div>
```

```css
.surface-card {
  container-type: inline-size;
  background-color: var(--surface-card, oklch(0.98 0.005 250));
  padding-inline: clamp(1rem, 3cqi, 1.75rem);
  padding-block: clamp(1rem, 3cqi, 1.75rem);
  border-radius: var(--radius-card, 16px);
  box-shadow: var(
    --shadow-elevation-1,
    0 1px 2px 0 oklch(0.2 0.03 255 / 0.05),
    0 2px 4px -1px oklch(0.2 0.03 255 / 0.04),
    inset 0 1px 0 0 oklch(1 0 0 / 0.85)
  );
}
```

---

## 2. Mutação de Espaçamento, Raios Concêntricos, `subgrid` e `:has()` em Cards

```css
/* ANTES ([FATO OBSERVADO]: Pixels arbitrários, mesmo border-radius interno/externo, card quebrando em sidebars estreitas) */
.card-legacy {
  width: 350px;
  padding: 23px;
  border-radius: 16px;
}
.card-legacy .metric-box {
  border-radius: 16px; /* Colisão óptica nos cantos! */
}

/* DEPOIS ([INFERÊNCIA TÉCNICA]: Tokens semânticos, @container, subgrid de 4 regiões e Raio Concêntrico R_in = max(4px, R_out - P)) */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: var(--space-grid-gap, clamp(1rem, 2.5vw, 1.5rem));
}

.card-shell {
  container-type: inline-size;
  container-name: card;
}

.ui-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-card-gap, 0.75rem);
  padding: var(--space-card-padding, clamp(1rem, 3cqi, 1.75rem));
  border-radius: var(--radius-card, 16px);
  background-color: var(--surface-card);
  box-shadow: var(--elevation-low);
}

.ui-card .metric-box {
  padding: var(--space-3) var(--space-4);
  border-radius: calc(var(--radius-card, 16px) - 6px); /* 10px concêntrico */
  font-variant-numeric: tabular-nums;
}

@container card (min-width: 340px) {
  .ui-card:has(> .card-media, > img) {
    display: grid;
    grid-template-columns: minmax(140px, 35%) 1fr;
  }
}
```

---

## 3. Mutação de Navegação: Barra Duplicada $\to$ Único DOM Adaptável (Bottom Nav $\leftrightarrow$ Sidebar Rail `240px`)

```css
/* ANTES ([FATO OBSERVADO]: Duas tags <nav> duplicadas no DOM ou menu fixo sem safe-area no mobile) */
.mobile-nav { display: block; height: 50px; }
.desktop-sidebar { display: none; }

/* DEPOIS ([INFERÊNCIA TÉCNICA]: Único <nav aria-label="Navegação Principal"> com env(safe-area-inset-bottom) e transição para Rail 240px em >= 48em) */
.adaptive-nav {
  position: fixed;
  inset-block-end: 0;
  inset-inline: 0;
  padding-block-end: env(safe-area-inset-bottom, 0px);
  background-color: var(--surface-card);
  box-shadow: var(--elevation-medium);
}

.nav-link {
  min-inline-size: 48px;
  min-block-size: 56px;
  touch-action: manipulation;
  user-select: none;
}

.nav-link[aria-current="page"] {
  font-weight: 600;
  color: var(--brand-primary);
  background-color: color-mix(in oklab, var(--brand-primary) 14%, transparent);
}

@media (min-width: 48em) {
  .adaptive-nav {
    position: sticky;
    inset-block-start: 0;
    block-size: 100dvh;
    inline-size: 240px;
  }
}
```
