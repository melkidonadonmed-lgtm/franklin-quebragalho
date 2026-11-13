# Protocolo `agent-browser` (@eX), Cálculo `SGA`/`TIF` e Rubrica `60-30-10 OKLCH` (`auditoria-projetos-sistema` v6.0.0)

Referência técnica de Tier 3 unificando a inspeção dinâmica via `agent-browser` / `chrome-devtools-mcp`, o motor matemático `SGA` + `TIF` (`deterministic_scorer.py`) e a rubrica de **Proporção `60-30-10` em `OKLCH` + Sombras em 3 Níveis**.

---

## 1. Regra Cromática `60-30-10` em `OKLCH` e Sombras em 3 Camadas (Eixos 3, 4 e 5)

| Proporção | Papel Estrutural | Tokens Semânticos Canônicos (`OKLCH` + `light-dark()`) | Regras de Auditoria |
| :---: | :--- | :--- | :--- |
| **60%** | **Superfície Dominante (Canvas / Fundo)** | `--bg-canvas` / `--surface-canvas`: Claro `oklch(0.985 0.004 255)` \| Escuro `oklch(0.16 0.02 260)` | Proibido `#000000` puro no Dark Mode; deve garantir respiro visual ($\ge 25\%$ de área livre). |
| **30%** | **Estrutura Secundária (Cards, Painéis, Recessos)** | `--bg-surface-1` / `--surface-card` (`L = 0.22`), `--bg-surface-2` / `--surface-elevated` (`L = 0.27`), `--surface-sunken` (`L = 0.13`) | Diferenciação de planos por elevação progressiva de Luminosidade $L$ e **Sombras em 3 Níveis** (`--shadow-elevation-1..3`). |
| **10%** | **Acento Cirúrgico e Ação Primária (CTA / Foco)** | `--brand-primary`: `oklch(0.62 0.19 255)` (derivado via `color-mix(in oklab, ...)` e `oklch(from ...)`) | Restrito a CTAs primários, `:focus-visible` e indicadores semânticos de `6px` / `2px`. Proibido espalhar cores neon. |

### Anatomia Obrigatória das Sombras em 3 Níveis (Proibido Sombra Única Chapada)

Cada nível (`--shadow-elevation-1` Repouso, `--shadow-elevation-2` Hover/Popover, `--shadow-elevation-3` Modal/Dock) combina **3 camadas físicas**:

1. **Umbra de Contato (Oclusão Curta):** `0 1px 2px 0 oklch(0.15 0.02 255 / 0.06..0.35)`
2. **Penumbra Difusa com `spread` Negativo (Luz Zenital 90°–120°):** `0 6px 12px -2px oklch(0.15 0.02 255 / 0.08..0.45)`
3. **Borda Especular Zenital Superior (`Top Catch-Light`):** `inset 0 1px 0 0 oklch(1 0 0 / 0.85)` (Claro) / `oklch(1 0 0 / 0.12)` (Escuro).

---

## 2. Equações do Score Global de Arquitetura (`SGA`) e Suficiência (`TIF`)

Calculadas automaticamente por `scripts/deterministic_scorer.py --scan <caminho>`:

- **`INE` (25% — Navegabilidade em 3 Camadas):** Avalia $\le 3$ tags `<nav>`, ausência de *Dead Ends*, profundidade $\le 3$ cliques (`Ctrl+K`) e cobertura dos 4 estados (`idle/empty`, `loading`, `success`, `error`).
- **`ICI` (20% — Coesão em Ilhas & Anti-Abas):** Avalia uso de `@container`, reuso de slots existentes (`<= 4` abas primárias, zero sub-abas aninhadas) e desacoplamento UI vs. I/O.
- **`IPC` (25% — Pureza de Código & Tokens `OKLCH`):** Penaliza hardcodes de URL/cor e acoplamento direto de banco/rede dentro de componentes visuais.
- **`IRM` (15% — Rigor de MVP):** Mede a razão de funções essenciais verificáveis vs. bloat desnecessário.
- **`ICTE` (15% — Tipografia Fluida & Anti-Squish):** Verifica `clamp()`, `65ch`, `tabular-nums`, `flex-shrink: 0; white-space: nowrap` e menus descompactados (`font-size >= 13px`, `gap >= 8px`).

$$\text{SGA} = 0.25 \cdot \text{INE} + 0.20 \cdot \text{ICI} + 0.25 \cdot \text{IPC} + 0.15 \cdot \text{IRM} + 0.15 \cdot \text{ICTE}$$

---

## 3. Protocolo de Inspeção Dinâmica com `agent-browser` (@eX) e `chrome-devtools-mcp` (Requer HITL)

```powershell
# 1. Auditoria determinística prévia de código e estrutura real (Sem HITL)
uv run python skills/auditoria-projetos-sistema/scripts/project_structure_and_code_auditor.py --target .
uv run python skills/auditoria-projetos-sistema/scripts/deterministic_scorer.py --scan .

# 2. Inspeção dinâmica Live DOM via agent-browser (Requer HITL quando abrir URL ativa)
agent-browser open $AppUrl
agent-browser wait 1500
agent-browser snapshot -i
agent-browser --color-scheme dark screenshot ./reports/dark_mode.png --full
agent-browser --color-scheme light screenshot ./reports/light_mode.png --full
agent-browser screenshot ./reports/audit_annotated.png --annotate
```

### Falhas Determinísticas Rastreadas no Snapshot `@eX`

- `[FAIL: VIOLACAO_60_30_10_OU_OKLCH]`: Ausência de tokens `oklch()`, uso de `#000000` puro ou poluição cromática fora da proporção `60-30-10`.
- `[FAIL: SOMBRA_LAVADA_OU_SEM_LUZ_ZENITAL]`: Sombra simples borrada de camada única sem Umbra + Penumbra (`spread` negativo) + `inset 0 1px 0 0`.
- `[FAIL: MENU_COMPACTADO_OU_PROLIFERACAO_ABAS]`: Botões de menu com `font-size < 13px`, `gap < 6px`, `min-block-size < 44px` (`< 48px` em `any-pointer: coarse`), ausência de `env(safe-area-inset-bottom)` na barra inferior mobile ou criação de sub-abas aninhadas.
- `[FAIL: ESPACAMENTO_ARBITRARIO_OU_RAIO_NAO_CONCENTRICO]`: Uso de pixels mágicos fora da escala `--space-*`, violação da Lei de Proximidade ($\text{padding interno} > \text{gap externo}$) ou `border-radius` interno igual ao externo sem descontar o `padding` ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$).
- `[FAIL: CARD_SEM_CONTAINER_OU_SUBGRID_QUEBRADO]`: Componente de card consultando `@media` em vez de `@container`, coluna de mídia vazia sem `:has(> img)`, ou `container-type: inline-size` aplicado no mesmo nó DOM que declara `subgrid`.
- `[FAIL: BORRAO_GPU_OU_TIPOGRAFIA_FRACA]`: Ausência de `antialiased` + `font-synthesis: none`, uso de `scale()` fracionário em texto, `clamp()` com $\max > 2.5\times \min$, `transition: ... allow-discrete` dentro do shorthand ou falta de `tabular-nums`.
- `[FAIL: DIVSOUP_OU_NO_INERTE]`: Tags `<div>` simulando botões sem ARIA ou controles placebo sem ação real (`X não ativa Y`).
