---
name: template-skill
description: >-
  Modelo padrao oficial para criacao de novas skills no Antigravity e no workspace Franklin Quebra-Galho, estruturado sob divulgacao progressiva, regras deterministicas, diretrizes de design tatil, modulos de paleta mineral, opcoes de preferencias e matriz de discrepancias.
license: MIT
metadata:
  version: "1.3.0"
  author: "Franklin-Main & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-14"
  tags:
    - "template"
    - "padrao-2026"
    - "design-tatil"
version: 1.3.0
updated_at: 2026-10-14
author: Franklin-Main & Melki
category: Engenharia e Governança de Skills
---

# Template de Skill (Padrao Franklin 2026)

Este documento define o modelo arquitetural canônico para a concepção, padronização e governança de novas habilidades no ecossistema Franklin Quebra-Galho e Google Antigravity. Toda skill criada deve seguir rigorosamente a estrutura de divulgação progressiva, asserções booleanas determinísticas (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) e alinhamento estrito com as preferências perenes de design tátil e ergonomia visual.

---

## 🎯 Quando Usar
- Ao criar uma nova habilidade ou refatorar um procedimento existente no catálogo.
- Quando o desenvolvedor ou o sistema solicitar: "crie uma nova skill", "padronize este fluxo como uma habilidade do Franklin", "evolua esta automação para o padrão 2026".
- Para garantir que qualquer nova ferramenta possua contratos de entrada, processamento defensivo, modelo de saída estruturado e matriz de discrepâncias.

---

## 🚫 Quando NAO Usar
- Para scripts rápidos de uso único descartáveis sem valor perene de reutilização.
- Para armazenar dados temporários de sessão ou notas atômicas soltas (utilize o cofre do Obsidian em `C:\Users\melki\dev\notes\` ou `.context/`).
- Para executar tarefas que violem as políticas de segurança defensiva ou operem comandos destrutivos sem Human-in-the-Loop.

---

## ⚙️ Pre-requisitos e Dependencias
- Ambiente Windows 11 com PowerShell 7 (`pwsh`).
- Dependências de runtime isoladas (`uv` para Python, módulos locais para Node.js).
- Acesso à hierarquia de governança do workspace (`.context/`, `workspace_index.json`, `C:\Users\melki\dev\notes\`).

---

## 🎨 Diretrizes Canônicas de Design e Preferências Melki (Padrão Franklin 2026)

Toda skill que envolva frontend, geração de interfaces, dashboards, relatórios visuais ou interação com o usuário deve incorporar obrigatoriamente os 4 módulos canônicos abaixo:

### Módulo 1: Minimalist Impact, Camadas Tonais 60-30-10 e Iluminação 135° (`DESIGN.md v4.5-soft`)
- **Pilha de Elevação Tonal (4+1 Camadas):** `60%` `surface-canvas` (`#F1F4F8` Light / `#12151B` Dark), `30%` camadas tonais (`surface-inset` `#E5E9F0` escavado para inputs e berço do ícone ativo na sidebar `#sidebar-active-tracker`, `surface-flat` `#E9EEF5`, `surface-raised` `.ui-card-soft` com iluminação direcional dupla a **135°** e `surface-contrast` `#1E293B` para inversão tonal Terrixa `.terrixa-notched`) e `10%` `--accent-point` único.
- **Autonomia de Superfícies & 4 Presets Soft UI:** *Nexus Slate Cerulean* (`#0284C7`), *Moss & Calm* (`#174930`), *Soft Sapphire* (`#1E6091`) e *Obsidian Dark* (`#38BDF8`), mantendo $L_{\text{card}} > L_{\text{canvas}}$ no dark mode.
- ❌ **Banimento Anti-Cobalto & Anti-Glassmorphism (`AUDIT-VIS-01`):** É categoricamente proibido o uso de azul cobalto elétrico (`#0044FF`, `#0057FF`, `#233DFF`, `#1D4ED8`), `backdrop-filter: blur()`, bordas neon ou bordas duras de `1px`.

### Módulo 2: Design Atômico (5 Camadas), Regra 1+2 e Composição Bento (`frontend-code-architect` v4.0)
- **Design Atômico & Modularidade:** Separar em Átomos, Moléculas, Organismos (`<SoftCard />`), Templates (Bento Grid 12 colunas) e Pages (`<= 300` linhas/arquivo).
- **Orçamento de Densidade (Regra 1+2) & Zero "Caixa dentro de Caixa":** No máximo **1 ação primária** em relevo e **2 secundárias** discretas visíveis por card (restante em menu `⋯`), com respiro amplo ($\ge 24\text{px}$).
- **Anti-Squish e Ergonomia TDAH:** Hierarquia escaneável em 3 segundos, busca rápida (`Ctrl+K`), `flex-shrink: 0; white-space: nowrap;` em botões/badges ($\ge 44\text{px}$) e toasts `role="status" aria-live="polite"` (zero `alert()` nativo).

### Módulo 3: Mapeamento de Opções e Preferências Pessoais do Desenvolvedor
- **Consulta Estruturada via `ask_question`:** Formulários de múltipla escolha apenas em bloqueios críticos/irreversíveis (máx. 1–2 perguntas).
- **Seletor de Presets Soft UI & Temas Minerais (`localStorage`):** *Nexus Slate Cerulean*, *Moss & Calm*, *Soft Sapphire*, *Obsidian Dark*, *Tactile Matte*, *Phantom Obsidian 4K*, *Quiet Luxury Titanium*, *Steadfast Stainless* e *Warm Editorial Paper*.
- **Ecossistema Open Source Autorizado (Copy-Paste):** Prioridade para componentes modulares desacoplados (**shadcn/ui**, **Radix UI**, **Tailwind CSS**, **Lucide Icons**).

### Módulo 4: Matriz de Detecção de Discrepâncias & Rubrica `frontend-testing-auditor` (`v2.5.0`)
- Checklist determinístico que avalia o produto da skill ($\text{Score} = 0.35\cdot\text{A11y} + 0.30\cdot\text{FSM} + 0.20\cdot\text{Tokens} + 0.15\cdot\text{Sec}$):
  * `[PASS / FAIL]` **`AUDIT-VIS-01` (Camadas Tonais 135° & Zero Blur/Cobalto):** Superfícies `.ui-card-soft` e `surface-inset` livres de `backdrop-filter: blur` e livres de azul cobalto (`#0044FF` / `#0057FF`)?
  * `[PASS / FAIL]` **`AUDIT-A11Y-01/02` (WCAG 2.1 AA & Foco sem Neon):** Zero violações no `jest-axe`, contraste $\ge 4.5:1$ e foco de teclado tracejado tátil?
  * `[PASS / FAIL]` **`AUDIT-STATE-01/02` (Máquina de Estados FSM):** Estados `Idle`, `Loading` (`aria-busy="true"`), `Error` (`role="alert"`) e `Pressed` (`surface-inset`) implementados?
  * `[PASS / FAIL]` **`AUDIT-SEC-01` (Sanitização XSS & Tipagem Estrita):** Bloqueio de injeção HTML/XSS e contratos tipados (`TypeScript strict` / `Pydantic`)?
  * `[PASS / FAIL]` **Orçamento 1+2, Anti-Squish (`>= 44px`) e Ergonomia TDAH (`Ctrl+K`)?**

---

## 📋 Passo a Passo de Execucao (Divulgacao Progressiva)

### 1. Coleta de Informacoes e Validacao Determinística
- Verifique os parâmetros de entrada e o ambiente de execução antes de iniciar.
- Valide conformidade com as regras em `rules/criterios_auditoria.md` emitindo marcadores booleanos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`).
- Exemplo de comando seguro em PowerShell:
  ```powershell
  Test-Path "caminho\alvo"
  ```

### 2. Simulacao (Dry-run / Preview) e Consulta de Preferências
- Sempre que houver mutações em lote, alterações visuais ou movimentação de arquivos, apresente um preview ao usuário.
- Se houver escolhas estéticas ou de arquitetura, acione `ask_question` oferecendo as opções alinhadas aos arquétipos do Melki.

### 3. Execucao Principal Defensiva
- Implemente os procedimentos de forma modular, com validação de bordas e tratamento de erros explícito (sem capturas silenciosas).
- Aplique as diretrizes dos 4 módulos de design sempre que o produto envolver interface, páginas ou relatórios.

### 4. Verificacao, Auditoria de Discrepâncias e Fechamento
- Execute a Matriz de Detecção de Discrepâncias do Módulo 4 e registre os status determinísticos.
- Reindexe o workspace se arquivos forem alterados (`python scripts/generate_workspace_index.py`).
- Finalize o turno com o bloco canônico de auto-reflexão operacional e destilação de memória.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)

A resposta final da skill deve conter:
1. **Entregável Principal Estruturado:** Código tipado, artefato Markdown/HTML ou arquivo gerado.
2. **Matriz de Discrepâncias com as Preferências:**
   - Tabela com os 8 itens avaliados (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) e medidas corretivas adotadas.
3. **Checklist Determinístico de Qualidade:**
   - Validações de pré-entrega conforme a Governança Unificada (código de saída do terminal comprovado).

---

## 📁 Estrutura Recomendada da Pasta da Skill
```text
.agents/skills/<nome-da-skill>/
├── SKILL.md            # Instrucoes nucleares com os 4 modulos (este arquivo)
├── references/         # Opcional: Manuais, paletas ou dados factuais imutaveis
├── rules/              # Criterios deterministicos de auditoria/rejeicao ([PASS]/[FAIL])
├── scripts/            # Opcional: Scripts auxiliares PowerShell / Python / Node
└── evals/              # Cenarios de teste empiricos (evals.json)
```
