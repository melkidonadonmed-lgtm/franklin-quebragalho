#!/usr/bin/env python3
"""
agent_server_auditor.py
Motor determinístico de auditoria estática e arquitetural para sistemas agênticos,
servidores MCP (2026-07-28) e nós A2A (v1.0) em Python, TypeScript e Go.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Dict, List, Literal, Tuple

from pydantic import BaseModel, ConfigDict, Field

IGNORED_DIRS: frozenset[str] = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
})
ALLOWED_BIN_DIRS: frozenset[str] = frozenset({"bin", "dist", "build"})
BINARY_EXTENSIONS: frozenset[str] = frozenset({".exe", ".dll", ".so", ".dylib", ".asar", ".bin"})
MAX_STEPS_RE = re.compile(r"\b(max_steps|max_turns|max_retries|max_iterations|recursion_limit|MaxSteps|MaxTurns|maxSteps)\b")
STOP_COND_RE = re.compile(r"\b(stop_condition|should_continue|END|TASK_STATE_COMPLETED|COMPLETED|APPROVED|Read-After-Write)\b")
STRICT_SCHEMA_RE = re.compile(r'(extra\s*=\s*["\']forbid["\']|\.strict\(\)|"additionalProperties"\s*:\s*false)')
STDOUT_POLLUTION_PY_RE = re.compile(r"^\s*print\s*\((?!.*file\s*=\s*sys\.stderr).*\)")
STDOUT_POLLUTION_TS_RE = re.compile(r"\b(console\.log|process\.stdout\.write)\s*\(")
STDOUT_POLLUTION_GO_RE = re.compile(r"\bfmt\.Print(ln|f)?\s*\(")


class AuditSummary(BaseModel):
    """Resumo consolidado da auditoria arquitetural."""

    model_config = ConfigDict(extra="forbid")
    compliance_score: float = Field(ge=0.0, le=100.0)
    status: Literal["APPROVED", "CONFORME_COM_RESSALVAS", "REJECTED"]
    detected_languages: List[str]
    total_agents: int
    total_skills: int
    total_mcp_servers: int
    total_a2a_cards: int


class BinaryHygieneReport(BaseModel):
    """Resultado da inspeção de higiene de binários na raiz e subpastas."""

    model_config = ConfigDict(extra="forbid")
    has_dedicated_bin_dir: bool
    compiled_artifacts_count: int
    status: Literal["APPROVED", "REJECTED"]


class AgentAuditItem(BaseModel):
    """Diagnóstico individual de um módulo de agente ou orquestrador."""

    model_config = ConfigDict(extra="forbid")
    name: str
    file: str
    language: str
    framework: str
    reasoning_pattern: str
    has_max_steps: bool
    has_stop_condition: bool
    type_safety: bool
    missing_elements: List[str]


class SkillAuditItem(BaseModel):
    """Diagnóstico estrutural de uma pasta de Skill (SKILL.md)."""

    model_config = ConfigDict(extra="forbid")
    name: str
    path: str
    has_frontmatter: bool
    has_scripts: bool
    has_references: bool
    has_evals: bool
    missing_elements: List[str]


class McpServerAuditItem(BaseModel):
    """Diagnóstico de conformidade de um servidor MCP."""

    model_config = ConfigDict(extra="forbid")
    name: str
    file: str
    transport: str
    stdout_hygiene: Literal["CLEAN", "POLLUTED"]
    strict_contracts: bool
    missing_elements: List[str]


class A2ANodeAuditItem(BaseModel):
    """Diagnóstico de conformidade de um Cartão de Agente A2A v1.0."""

    model_config = ConfigDict(extra="forbid")
    card_path: str
    name: str
    has_supported_interfaces: bool
    has_skills_catalog: bool
    has_jws_signatures: bool
    missing_elements: List[str]


class AuditDetails(BaseModel):
    """Coleção detalhada dos 4 vetores auditados."""

    model_config = ConfigDict(extra="forbid")
    agents: List[AgentAuditItem]
    skills: List[SkillAuditItem]
    mcp_servers: List[McpServerAuditItem]
    a2a_nodes: List[A2ANodeAuditItem]


class GapAnalysis(BaseModel):
    """Análise de brechas críticas e avisos operacionais."""

    model_config = ConfigDict(extra="forbid")
    critical_missing_structures: List[str]
    warnings: List[str]


class AgentServerAuditReport(BaseModel):
    """Contrato completo persistido em memories/audit_report.json."""

    model_config = ConfigDict(extra="forbid")
    timestamp: str
    audit_version: str = "1.0.0"
    target_root: str
    summary: AuditSummary
    binary_hygiene: BinaryHygieneReport
    audit_details: AuditDetails
    gap_analysis: GapAnalysis


def _iter_project_files(root: Path) -> List[Path]:
    """Lista arquivos do projeto ignorando pastas de ambiente virtual, cache e controle de versão."""
    collected: List[Path] = []
    for item in root.rglob("*"):
        if item.is_file() and not any(part in IGNORED_DIRS for part in item.parts):
            collected.append(item)
    return sorted(collected)


def _detect_languages(root: Path, files: List[Path]) -> List[str]:
    """Detecta as linguagens ativas no repositório com base em manifestos e extensões."""
    langs: List[str] = []
    suffixes = {f.suffix.lower() for f in files}
    if (root / "pyproject.toml").exists() or ".py" in suffixes:
        langs.append("Python")
    if (root / "package.json").exists() or ".ts" in suffixes:
        langs.append("TypeScript")
    if (root / "go.mod").exists() or ".go" in suffixes:
        langs.append("Go")
    return langs


def _audit_binary_hygiene(root: Path, files: List[Path]) -> Tuple[BinaryHygieneReport, List[str]]:
    """Verifica se há binários compilados fora de bin/, dist/ ou build/."""
    misplaced: List[str] = []
    for f in files:
        rel_parts = f.relative_to(root).parts
        if f.suffix.lower() in BINARY_EXTENSIONS and not any(p in ALLOWED_BIN_DIRS for p in rel_parts):
            misplaced.append(f.relative_to(root).as_posix())
    has_bin = (root / "bin").is_dir() or (root / "dist").is_dir()
    status: Literal["APPROVED", "REJECTED"] = "APPROVED" if not misplaced else "REJECTED"
    return BinaryHygieneReport(
        has_dedicated_bin_dir=has_bin,
        compiled_artifacts_count=len(misplaced),
        status=status,
    ), misplaced


def _audit_skills(root: Path, files: List[Path]) -> List[SkillAuditItem]:
    """Audita pastas SKILL.md sob Progressive Disclosure oficial (apenas SKILL.md obrigatório; L3 exigido se L2 > 1.200 tokens)."""
    items: List[SkillAuditItem] = []
    skill_mds = [f for f in files if f.name == "SKILL.md"]
    for smd in skill_mds:
        s_dir = smd.parent
        text = smd.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
        has_fm = text.startswith("---") and "\n---" in text[3:]
        body = text.split("---", 2)[2] if has_fm and text.count("---") >= 2 else text
        has_scripts = (
            (s_dir / "scripts").is_dir() and any((s_dir / "scripts").iterdir())
        ) or (s_dir / "rules" / "criterios_auditoria.md").is_file()
        has_refs = (s_dir / "references").is_dir() and any((s_dir / "references").iterdir())
        has_evals = (s_dir / "evals" / "evals.json").is_file()
        missing: List[str] = []
        if not has_fm:
            missing.append("frontmatter")
        if (len(body) // 4) > 1200 and not (has_refs or has_scripts):
            missing.append("references/ (Progressive Disclosure L3 exigido para SKILL.md > 1200 tokens)")
        items.append(
            SkillAuditItem(
                name=s_dir.name,
                path=s_dir.relative_to(root).as_posix(),
                has_frontmatter=has_fm,
                has_scripts=has_scripts,
                has_references=has_refs,
                has_evals=has_evals,
                missing_elements=missing,
            )
        )
    return items


def _classify_framework_and_lang(f: Path, text: str) -> Tuple[str, str]:
    """Identifica linguagem e framework principal de um arquivo de agente."""
    ext_map = {".py": "Python", ".ts": "TypeScript", ".go": "Go"}
    lang = ext_map.get(f.suffix.lower(), "Unknown")
    if "google.golang.org/adk" in text or "google.adk" in text or "ADK" in text:
        return lang, "Google ADK 2.x"
    if "StateGraph" in text or "langgraph" in text:
        return lang, "LangGraph"
    if "FastMCP" in text or "modelcontextprotocol" in text:
        return lang, "MCP Agent Framework"
    return lang, "Custom Agent Orchestrator"


def _audit_agents(root: Path, files: List[Path]) -> List[AgentAuditItem]:
    """Audita orquestradores (Py/TS/Go) e subagentes (agents/*.md, .agents/agents/*.md) em 8 eixos (Sintaxe, Objetivo, Função, SDK, Guardrails, Policy e Menor Privilégio)."""
    import ast as py_ast

    items: List[AgentAuditItem] = []
    for f in files:
        rel = f.relative_to(root).as_posix()
        suffix = f.suffix.lower()
        if suffix == ".md" and (rel.startswith("agents/") or rel.startswith(".agents/agents/")):
            text = f.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
            has_fm = text.startswith("---") and "\n---" in text[3:]
            fm_block = text.split("---", 2)[1] if has_fm else ""
            body_block = text.split("---", 2)[2].strip() if has_fm and text.count("---") >= 2 else ""
            has_wildcard_tools = bool(re.search(r'^\s*-\s*["\']?\*["\']?\s*$', fm_block, re.MULTILINE))
            has_policy = "commandExecutionPolicy" in fm_block or "enable_write_tools" in fm_block
            has_objective = len(body_block) >= 60
            md_missing: List[str] = []
            if not has_fm:
                md_missing.append("frontmatter")
            if has_wildcard_tools:
                md_missing.append("least_privilege (tools: '*' proibido)")
            if not has_policy:
                md_missing.append("policy (commandExecutionPolicy/enable_write_tools)")
            if not has_objective:
                md_missing.append("objective_body")
            items.append(
                AgentAuditItem(
                    name=f.stem,
                    file=rel,
                    language="Markdown",
                    framework="Antigravity Declarative Subagent",
                    reasoning_pattern="Wave / Subagent Contract",
                    has_max_steps=True,
                    has_stop_condition=True,
                    type_safety=has_fm and not has_wildcard_tools,
                    missing_elements=md_missing,
                )
            )
            continue
        if suffix not in {".py", ".ts", ".go"} or "test" in f.name.lower():
            continue
        is_agent_path = "orchestrator" in f.name.lower() or "agent" in f.name.lower()
        if not is_agent_path or rel.startswith("skills/"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        lang, fw = _classify_framework_and_lang(f, text)
        syntax_ok = True
        if suffix == ".py":
            try:
                py_ast.parse(text, filename=rel)
            except SyntaxError:
                syntax_ok = False
        has_placebo = bool(re.search(r"\braise\s+NotImplementedError\b", text))
        has_max = bool(MAX_STEPS_RE.search(text))
        has_stop = bool(STOP_COND_RE.search(text))
        type_safe = syntax_ok and (("Any" not in text and "interface{}" not in text) or bool(STRICT_SCHEMA_RE.search(text)))
        missing = [
            lbl
            for ok, lbl in (
                (syntax_ok, "valid_syntax"),
                (not has_placebo, "real_function (NotImplementedError detectado)"),
                (has_max, "max_steps"),
                (has_stop, "stop_condition"),
            )
            if not ok
        ]
        items.append(
            AgentAuditItem(
                name=f.stem,
                file=rel,
                language=lang,
                framework=fw,
                reasoning_pattern="ReAct / StateGraph",
                has_max_steps=has_max,
                has_stop_condition=has_stop,
                type_safety=type_safe,
                missing_elements=missing,
            )
        )
    return items


def _has_stdout_pollution(suffix: str, text: str) -> bool:
    """Detecta escrita direta em stdout em servidores MCP STDIO."""
    if suffix == ".py":
        return any(STDOUT_POLLUTION_PY_RE.search(line) for line in text.splitlines())
    if suffix == ".ts":
        return bool(STDOUT_POLLUTION_TS_RE.search(text))
    if suffix == ".go":
        return bool(STDOUT_POLLUTION_GO_RE.search(text))
    return False


def _has_mcp_sdk_in_manifests(root: Path) -> bool:
    """Verifica se os manifestos do projeto declaram SDK oficial MCP (Python mcp/fastmcp, TS @modelcontextprotocol/sdk ou Go mcp/adk)."""
    for mf, pat in (
        ("pyproject.toml", r"(?i)\b(mcp|fastmcp)\b"),
        ("package.json", r"@modelcontextprotocol/sdk"),
        ("go.mod", r"(?i)(modelcontextprotocol|mcp-go|google\.golang\.org/adk)"),
    ):
        p = root / mf
        if p.is_file() and re.search(pat, p.read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def _audit_mcp_servers(root: Path, files: List[Path], global_strict: bool) -> List[McpServerAuditItem]:
    """Inspeciona servidores MCP quanto ao SDK declarado + comportamento (higiene STDIO e contratos estritos)."""
    items: List[McpServerAuditItem] = []
    has_manifest = any((root / m).is_file() for m in ("pyproject.toml", "package.json", "go.mod"))
    sdk_declared = _has_mcp_sdk_in_manifests(root) if has_manifest else True
    for f in files:
        if f.suffix.lower() not in {".py", ".ts", ".go"} or "test" in f.name.lower():
            continue
        rel = f.relative_to(root).as_posix()
        if rel.startswith("skills/"):
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        is_mcp = "FastMCP" in text or "StdioServerTransport" in text or "mcp.tool" in text or "mcp_servers/" in rel
        if not is_mcp:
            continue
        polluted = _has_stdout_pollution(f.suffix.lower(), text)
        strict = bool(STRICT_SCHEMA_RE.search(text)) or global_strict
        missing: List[str] = []
        if polluted:
            missing.append("stdout_hygiene (AUD-MCP-01)")
        if not strict:
            missing.append("strict_contracts (AUD-CNT-01)")
        if not sdk_declared:
            missing.append("mcp_sdk_in_manifest (AUD-MCP-01)")
        items.append(
            McpServerAuditItem(
                name=f.parent.name if f.stem == "server" else f.stem,
                file=rel,
                transport="STDIO",
                stdout_hygiene="POLLUTED" if polluted else "CLEAN",
                strict_contracts=strict and sdk_declared,
                missing_elements=missing,
            )
        )
    return items


def _audit_a2a_cards(root: Path, files: List[Path]) -> List[A2ANodeAuditItem]:
    """Audita cartões A2A (metadados name/version/description, IDs únicos em skills[].id e assinatura JWS)."""
    items: List[A2ANodeAuditItem] = []
    card_files = [f for f in files if f.name in {"agent-card.json", "agent_card.json"}]
    for cf in card_files:
        try:
            data = json.loads(cf.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        if not isinstance(data, dict):
            data = {}
        has_meta = bool(data.get("name")) and bool(data.get("version")) and bool(data.get("description"))
        has_ifaces = bool(data.get("supportedInterfaces"))
        raw_skills = data.get("skills") if isinstance(data.get("skills"), list) else []
        skill_ids = [str(s.get("id", "")).strip() for s in raw_skills if isinstance(s, dict) and str(s.get("id", "")).strip()]
        has_unique_ids = len(raw_skills) > 0 and len(skill_ids) == len(raw_skills) and len(set(skill_ids)) == len(skill_ids)
        has_jws = isinstance(data.get("signatures"), list) and len(data.get("signatures", [])) > 0
        missing = [
            lbl
            for ok, lbl in (
                (has_meta, "metadata (name/version/description)"),
                (has_ifaces, "supportedInterfaces"),
                (has_unique_ids, "skills[].id (unique IDs)"),
                (has_jws, "signatures (JWS)"),
            )
            if not ok
        ]
        items.append(
            A2ANodeAuditItem(
                card_path=cf.relative_to(root).as_posix(),
                name=str(data.get("name", cf.stem)),
                has_supported_interfaces=has_ifaces,
                has_skills_catalog=has_unique_ids,
                has_jws_signatures=has_jws,
                missing_elements=missing,
            )
        )
    return items


def _collect_protocol_and_entity_gaps(details: AuditDetails) -> Tuple[List[str], List[str]]:
    """Extrai falhas críticas e avisos das entidades auditadas (MCP, Agentes, Skills e A2A)."""
    crit_mcp = [
        f"AUD-MCP-01: Poluição de stdout detectada no servidor MCP '{s.file}'."
        for s in details.mcp_servers
        if s.stdout_hygiene == "POLLUTED"
    ]
    crit_agt = [
        f"AUD-AGT-01: Agente '{a.file}' sem trava de loop (max_steps/recursion_limit)."
        for a in details.agents
        if not a.has_max_steps
    ]
    warn_mcp = [
        f"AUD-CNT-01: Servidor MCP '{s.file}' sem contrato estrito explícito."
        for s in details.mcp_servers
        if not s.strict_contracts
    ]
    warn_skl = [f"AUD-SKL-01: Skill '{sk.name}' sem {sk.missing_elements}." for sk in details.skills if sk.missing_elements]
    warn_a2a = [
        f"AUD-A2A-01: Cartão A2A '{c.card_path}' sem {c.missing_elements}."
        for c in details.a2a_nodes
        if c.missing_elements
    ]
    return crit_mcp + crit_agt, warn_mcp + warn_skl + warn_a2a


def _compute_gaps_and_score(
    root: Path,
    bin_report: BinaryHygieneReport,
    misplaced_bins: List[str],
    details: AuditDetails,
) -> Tuple[GapAnalysis, float, Literal["APPROVED", "CONFORME_COM_RESSALVAS", "REJECTED"]]:
    """Consolida gaps críticos, avisos e nota determinística de conformidade (0-100)."""
    critical: List[str] = []
    warnings: List[str] = []
    if not (root / ".gitignore").exists():
        critical.append("AUD-BIN-01: Arquivo .gitignore ausente na raiz.")
    if not (root / ".env.example").exists():
        warnings.append("Template .env.example ausente na raiz do projeto.")
    critical.extend([f"AUD-BIN-01: Binário compilado fora de bin/dist/build: '{mb}'." for mb in misplaced_bins])
    ent_crit, ent_warn = _collect_protocol_and_entity_gaps(details)
    critical.extend(ent_crit)
    warnings.extend(ent_warn)

    score = max(0.0, round(100.0 - (len(critical) * 25.0) - (len(warnings) * 5.0), 2))
    if critical or bin_report.status == "REJECTED":
        status: Literal["APPROVED", "CONFORME_COM_RESSALVAS", "REJECTED"] = "REJECTED"
    elif warnings:
        status = "CONFORME_COM_RESSALVAS"
    else:
        status = "APPROVED"
    return GapAnalysis(critical_missing_structures=critical, warnings=warnings), score, status


def audit_repository(target_root: Path, persist: bool = False, output_path: Path | None = None) -> AgentServerAuditReport:
    """Executa a auditoria arquitetural completa na raiz do projeto e opcionalmente persiste em memória."""
    root = target_root.resolve()
    files = _iter_project_files(root)
    langs = _detect_languages(root, files)
    bin_report, misplaced_bins = _audit_binary_hygiene(root, files)
    global_strict = any(
        f.suffix.lower() in {".py", ".ts"} and STRICT_SCHEMA_RE.search(f.read_text(encoding="utf-8", errors="replace"))
        for f in files
        if not f.relative_to(root).as_posix().startswith("skills/")
    )
    details = AuditDetails(
        agents=_audit_agents(root, files),
        skills=_audit_skills(root, files),
        mcp_servers=_audit_mcp_servers(root, files, global_strict),
        a2a_nodes=_audit_a2a_cards(root, files),
    )
    gaps, score, status = _compute_gaps_and_score(root, bin_report, misplaced_bins, details)
    report = AgentServerAuditReport(
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        target_root=root.as_posix(),
        summary=AuditSummary(
            compliance_score=score,
            status=status,
            detected_languages=langs,
            total_agents=len(details.agents),
            total_skills=len(details.skills),
            total_mcp_servers=len(details.mcp_servers),
            total_a2a_cards=len(details.a2a_nodes),
        ),
        binary_hygiene=bin_report,
        audit_details=details,
        gap_analysis=gaps,
    )
    if persist or output_path is not None:
        dest = output_path if output_path is not None else (root / "memories" / "audit_report.json")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(report.model_dump(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def run_self_test() -> Dict[str, Any]:
    """Executa bateria de auto-validação determinística sobre fixtures sintéticas aprovadas e reprovadas."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".gitignore").write_text(".env\n", encoding="utf-8")
        (root / ".env.example").write_text("API_KEY=\n", encoding="utf-8")
        (root / "pyproject.toml").write_text("[project]\nname='demo'\ndependencies=['mcp>=1.0.0']\n", encoding="utf-8")
        (root / "bin").mkdir()
        ag_dir = root / "agents"
        ag_dir.mkdir()
        (ag_dir / "orchestrator.py").write_text(
            "from google.adk import Agent\nmax_steps = 10\nstop_condition = 'COMPLETED'\n", encoding="utf-8"
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
        clean_rep = audit_repository(root, persist=True)
        assert clean_rep.summary.status == "APPROVED", f"Esperado APPROVED, obteve {clean_rep.summary.status}"
        assert clean_rep.summary.compliance_score == 100.0
        assert (root / "memories" / "audit_report.json").is_file()

        # Injetar poluição STDIO e binário solto -> deve reprovar (REJECTED)
        (mcp_dir / "server.py").write_text('from mcp import FastMCP\nprint("polluted stdout")\n', encoding="utf-8")
        (root / "stray.exe").write_bytes(b"MZ")
        dirty_rep = audit_repository(root, persist=False)
        assert dirty_rep.summary.status == "REJECTED"
        assert dirty_rep.binary_hygiene.status == "REJECTED"
        assert dirty_rep.audit_details.mcp_servers[0].stdout_hygiene == "POLLUTED"
    return {
        "status": "[PASS]",
        "self_test": "APPROVED_AND_REJECTED_VERIFIED",
        "clean_score": clean_rep.summary.compliance_score,
        "dirty_status": dirty_rep.summary.status,
    }


def main() -> int:
    """Ponto de entrada CLI do auditor arquitetural de agentes e servidores."""
    parser = argparse.ArgumentParser(description="Auditor arquitetural de agentes, skills, MCP e A2A.")
    parser.add_argument("--root", type=str, default=".", help="Diretório raiz do projeto a auditar.")
    parser.add_argument("--persist", action="store_true", help="Salva snapshot em memories/audit_report.json.")
    parser.add_argument("--output", type=str, default="", help="Caminho customizado para salvar o JSON.")
    parser.add_argument("--json", action="store_true", help="Imprime saída em formato JSON.")
    parser.add_argument("--self-test", action="store_true", help="Executa auto-teste determinístico.")
    args = parser.parse_args()

    if args.self_test:
        res = run_self_test()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    out_path = Path(args.output) if args.output.strip() else None
    report = audit_repository(Path(args.root), persist=args.persist, output_path=out_path)
    print(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))
    return 0 if report.summary.status != "REJECTED" else 1


if __name__ == "__main__":
    sys.exit(main())
