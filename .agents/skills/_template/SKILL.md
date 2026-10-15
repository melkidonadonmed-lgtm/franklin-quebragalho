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

### Módulo 1: Física de Luz/Sombra e Superfícies Minerais (Flexíveis por Projeto)
- **Destaque por Luz, Sombra e Profundidade (NÃO por Cor Hiperdestacada):** Botões primários, abas ativas, badges e cartões destacam-se por **incidência de luz zenital** (`radial-gradient` / `linear-gradient` no topo + `inset 0 1px 0`), **cavidades esculpidas** (`sunken wells`) e **sombras multicamadas**, nunca por cores vibrantes/neon.
- **Autonomia de Superfícies Minerais:** Varie tons neutros conforme a identidade do projeto (ardósia, titânio, basalto, calcário, papel algodão, sálvia mineral) mantendo `L_card > L_canvas` no dark mode.
- ❌ **Banimento Anti-Cobalto:** É categoricamente proibido o uso de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores fluorescentes saturadas.

### Módulo 2: Minimalismo, Regra 1+2 e Composição Visual (Tactile Matte 4K)
- **Orçamento de Densidade (Regra 1+2):** No máximo **1 ação primária** (tecla iluminada em relevo) e **2 secundárias** discretas visíveis por card (restante em menu `⋯`).
- **Zero "Caixa dentro de Caixa":** Separe metadados com tipografia, espaço livre (*whitespace* $\ge 30\%$) e divisórias sutis de `1px`.
- **Anti-Squish e Ergonomia TDAH:** Hierarquia escaneável em 3 segundos, busca rápida (`Ctrl+K`), `flex-shrink: 0; white-space: nowrap;` em botões/badges e ausência de `alert()` nativo bloqueante.

### Módulo 3: Mapeamento de Opções e Preferências Pessoais do Desenvolvedor
- **Consulta Estruturada via `ask_question`:** Formulários de múltipla escolha apenas em bloqueios críticos/irreversíveis (máx. 1–2 perguntas).
- **Seletor dos 5 Temas em `localStorage` (Sob Demanda / Cockpits):** *Tactile Matte*, *Phantom Obsidian 4K*, *Quiet Luxury Titanium*, *Steadfast Stainless* e *Warm Editorial Paper* (dentro do catálogo de 22 temas `v2.6.0-2026`).
- **Ecossistema Open Source Autorizado (Copy-Paste):** Prioridade para componentes modulares desacoplados (**shadcn/ui**, **Radix UI**, **Tailwind CSS**, **Lucide Icons**).

### Módulo 4: Matriz de Detecção de Discrepâncias com as Preferências
- Checklist determinístico que avalia o produto da skill contra os padrões perenes:
  * `[PASS / FAIL]` **Destaque por Luz/Sombra (Zero Cor Hiperdestacada):** Botões e abas destacam-se por luz zenital e relevo em vez de cores berrantes?
  * `[PASS / FAIL]` **Orçamento 1+2 e Zero Caixa em Caixa:** Máximo de 1 ação primária + 2 secundárias por card e $\ge 30\%$ de whitespace?
  * `[PASS / FAIL]` **Ausência de Cobalto Neon:** A paleta está livre de azuis elétricos saturados (`#0044FF`)?
  * `[PASS / FAIL]` **Profundidade no Dark Mode:** Cartões são mais claros que o fundo (`L_card > L_canvas`)?
  * `[PASS / FAIL]` **Sombras Multicamadas e Rim Light:** Elementos elevados possuem oclusão + projeção + chanfro superior?
  * `[PASS / FAIL]` **Anti-Squish Ativo:** Botões e badges possuem `flex-shrink: 0; white-space: nowrap;`?
  * `[PASS / FAIL]` **Usabilidade e Ergonomia TDAH:** Escaneável em 3s, sem `alert()` nativo e com alvos >= 40x40px?
  * `[PASS / FAIL]` **Desacoplamento e Tipagem:** Camadas Domínio/I-O/UI separadas e contratos tipados (`pydantic`/`dataclass`)?

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
