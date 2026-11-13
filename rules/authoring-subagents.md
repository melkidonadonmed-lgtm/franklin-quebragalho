---
trigger: model_decision
description: "Diretrizes oficiais do Google Antigravity para definir subagentes declarativos (agents/*.md, Menor Privilégio, tools explícitos, guardrails max_steps/HITL, Context Fork e Swarm)."
---

# Regras Oficiais para Subagentes Declarativos (`agents/*.md`) e Orquestração

1. **Locais de Descoberta & Nomes Seguros:**
   - Workspace: `.agents/agents/<name>.md`; Global: `~/.gemini/config/agents/<name>.md`; Plugin: `plugins/<plugin>/agents/<name>.md`.
   - Evite colisão de `name` com agentes integrados (`self`, `research`, `browser`, `deepagent`, `review-agent`) ou subagentes já registrados no manifesto do plugin.

2. **Frontmatter & Menor Privilégio (`Least Privilege`):**
   - Campos canônicos: `name`, `description` (obrigatório — guia quando o coordenador delega), `subagent: true`, `mainAgent: false`.
   - **Declaração Explícita de Ferramentas (`tools`):** Especifique sempre `tools: [...]` (omissão cai em conjunto mínimo somente-leitura) com nomes nativos (`read_file`, `edit_file`, `write_file`, `run_command`, `manage_task`, `search_web`, `invoke_subagent`); ferramentas MCP devem ser vinculadas via `mcpServers`/`inheritMcp` (não liste `call_mcp_tool` em `tools:`). **É proibido usar `tools: ["*"]` ou `call_mcp_tool` em `tools:`** (`validate_skills.py` / `sync_gemini_ecosystem.py`).
   - **Auditores / Observadores / Gatekeepers:** Exija explicitamente perfil somente-leitura (`enable_write_tools: false` ou ausência de `write_file`/`edit_file`/`run_command` mutável) e `enable_subagent_tools: false` salvo quando o papel for coordenador.
   - **Modelo & Política:** Use `model: inherit` (nunca fixe modelos depreciados como `gemini-2.5-flash`/`2.5-pro`, `antigravity-preview-05-2026` ou `3.1-flash-live-preview`; o host/Orchestrator roteia entre `Gemini 4 Carbon`/`Argon` para plano e `Gemini 4 Hydrogen` para execução) e defina `commandExecutionPolicy: sandbox | auto | off`, `inheritMcp` e `inheritCustomizations` conforme necessidade real.

3. **Contenção, Loops & Portões HITL:**
   - Todo subagente com loop ou ferramentas deve declarar limites determinísticos (`max_steps`, `max_turns` ou `recursion_limit`), `stop_condition` verificável e parada HITL antes de mutações destrutivas, alteração de `.env`/segredos ou efeitos externos.

4. **Isolamento de Contexto (*Context Fork*) & Anti-Colisão Paralela (`[P]`):**
   - Nunca repasse transcrições brutas entre coordenador e subagentes; injete apenas envelope enxuto do estado necessário e `<= 5` regras operacionais.
   - Em ondas paralelas (`invoke_subagent` ou `swarm` com `workspace: "share"` para múltiplos autores e `"inherit"` para leitores/verificadores), proíba escrita simultânea de dois subagentes no mesmo arquivo e execute sempre verificação **Read-After-Write** ao consolidar o resultado.
