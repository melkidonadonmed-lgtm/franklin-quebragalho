---
name: auditoria-projetos-sistema
description: >-
  Audita a integridade estrutural, arquivos essenciais (AGENTS.md, README, CONTEXT, DESIGN, SPEC), higiene de repositório (.env, .gitignore, Git), orfandade de código, desacoplamento/tipagem/chunking, discrepâncias entre escopo documentado e executado, conformidade de UI/UX e esteira visual via agent-browser (snapshots @eX) com nota ponderada (0 a 100). Não use para refatorar código sem aprovação prévia.
license: MIT
metadata:
  version: "2.3.0"
  author: "Franklin-Main & Melki"
  category: "Auditoria Estrutural e Higiene de Repositório"
  updated_at: "2026-10-19"
  tags:
    - "auditoria"
    - "agent-browser"
    - "higiene-repo"
    - "qualidade"
version: 2.3.0
updated_at: 2026-10-19
author: Franklin-Main & Melki
category: Auditoria Estrutural e Higiene de Repositório
---

# Auditoria Estrutural de Projetos, Código e UI/UX (`auditoria-projetos-sistema` v2.3.0)

Esteira de inspeção técnica e visual para repositórios de software: audita governança física (`AGENTS.md`, `README.md`, `DESIGN.md`), identifica código órfão, confronta documentação vs. implementação real, avalia coesão de UI/UX (`DESIGN.md v4.5-soft`) e executa inspeção dinâmica do DOM via **`agent-browser`** (`@eX`), consolidando nota ponderada de `0 a 100`.

---

## 🎯 Gatilhos de Ativação (Quando Usar)
- Auditar um projeto/repositório por completo (estrutura de pastas, `.gitignore`, `.env.example`, lockfiles).
- Confrontar funcionalidades prometidas no `README.md`/`CONTEXT.md` contra o código real (`[IMPLEMENTADO_FUNCIONAL]`, `[MOCK_SUPERFICIAL]`, `[INEXISTENTE_DOCUMENTADO]`, `[CÓDIGO_FANTASMA]`).
- Auditar qualidade de código, orfandade, chunking estruturado e nós interativos via `agent-browser snapshot -i`.

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
1. Conferir artefatos vitais: `AGENTS.md`, `README.md`, `CONTEXT.md`, `DESIGN.md` (`v4.5-soft` quando houver UI), `SPEC.md`/`TODO.md`, `.env.example` e `.gitignore` (bloqueando `node_modules/`, `.env`, `.venv/`, `.next/`, `dist/`).
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

### Módulo 4: Auditoria de UI/UX, Temas e Nós Interativos (20 pts)
1. **Temas e Tokens (`DESIGN.md v4.5-soft`)**: Verificar contraste WCAG 2.1 AA ($\ge 4.5:1$), separação de luminância no Dark Mode ($L_{\text{card}} > L_{\text{canvas}}$), banimento de azul cobalto (`#0044FF`/`#1D4ED8`) e blindagem `anti-squish` (`flex-shrink: 0; white-space: nowrap`, alvos $\ge 44\text{px}$).
2. **Inspeção de Nós `@eX`**: Detectar botões sem `aria-label`, `divsoup` (`[FAIL: DIVSOUP_ACESSIBILIDADE]`) e botões inertes (`[FAIL: NO_INERTE_SEM_ACAO]`).

### Módulo 5: Esteira Visual Automatizada com `agent-browser` (Requer HITL)
- Exige confirmação explícita do usuário antes de abrir URLs ativas.
- Executa captura Dark/Light Mode, screenshot anotado (`--annotate`) e snapshots `@eX` por aba/menu conforme comandos detalhados em [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md).

### Módulo 6: Integrações MCP e Schemas (15 pts)
- Validar caminhos absolutos, proteção de variáveis de ambiente em `mcp_config.json` e schemas de entrada estritos (`extra="forbid"`).

### Módulo 7: Rubrica Ponderada (0 a 100 pts)
- Soma exata: **Governança (20)** + **Coerência Funcional (20)** + **Qualidade/Higiene (25)** + **UI/UX & Nós (20)** + **Segurança/Git/MCP (15)** = **100 pts** (`90–100`: Enterprise; `70–89`: Moderado; `50–69`: Instável; `< 50`: Reprovado).

---

## 📤 Saídas e Entregáveis
Emitir o **Relatório de Auditoria Técnica e Visual** seguindo o template completo de 8 seções em [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md) e validando cada regra de [`rules/criterios_auditoria.md`](rules/criterios_auditoria.md) com `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`.
