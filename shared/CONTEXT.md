# CONTEXTO OPERACIONAL — `franklin-quebragalho/shared`

Pacote Python standalone embutido em `C:\Users\melki\dev\repos\franklin-quebragalho\shared` que provê os motores de segurança Zero-Trust, checkpoints Human-in-the-Loop (HITL), ponte criptográfica Agent2Agent (`A2A v1.0` + JWS) e consultoria da especificação MCP `2026-07-28`.
- `harness.py`: `SemanticGuard`, `RiskLevel`, `evaluate_action_risk` e `CheckpointStore`.
- `a2a_bridge.py`: `build_franklin_agent_card`, `sign_agent_card`, `verify_agent_card_signature` e `FranklinA2ATaskManager`.
- `mcp_2026_advisor.py`: `advise_mcp_architecture` e gerador de manifesto `.mcpb` v0.4.
- `tools/frontmatter_parser.py`: Parser determinístico de frontmatter YAML para as 29 skills canônicas.
