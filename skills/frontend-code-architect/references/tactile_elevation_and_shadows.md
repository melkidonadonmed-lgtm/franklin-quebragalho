# Referência Técnica: Sombras em Camadas (`OKLCH`), `@container`, 4 Variantes de Cards e Blueprints dos 3 Níveis de Complexidade (`v7.0.0`)

> **Quando consultar esta referência (`franklin_skills_get(skill_name="frontend-code-architect", section="references")`):**
> Utilize este módulo ao implementar ou refatorar projetos nos **3 Níveis de Complexidade** (Eixo 9), superfícies (`.sculpted-card` / `<Card />`), navegação estrutural (`<Breadcrumbs />`) e temas reativos (`OKLCH` + `light-dark()` + anti-FOUC).

---

## 1. Modelo Simulado 1 (Baixa Complexidade): Landing Page & Hub Institucional ("Aura Studio")

- **Quando utilizar:** Sites institucionais, hotsites de produto, portfólios interativos ou documentações estáticas (1 a 2 devs).
- **Filosofia:** Zero-Runtime CSS, organização plana orientada a camadas (`@layer tokens, reset, layouts, components, utilities;`).

```text
aura-studio-landing/
├── index.html                   # Semântica HTML5 + <meta name="color-scheme" content="light dark">
├── precos.html
├── manifest.json
├── assets/
│   ├── css/
│   │   ├── main.css             # @layer tokens, reset, layouts, components, utilities;
│   │   ├── 01-tokens.css        # Primitivos, semânticos OKLCH, sombras e tipografia fluida
│   │   ├── 02-reset.css         # box-sizing: border-box, propriedades lógicas e display: flow-root
│   │   ├── 03-layouts.css       # Macrolayouts (Grid RAM, header, footer)
│   │   ├── 04-components.css    # Microlayouts (Cards com @container, botões, breadcrumbs)
│   │   └── 05-utilities.css     # Utilitários de espaçamento, isolation: isolate e blend-modes
│   ├── js/
│   │   ├── theme-switcher.js    # Alternância light/dark persistida no localStorage
│   │   └── main.js
│   └── media/
│       ├── icons/favicon.svg    # Favicon adaptável com @media (prefers-color-scheme: dark)
│       └── images/
└── README.md
```

---

## 2. Modelo Simulado 2 (Média Complexidade): SPA Modular Orientada a Domínio ("FinPulse Analytics")

- **Quando utilizar:** Painéis financeiros, CRMs, sistemas internos (React/Vue/Angular + TS) com múltiplos fluxos de estado (3 a 8 devs).
- **Filosofia:** *Feature-Driven Architecture*: componentes atômicos puros em `src/components/ui`, macrolayouts em `src/components/layout` e módulos de negócio isolados em `src/features/<dominio>/`.

```text
finpulse-spa/
├── index.html
├── package.json
├── tsconfig.json
└── src/
    ├── app/
    │   ├── App.tsx
    │   ├── providers/ThemeProvider.tsx
    │   └── router/AppRouter.tsx
    ├── styles/
    │   ├── tokens.css           # Tokens primitivos e semânticos OKLCH + Elevação
    │   └── globals.css          # Reset lógico, tipografia fluida e regras globais
    ├── components/
    │   ├── ui/
    │   │   ├── Button/
    │   │   ├── Card/            # Polimórfico (as='article'|'section'|'div', variant='elevated'|'outlined'|'subtle')
    │   │   └── Breadcrumbs/     # <nav aria-label="Caminho de navegação"><ol role="list">
    │   └── layout/
    │       ├── AppShell.tsx
    │       ├── SidebarGlobalNav.tsx
    │       └── Topbar.tsx
    ├── features/
    │   ├── portfolio-metrics/   # api/, components/, hooks/, types/, index.ts
    │   └── transactions/        # api/, components/, index.ts
    ├── hooks/
    ├── utils/
    └── main.tsx
```

---

## 3. Modelo Simulado 3 (Alta Complexidade): Plataforma SaaS Fullstack & PWA ("NexusCloud Enterprise")

- **Quando utilizar:** Plataformas SaaS multi-tenant, e-commerces e PWAs híbridos com SSR, RSC, SEO dinâmico e múltiplos layouts (8+ devs).
- **Filosofia:** App Router com **Grupos de Rotas `(marketing)` e `(workspace)`** para isolar Macrolayouts sem afetar a URL, e **Pastas Privadas `_components`** para colocação segura ao lado das rotas.

```text
nexuscloud-enterprise/
├── public/icons/                # Ícones PWA (192x192, 512x512, maskable)
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root Layout (Fontes variáveis, Viewport API e script anti-FOUC)
│   │   ├── manifest.ts          # Web App Manifest dinâmico (PWA)
│   │   ├── global-error.tsx
│   │   ├── not-found.tsx
│   │   ├── (marketing)/         # Grupo 1: Páginas Públicas (Navbar Transparente + Footer)
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── precos/page.tsx
│   │   │   └── _components/     # HeroGradientOklch.tsx, PricingComparisonGrid.tsx
│   │   ├── (workspace)/         # Grupo 2: App Logado & PWA (Sidebar Global + Breadcrumbs + Topbar)
│   │   │   ├── layout.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx
│   │   │   │   └── _components/ # RealtimeTelemetryCard.tsx, ServerLoadGrid.tsx
│   │   │   └── projetos/[projetoId]/
│   │   │       ├── page.tsx
│   │   │       └── opengraph-image.tsx
│   │   └── api/v1/telemetria/route.ts
│   ├── components/
│   │   ├── ui/                  # Button, Card, Dialog, Badge, Input
│   │   └── navigation/          # GlobalNav, LocalTableOfContents, StructuralBreadcrumbs
│   ├── lib/
│   ├── config/
│   └── styles/design-system.css
└── next.config.ts
```

### Root Layout com Prevenção de FOUC e `Viewport` API (`src/app/layout.tsx`)

```tsx
import type { Metadata, Viewport } from 'next';
import '@/styles/design-system.css';

export const viewport: Viewport = {
  colorScheme: 'light dark',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#f8fafc' },
    { media: '(prefers-color-scheme: dark)', color: '#0f172a' },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var saved = localStorage.getItem('nexus-theme');
                  if (saved === 'dark' || saved === 'light') {
                    document.documentElement.setAttribute('data-theme', saved);
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

---

## 4. Referência de Interatividade, Apontadores (`pointer: coarse`), Macro/Microlayout (`@container`) e Dashboard Analítico

Consulte os códigos completos em [`Guia de Arquitetura para Interfaces Frontend Complexas (Macro-Micro, OKLCH e Acessibilidade).md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Guia%20de%20Arquitetura%20para%20Interfaces%20Frontend%20Complexas%20(Macro-Micro,%20OKLCH%20e%20Acessibilidade).md):

```css
/* 1. Botão Base + Regra LVHA (:link -> :visited -> :hover -> :active) + Apontadores */
.btn-acao {
  padding: 0.5em 1em; border-radius: 6px;
  background-color: var(--brand-primary, oklch(0.62 0.21 259));
  color: #ffffff; font-weight: 600;
  user-select: none; touch-action: manipulation;
  transition: background-color 0.2s ease, transform 0.1s ease;
}
@media (any-pointer: coarse) {
  .btn-acao { padding: 0.85em 1.5em; min-height: 48px; min-width: 48px; }
}
.btn-acao:hover { background-color: oklch(from var(--brand-primary) calc(l - 0.08) c h); }
.btn-acao:focus { outline: none; }
.btn-acao:focus-visible { outline: 2px solid oklch(0.68 0.17 237); outline-offset: 2px; }

/* 2. Macrolayout 3 Colunas (Header + Sidebar + Canvas + Chat) e Microlayout @container */
.app-layout {
  display: grid; height: 100vh; width: 100vw;
  grid-template-rows: 60px 1fr;
  grid-template-columns: 240px 1fr 340px;
  grid-template-areas: "header header header" "sidebar canvas chat";
}
.floating-analytics-card {
  width: clamp(260px, 30vw, 440px); resize: horizontal; overflow: auto;
  container-type: inline-size; container-name: analyticsCard;
}
@container analyticsCard (min-width: 320px) {
  .card-metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); }
}
.chat-messages-scroll { overflow-y: auto; overscroll-behavior-y: contain; }
```

---

## 5. Grafo Interativo (`@xyflow/react` + `WebSocket` + `Chokidar`) e Roteamento Dinâmico Next.js 15+ App Router

Consulte a implementação completa (`server/watcher.ts`, `src/app/api/scan/route.ts`, `animated-node.css`, `CustomFileNode.tsx` e `FileMapInteractive.tsx`) em [`Padrão de Grafo Interativo e Ações em Tempo Real (Batch 150ms + Web Worker + LOD).md`](file:///C:/Users/melki/dev/notes/Mem%C3%B3ria/Padr%C3%A3o%20de%20Grafo%20Interativo%20e%20A%C3%A7%C3%B5es%20em%20Tempo%20Real%20(Batch%20150ms%20+%20Web%20Worker%20+%20LOD).md):

1. **Invariantes do Grafo Reativo (`@xyflow/react` + `ws` / SSE):**
   - **Normalização Multiplataforma no Watcher (`server/watcher.ts`):** `const relativePath = path.relative(targetDir, filePath).replace(/\\/g, '/');` com `chokidar.watch(targetDir, { ignored: /(^|[\/\\])\../, persistent: true, ignoreInitial: true })`.
   - **Prevenção de Re-renderização Infinita:** Declare `const nodeTypes = { customFile: CustomFileNode };` **fora** do escopo do componente React e ative `onlyRenderVisibleElements={true}` no `<ReactFlow />`.
   - **Pulso Visual em Edições (`change`) vs. Re-scan Estrutural (`add`/`unlink`):** Eventos `change` acionam `triggerNodeFlash(data.relativePath)` (`1500ms` com `.node-flashing`) e atualizam apenas o preview aberto; eventos estruturais (`add`, `unlink`, `addDir`, `unlinkDir`) acionam `reloadTree()` (`/api/scan`).
   - **Alternativa Enxuta Serverless (SSE):** Em vez de processo Node separado na porta `3001`, exponha `src/app/api/stream/route.ts` com `ReadableStream` e consuma no navegador via `new EventSource('/api/stream')`.

2. **Roteamento Dinâmico no Next.js 15+ App Router (`params` e `searchParams` Assíncronos):**
   - **Segmentos:** `[slug]` (`{ slug: 'a' }`), `[...slug]` Catch-all obrigatório (`{ slug: ['a', 'b'] }`), `[[...slug]]` Catch-all opcional incluindo raiz (`{ slug: undefined | ['a', 'b'] }`).
   - **Server Component (`page.tsx`):** `export default async function Page({ params }: { params: Promise<{ slug: string }> }) { const { slug } = await params; ... }` combinado com `export async function generateStaticParams()` e `notFound()`.
   - **Client Component (`'use client'`):** Desembrulhe a Promise com `import { use } from 'react'; const { slug } = use(params);`.
   - **Layouts (`layout.tsx`) vs. `searchParams`:** `layout.tsx` recebe `params: Promise<...>`, mas **nunca** `searchParams` (Layouts não re-renderizam na navegação entre subrotas; ler query strings no Layout causaria *stale state*). No cliente, envolva `useSearchParams()` em `<Suspense>`.
   - **Route Handlers (`route.ts`):** `export async function GET(_req: NextRequest, ctx: { params: Promise<{ id: string }> }) { const { id } = await ctx.params; ... }`.
