# `Before vs. After` Mutation Patterns (`plan-uiux`)

## 1. Surface & Tactile Action Mutation (`OKLCH` + 3-Layer Shadows)

```tsx
// BEFORE ([OBSERVED FACT]: Generic utility styles lacking theme support, OKLCH, or a11y)
<div className="bg-gray-100 p-4 shadow">
  <button onClick={handleClick}>Submit</button>
</div>

// AFTER ([TECHNICAL INFERENCE]: OKLCH tokens, 60-30-10 ratio, >= 48px coarse touch target)
<div className="surface-card">
  <button className="btn-primary" type="button" onClick={handleClick}>
    Submit
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

## 2. Spacing, Concentric Radii, `subgrid` & `:has()` Card Mutation

```css
/* BEFORE ([OBSERVED FACT]: Arbitrary pixels, matching inner/outer radii, card breaking inside narrow sidebars) */
.card-legacy {
  width: 350px;
  padding: 23px;
  border-radius: 16px;
}
.card-legacy .metric-box {
  border-radius: 16px; /* Optical corner collision! */
}

/* AFTER ([TECHNICAL INFERENCE]: Semantic tokens, @container, 4-region subgrid, Concentric Radius R_in = max(4px, R_out - P)) */
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
  border-radius: calc(var(--radius-card, 16px) - 6px); /* 10px concentric */
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

## 3. Navigation Mutation: Duplicate Bars $\to$ Single Adaptive DOM (Bottom Nav $\leftrightarrow$ `240px` Sidebar Rail)

```css
/* BEFORE ([OBSERVED FACT]: Two duplicated <nav> blocks in DOM or fixed bar missing mobile safe-area inset) */
.mobile-nav { display: block; height: 50px; }
.desktop-sidebar { display: none; }

/* AFTER ([TECHNICAL INFERENCE]: Single <nav aria-label="Primary navigation"> with env(safe-area-inset-bottom) transitioning to 240px Rail at >= 48em) */
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
