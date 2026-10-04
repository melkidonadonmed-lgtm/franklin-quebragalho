# CONTEXTO OPERACIONAL E BÚSSOLA COGNITIVA

- **Projeto:** [NOME_DO_PROJETO]
- **Versão:** `1.0.0`
- **Data de Inicialização:** 2026-10-04
- **Arquitetura Base:** Universal Modular App (React + Vite + TypeScript + Tailwind CSS)

---

## 1. PROPÓSITO E ESCOPO DO SISTEMA

Este repositório foi inicializado a partir da **Arquitetura Universal de Projetos** do desenvolvedor Melki. Seu objetivo é fornecer uma solução com estabilidade de produção, zero dependências redundantes e experiência de usuário de nível executivo.

---

## 2. GUARDRAILS TÉCNICOS E REGRAS INEGOCIÁVEIS

1. **Local-First & Resiliência:** Todo processamento que puder ser feito localmente e no cliente deve ser priorizado.
2. **Separação Estrita de Responsabilidades:**
   - Componentes visuais (`src/components/`) são puramente de apresentação e nunca executam chamadas de rede diretamente.
   - Chamadas HTTP residem em `src/services/`.
   - Estado compartilhado e regras de consumo residem em `src/hooks/` e `src/context/`.
3. **Design System Tátil Obrigatório:**
   - Todo componente deve estar em total conformidade com as especificações contidas em `docs/frontend.design.md`.
   - Proibição de cores hardcoded (`#ffffff`, `bg-white`, `#000000`).
   - Uso de sombras multicamadas táteis para relevo tridimensional.
   - Proibição de azul cobalto saturado.
4. **Semântica de Interação e Acessibilidade:**
   - Botões devem ser `<button type="button">` com altura mínima de 44px e blindagem anti-squish (`shrink-0 whitespace-nowrap`).
   - Zero elementos não-semânticos clicáveis (`<div onClick>`).
   - Todos os controles devem ser operáveis via teclado com indicador `:focus-visible`.
5. **Tipagem Estrita:** TypeScript com `strict: true` em todo o código-fonte. Tipos `any` não fundamentados são terminantemente proibidos.

---

## 3. MAPA DE DIRETÓRIOS E CONTRATOS

```text
meu-projeto/
├── docs/                         # Bússola cognitiva e especificações canônicas
│   ├── CONTEXT.md                # Este documento de limites e guardrails
│   ├── SPEC.md                   # Escopo fechado do MVP atual e backlog
│   └── frontend.design.md        # Especificação técnica do Design System Tátil
├── src/                          # Código-fonte desacoplado da aplicação
│   ├── components/               # Atomic Design (atoms, molecules, organisms, templates)
│   ├── context/                  # Contextos globais (tema, sessão)
│   ├── hooks/                    # Hooks reutilizáveis
│   ├── services/                 # Adaptadores de rede e clientes de API
│   ├── styles/                   # Tokens globais CSS e reset tátil
│   ├── types/                    # Interfaces e contratos TypeScript
│   └── canvas/                   # Motor de renderização em multi-pass Canvas 2D
└── tests/                        # Testes automatizados (unitários e e2e)
```
