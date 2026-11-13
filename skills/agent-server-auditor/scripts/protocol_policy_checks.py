"""
protocol_policy_checks.py
Regras modulares de conformidade Gemini 4 / Antigravity / Google GenAI SDK
para subagentes declarativos (agents/*.md) e código de servidor/agente (Py/TS/Go).
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple

ALLOWED_EXEC_POLICIES: frozenset[str] = frozenset({"auto", "sandbox", "off"})
LEGACY_AGENT_KEYS: Tuple[str, ...] = (
    "enable_write_tools",
    "enable_mcp_tools",
    "enable_subagent_tools",
    "wave",
    "parent_persona",
    "covered_modules",
)
FORBIDDEN_AGENT_TOOLS: frozenset[str] = frozenset({"*", "call_mcp_tool"})
LEGACY_SDK_RE = re.compile(
    r"(?:^\s*(?:import|from)\s+google\.generativeai\b|google\.generativeai\.(?:configure|GenerativeModel)|"
    r"(?:import\b[^;\n]*\bfrom|(?:import|require)\s*\()\s*['\"](?:@google/generative-?ai|@google-cloud/vertexai)['\"]|"
    r"\bimport\s+['\"](?:@google/generative-?ai|@google-cloud/vertexai)['\"]|"
    r"['\"]google\.golang\.org/generative-ai(?:/[^'\"\s]*)?['\"])",
    re.IGNORECASE | re.MULTILINE,
)
RETIRED_MODEL_RE = re.compile(
    r"(?<![a-z0-9-])("
    r"gemini-1\.(?:0|5)-[a-z0-9.-]*|"
    r"gemini-2\.0-[a-z0-9.-]*|"
    r"gemini-live-2\.5-[a-z0-9.-]*|"
    r"gemini-2\.5-(?!flash-lite(?![a-z0-9-]))[a-z0-9.-]*|"
    r"gemini-3(?:\.0)?-pro(?:-image)?-preview|"
    r"(?:gemini-)?3\.1-(?:flash-live-preview|flash-lite-preview|flash-image-preview|[a-z0-9-]*tts-preview)|"
    r"gemini-embedding-(?:2-preview|exp(?:-03-07)?)|"
    r"gemini-omni-(?:1\.1-flash|flash-preview)|"
    r"gemini-robotics-er-1\.[56]-preview|"
    r"deep-research-pro-preview-12-2025|"
    r"antigravity-preview-05-2026|"
    r"gemini-3\.8-flash-lite(?!-tts)|"
    r"gemini-3\.5-flash(?!-lite)|"
    r"text-embedding-004|embedding-(?:001|gecko-001)|"
    r"imagen-[34]\.0-[a-z0-9.-]*|"
    r"veo-[23]\.[01]-[a-z0-9.-]*"
    r")(?![a-z0-9-])",
    re.IGNORECASE,
)
GENAI_SDK_CLIENT_RE = re.compile(
    r"(google\.genai|@google/genai|google\.golang\.org/genai|genai\.Client|GoogleGenAI)"
)
V1BETA_REQUIRED_FEATURE_RE = re.compile(
    r"(?:\binteractions\.create\b|\bclient\.interactions\b|gemini-decision-1|antigravity-preview-09-2026)"
)
V1BETA_CONFIG_RE = re.compile(
    r"(?:v1beta|v1beta1|api_version|apiVersion|APIVersion|GOOGLE_GENAI_API_VERSION)"
)
REGEX_DEF_LINE_RE = re.compile(r"\b(re\.compile|regexp\.MustCompile|new\s+RegExp)\s*\(")
SKIP_SCAN_PREFIXES: Tuple[str, ...] = ("skills/", "tests/", "rules/", "references/", "memories/", "docs/")


def _paren_delta(line: str) -> int:
    """Calcula saldo líquido de parênteses ignorando escapes e classes regex."""
    cleaned = re.sub(r"\\.|\[[^\]]*\]", "", line)
    return cleaned.count("(") - cleaned.count(")")


def _strip_non_executable_lines(text: str) -> str:
    """Remove comentários e definições de regex (1 ou N linhas) contra falsos positivos."""
    kept: List[str] = []
    regex_paren_depth = 0
    in_block_comment = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if in_block_comment:
            in_block_comment = "*/" not in stripped
            continue
        if stripped.startswith("/*"):
            in_block_comment = "*/" not in stripped
            continue
        if regex_paren_depth > 0:
            regex_paren_depth = max(0, regex_paren_depth + _paren_delta(raw_line))
            continue
        if not stripped or stripped.startswith(("#", "//", "*")):
            continue
        if REGEX_DEF_LINE_RE.search(stripped):
            regex_paren_depth = max(0, _paren_delta(raw_line))
            continue
        kept.append(raw_line)
    return "\n".join(kept)


def _parse_frontmatter_yaml(fm_block: str) -> Dict[str, Any]:
    """Faz parse seguro do frontmatter YAML com PyYAML quando disponível."""
    try:
        import yaml
    except ImportError as exc:
        _ = exc
        return {}
    try:
        loaded = yaml.safe_load(fm_block)
    except (yaml.YAMLError, ValueError, TypeError) as exc:
        _ = exc
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _find_forbidden_tools(fm_dict: Dict[str, Any], fm_block: str) -> List[str]:
    """Detecta tools proibidas ('*' ou 'call_mcp_tool') na lista tools de subagentes."""
    raw_tools = fm_dict.get("tools")
    if isinstance(raw_tools, list):
        return sorted({str(t).strip() for t in raw_tools if str(t).strip() in FORBIDDEN_AGENT_TOOLS})
    found: List[str] = []
    if re.search(r"^\s*-\s*[\"']?\*[\"']?\s*$", fm_block, re.MULTILINE) or re.search(
        r"tools:\s*\[[^\]]*[\"']?\*[\"']?", fm_block
    ):
        found.append("*")
    if re.search(r"^\s*-\s*[\"']?call_mcp_tool[\"']?\s*$", fm_block, re.MULTILINE) or re.search(
        r"tools:\s*\[[^\]]*call_mcp_tool", fm_block
    ):
        found.append("call_mcp_tool")
    return found


def _find_legacy_agent_keys(fm_dict: Dict[str, Any], fm_block: str) -> List[str]:
    """Detecta chaves legadas não-Antigravity no frontmatter de subagentes."""
    if fm_dict:
        return [key for key in LEGACY_AGENT_KEYS if key in fm_dict]
    return [
        key
        for key in LEGACY_AGENT_KEYS
        if re.search(rf"^{re.escape(key)}\s*:", fm_block, re.MULTILINE)
    ]


def audit_subagent_markdown(text: str) -> Tuple[List[str], bool]:
    """Audita contrato Antigravity oficial de subagentes em agents/*.md."""
    cleaned = text.lstrip("\ufeff")
    has_fm = cleaned.startswith("---") and "\n---" in cleaned[3:]
    if not has_fm:
        return ["frontmatter"], False

    parts = cleaned.split("---", 2)
    fm_block = parts[1]
    body_block = parts[2].strip() if len(parts) > 2 else ""
    fm_dict = _parse_frontmatter_yaml(fm_block)

    missing: List[str] = []
    forbidden_tools = _find_forbidden_tools(fm_dict, fm_block)
    if forbidden_tools:
        missing.append(f"AUD-AGT-02: tools proibidas ({', '.join(forbidden_tools)})")

    legacy_keys = _find_legacy_agent_keys(fm_dict, fm_block)
    if legacy_keys:
        missing.append(f"AUD-AGT-02: chaves legadas proibidas ({', '.join(legacy_keys)})")

    raw_pol = fm_dict.get("commandExecutionPolicy")
    if raw_pol is False and re.search(r"^commandExecutionPolicy:\s*off\s*$", fm_block, re.MULTILINE):
        policy = "off"
    elif fm_dict:
        policy = str(raw_pol or "").strip()
    else:
        m_pol = re.search(r"^commandExecutionPolicy:\s*[\"']?([A-Za-z0-9_-]+)", fm_block, re.MULTILINE)
        policy = m_pol.group(1) if m_pol else ""
    if policy not in ALLOWED_EXEC_POLICIES:
        missing.append("AUD-AGT-02: commandExecutionPolicy válido obrigatório (auto|sandbox|off)")

    if len(body_block) < 60:
        missing.append("objective_body")

    type_safe = not forbidden_tools and not legacy_keys and policy in ALLOWED_EXEC_POLICIES
    return missing, type_safe


def scan_code_protocol_violations(rel: str, text: str) -> List[str]:
    """Detecta SDKs depreciados, modelos aposentados e falta de api_version='v1beta'."""
    active = _strip_non_executable_lines(text)
    if not active:
        return []
    violations: List[str] = []
    sdk_match = LEGACY_SDK_RE.search(active)
    if sdk_match:
        violations.append(f"AUD-SDK-01: SDK legado depreciado '{sdk_match.group(0).strip()}' em '{rel}'.")
    model_match = RETIRED_MODEL_RE.search(active)
    if model_match:
        violations.append(f"AUD-MOD-01: Modelo aposentado/banido '{model_match.group(1)}' em '{rel}'.")
    if (
        GENAI_SDK_CLIENT_RE.search(active)
        and V1BETA_REQUIRED_FEATURE_RE.search(active)
        and not V1BETA_CONFIG_RE.search(active)
    ):
        violations.append(
            f"AUD-API-01: Uso de interactions/decisions/antigravity-preview-09-2026 sem api_version='v1beta' em '{rel}'."
        )
    return violations


def collect_code_protocol_gaps(root: Path, files: List[Path]) -> List[str]:
    """Varre módulos Py/TS/Go do repositório contra violações de SDK, modelo e v1beta."""
    gaps: List[str] = []
    for f in files:
        if f.suffix.lower() not in {".py", ".ts", ".go"} or "test" in f.name.lower():
            continue
        rel = f.relative_to(root).as_posix()
        if rel.startswith(SKIP_SCAN_PREFIXES):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        gaps.extend(scan_code_protocol_violations(rel, text))
    return gaps


def populate_clean_self_test_tree(root: Path) -> Tuple[Path, Path]:
    """Cria árvore sintética limpa de projeto agêntico para auto-teste determinístico."""
    (root / ".gitignore").write_text(".env\n", encoding="utf-8")
    (root / ".env.example").write_text("API_KEY=\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname='demo'\ndependencies=['mcp>=1.0.0']\n", encoding="utf-8")
    (root / "bin").mkdir()
    ag_dir = root / "agents"
    ag_dir.mkdir()
    (ag_dir / "orchestrator.py").write_text(
        "from google import genai\nfrom google.adk import Agent\n"
        "client = genai.Client(http_options={'api_version': 'v1beta'})\n"
        "max_steps = 10\nstop_condition = 'COMPLETED'\n",
        encoding="utf-8",
    )
    (ag_dir / "clean_subagent.md").write_text(
        "---\nname: clean-subagent\ndescription: \"Subagente seguro.\"\nmodel: inherit\n"
        "commandExecutionPolicy: \"sandbox\"\ntools:\n  - read_file\n---\n"
        + ("Subagente declarativo completo com objetivo explícito e escopo seguro. " * 2),
        encoding="utf-8",
    )
    mcp_dir = root / "mcp_servers" / "clean_srv"
    mcp_dir.mkdir(parents=True)
    (mcp_dir / "server.py").write_text(
        'import sys\nfrom mcp import FastMCP\nmodel_config = ConfigDict(extra="forbid")\nprint("ok", file=sys.stderr)\n',
        encoding="utf-8",
    )
    sk_dir = root / "skills" / "demo-skill"
    for sub in ("scripts", "references", "evals"):
        (sk_dir / sub).mkdir(parents=True)
    (sk_dir / "SKILL.md").write_text("---\nname: demo-skill\n---\n# Body\n", encoding="utf-8")
    (sk_dir / "scripts" / "run.py").write_text("x = 1\n", encoding="utf-8")
    (sk_dir / "references" / "ref.md").write_text("# Ref\n", encoding="utf-8")
    (sk_dir / "evals" / "evals.json").write_text('[{"eval_id":"1","prompt":"p","assertions":["a"]}]', encoding="utf-8")
    a2a_dir = root / ".well-known"
    a2a_dir.mkdir()
    (a2a_dir / "agent-card.json").write_text(
        json.dumps({
            "name": "demo-node",
            "description": "Nó A2A de demonstração",
            "version": "1.0.0",
            "supportedInterfaces": [{"protocolBinding": "JSONRPC"}],
            "skills": [{"id": "demo-skill"}],
            "signatures": [{"signature": "sig"}],
        }),
        encoding="utf-8",
    )
    return ag_dir, mcp_dir

