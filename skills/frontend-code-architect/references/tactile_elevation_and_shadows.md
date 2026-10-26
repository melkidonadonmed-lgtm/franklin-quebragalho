# Referência Técnica & Módulo de Exemplo: Elevação Óptica em Camadas, Chanfro Especular e Dinâmica Tátil

> **Quando consultar esta referência (`franklin_skills_get(skill_name="frontend-code-architect", section="references")`):**
> Utilize este módulo ao implementar ou refatorar botões (`.btn-tactile`), cards (`.card-tactile`), menus e modais (`.modal-tactile`) que exijam **sombras multifásicas realistas (Oclusão de Contato + Key Light)**, **chanfro especular superior (`--specular-rim`)** e **amortecimento mecânico ao clique (`:active`)** em CSS nativo ou Tailwind CSS.

---

## 1. Vetores Ópticos do Sistema de Elevação Tátil

1. **Oclusão de Contato (*Ambient Occlusion*):** Camada curta (`1px` a `3px`) de baixa opacidade (`4%` a `6%` no Light Mode) que ancora o componente à superfície base.
2. **Difusão Direcional (*Key Light*):** Projeção descendente no eixo Y (`4px` a `32px`) comunicando a distância no eixo Z sem criar halos escuros pesados ou pretos puros (`#000000`) no Light Mode.
3. **Chanfro Especular (*Specular Micro-Bevel*):** Highlight interno de `1px` no topo (`inset 0 1px 0 0 rgba(255, 255, 255, ...)`) combinado com borda perimetral translúcida (`1px solid rgba(15, 23, 42, 0.08)`).
4. **Resposta Mecânica (`Hover` / `Active` / `Focus`):**
   - **Repouso:** `--elevation-low` + `--specular-rim-interactive`
   - **Hover:** `transform: translateY(-1px)` + `--elevation-medium` (`160ms cubic-bezier(0.2, 0, 0, 1)`)
   - **Active (Pressed):** `transform: translateY(1px) scale(0.99)` + `--elevation-pressed` (`100ms cubic-bezier(0.2, 0.8, 0.2, 1)`)
   - **Focus-Visible:** Anel de contraste desacoplado (`0 0 0 3px rgba(59, 130, 246, 0.35)`)

---

## 2. Tokens CSS & Componentes (`elevation-tactile-system.css`)

```css
:root {
  --surface-canvas: #f8fafc;
  --surface-raised: #ffffff;
  --surface-overlay: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --brand-primary: #2563eb;
  --brand-primary-hover: #1d4ed8;
  --brand-text: #ffffff;

  --border-subtle: rgba(15, 23, 42, 0.08);
  --border-focus: #3b82f6;

  --specular-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.75);
  --specular-rim-interactive: inset 0 1px 0 0 rgba(255, 255, 255, 0.35);

  --motion-press: 100ms cubic-bezier(0.2, 0.8, 0.2, 1);
  --motion-release: 160ms cubic-bezier(0.2, 0, 0, 1);

  --elevation-low: 
    0 1px 2px -1px rgba(15, 23, 42, 0.06),
    0 2px 4px 0 rgba(15, 23, 42, 0.04);

  --elevation-medium: 
    0 2px 4px -1px rgba(15, 23, 42, 0.06),
    0 6px 14px -2px rgba(15, 23, 42, 0.08);

  --elevation-high: 
    0 4px 8px -2px rgba(15, 23, 42, 0.05),
    0 16px 32px -4px rgba(15, 23, 42, 0.10);

  --elevation-pressed: 
    0 1px 1px 0 rgba(15, 23, 42, 0.08),
    inset 0 1px 2px rgba(15, 23, 42, 0.12);
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface-canvas: #090d16;
    --surface-raised: #131b2e;
    --surface-overlay: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --brand-primary: #3b82f6;
    --brand-primary-hover: #2563eb;
    --brand-text: #ffffff;

    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-focus: #60a5fa;

    --specular-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.14);
    --specular-rim-interactive: inset 0 1px 0 0 rgba(255, 255, 255, 0.22);

    --elevation-low: 
      0 1px 2px 0 rgba(0, 0, 0, 0.40),
      0 2px 6px -1px rgba(0, 0, 0, 0.35);

    --elevation-medium: 
      0 3px 6px -1px rgba(0, 0, 0, 0.50),
      0 8px 20px -2px rgba(0, 0, 0, 0.45);

    --elevation-high: 
      0 6px 12px -2px rgba(0, 0, 0, 0.60),
      0 20px 40px -4px rgba(0, 0, 0, 0.55);

    --elevation-pressed: 
      0 1px 1px 0 rgba(0, 0, 0, 0.50),
      inset 0 1px 3px rgba(0, 0, 0, 0.60);
  }
}
```

> Para o código completo do plugin Tailwind CSS (`tailwind.config.js` com `tactile-low`, `tactile-md`, `tactile-lg`, `tactile-pressed` e classes `.btn-tactile` / `.card-tactile`), consulte `skills/frontend-ui-ux-auditor/references/tactile_elevation_and_shadows.md`.
