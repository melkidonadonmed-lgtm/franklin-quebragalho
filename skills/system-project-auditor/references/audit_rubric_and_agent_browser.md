# `agent-browser` (@eX) Protocol, `SGA`/`TIF` Calculus & `60-30-10 OKLCH` Rubric (`system-project-auditor` v6.1.0)

Level 3 technical reference unifying stack-adaptive `SGA` + `TIF` scoring (`deterministic_scorer.py`), live DOM inspection via `agent-browser` / `chrome-devtools-mcp` (UI targets only), and the **60-30-10 `OKLCH` + 3-Level Shadows** rubric (`[PASS: N/A_BACKEND_ONLY]` when `has_ui_layer == False`).

---

## 1. `60-30-10` Color Ratio in `OKLCH` and 3-Layer Shadows (Axes 3, 4 & 5)

| Ratio | Structural Role | Canonical Semantic Tokens (`OKLCH` + `light-dark()`) | Audit Rules |
| :---: | :--- | :--- | :--- |
| **60%** | **Dominant Surface (Canvas / Background)** | `--bg-canvas` / `--surface-canvas`: Light `oklch(0.985 0.004 255)` \| Dark `oklch(0.16 0.02 260)` | Pure `#000000` is banned in Dark Mode; maintain visual breathing room ($\ge 25\%$ whitespace). |
| **30%** | **Secondary Structure (Cards, Panels, Wells)** | `--bg-surface-1` / `--surface-card` (`L = 0.22`), `--bg-surface-2` / `--surface-elevated` (`L = 0.27`), `--surface-sunken` (`L = 0.13`) | Plane separation via progressive lightness $L$ steps and **3-Level Shadows** (`--shadow-elevation-1..3`). |
| **10%** | **Surgical Accent & Primary CTA / Focus** | `--brand-primary`: `oklch(0.62 0.19 255)` (derived via `color-mix(in oklab, ...)` and `oklch(from ...)`) | Restricted to primary CTAs, `:focus-visible`, and `6px` / `2px` semantic indicators. No neon sprawl. |

### Mandatory Anatomy of 3-Level Shadows (Single Flat Shadow Banned)

Each elevation level (`--shadow-elevation-1` Resting, `--shadow-elevation-2` Hover/Popover, `--shadow-elevation-3` Modal/Dock) combines **3 physical layers**:

1. **Contact Umbra (Short Occlusion):** `0 1px 2px 0 oklch(0.15 0.02 255 / 0.06..0.35)`
2. **Diffuse Penumbra with Negative `spread` (Zenith Light 90°–120°):** `0 6px 12px -2px oklch(0.15 0.02 255 / 0.08..0.45)`
3. **Top Zenithal Specular Rim (`Top Catch-Light`):** `inset 0 1px 0 0 oklch(1 0 0 / 0.85)` (Light) / `oklch(1 0 0 / 0.12)` (Dark).

---

## 2. Global Architecture Score (`SGA`) & Functional Sufficiency (`TIF`) Equations

Computed automatically by `scripts/deterministic_scorer.py --scan <path>`:

- **`INE` (25% — 3-Layer Navigability):** Checks $\le 3$ `<nav>` landmarks, zero Dead Ends, depth $\le 3$ clicks (`Ctrl+K`), and coverage of all 4 FSM states (`idle/empty`, `loading`, `success`, `error`).
- **`ICI` (20% — Island Cohesion & Anti-Tab-Sprawl):** Checks `@container`, in-place slot reuse (`<= 4` primary tabs, zero nested sub-tabs), and UI vs. I/O decoupling.
- **`IPC` (25% — Code Purity & `OKLCH` Tokens):** Penalizes hardcoded URLs/colors and direct DB/network coupling inside UI components.
- **`IRM` (15% — MVP Rigor):** Measures verifiable core capabilities vs. unnecessary bloat.
- **`ICTE` (15% — Fluid Typography & Anti-Squish):** Verifies `clamp()`, `65ch`, `tabular-nums`, `flex-shrink: 0; white-space: nowrap`, and unpacked menus (`font-size >= 13px`, `gap >= 8px`).

$$\text{SGA} = 0.25 \cdot \text{INE} + 0.20 \cdot \text{ICI} + 0.25 \cdot \text{IPC} + 0.15 \cdot \text{IRM} + 0.15 \cdot \text{ICTE}$$

---

## 3. Dynamic Inspection Protocol with `agent-browser` (@eX) & `chrome-devtools-mcp` (HITL Required)

```powershell
# 1. Prior deterministic AST and physical structure scan (No HITL)
uv run python skills/system-project-auditor/scripts/project_structure_and_code_auditor.py --target .
uv run python skills/system-project-auditor/scripts/deterministic_scorer.py --scan .

# 2. Live DOM dynamic inspection via agent-browser (Requires HITL when opening active URL)
agent-browser open $AppUrl
agent-browser wait 1500
agent-browser snapshot -i
agent-browser --color-scheme dark screenshot ./reports/dark_mode.png --full
agent-browser --color-scheme light screenshot ./reports/light_mode.png --full
agent-browser screenshot ./reports/audit_annotated.png --annotate
```

### Deterministic Failures Tracked in `@eX` Snapshots

- `[FAIL: VIOLATION_60_30_10_OR_OKLCH]`: Missing `oklch()` tokens, pure `#000000`, or chromatic sprawl violating `60-30-10`.
- `[FAIL: WASHED_SHADOW_OR_NO_ZENITH_LIGHT]`: Single blurred shadow lacking Umbra + negative-spread Penumbra + `inset 0 1px 0 0`.
- `[FAIL: COMPACT_MENU_OR_TAB_PROLIFERATION]`: Menu buttons with `font-size < 13px`, `gap < 6px`, `min-block-size < 44px` (`< 48px` on `any-pointer: coarse`), missing `env(safe-area-inset-bottom)` on mobile bottom bar, or nested sub-tabs.
- `[FAIL: ARBITRARY_SPACING_OR_NON_CONCENTRIC_RADIUS]`: Magic pixel values outside `--space-*`, Proximity Law violations ($\text{inner padding} > \text{outer gap}$), or inner `border-radius` equal to outer without subtracting padding ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$).
- `[FAIL: CARD_WITHOUT_CONTAINER_OR_BROKEN_SUBGRID]`: Card querying `@media` instead of `@container`, empty media slot without `:has(> img)`, or `container-type: inline-size` set on the same DOM node declaring `subgrid`.
- `[FAIL: GPU_BLUR_OR_WEAK_TYPOGRAPHY]`: Missing `antialiased` + `font-synthesis: none`, fractional `scale()` on text, `clamp()` with $\max > 2.5\times \min$, `transition: ... allow-discrete` inside shorthand, or missing `tabular-nums`.
- `[FAIL: DIVSOUP_OR_INERT_NODE]`: `<div>` elements faking buttons without ARIA or placebo controls with no real handler (`X does not activate Y`).
