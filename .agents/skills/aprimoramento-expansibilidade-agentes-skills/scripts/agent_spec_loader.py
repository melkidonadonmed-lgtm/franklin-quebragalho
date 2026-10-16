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
    description: str = ""
    version: str = "1.0.0"
    model: str = "gemini-2.5-pro"
    temperature: float = 0.1
    role: str = "Especialista Autônomo"
    parent_persona: str = "FrontCraftMaster"
    wave: int = 1
    workspace: str = "inherit"
    enable_write_tools: bool = True
    enable_mcp_tools: bool = True
    covered_modules: List[str] = Field(default_factory=list)
    system_prompt: str = "Atue com rigor técnico, valide evidências no disco e mantenha qualidade linear alta."
    guardrails: AgentGuardrailsSpec = Field(default_factory=AgentGuardrailsSpec)
    mcp_servers: List[MCPServerSpec] = Field(
        default_factory=lambda: [MCPServerSpec(name="franklin-skills", type="workspace", scope="read_only")]
    )


AgentGuardrailsSpec.model_rebuild()
MCPServerSpec.model_rebuild()
DeclarativeAgentSpec.model_rebuild(
    _types_namespace={
        "List": List,
        "Optional": Optional,
        "Dict": Dict,
        "Any": Any,
        "AgentGuardrailsSpec": AgentGuardrailsSpec,
        "MCPServerSpec": MCPServerSpec,
    }
)


def _extract_yaml_and_body(raw_content: str) -> tuple[str, str]:
    """Extrai YAML frontmatter e corpo Markdown caso o arquivo comece com '---'."""
    stripped = raw_content.lstrip("\ufeff").strip()
    lines = stripped.splitlines()
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            line = lines[idx]
            if line.strip() == "---":
                yaml_block = "\n".join(lines[1:idx])
                markdown_body = "\n".join(lines[idx + 1 :]).strip()
                return yaml_block, markdown_body
            if line.startswith("# ") and idx > 1 and not lines[idx - 1].strip():
                raise ValueError(
                    "Frontmatter YAML malformado: delimitador de fechamento '---' ausente antes do corpo Markdown."
                )
        raise ValueError(
            "Frontmatter YAML malformado: delimitador de fechamento '---' ausente."
        )
    return raw_content, ""


def _parse_scalar(val: str) -> Any:
    """Converte um valor escalar YAML básico em tipo Python."""
    v = val.strip()
    if not v:
        return ""
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~", "none"):
        return None
    if v.startswith("[") or v.startswith("{"):
        try:
            return json.loads(v)
        except Exception:
            pass
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def _parse_yaml_mapping(lines: List[str]) -> Dict[str, Any]:
    """Analisa um bloco de mapeamento YAML sem depender de PyYAML."""
    result: Dict[str, Any] = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if ":" not in stripped:
            i += 1
            continue
        key_part, val_part = stripped.split(":", 1)
        key = key_part.strip()
        val_str = val_part.strip()
        i += 1

        if val_str in (">-", ">", "|", "|-"):
            block_lines: List[str] = []
            while i < n:
                sub = lines[i]
                sub_strip = sub.strip()
                sub_indent = len(sub) - len(sub.lstrip(" "))
                if sub_strip and sub_indent <= indent:
                    break
                if sub_strip:
                    block_lines.append(sub_strip)
                elif val_str.startswith("|"):
                    block_lines.append("")
                i += 1
            sep = " " if val_str.startswith(">") else "\n"
            result[key] = sep.join(block_lines).strip()
        elif val_str == "":
            sub_lines: List[str] = []
            while i < n:
                sub = lines[i]
                sub_strip = sub.strip()
                sub_indent = len(sub) - len(sub.lstrip(" "))
                if sub_strip and sub_indent <= indent:
                    break
                if sub_strip:
                    sub_lines.append(sub)
                i += 1
            if not sub_lines:
                result[key] = None
            elif sub_lines[0].strip().startswith("- "):
                items: List[Any] = []
                j = 0
                while j < len(sub_lines):
                    sline = sub_lines[j]
                    sstrip = sline.strip()
                    sindent = len(sline) - len(sline.lstrip(" "))
                    if sstrip.startswith("- "):
                        after_dash = sstrip[2:].strip()
                        if ":" in after_dash and not (
                            after_dash.startswith('"') or after_dash.startswith("'")
                        ):
                            item_dict: Dict[str, Any] = {}
                            ik, iv = after_dash.split(":", 1)
                            item_dict[ik.strip()] = _parse_scalar(iv)
                            j += 1
                            while j < len(sub_lines):
                                next_line = sub_lines[j]
                                next_strip = next_line.strip()
                                next_indent = len(next_line) - len(next_line.lstrip(" "))
                                if next_strip.startswith("- ") and next_indent <= sindent:
                                    break
                                if ":" in next_strip:
                                    nk, nv = next_strip.split(":", 1)
                                    item_dict[nk.strip()] = _parse_scalar(nv)
                                j += 1
                            items.append(item_dict)
                        else:
                            items.append(_parse_scalar(after_dash))
                            j += 1
                    else:
                        j += 1
                result[key] = items
            else:
                result[key] = _parse_yaml_mapping(sub_lines)
        else:
            result[key] = _parse_scalar(val_str)
    return result


def _parse_yaml_fallback(yaml_text: str) -> Any:
    """Fallback determinístico em Python puro caso PyYAML não esteja instalado."""
    stripped = yaml_text.strip()
    if not stripped:
        return {}
    if stripped.startswith("{"):
        return json.loads(stripped)
    raw_lines = [l for l in yaml_text.splitlines() if l.strip() and not l.strip().startswith("#")]
    if not raw_lines:
        return {}
    first = raw_lines[0].strip()
    if first.startswith("agent:"):
        after = first.split(":", 1)[1].strip()
        if after:
            return {"agent": _parse_scalar(after)}
        return {"agent": _parse_yaml_mapping(raw_lines[1:])}
    return _parse_yaml_mapping(raw_lines)


def load_agent_spec(yaml_path_or_str: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Carrega um manifesto declarativo de agente (de um arquivo .yaml, .md com frontmatter ou string YAML)
    aplicando Zero-Config Defaults via Pydantic para que você nunca precise lembrar
    de todos os campos.
    """
    candidate = Path(yaml_path_or_str)
    if candidate.exists() and candidate.is_file():
        raw_content = candidate.read_text(encoding="utf-8")
    else:
        raw_content = yaml_path_or_str

    yaml_text, markdown_body = _extract_yaml_and_body(raw_content)

    if yaml is not None:
        parsed = yaml.safe_load(yaml_text)
    else:
        parsed = _parse_yaml_fallback(yaml_text)

    if isinstance(parsed, dict):
        raw_agent = parsed.get("agent") if "agent" in parsed else parsed
        if raw_agent is None:
            raise ValueError("Bloco 'agent' no manifesto YAML não pode ser nulo (None).")
        if not isinstance(raw_agent, dict):
            raise ValueError("Manifesto YAML inválido: o bloco de configuração deve ser um mapeamento (dict).")
        agent_dict: Dict[str, Any] = dict(raw_agent)
    else:
        agent_dict = {}

    if markdown_body and "system_prompt" not in agent_dict:
        agent_dict["system_prompt"] = markdown_body

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
