# ESPECIFICAÇÃO TÉCNICA DE UI/UX: DESIGN SYSTEM PREMIUM & TÁTIL

- **Arquivo:** `frontend.design.md`
- **Versão:** `2.0.0`
- **Padrão Estético:** *Luxury Obsidian & Mineral Slate* (Inspiração Apple Human Interface / Linear Dark Tactile)
- **Princípio Central:** Preferir sensação física de vida, relevo tridimensional tátil e profundidade (sombras multicamadas e rim-light superior) em vez de saturação cromática agressiva ou contraste chapado.

---

## 1. ESTILO ATUAL & PALETA DETECTADA

### 1.1 Mapeamento Cromático Ativo (Mineral Obsidian)

A arquitetura visual rejeita fundos pretos absolutos (`#000000`) e azuis saturados artificiais (cobalto/elétrico). Cada camada tem elevação com luminosidade progressiva:

- **Fundo Primário do Canvas (`--canvas-bg`):** `#090B0E` (Ardósia Abissal profunda e antirreflexo).
- **Superfície Nível 1 / Cartões (`--surface-card`):** `#11141A` (Painel com relevo óptico sutil, rigorosamente mais claro que o fundo).
- **Superfície Nível 2 / Modais e Popovers (`--surface-panel`):** `#181D26` (Painéis flutuantes com sombras amplas).
- **Superfície Nível 3 / Elementos Sunken / Inputs (`--surface-sunken`):** `#0B0E13` (Relevo negativo com sombra interna).
- **Borda de Contorno Zenital / Rim-Light (`--border-rim`):** `rgba(255, 255, 255, 0.08)` (Chanfro de 1px simulando reflexo de luz superior).
- **Borda de Destaque Interativo (`--border-rim-highlight`):** `rgba(255, 255, 255, 0.16)`.
- **Borda de Separação Sutil (`--border-subtle`):** `rgba(255, 255, 255, 0.05)`.
- **Texto Principal (`--text-primary`):** `#F3F4F6` (Cinza mineral claro 95% de luminosidade).
- **Texto Secundário (`--text-secondary`):** `#9CA3AF` (Leitura auxiliar e metadados).
- **Texto Desabilitado / Placeholder (`--text-muted`):** `#6B7280`.
- **Acento Primário de Ação (`--accent-action`):** `#38BDF8` (Sky Blue Mineral sóbrio) ou `#3B82F6` (Petroleum Blue calibrado).
- **Acento de Foco (`--accent-focus`):** `rgba(56, 189, 248, 0.45)`.
- **Status de Sucesso (`--status-success`):** `#10B981` (Esmeralda suave).
- **Status de Alerta (`--status-warning`):** `#F59E0B` (Âmbar mineral).
- **Status de Erro (`--status-danger`):** `#EF4444` (Rubi controlado, sem vermelho estourado).

---

## 2. PROPOSTAS DE PALETAS ALTERNATIVAS

### 2.1 Proposta de Paleta 1 (Design Moderno & Alto Contraste - WCAG 2.1 AAA)

Ideal para painéis com leitura contínua de relatórios técnicos e dados críticos:

| Token Semântico | Valor Hexadecimal / RGBA | Finalidade | Taxa de Contraste (WCAG) |
| :--- | :--- | :--- | :--- |
| `surface-contrast-bg` | `#080A0D` | Canvas de alto contraste | N/A |
| `surface-contrast-card` | `#12161F` | Cartão com borda refinada | 14.8:1 contra texto |
| `text-contrast-title` | `#FFFFFF` | Cabeçalhos e números-chave | 19.5:1 (AAA) |
| `text-contrast-body` | `#E2E8F0` | Texto corrido | 13.2:1 (AAA) |
| `accent-contrast` | `#38BDF8` | Links, botões de ação e abas ativas | 7.4:1 (AAA) |

### 2.2 Proposta de Paleta 2 (Tema Semântico / Dark Mode Adaptativo)

Tokens dinâmicos que alternam entre o Dark Mineral e o Light Alabaster através de atributos `data-theme`:

| Token Semântico | Dark Mineral (`data-theme="dark"`) | Light Alabaster (`data-theme="light"`) |
| :--- | :--- | :--- |
| `--canvas-bg` | `#090B0E` | `#F8FAFC` |
| `--surface-card` | `#11141A` | `#FFFFFF` |
| `--surface-panel` | `#181D26` | `#F1F5F9` |
| `--border-rim` | `rgba(255, 255, 255, 0.08)` | `rgba(0, 0, 0, 0.08)` |
| `--text-primary` | `#F3F4F6` | `#0F172A` |
| `--text-secondary` | `#9CA3AF` | `#475569` |
| `--shadow-raised` | `0 4px 14px -2px rgba(0,0,0,0.5)` | `0 4px 14px -2px rgba(15,23,42,0.08)` |

---

## 3. SISTEMA DE ELEVAÇÃO E MULTI-SOMBRA

O segredo do acabamento premium está na **física da luz zenital**: um cartão nunca possui apenas uma sombra genérica e borrada. Ele é composto por 3 camadas sobrepostas:
1. **Sombra de Contato (Oclusão de Ambiente):** curta, nítida e opaca, fixando o elemento na superfície.
2. **Sombra Difusa (Penumbra):** ampla, suave e translúcida, transmitindo a distância da superfície.
3. **Rim Light (Chanfro Zenital):** linha de 1px no topo interior do cartão, simulando a reflexão de luz que atinge a borda superior biselada.

### 3.1 Fórmulas CSS Multicamadas

```css
/* Elevação Nível 0: Elemento Sunken (Relevo Negativo para Inputs e Wells) */
--shadow-tactile-inset: 
  inset 0 2px 4px 0 rgba(0, 0, 0, 0.45),
  inset 0 0 0 1px rgba(0, 0, 0, 0.3),
  0 1px 0 0 var(--border-rim);

/* Elevação Nível 1: Superfície Padrão / Cartões */
--shadow-tactile-card: 
  0 1px 2px 0 rgba(0, 0, 0, 0.35),
  0 4px 12px -2px rgba(0, 0, 0, 0.4),
  inset 0 1px 0 0 var(--border-rim);

/* Elevação Nível 2: Elemento Flutuante / Modais / Toasts / Dropdowns */
--shadow-tactile-raised: 
  0 2px 4px 0 rgba(0, 0, 0, 0.3),
  0 12px 28px -4px rgba(0, 0, 0, 0.6),
  0 20px 48px -8px rgba(0, 0, 0, 0.5),
  inset 0 1px 0 0 var(--border-rim-highlight);

/* Elevação Nível 3: Botão Interativo Pressionável */
--shadow-tactile-button: 
  0 1px 2px 0 rgba(0, 0, 0, 0.3),
  0 2px 6px -1px rgba(0, 0, 0, 0.4),
  inset 0 1px 0 0 rgba(255, 255, 255, 0.15);

--shadow-tactile-button-active: 
  inset 0 2px 4px 0 rgba(0, 0, 0, 0.4),
  0 0 0 1px rgba(0, 0, 0, 0.2);
```

### 3.2 Motor de Multi-Sombra em Canvas 2D (Dupla Passagem)

Quando gráficos, diagramas de nós ou painéis forem renderizados em elementos HTML5 `<canvas>`, a API nativa do Canvas 2D não suporta múltiplas sombras em uma única chamada de desenho (`ctx.shadowBlur`). Portanto, é obrigatório executar o pipeline de **dupla passagem com chanfro**:

```typescript
export interface ElevationCanvasOptions {
  x: number;
  y: number;
  width: number;
  height: number;
  radius: number;
  fillColor: string;
  rimColor?: string;
}

export function drawElevatedCard(
  ctx: CanvasRenderingContext2D,
  options: ElevationCanvasOptions
): void {
  const { x, y, width, height, radius, fillColor, rimColor = 'rgba(255, 255, 255, 0.1)' } = options;

  ctx.save();

  // Passagem 1: Sombra Difusa Ampla
  ctx.shadowColor = 'rgba(0, 0, 0, 0.45)';
  ctx.shadowBlur = 18;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = 8;
  drawRoundedRect(ctx, x, y, width, height, radius);
  ctx.fillStyle = fillColor;
  ctx.fill();

  // Passagem 2: Sombra de Contato Nítida
  ctx.shadowColor = 'rgba(0, 0, 0, 0.35)';
  ctx.shadowBlur = 4;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = 2;
  drawRoundedRect(ctx, x, y, width, height, radius);
  ctx.fillStyle = fillColor;
  ctx.fill();

  ctx.restore();

  // Passagem 3: Micro-borda e Rim Light Zenital (1px)
  ctx.save();
  drawRoundedRect(ctx, x + 0.5, y + 0.5, width - 1, height - 1, radius);
  ctx.lineWidth = 1;
  ctx.strokeStyle = rimColor;
  ctx.stroke();

  // Destaque zenital superior
  ctx.beginPath();
  ctx.moveTo(x + radius, y + 0.5);
  ctx.lineTo(x + width - radius, y + 0.5);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.18)';
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.restore();
}

function drawRoundedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number
): void {
  ctx.beginPath();
  ctx.roundRect ? ctx.roundRect(x, y, w, h, r) : ctx.rect(x, y, w, h);
  ctx.closePath();
}
```

---

## 4. DECOMPOSIÇÃO MODULAR & ARQUITETURA DE COMPONENTES (ATOMIC DESIGN)

A arquitetura de interface segue rigorosamente o modelo atômico com separação limpa de estado e apresentação:

```text
src/components/
├── atoms/                # Átomos: Indivisíveis, puros, orientados a tokens
│   ├── TactileButton.tsx # Botões com feedback cinestésico e blindagem anti-squish
│   ├── SunkenInput.tsx   # Inputs com relevo negativo e rótulos semânticos
│   └── Badge.tsx         # Pílulas de status mineral
├── molecules/            # Moléculas: Combinação funcional de átomos
│   ├── NotificationToast.tsx # Alertas com ARIA role="alert" e dismiss por ESC
│   └── SearchBar.tsx     # Barra de pesquisa com atalho de teclado visual (Kbd)
├── organisms/            # Organismos: Estruturas complexas de domínio
│   ├── TabsNav.tsx       # Abas com navegação por teclado (Arrow/Home/End)
│   ├── AppSidebar.tsx    # Navegação lateral descompactada com espaçamento nobre
│   └── TopHeader.tsx     # Barra superior com ações de perfil e alternador de tema
└── templates/            # Templates: Grid e casca estrutural
    └── DashboardLayout.tsx # Layout responsivo com AppShell e área de conteúdo
```

### 4.1 Diretrizes de Navegação e Menus Nobres (Anti-Compactação)

- **Espaçamento Nobre na Sidebar:** A barra de navegação lateral deve respirar. A largura mínima é de `256px` (`w-64`). Itens de menu devem possuir altura mínima de `40px` com `py-2.5 px-3` e `gap-3`.
- **Proibição de Densidade Sufocante:** É terminantemente proibido empilhar itens de menu colados sem espaço para respiro visual (`my-1` ou `gap-1.5` mínimo entre links).
- **Abas (`TabsNav`):** As abas devem comportar-se como teclas mecânicas reais. A aba selecionada possui relevo sutil, chanfro zenital e texto em alto contraste, enquanto as abas inativas possuem fundo transparente e reagem suavemente ao hover (`transition-colors duration-150`).

### 4.2 Botões Ergonômicos e Blindagem Anti-Squish

- **Altura Mínima de Toque:** Todo botão interativo deve ter altura mínima de `40px` (preferencialmente `44px` para conformidade WCAG AAA / Mobile Touch).
- **Blindagem Anti-Squish:** Sempre aplicar as classes `shrink-0 whitespace-nowrap` em botões, tags e ícones para impedir que compressões no flexbox quebrem rótulos ou achatem botões.
- **Feedback Tátil Cinestésico:** Ao pressionar o botão, ele deve afundar sutilmente (`active:scale-[0.98]` ou `active:translate-y-[1px]`), com transição ultrarrápida (`duration-100 ease-out`).

---

## 5. ELEMENTOS RECOMENDADOS PARA REMOÇÃO & PODA DO DOM

A otimização de renderização exige manter o DOM limpo e enxuto:

1. **Anti-Divsoup:** Eliminar contêineres intermediários (`<div><div><p>...</p></div></div>`) que apenas encapsulam regras de layout facilmente combináveis no elemento pai (`flex flex-col gap-4`).
2. **Banimento de `backdrop-filter: blur` em Massa:** O uso desenfreado de `backdrop-blur` em tabelas longas ou itens de lista com scroll provoca *repaints* massivos na GPU e queda brusca de taxa de quadros (FPS). Limitar o blur exclusivamente à casca estática do Header e Modais.
3. **Erradicação de CSS Inline:** Estilos inline (`style="background: #111;"`) são anti-padrões de manutenibilidade e impedem a reatividade de temas. Todo estilo deve vir dos tokens do Tailwind ou classes de `globals.css`.
4. **Remoção de Elementos Fantasma de Layout:** Proibir o uso de `<div style="height: 20px" />` como espaçador. O espaçamento deve ser governado por propriedades nativas do CSS (`gap`, `margin`, `padding`).

---

## 6. RESTRIÇÕES DIRETIVAS INEGOCIÁVEIS

1. **Proibição de Cores Fixas (Hardcoded):** NUNCA declare `#ffffff`, `#000000`, `bg-white` ou `text-black` diretamente em nós JSX/HTML. Sempre utilize os tokens semânticos (`bg-[var(--surface-card)]`, `text-[var(--text-primary)]`).
2. **Semântica de Interação Rígida:** NUNCA utilize elementos não semânticos para capturar cliques (ex.: `<div onClick={...}>` ou `<span onClick={...}>`). Todo elemento interativo deve ser um `<button type="button">` ou `<a>`, equipado com tratamento de teclado (Enter e Espaço nativos do botão) e atributos ARIA adequados.
3. **Indicadores Visuais de Foco Invioláveis:** NUNCA use `outline-none` de forma isolada. É obrigatório fornecer o anel de foco acessível via `:focus-visible` com contraste de pelo menos `3:1` contra a superfície:
   ```css
   focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent-action)] focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--canvas-bg)]
   ```
4. **Proibição de Azul Cobalto Saturado:** As interfaces do desenvolvedor banem cores neon e azuis agressivos (ex.: `#0044FF`, `#1D4ED8`, `bg-blue-600` padrão saturado). Preferir Ardósia, Minerais Foscos e o Acento Petróleo/Sky Blue calibrado.
5. **Separação de Rede e Componente:** NENHUM componente de apresentação do Design System pode instanciar chamadas de rede diretas (`fetch`, `axios`). As chamadas de API devem residir em `src/services/` e ser consumidas através de Custom Hooks em `src/hooks/`.

---

## 7. EXEMPLOS INTEGRADOS DE AUDITORIA & REFATORAÇÃO (FEW-SHOT PROMPTS)

### Exemplo 1: Detecção e Refatoração de Botão Não-Semântico

**Input Analisado:**
```tsx
<div 
  onClick={() => submitData()} 
  style={{ background: '#0044ff', color: '#fff', padding: '5px', borderRadius: '4px' }}
>
  Salvar
</div>
```

**Diagnóstico Determinístico:**
- `[FAIL]` **Semântica:** Div interativa sem `role="button"`, sem `tabindex="0"` e inacessível por teclado (violação WCAG 2.1 Critério 2.1.1).
- `[FAIL]` **Cromia:** Uso de azul cobalto agressivo `#0044ff` banido pelas diretrizes do desenvolvedor.
- `[FAIL]` **Ergonomia:** Alvo de clique com padding reduzido (`5px`), inferior à altura mínima recomendada de 44px.
- `[FAIL]` **Estilização:** CSS inline com valores hardcoded não adaptativos.

**Refatoração Canônica Aplicada:**
```tsx
import React from 'react';

interface SaveButtonProps {
  onClick: () => void;
  isLoading?: boolean;
}

export const SaveButton: React.FC<SaveButtonProps> = ({ onClick, isLoading }) => {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={isLoading}
      className="
        inline-flex items-center justify-center
        h-11 px-5 gap-2
        shrink-0 whitespace-nowrap
        text-sm font-medium tracking-wide
        text-white
        bg-[var(--accent-action)]
        hover:brightness-110
        active:scale-[0.98]
        rounded-lg
        shadow-[var(--shadow-tactile-button)]
        focus-visible:outline-none
        focus-visible:ring-2
        focus-visible:ring-[var(--accent-action)]
        focus-visible:ring-offset-2
        focus-visible:ring-offset-[var(--canvas-bg)]
        transition-all duration-150 ease-out
        disabled:opacity-50 disabled:cursor-not-allowed
      "
    >
      <span>Salvar Alterações</span>
    </button>
  );
};
```

### Exemplo 2: Abas com Acessibilidade por Teclado e Relevo Mecânico

**Refatoração Canônica Aplicada (`TabsNav.tsx`):**
```tsx
import React, { useRef } from 'react';

export interface TabItem {
  id: string;
  label: string;
  count?: number;
}

interface TabsNavProps {
  tabs: TabItem[];
  activeTab: string;
  onTabChange: (id: string) => void;
}

export const TabsNav: React.FC<TabsNavProps> = ({ tabs, activeTab, onTabChange }) => {
  const tabsRef = useRef<(HTMLButtonElement | null)[]>([]);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let nextIndex: number | null = null;
    if (e.key === 'ArrowRight') {
      nextIndex = (index + 1) % tabs.length;
    } else if (e.key === 'ArrowLeft') {
      nextIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (e.key === 'Home') {
      nextIndex = 0;
    } else if (e.key === 'End') {
      nextIndex = tabs.length - 1;
    }

    if (nextIndex !== null) {
      e.preventDefault();
      tabsRef.current[nextIndex]?.focus();
      onTabChange(tabs[nextIndex].id);
    }
  };

  return (
    <nav
      role="tablist"
      aria-label="Abas de Navegação Principal"
      className="
        inline-flex items-center p-1.5 gap-1.5
        bg-[var(--surface-sunken)]
        rounded-xl
        border border-[var(--border-subtle)]
        shadow-[var(--shadow-tactile-inset)]
      "
    >
      {tabs.map((tab, idx) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            ref={(el) => (tabsRef.current[idx] = el)}
            role="tab"
            type="button"
            id={`tab-${tab.id}`}
            aria-selected={isActive}
            aria-controls={`panel-${tab.id}`}
            tabIndex={isActive ? 0 : -1}
            onClick={() => onTabChange(tab.id)}
            onKeyDown={(e) => handleKeyDown(e, idx)}
            className={`
              relative inline-flex items-center justify-center
              h-9 px-4 gap-2
              shrink-0 whitespace-nowrap
              text-xs font-semibold tracking-wider uppercase
              rounded-lg
              transition-all duration-150 ease-out
              focus-visible:outline-none
              focus-visible:ring-2
              focus-visible:ring-[var(--accent-action)]
              focus-visible:ring-offset-2
              focus-visible:ring-offset-[var(--surface-sunken)]
              ${
                isActive
                  ? 'bg-[var(--surface-card)] text-[var(--text-primary)] shadow-[var(--shadow-tactile-card)] border-t border-[var(--border-rim-highlight)]'
                  : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.03)]'
              }
            `}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span
                className={`
                  px-1.5 py-0.5 text-[10px] rounded-full font-mono
                  ${
                    isActive
                      ? 'bg-[var(--accent-action)] text-slate-950 font-bold'
                      : 'bg-[rgba(255,255,255,0.08)] text-[var(--text-secondary)]'
                  }
                `}
              >
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </nav>
  );
};
```
