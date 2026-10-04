# ESPECIFICAÇÃO DE ESCOPO E ROADMAP (SPEC.md)

- **Projeto:** [NOME_DO_PROJETO]
- **Status:** MVP em Desenvolvimento
- **Última Atualização:** 2026-10-04

---

## 1. ESCOPO DO MVP (FASE ATUAL)

### 1.1 Entregáveis Centrais
- [ ] Implementação da casca de interface em `src/App.tsx` com navegação por abas (`TabsNav`).
- [ ] Configuração do tema mineral escuro (*Tactile Matte / Luxury Obsidian*) em `src/styles/globals.css`.
- [ ] Barra lateral de navegação com espaçamento nobre e ergonomia de toque (`AppSidebar`).
- [ ] Integração do motor multi-sombra em Canvas 2D (`src/canvas/elevationRenderer.ts`) para renderização gráfica de alta definição.
- [ ] Cobertura de acessibilidade visual com conformidade WCAG 2.1 nível AA/AAA.

---

## 2. CRITÉRIOS DETERMINÍSTICOS DE ACEITE

- `[PASS / FAIL]` **Zero Cores Hardcoded:** Nenhum elemento utiliza `#ffffff` ou `bg-white` estático.
- `[PASS / FAIL]` **Semântica Interativa:** Todos os elementos de ação utilizam botões semânticos nativos.
- `[PASS / FAIL]` **Anti-Squish em Botões:** Todos os botões possuem `shrink-0 whitespace-nowrap`.
- `[PASS / FAIL]` **Navegação por Teclado:** Abas e modais respondem corretamente às teclas de seta, Escape e Tab.
- `[PASS / FAIL]` **Tipagem Estrita:** Compilação do TypeScript sem erros com `strict: true`.

---

## 3. BACKLOG ISOLADO (FUTURAS FASES)

- [ ] Suporte a internacionalização (i18n).
- [ ] Cache e persistência local via IndexedDB / LocalStorage com criptografia leve.
- [ ] Suíte completa de testes de ponta a ponta com Playwright.
