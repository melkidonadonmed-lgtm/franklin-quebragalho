# Critérios Determinísticos de Auditoria — `design-md` (`v4.5.0`)

Critérios objetivos e falsificáveis (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) para auditar a geração e atualização do contrato arquitetural `DESIGN.md v4.5-soft` (Módulo **M3**).

---

## 1. Cabeçalho YAML e Economia Tonal 60-30-10 (`[AUDIT-DESIGN-01]`)
- **`[PASS]`**: O arquivo `DESIGN.md` na raiz do projeto contém frontmatter YAML com `version: "4.5-soft"`, especifica a economia tonal **60-30-10** e declara as 4+1 camadas (`--surface-canvas: #F1F4F8`, `--surface-inset: #E5E9F0`, `--surface-flat: #E9EEF5`, `--surface-raised: #F1F4F8` e `--surface-contrast: #1E293B`).
- **`[FAIL: CONTRATO_INCOMPLETO]`**: Ausência do frontmatter `version: "4.5-soft"` ou omissão das camadas tonais canônicas.
- **`[UNVERIFIED]`**: Caminho raiz do projeto inacessível no disco.

## 2. Iluminação Direcional a 135° e Banimento de Bordas Duras / Blur (`[AUDIT-DESIGN-02]`)
- **`[PASS]`**: Define sombras duplas a **135°** (`--shadow-raised-135` para `.ui-card-soft` e `--shadow-inset-135` para cavidades `surface-inset`), proibindo expressamente `backdrop-filter: blur()` e bordas duras de `1px` em cards Bento.
- **`[FAIL: VIOLACAO_FISICA_135]`**: Uso de glassmorphism (`backdrop-blur`), sombras genéricas sem par de luz/sombra a 135° ou delimitação por bordas `1px solid`.

## 3. Banimento Absoluto de Azul Cobalto e Neon (`[AUDIT-DESIGN-03]`)
- **`[PASS]`**: Paleta 100% livre de azul cobalto elétrico (`#0044FF`, `#0057FF`, `#1D4ED8`, `#233DFF`, `#2563EB`) e neons, adotando **Cerulean Sapphire** (`#0284C7`), **Ocean Sapphire** (`#1E6091`), **Forest Moss** (`#174930`) ou **Mineral Ice** (`#38BDF8` no dark mode).
- **`[FAIL: COBALTO_DETECTADO]`**: Presença de qualquer código hexadecimal ou token de azul cobalto/neon como cor de destaque.

## 4. Catálogo dos 8 Kits Soft Tactile UI e Integração de Esteira (`[AUDIT-DESIGN-04]`)
- **`[PASS]`**: Documenta os 8 Kits Soft Tactile UI (`<SoftCard />`, `.ui-btn-tactile`, `.badge-soft`, `.swatch-disc`, `.tactile-thumb`, `.tactile-range`, `.surface-inset-pill`, `.activity-row`), o `#sidebar-active-tracker` deslizante e a integração com `frontend-code-architect` (`v4.1.0`) e `frontend-testing-auditor` (`v2.6.0`).
- **`[FAIL: KITS_AUSENTES]`**: Omissão dos 8 Kits Soft UI ou ausência de mapeamento para a arquitetura de 5 camadas atômicas.
