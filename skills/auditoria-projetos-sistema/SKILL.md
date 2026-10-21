---
name: auditoria-projetos-sistema
description: >-
  Audita integridade estrutural de repositórios (AGENTS.md, README, DESIGN, SPEC, Git/.env), código órfão, tipagem/chunking, alinhamento do tema visual ao propósito do projeto e esteira dinâmica via agent-browser (@eX) com nota de 0 a 100. Use para auditar projetos; não use para refatorar código sem aprovação.
license: MIT
metadata:
  version: "3.0.0"
  author: "Franklin-Main & Melki"
  category: "Auditoria Estrutural, Estilo por Propósito e Higiene de Repositório"
  updated_at: "2026-10-19"
  tags:
    - "auditoria"
    - "agent-browser"
    - "estilo-por-proposito"
    - "higiene-repo"
    - "qualidade"
version: 3.0.0
updated_at: 2026-10-19
author: Franklin-Main & Melki
category: Auditoria Estrutural, Estilo por Propósito e Higiene de Repositório
---

# Auditoria Estrutural de Projetos, Código e Arquitetura Visual por Propósito (`auditoria-projetos-sistema` v3.0.0)

Esteira de inspeção técnica e visual para repositórios de software: audita governança física (`AGENTS.md`, `README.md`, `DESIGN.md`), identifica código órfão, confronta documentação vs. implementação real, diagnostica se o **tema e estilo visual encaixam no propósito do projeto** (avaliando espaçamento, contraste, tipografia, estilo, camadas e hierarquia sem impor paletas fixas) e executa inspeção dinâmica do DOM via **`agent-browser`** (`@eX`), consolidando nota ponderada de `0 a 100`.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Auditar um projeto/repositório por completo (estrutura de pastas, `.gitignore`, `.env.example`, lockfiles).
- Confrontar funcionalidades prometidas no `README.md`/`CONTEXT.md` contra o código real (`[IMPLEMENTADO_FUNCIONAL]`, `[MOCK_SUPERFICIAL]`, `[INEXISTENTE_DOCUMENTADO]`, `[CÓDIGO_FANTASMA]`).
- Avaliar se a interface respeita o **propósito do projeto** (SaaS/Conversão, Editorial, FinTech, IA Nativa, MedTech, Terminal/DevTools), encaixando o melhor tema (*Ad Lucem*, *Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Preto Terminal IBM `Ex Umbris`*, *AETHER 2027*) e auditando espaçamento, contraste, tipografia, camadas e nós `@eX`.

### Quando NÃO Usar (Fronteira Estrita)
- Para refatorar código em massa antes da aprovação do relatório de auditoria.
- Para auditar exclusivamente um arquivo Python isolado via AST (use `code-acceptability-auditor`) ou apenas suítes de testes (use `test-quality-auditor`).

---

## 📥 Entradas Esperadas
- `project_root_path` (obrigatório): Caminho da raiz do projeto auditado.
- `audit_scope` (opcional): `completo` (padrão), `somente_arquitetura_git`, `somente_ui_ux` ou `somente_codigo`.
- `enable_visual_run` (opcional, booleano): Habilita navegação via `agent-browser` (padrão: `false`, exige aprovação prévia HITL).
- `app_url` (opcional): URL local/staging para inspeção dinâmica via `agent-browser`.

---

## 🔄 Processamento Interno (7 Módulos Desacoplados)

### Módulo 1: Governança de Pastas, Higiene de Repositório e Git (20 pts)
1. Conferir artefatos vitais: `AGENTS.md`, `README.md`, `CONTEXT.md`, `DESIGN.md` (quando houver UI), `SPEC.md`/`TODO.md`, `.env.example` e `.gitignore` (bloqueando `node_modules/`, `.env`, `.venv/`, `.next/`, `dist/`).
2. Verificar pastas `.agents/skills/` (ou `skills/`), `mcp_servers/`, `scripts/`, `tests/`, unicidade de lockfile e ausência absoluta de segredos comitados.

### Módulo 2: Confronto Documentação vs. Realidade (20 pts)
- Extrair premissas do `README.md`/`CONTEXT.md` e classificar cada item no código como:
  - `[IMPLEMENTADO_FUNCIONAL]`: Lógica completa e conectada.
  - `[MOCK_SUPERFICIAL]`: Componente visual estático sem conexão real.
  - `[INEXISTENTE_DOCUMENTADO]`: Prometido na documentação, ausente no código.
  - `[CÓDIGO_FANTASMA]`: Módulo implementado mas não documentado.

### Módulo 3: Qualidade de Código, Tipagem, Chunking e Orfandade (25 pts)
1. **Orfandade**: Rastrear arquivos e exports nunca consumidos a partir dos entrypoints (`main`, `app`, `index`).
2. **Desacoplamento, Tipagem e Guardrails AST**: Executar [`scripts/frontiercode_maintainability_guardrail.py`](scripts/frontiercode_maintainability_guardrail.py) para validar SRP, tipagem estrita (`pydantic`/`dataclasses`, zero `any`) e ausência de `except: pass`.
3. **Chunking Estruturado**: Executar [`scripts/ai_ready_data_pipeline.py`](scripts/ai_ready_data_pipeline.py) validando sanitização prévia, quebra em fronteiras sintáticas e metadados obrigatórios (`source_id`, `chunk_index`, `byte_range`).

### Módulo 4: Auditoria de Propósito, Estilo, Arquétipos, Nitidez, Contraste, Camadas e Nós (20 pts)
Consulte [`../_template/references/preferencias_estilo_e_temas.md`](../_template/references/preferencias_estilo_e_temas.md), [`../minimal-impact-ui/SKILL.md`](../minimal-impact-ui/SKILL.md) e o modelo [`../minimal-impact-ui/references/atlas_ex_umbris_winui.html`](../minimal-impact-ui/references/atlas_ex_umbris_winui.html):
1. **Enquadramento de Propósito, Tema & Arquétipo de Página (4 pts)**: Identificar o objetivo central do projeto (*Conversão/SaaS*, *Editorial/Leitura*, *FinTech/Confiança*, *IA Nativa/AETHER*, *MedTech Clínico* ou *DevTools/Terminal IBM*), verificar se a atmosfera adotada (*Cinza `#57545d` + Menus `#8e8999`*, *Claro Editorial `#F3F3F5` Ad Lucem*, *Preto Terminal IBM `#070709` Ex Umbris*) e o **Arquétipo Espacial** (*Split-Screen Workbench*, *Timeline*, *Kanban*, *Canvas de Nós*, *Wizard Foco Anti-TDAH*, *Catálogo WinUI Gallery*) servem ao propósito.
2. **Contraste, Proporção Cromática (98/2), Menus `#8e8999` & Botões (4 pts)**: Validar contraste WCAG 2.1 AA/AAA, tinta escura `#16151A` sobre menus `#8e8999` (proibido texto branco lavado), texto escuro (`#091318`/`#062016`) em botões preenchidos Azul (`#35acd8`) ou Verde (`#10B981`), e isolamento de acento (98/2).
3. **Nitidez Tipográfica Absoluta (Zero Letras Vermelhas Embaçadas) & `tabular-nums` (4 pts)**: Proibir letras vermelhas puras (`color: #e13535`) ou serifas finas embaçadas sobre fundos cinza (`#57545d`/`#49464f`) ou pretos (`#070709`); exigir `.highlight-surgical` (Semibold + sublinhado `2px`) em títulos e `.accent-text` (`#FFFFFF` + fundo `--punctual-soft` + `border-left: 2.5px`) em badges, além de `tabular-nums` e `IBM Plex Mono` no tema `dark`.
4. **Espaçamento, Camadas Esculpidas, Rim Light & Motion WinUI (4 pts)**: Auditar respiro ($\ge 25\%$), Bento Grid assimétrico (`col-span-2`), sombras esculpidas em 3 camadas + `1px` Rim Light (`--shadow-sculpted`), contraste alternado (`.surface-contrast` `#232127`/`#18181C`), curvas físicas `cubic-bezier(0.16, 1, 0.3, 1)` e alvos $\ge 44 \times 44\text{px}$.
5. **Inspeção de Nós Interativos `@eX` & FSM (4 pts)**: Detectar botões sem `aria-label`, `divsoup` (`[FAIL: DIVSOUP_ACESSIBILIDADE]`), estados FSM ausentes (`idle | loading | error | pressed`) e botões inertes (`[FAIL: NO_INERTE_SEM_ACAO]`).

### Módulo 5: Esteira Visual Automatizada com `agent-browser` (Requer HITL)
- Exige confirmação explícita do usuário antes de abrir URLs ativas.
- Executa captura de temas, screenshot anotado (`--annotate`) e snapshots `@eX` por aba/menu conforme [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md).

### Módulo 6: Integrações MCP e Schemas (15 pts)
- Validar caminhos absolutos, proteção de variáveis de ambiente em `mcp_config.json` e schemas de entrada estritos (`extra="forbid"`).

### Módulo 7: Rubrica Ponderada (0 a 100 pts)
- Soma exata: **Governança (20)** + **Coerência Funcional (20)** + **Qualidade/Higiene (25)** + **Propósito, Estilo, UI/UX & Nós (20)** + **Segurança/Git/MCP (15)** = **100 pts** (`90–100`: Enterprise; `70–89`: Moderado; `50–69`: Instável; `< 50`: Reprovado).

---

## 📤 Saídas e Entregáveis
Emitir o **Relatório de Auditoria Técnica e Visual** seguindo o template completo de 8 seções em [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md) e validando cada regra de [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) com `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`.
