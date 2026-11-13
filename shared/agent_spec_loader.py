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
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

logger = logging.getLogger("AgentSpecLoader")

try:
    import yaml
except ImportError:
    yaml = None  # Fallback se PyYAML não estiver ativo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class AgentGuardrailsSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_steps: int = 10
    max_tool_calls: int = 8
    timeout_seconds: int = 60
    stop_condition: str = "TASK_STATE_COMPLETED"
    human_in_the_loop_on: List[str] = Field(
        default_factory=lambda: ["delete_record", "remove_item", "send_external_email", "drop_table"]
    )


class MCPServerSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: str = "workspace"
    command: Optional[str] = None
    scope: str = "read_only"


class DeclarativeAgentSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str = ""
    goal: str = ""
    version: str = "1.0.0"
    model: str = Field(
        default_factory=lambda: os.getenv("ADK_MODEL") or os.getenv("GEMINI_MODEL") or "inherit"
    )
    role: str = "Especialista Autônomo"
    parent_persona: str = "UI-Architect"
    wave: int = 1
    workspace: str = "inherit"
    enable_write_tools: Optional[bool] = None
    enable_mcp_tools: Optional[bool] = None
    enable_subagent_tools: Optional[bool] = None
    subagent: bool = True
    mainAgent: bool = False
    commandExecutionPolicy: str = "sandbox"
    inheritMcp: bool = True
    inheritCustomizations: bool = True
    tools: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    mcpServers: List[Any] = Field(default_factory=list)
    covered_modules: List[str] = Field(default_factory=list)
    system_prompt: str = "Atue com rigor técnico, valide evidências no disco e mantenha qualidade linear alta."
    guardrails: AgentGuardrailsSpec = Field(default_factory=AgentGuardrailsSpec)
    mcp_servers: List[MCPServerSpec] = Field(
        default_factory=lambda: [
            MCPServerSpec(name="franklin-skills", type="workspace", scope="read_only"),
            MCPServerSpec(
                name="google-developer-knowledge",
                type="remote",
                command="https://developerknowledge.googleapis.com/mcp",
                scope="read_only",
            ),
        ]
    )

    @model_validator(mode="after")
    def _derive_effective_capabilities(self) -> "DeclarativeAgentSpec":
        """Deriva enable_* a partir de tools/commandExecutionPolicy/inheritMcp quando omitidos."""
        write_tool_names = {
            "write_to_file", "replace_file_content", "multi_replace_file_content", "write_file", "edit_file"
        }
        if self.enable_write_tools is None:
            if self.tools:
                self.enable_write_tools = any(t in write_tool_names for t in self.tools)
            else:
                self.enable_write_tools = self.commandExecutionPolicy != "off"
        if self.enable_mcp_tools is None:
            self.enable_mcp_tools = self.inheritMcp
        if self.enable_subagent_tools is None:
            self.enable_subagent_tools = (not self.tools) or ("invoke_subagent" in self.tools)
        return self


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
        except (json.JSONDecodeError, ValueError) as exc:
            _ignored_err = str(exc)
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def _consume_yaml_dict_item(sub_lines: List[str], start_j: int, sindent: int, after_dash: str) -> tuple[Dict[str, Any], int]:
    """Extrai um item de lista YAML composto por pares chave: valor."""
    item_dict: Dict[str, Any] = {}
    ik, iv = after_dash.split(":", 1)
    item_dict[ik.strip()] = _parse_scalar(iv)
    j = start_j + 1
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
    return item_dict, j


def _parse_yaml_list(sub_lines: List[str]) -> List[Any]:
    """Converte uma lista de linhas YAML começando com '- ' em lista Python."""
    items: List[Any] = []
    j = 0
    while j < len(sub_lines):
        sline = sub_lines[j]
        sstrip = sline.strip()
        if not sstrip.startswith("- "):
            j += 1
            continue
        sindent = len(sline) - len(sline.lstrip(" "))
        after_dash = sstrip[2:].strip()
        is_unquoted_kv = ":" in after_dash and not (after_dash.startswith('"') or after_dash.startswith("'"))
        if is_unquoted_kv:
            item_dict, j = _consume_yaml_dict_item(sub_lines, j, sindent, after_dash)
            items.append(item_dict)
        else:
            items.append(_parse_scalar(after_dash))
            j += 1
    return items


def _collect_indented_block(lines: List[str], start_i: int, indent: int) -> tuple[List[str], int]:
    """Coleta linhas consecutivas cuja indentação seja maior que indent."""
    collected: List[str] = []
    i = start_i
    while i < len(lines):
        sub = lines[i]
        sub_strip = sub.strip()
        if sub_strip and (len(sub) - len(sub.lstrip(" "))) <= indent:
            break
        collected.append(sub)
        i += 1
    return collected, i


def _resolve_block_value(val_str: str, block_raw: List[str]) -> Any:
    """Resolve valor de bloco YAML multiline ('|', '>') ou sub-bloco vazio."""
    if val_str in (">-", ">", "|", "|-"):
        out_lines = [s.strip() if s.strip() else "" for s in block_raw if s.strip() or val_str.startswith("|")]
        sep = " " if val_str.startswith(">") else "\n"
        return sep.join(out_lines).strip()
    non_empty = [s for s in block_raw if s.strip()]
    if not non_empty:
        return None
    if non_empty[0].strip().startswith("- "):
        return _parse_yaml_list(non_empty)
    return _parse_yaml_mapping(non_empty)


def _parse_yaml_mapping(lines: List[str]) -> Dict[str, Any]:
    """Analisa um bloco de mapeamento YAML sem depender de PyYAML."""
    result: Dict[str, Any] = {}
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        key_part, val_part = stripped.split(":", 1)
        key, val_str = key_part.strip(), val_part.strip()
        i += 1
        if val_str in (">-", ">", "|", "|-", ""):
            block_raw, i = _collect_indented_block(lines, i, indent)
            result[key] = _resolve_block_value(val_str, block_raw)
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


def _normalize_agent_dict(parsed: Any, markdown_body: str) -> Dict[str, Any]:
    """Extrai e normaliza o dicionário de configuração do agente a partir do YAML parseado."""
    if not isinstance(parsed, dict):
        agent_dict: Dict[str, Any] = {}
    else:
        raw_agent = parsed.get("agent") if "agent" in parsed else parsed
        if raw_agent is None:
            raise ValueError("Bloco 'agent' no manifesto YAML não pode ser nulo (None).")
        if not isinstance(raw_agent, dict):
            raise ValueError("Manifesto YAML inválido: o bloco de configuração deve ser um mapeamento (dict).")
        agent_dict = dict(raw_agent)

    if markdown_body and "system_prompt" not in agent_dict:
        agent_dict["system_prompt"] = markdown_body

    raw_servers = agent_dict.get("mcp_servers")
    if isinstance(raw_servers, list):
        agent_dict["mcp_servers"] = [{"name": s} if isinstance(s, str) else s for s in raw_servers if isinstance(s, (str, dict))]
    return agent_dict


def load_agent_spec(yaml_path_or_str: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Carrega um manifesto declarativo de agente (de um arquivo .yaml, .md com frontmatter ou string YAML)
    aplicando Zero-Config Defaults via Pydantic.
    """
    candidate = Path(yaml_path_or_str)
    raw_content = candidate.read_text(encoding="utf-8") if (candidate.exists() and candidate.is_file()) else yaml_path_or_str
    yaml_text, markdown_body = _extract_yaml_and_body(raw_content)
    parsed = yaml.safe_load(yaml_text) if yaml is not None else _parse_yaml_fallback(yaml_text)
    agent_dict = _normalize_agent_dict(parsed, markdown_body)
    validated_spec = DeclarativeAgentSpec(**agent_dict)
    spec_data = validated_spec.model_dump()

    if verbose:
        logger.info("[*] Instanciando Agente: %s (v%s)", spec_data["name"], spec_data["version"])
        logger.info("[*] Modelo Base: %s", spec_data["model"])
        logger.info("[*] Servidores MCP Conectados: %s", [s["name"] for s in spec_data["mcp_servers"]])
        logger.info("[*] Guardrails Ativos: Max Calls = %s", spec_data["guardrails"]["max_tool_calls"])

    return spec_data


if __name__ == "__main__":
    manifesto_exemplo = """
agent:
  name: "state-checker-observer"
  version: "1.1.0"
  model: "inherit"
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
