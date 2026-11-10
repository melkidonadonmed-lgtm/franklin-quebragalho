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
  padding-inline: clamp(1rem, 2cqi, 1.5rem);
  padding-block: clamp(1rem, 2cqi, 1.5rem);
  box-shadow:
    0 1px 2px oklch(0.2 0.02 250 / 0.06),
    0 4px 8px oklch(0.2 0.02 250 / 0.04);
}
```
