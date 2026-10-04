# Universal App Template

> **Padrão Arquitetural**: React 18 + TypeScript + Vite + Tailwind CSS  
> **Design System**: *Luxury Obsidian & Mineral Slate* (Tactile Matte)  
> **Origem**: Arquitetura Universal de Projetos Melki 2026  

---

## 🚀 Como Iniciar

### 1. Instalar Dependências
```powershell
npm install
```

### 2. Rodar Servidor de Desenvolvimento Local
```powershell
npm run dev
```

### 3. Build de Produção e Verificação de Tipos
```powershell
npm run build
```

---

## 📂 Arquitetura de Diretórios

- `docs/frontend.design.md`: Especificação canônica do Design System Tátil com paletas, fórmulas de sombras e acessibilidade WCAG.
- `docs/CONTEXT.md`: Bússola cognitiva e guardrails inegociáveis.
- `docs/SPEC.md`: Escopo fechado do MVP e critérios determinísticos de aceite.
- `src/components/`: Componentes organizados segundo o Atomic Design (`atoms`, `molecules`, `organisms`, `templates`).
- `src/canvas/`: Motor de renderização multi-pass em Canvas 2D (`elevationRenderer.ts`).
- `src/styles/globals.css`: Variáveis CSS `:root`, relevos táteis e foco acessível.
