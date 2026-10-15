"""
agent_spec_loader.py
Carregador Declarativo de Agentes (Declarative YAML Agent Spec com MCP) — Padrão Zero-Config (TDAH-Friendly).

Objetivo:
Evitar código imperativo repetitivo e, ao mesmo tempo, NÃO engessar o desenvolvedor:
você pode escrever um manifesto YAML mínimo (apenas `name` e `system_prompt` ou `goal`),
e o carregador injeta defaults inteligentes de modelo, temperatura, guardrails e servidores MCP.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

try:
    import yaml
except ImportError:
    yaml = None  # Fallback se PyYAML não estiver ativo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class AgentGuardrailsSpec(BaseModel):
    max_tool_calls: int = 8
    timeout_seconds: int = 60
    human_in_the_loop_on: List[str] = Field(
        default_factory=lambda: ["delete_record", "remove_item", "send_external_email", "drop_table"]
    )


class MCPServerSpec(BaseModel):
    name: str
    type: str = "workspace"
    command: Optional[str] = None
    scope: str = "read_only"


class DeclarativeAgentSpec(BaseModel):
    name: str
    version: str = "1.0.0"
    model: str = "gemini-2.5-pro"
    temperature: float = 0.1
    role: str = "Especialista Autônomo"
    system_prompt: str = "Atue com rigor técnico, valide evidências no disco e mantenha qualidade linear alta."
    guardrails: AgentGuardrailsSpec = Field(default_factory=AgentGuardrailsSpec)
    mcp_servers: List[MCPServerSpec] = Field(
        default_factory=lambda: [MCPServerSpec(name="franklin-skills", type="workspace", scope="read_only")]
    )


def load_agent_spec(yaml_path_or_str: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Carrega um manifesto declarativo de agente (de um arquivo .yaml ou string YAML)
    aplicando Zero-Config Defaults via Pydantic para que você nunca precise lembrar
    de todos os campos.
    """
    candidate = Path(yaml_path_or_str)
    if candidate.exists() and candidate.is_file():
        raw_content = candidate.read_text(encoding="utf-8")
    else:
        raw_content = yaml_path_or_str

    if yaml is not None:
        parsed = yaml.safe_load(raw_content)
    else:
        parsed = json.loads(raw_content)

    agent_dict = parsed.get("agent", parsed) if isinstance(parsed, dict) else {}

    # Normalizar mcp_servers caso o usuário passe apenas strings (ex: ["franklin-skills"])
    if "mcp_servers" in agent_dict and isinstance(agent_dict["mcp_servers"], list):
        norm_servers = []
        for s in agent_dict["mcp_servers"]:
            if isinstance(s, str):
                norm_servers.append({"name": s})
            elif isinstance(s, dict):
                norm_servers.append(s)
        agent_dict["mcp_servers"] = norm_servers

    validated_spec = DeclarativeAgentSpec(**agent_dict)
    spec_data = validated_spec.model_dump()

    if verbose:
        print(f"[*] Instanciando Agente: {spec_data['name']} (v{spec_data['version']})")
        print(f"[*] Modelo Base: {spec_data['model']} | Temperatura: {spec_data['temperature']}")
        print(f"[*] Servidores MCP Conectados: {[s['name'] for s in spec_data['mcp_servers']]}")
        print(f"[*] Guardrails Ativos: Max Calls = {spec_data['guardrails']['max_tool_calls']}")

    return spec_data


if __name__ == "__main__":
    manifesto_exemplo = """
agent:
  name: "state-checker-observer"
  version: "1.1.0"
  model: "gemini-2.5-pro"
  temperature: 0.1
  system_prompt: |
    Você é o Subagente Observador de Estado e Validador de Qualidade (State Checker & Audit Observer).
    Confronte os achados dos subagentes executores com a AST real, descarte falsos positivos e calcule Snorm.
  guardrails:
    max_tool_calls: 6
    timeout_seconds: 45
    human_in_the_loop_on: ["delete_file", "apply_mass_refactor"]
  mcp_servers:
    - name: "franklin-skills"
      type: "workspace"
      scope: "read_only"
"""
    spec_carregada = load_agent_spec(manifesto_exemplo)
    print("Agente instanciado com sucesso:", spec_carregada["name"])
