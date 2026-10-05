---
name: template-skill
description: >-
  Modelo padrao oficial para criacao de novas skills no Antigravity e no workspace Franklin Quebra-Galho, estruturado sob divulgacao progressiva, regras deterministicas, diretrizes de design tatil, modulos de paleta mineral, opcoes de preferencias e matriz de discrepancias.
license: MIT
metadata:
  version: "1.2.0"
  author: "Franklin-Main & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-04"
  tags:
    - "template"
    - "padrao-2026"
    - "design-tatil"
version: 1.2.0
updated_at: 2026-10-04
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
- Para armazenar dados temporários de sessão ou notas atômicas soltas (utilize o Obsidian Vault ou `.context/`).
- Para executar tarefas que violem as políticas de segurança defensiva ou operem comandos destrutivos sem Human-in-the-Loop.

---

## ⚙️ Pre-requisitos e Dependencias
- Ambiente Windows 11 com PowerShell 7 (`pwsh`).
- Dependências de runtime isoladas (`uv` para Python, módulos locais para Node.js).
- Acesso à hierarquia de governança do workspace (`.context/`, `workspace_index.json`).

---

## 🎨 Diretrizes Canônicas de Design e Preferências Melki (Padrão Franklin 2026)

Toda skill que envolva frontend, geração de interfaces, dashboards, relatórios visuais ou interação com o usuário deve incorporar obrigatoriamente os 4 módulos canônicos abaixo:

### Módulo 1: Paleta de Cores Canônica (Superfícies Ardósia/Creme & Acentos Minerais)
- **Tema Escuro (Dark Mode):** Canvas Ardósia Grafite (`#0B101B` / `#090B10`) com Cartões Elevados mais claros (`#162033` / `#141B2D`) e divisores translúcidos (`rgba(255, 255, 255, 0.08)`).
- **Tema Claro (Light Mode):** Canvas Creme Suave (`#FDFEE9`, `#F8F7F2`) ou Polar Sand (`#EEF2F6`) com Cartões em Branco Puro (`#FFFFFF`) ou Primer Cinzento (`#E6E7E2`).
- **Acentos Minerais Autorizados:** Petroleum Blue (`#2B4C7E`), Slate Navy (`#203657`, `#4A5B73`), Royal Navy (`#042698`), Ouro Champanhe (`#D4AF37`, `#C5A059`), Sage Clínico (`#2D6A4F`, `#10B981`) e Amber Matte (`#925C18`, `#F59E0B`).
- ❌ **Banimento Anti-Cobalto:** É categoricamente proibido o uso de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes ácidas com saturação descalibrada.

### Módulo 2: Diretrizes de Design Tátil e Composição Visual (Tactile Matte 4K)
- **Anti-Glassmorphism:** Proibido o uso de vidros translúcidos difusos (`backdrop-filter: blur`), gradientes reflexivos e contornos neon brilhantes.
- **Regra de Ouro da Profundidade:** No dark mode, os cartões devem ser estritamente mais claros que o canvas (`L_card > L_canvas`), garantindo relevo e projeção visível da sombra externa.
- **Sistema de Sombras Multicamadas:** Combinação obrigatória de sombra de contato curta (`0 2px 4px rgba(0, 0, 0, 0.4)`) com sombra de projeção difusa ampla (`0 10px 25px -4px rgba(0, 0, 0, 0.65)`).
- **Rim Light Zenital:** Micro-chanfro óptico superior mineral (`border-top: 1px solid rgba(255, 255, 255, 0.14)` ou `inset 0 1px 0 rgba(255, 255, 255, 0.12)`).
- **Anti-Squish em Botões e Tags:** Uso obrigatório de `flex-shrink: 0;` e `white-space: nowrap;` em botões de ação e badges.
- **Ergonomia e Suporte TDAH:** Atalho central de busca rápida (`Ctrl+K`), feedbacks cinestésicos físicos (`active:scale-95`), grids com largura de coluna >= 350px e ausência de `alert()` nativo bloqueante.

### Módulo 3: Mapeamento de Opções e Preferências Pessoais do Desenvolvedor
- **Consulta Estruturada via `ask_question`:** Formulários de múltipla escolha com opções pré-configuradas e recomendação explícita.
- **Arquétipos Visuais Pré-aprovados:** Suporte nativo aos arquétipos *Tactile Matte Minimalist* (padrão Melki), *Phantom Obsidian 4K*, *Luxury Deep Blue*, *Gilded Navy Heritage* e *Polar Sand Light*.
- **Ecossistema Open Source Autorizado (Copy-Paste):** Prioridade absoluta para componentes modulares desacoplados (padrão **shadcn/ui**, **Radix UI**, **Tailwind UI / Catalyst**, **Lucide Icons** e **Geist Design**).
- **Mockups de Referência:** Geração de artefatos executáveis em HTML para validação visual prévia.

### Módulo 4: Matriz de Detecção de Discrepâncias com as Preferências
- Checklist determinístico que avalia o produto da skill contra os padrões perenes:
  * `[PASS / FAIL]` **Ausência de Cobalto Neon:** A paleta está livre de azuis elétricos saturados?
  * `[PASS / FAIL]` **Profundidade no Dark Mode:** Cartões são visivelmente mais claros que o fundo?
  * `[PASS / FAIL]` **Sombras Multicamadas:** Elementos elevados possuem sombras físicas calibradas?
  * `[PASS / FAIL]` **Fio de Luz Superior:** Há presença de rim-light zenital nos cartões?
  * `[PASS / FAIL]` **Superfície Sólida Fosca:** Ausência de vidros borrados (glassmorphism) e neon?
  * `[PASS / FAIL]` **Anti-Squish Ativo:** Botões e badges impedem quebra vertical de texto?
  * `[PASS / FAIL]` **Usabilidade e Ergonomia:** Interface sem diálogos bloqueantes e com alvos >= 40x40px?
  * `[PASS / FAIL]` **Padrão Modular:** Utilização do modelo copy-paste (shadcn/ui) sem pacotes caixa-preta?

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
