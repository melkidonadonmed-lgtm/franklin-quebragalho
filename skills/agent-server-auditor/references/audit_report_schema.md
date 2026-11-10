# Esquema Canônico do Relatório de Auditoria (`memories/audit_report.json`)

```json
{
  "timestamp": "2026-10-26T10:15:00Z",
  "audit_version": "1.0.0",
  "target_root": "/workspace/meu-projeto",
  "summary": {
    "compliance_score": 88.5,
    "status": "CONFORME_COM_RESSALVAS",
    "detected_languages": ["Python", "TypeScript", "Go"],
    "total_agents": 3,
    "total_skills": 2,
    "total_mcp_servers": 1,
    "total_a2a_cards": 1
  },
  "binary_hygiene": {
    "has_dedicated_bin_dir": true,
    "compiled_artifacts_count": 0,
    "status": "APPROVED"
  },
  "audit_details": {
    "agents": [
      {
        "name": "orchestrator",
        "file": "agents/orchestrator.py",
        "language": "Python",
        "framework": "Google ADK 2.x",
        "reasoning_pattern": "ReAct (Reasoning + Acting)",
        "has_max_steps": true,
        "has_stop_condition": true,
        "type_safety": true,
        "missing_elements": []
      }
    ],
    "skills": [
      {
        "name": "agent-server-auditor",
        "path": "skills/agent-server-auditor",
        "has_frontmatter": true,
        "has_scripts": true,
        "has_references": true,
        "has_evals": true,
        "missing_elements": []
      }
    ],
    "mcp_servers": [
      {
        "name": "db_connector",
        "file": "mcp_servers/db_connector/server.py",
        "transport": "STDIO",
        "stdout_hygiene": "CLEAN",
        "strict_contracts": true,
        "missing_elements": []
      }
    ],
    "a2a_nodes": [
      {
        "card_path": ".well-known/agent-card.json",
        "name": "finance-analyst",
        "has_supported_interfaces": true,
        "has_skills_catalog": true,
        "has_jws_signatures": true,
        "missing_elements": []
      }
    ]
  },
  "gap_analysis": {
    "critical_missing_structures": [],
    "warnings": [
      "Subagente 'intent_diagnostician.py' não declara timeout explícito para chamadas de ferramentas."
    ]
  }
}
```
