---
name: auditoria-projetos-sistema
description: "Audita código real (AST), estrutura física, diagnóstico de MVP, navegação em 3 camadas (X ativa Y / SGA), Regra 60-30-10 OKLCH e DOM via agent-browser @eX (0 a 100). Use para auditar projetos e MVP; não use para refatorar código."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "6.0.0"
  updated_at: "2026-11-13"
  author: "Melki & Franklin-Main"
  category: "Auditoria Unificada de Projetos, Código Real, MVP, Navegação em Ilhas (SGA) e Física Visual 60-30-10 OKLCH"
  tags: ["auditoria-projetos-sistema", "antigravity-project-auditor", "nav-x-func", "mvp", "ast-code-audit", "60-30-10-oklch", "3-layer-navigation", "agent-browser", "sga-score"]
---
# SKILL: `auditoria-projetos-sistema` (`v6.0.0`) — Código Real, MVP, `SGA` & OKLCH

> **Fusão Canônica 3-em-1 (`auditoria-projetos-sistema` + `antigravity-project-auditor` + `nav-x-func`):** Proibido opinar apenas lendo `.md` — execute primeiro os scanners em `scripts/` para validar código-fonte (AST) e disco. Critérios completos OKLCH e template de laudo constam em [`references/auditoria_report_e_eixos_oklch.md`](references/auditoria_report_e_eixos_oklch.md), [`references/matriz_5_pilares_e_hand_off_2026.md`](references/matriz_5_pilares_e_hand_off_2026.md), [`references/rubrica_auditoria_e_agent_browser.md`](references/rubrica_auditoria_e_agent_browser.md) e [`references/taxonomia_subagentes_ui_6_camadas.md`](references/taxonomia_subagentes_ui_6_camadas.md).

## 1. Gatilhos e 3 Modos Claros de Execução

- **Modo 1 (`mvp_and_plan`):** Diagnóstico de MVP e perguntas focadas (80/20 quando direcionado), usando `project_structure_and_code_auditor.py` para gerar tabela dos **5 Pilares** e **Plano em 3 Fases**.
- **Modo 2 (`deep_code_and_nav_audit` — padrão):** Saúde AST, arquivos órfãos, paridade Docs vs. Disco, Navegação 3 Camadas (`X ativa Y`), `OKLCH 60-30-10`, Sombras 3 Níveis, Nota `0–100`, `SGA` e `TIF`.
- **Modo 3 (`live_dom_inspection` — HITL):** Inspeção viva de `@eX`, menus (`>=13px`, `gap>=8px`), FSM (`idle|loading|success|error`) e Dark/Light via `agent-browser` (`open`, `snapshot -i`, `click`) ou `chrome-devtools-mcp`.

## 2. Entradas e Ferramentas Determinísticas (`scripts/`)

- **Entradas:** `project_root_path` (obrigatório), `execution_mode`, `user_focus_query`, `app_url` (Modo 3 sob HITL).
- **Scanners CLI:**
  ```powershell
  uv run python skills/auditoria-projetos-sistema/scripts/project_structure_and_code_auditor.py --target <caminho>
  uv run python skills/auditoria-projetos-sistema/scripts/frontiercode_maintainability_guardrail.py <arquivo.py>
  uv run python skills/auditoria-projetos-sistema/scripts/deterministic_scorer.py --scan <caminho>
  uv run python skills/auditoria-projetos-sistema/scripts/ai_ready_data_pipeline.py
  ```

## 3. Processamento Modular nos 5 Pilares (`0–100 pts`)

1. **Módulo 1 — Governança & Paridade Docs vs. Disco (`40 pts`):** Checar `README.md`, `AGENTS.md`, `SPEC.md`/`CONTEXT.md`, `CURRENT_STATE.md`, `DESIGN.md`, `rules/`, `.env.example`, `.gitignore`, Nível 1/2/3 e classificar itens em `[IMPLEMENTADO_FUNCIONAL | MOCK_SUPERFICIAL | INEXISTENTE_DOCUMENTADO | CÓDIGO_FANTASMA]`.
2. **Módulo 2 — AST, Órfãos & Segurança/MCP (`40 pts`):** Detectar exports órfãos, stubs vazios, funções `>60` linhas, `Pydantic v2 extra="forbid"` / `Zod .strict()` e higiene STDIO; quando usar Gemini/Live/Decisions/WS/JSON-RPC, valide via `google-developer-knowledge`/`gemini_get_doc` (evite `gemini_search_docs`, desabilitada) e aplique o protocolo da skill `agent-server-auditor`.
3. **Módulo 3 — `60-30-10 OKLCH`, Sombras 3 Níveis & Navegação `SGA` (`20 pts`):** Validar tokens OKLCH, Umbra + Penumbra + Catch-Light, `<=3 <nav>`, Ordem DOM = Visual, `@container` + `subgrid`, `clamp()`/`65ch`/`tabular-nums` ([`references/auditoria_report_e_eixos_oklch.md`](references/auditoria_report_e_eixos_oklch.md)).

## 4. Limites, Exceções e Guardrails

- **Proibido** diagnosticar sem rodar `project_structure_and_code_auditor.py`, alterar código durante auditoria inicial sem aprovação HITL ou aprovar placeholders (`onClick={() => {}}`, `pass`).
- **Fronteira Limpa:** Para estruturar repositórios do zero (`ideation_to_v1`) ou reescrever `README.md` (`project_organizer_sync`), use `organizador-projetos-ideias`. Em projetos Android, acople `android-agy-projects` (ou `re-a-ndroid` para APK).

## 5. Saídas e Entregáveis ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md))

Emita com `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`: (1) Score Geral `XX/100`, `SGA`, `TIF`, (2) Diagnóstico MVP & Paridade AST vs. Docs, (3) Matriz dos 5 Pilares e (4) Plano Executável em 3 Fases conforme [`references/auditoria_report_e_eixos_oklch.md`](references/auditoria_report_e_eixos_oklch.md).
