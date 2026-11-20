"""
_sync_project_profiles.py
Per-repository customization profiles, Triad canonicalization, and filesystem copy helpers
extracted from scripts.sync_gemini_ecosystem to keep modules concise (<= 600 lines).
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any, Callable

CONTEXT_MIRRORS: tuple[tuple[str, Path], ...] = (
    ("CONTEXT.md", Path(".context") / "context.md"),
    ("SPEC.md", Path(".context") / "spec.md"),
)


def remove_dir_or_link(target: Path) -> None:
    """Remove diretório físico, symlink ou junction do Windows com segurança."""
    if not target.exists() and not target.is_symlink():
        return
    try:
        if target.is_symlink() or (hasattr(target, "is_junction") and target.is_junction()):
            os.rmdir(target)
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink(missing_ok=True)
    except OSError:
        try:
            target.unlink(missing_ok=True)
        except OSError:
            shutil.rmtree(target, ignore_errors=True)


def copy_tree(src: Path, dst: Path) -> int:
    """Copia recursivamente todos os arquivos de src para dst usando cópias físicas."""
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.rglob("*"):
        if "__pycache__" in item.parts:
            continue
        target = dst / item.relative_to(src)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(item, target)
                count += 1
            except PermissionError as exc:
                _locked_err = str(exc)
    return count


def list_skill_dir_names(base_dir: Path) -> set[str]:
    """Retorna os nomes de subpastas de skills válidas (contendo SKILL.md) em base_dir."""
    if not base_dir.exists():
        return set()
    return {p.name for p in base_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}


def mirror_context_to_root(repo_dir: Path) -> list[str]:
    """[LOCK-03] Maintain .context/context.md and .context/spec.md as canonical files without root mirrors."""
    written: list[str] = []
    if not repo_dir.is_dir():
        return written
    root_entries = [p for p in repo_dir.iterdir() if p.is_file()]
    for root_name, ctx_rel in CONTEXT_MIRRORS:
        ctx_f = repo_dir / ctx_rel
        matches = [p for p in root_entries if p.name.lower() == root_name.lower()]
        if not ctx_f.is_file() and matches:
            legacy_src = next((p for p in matches if p.name == root_name), matches[0])
            ctx_f.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(legacy_src, ctx_f)
            written.append(ctx_rel.as_posix())
        if ctx_f.is_file():
            for dup in matches:
                dup.unlink(missing_ok=True)
    return written


def build_base_ui_and_mcp_profiles(
    ui_u: list[str], mcp_f: list[str], mcp_u: list[str],
    ui_subagents: tuple[str, ...], gov_subagents: tuple[str, ...],
) -> dict[str, dict[str, Any]]:
    """Constrói os perfis base de UI, mobile e servidores MCP."""
    ui_profile = {"franklin_skills": [], "user_skills": ui_u, "subagents": ui_subagents}
    mcp_profile = {"franklin_skills": mcp_f, "user_skills": mcp_u, "subagents": gov_subagents}
    profiles: dict[str, dict[str, Any]] = {"frontcraft-studio": dict(ui_profile)}
    profiles["shredded-shape"] = {
        "franklin_skills": [],
        "user_skills": [],
        "plugin_skills": [
            ("modern-web-guidance-plugin", ["modern-web-guidance"]),
            ("chrome-devtools-plugin", ["chrome-devtools", "a11y-debugging", "debug-optimize-lcp", "memory-leak-debugging"]),
        ],
        "subagents": ui_subagents,
    }
    profiles["mytts"] = {
        "franklin_skills": [],
        "user_skills": ui_u,
        "local_skills": [(".agents/skills", ["gemini-tts-expressive-audio"])],
        "subagents": ui_subagents,
    }
    profiles["astral-pet-assist"] = {
        "franklin_skills": ["android-agy-projects", "code-quality-audit-3d-physics"],
        "user_skills": ui_u,
        "subagents": ui_subagents,
    }
    profiles["android-auto-first-app"] = {
        "franklin_skills": ["android-agy-projects", "re-a-ndroid"],
        "user_skills": [*ui_u, "android-for-cars-parked-apps"],
        "subagents": ui_subagents,
    }
    profiles["skills-web"] = {
        "franklin_skills": ["technical-markdown-writer", "refine-prompt", "flow-filetree-organizer"],
        "user_skills": ["agent-skill-evaluator", "skill-repair"],
        "subagents": gov_subagents,
    }
    for name in ("mcp-web-agents", "webmcp", "google-auth-mcp", "caveman-agent", "epic-volta"):
        profiles[name] = dict(mcp_profile)
    return profiles


def build_project_customization_profiles(
    root_dir: Path, ui_subagents: tuple[str, ...], gov_subagents: tuple[str, ...],
) -> dict[str, dict[str, Any]]:
    """Retorna o mapa de skills e subagentes específicos de cada repositório em dev/repos."""
    ui_u = ["vercel-react-best-practices", "web-design-guidelines", "ai-sdk", "live-api-function-auditor"]
    mcp_f = ["agent-server-auditor", "high-level-context-planner", "chained-plan-orchestrator", "refine-prompt", "context-sentinel"]
    mcp_u = ["api-auditor", "build-mcp-server", "build-mcp-app", "build-mcpb", "mcp-use-app-builder", "live-api-function-auditor"]
    adk_local_skills = ["backend-architecture-skill", "backfront-stress", "code-quality-validation", "context-architecture-skill", "estante", "gatekeeper-eval", "temperea"]
    all_franklin = sorted(list_skill_dir_names(root_dir / "skills"))
    profiles = build_base_ui_and_mcp_profiles(ui_u, mcp_f, mcp_u, ui_subagents, gov_subagents)
    profiles.update({
        "GoSTylo": {"franklin_skills": [*mcp_f], "user_skills": [*ui_u, *mcp_u, "developing-genkit-go"], "subagents": (*ui_subagents, *gov_subagents)},
        "PCM": {
            "franklin_skills": ["html-pdf-converter", "technical-markdown-writer"],
            "user_skills": ["clinical-change-safety", "ui-pdf-validation", *ui_u],
            "plugin_skills": [("firebase", ["firebase_firestore", "firebase_auth_basics", "firebase_hosting_basics", "firestore_rules_creation", "firebase_security_rules_auditor"])],
            "subagents": (*ui_subagents, "prescmed-clinical-reviewer.md"),
        },
        "appmy": {
            "franklin_skills": ["android-agy-projects", "re-a-ndroid", "code-quality-audit-3d-physics"],
            "user_skills": [
                "agp-9-upgrade", "android-cli", "android-intent-security", "android-permissions-security", "android-profiler", "android-ui-audit",
                "anr-audit-and-fix", "appfunctions", "camerax", "edge-to-edge", "glance-appwidget-updates-and-memory", "glance-canonical-layouts",
                "jetpack-compose-performance", "litert-lm", "litert-runtime", "ml-kit-genai-prompt-api", "mlkit-agent-api", "navigation-3",
                "navigation-event", "play-billing-library-version-upgrade", "play-policy-insights", "r8-analyzer", "restore-credentials", "testing-setup", "verified-email",
            ],
            "plugin_skills": [("android-cli-plugin", ["compose-preview", "device-hub"])],
            "subagents": (*ui_subagents,),
        },
        "adk-go-mcp": {
            "franklin_skills": [*mcp_f],
            "user_skills": [*mcp_u, "code-analysis-causal-review-team", "google-agents-cli-adk-code", "google-agents-cli-deploy", "google-agents-cli-eval", "google-agents-cli-observability", "google-agents-cli-publish", "google-agents-cli-scaffold", "google-agents-cli-workflow"],
            "plugin_skills": [("data-agent-kit-plugin", ["bigquery-ai-ml", "bigquery-observability", "bigquery-optimization", "bigquery-troubleshooting", "building-data-apps", "enforcing-resource-attribution"])],
            "local_skills": [("skills", adk_local_skills)],
            "subagents": (*ui_subagents, *gov_subagents),
        },
        "adk-py-agents": {
            "franklin_skills": [*mcp_f],
            "user_skills": [*mcp_u, "google-agents-cli-adk-code", "google-agents-cli-deploy", "google-agents-cli-eval", "google-agents-cli-observability", "google-agents-cli-workflow"],
            "plugin_skills": [("data-agent-kit-plugin", ["bigquery-ai-ml", "bigquery-observability", "building-data-apps", "enforcing-resource-attribution"])],
            "local_skills": [("skills", ["weather-skill"])],
            "subagents": (*gov_subagents,),
        },
        "adk-ts-agent": {
            "franklin_skills": mcp_f,
            "user_skills": [*mcp_u, "google-agents-cli-adk-code", "google-agents-cli-eval"],
            "local_skills": [("skills", ["weather-skill"])],
            "subagents": (*gov_subagents,),
        },
        "franklin-quebragalho": {
            "franklin_skills": all_franklin,
            "user_skills": ["agent-skill-evaluator", "skill-repair", "build-mcp-server", "api-auditor", "live-api-function-auditor", "code-analysis-causal-review-team"],
            "subagents": (*ui_subagents, *gov_subagents),
        },
        "workspace-mcp": {"franklin_skills": [*mcp_f, "gdrive-cleanup-auditor", "gdrive-taxonomy-organizer"], "user_skills": mcp_u, "subagents": gov_subagents},
        "genkit-app": {"franklin_skills": mcp_f, "user_skills": [*mcp_u, "developing-genkit-js", "developing-genkit-go", "developing-genkit-python"], "subagents": gov_subagents},
    })
    return profiles


def build_repo_skill_entries(
    repo_name: str, repo_dir: Path, profile: dict[str, Any],
    franklin_skills_path: str, user_skills_path: str, plugins_base: str,
    root_name: str, core_franklin: tuple[str, ...], core_user: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Monta a lista de entradas para .agents/skills.json de um repositório específico."""
    entries: list[dict[str, Any]] = []
    f_skills = [s for s in profile.get("franklin_skills", []) if s not in set(core_franklin)]
    u_skills = [s for s in profile.get("user_skills", []) if s not in set(core_user)]
    if f_skills:
        entries.append({"path": "skills" if repo_name == root_name else franklin_skills_path, "include_only": f_skills})
    if u_skills:
        entries.append({"path": user_skills_path, "include_only": u_skills})
    for plugin_name, p_skills in profile.get("plugin_skills", []):
        entries.append({"path": f"{plugins_base}/{plugin_name}/skills", "include_only": p_skills})
    for rel_dir, l_skills in profile.get("local_skills", []):
        entries.append({"path": (repo_dir / rel_dir).resolve().as_posix(), "include_only": l_skills})
    return entries


def sync_project_scoped_customizations(
    agents_src: Path | list[Path],
    *,
    root_dir: Path,
    repos_root: Path,
    gemini_root: Path,
    user_home: Path,
    ui_subagents: tuple[str, ...],
    gov_subagents: tuple[str, ...],
    core_franklin: tuple[str, ...],
    core_user: tuple[str, ...],
    sync_config_agents_fn: Callable[..., int],
) -> int:
    """Gera .agents/skills.json e .agents/agents/*.md sob medida sem duplicar skills core globais."""
    profiles = build_project_customization_profiles(root_dir, ui_subagents, gov_subagents)
    franklin_skills_path = (root_dir / "skills").as_posix()
    catalog_skills_dir = gemini_root / "skill-catalog" / "user-skills"
    has_catalog = catalog_skills_dir.exists() and any(catalog_skills_dir.iterdir())
    user_skills_path = catalog_skills_dir.as_posix() if has_catalog else (user_home / ".agents" / "skills").as_posix()
    plugins_base = (gemini_root / "config" / "plugins").as_posix()
    base_roots = [agents_src] if isinstance(agents_src, Path) else list(agents_src)
    configured_repos = 0

    for repo_name, profile in profiles.items():
        repo_dir = repos_root / repo_name
        if not repo_dir.is_dir():
            continue
        dot_agents = repo_dir / ".agents"
        dot_agents.mkdir(parents=True, exist_ok=True)
        entries = build_repo_skill_entries(
            repo_name, repo_dir, profile, franklin_skills_path, user_skills_path,
            plugins_base, root_dir.name, core_franklin, core_user,
        )
        (dot_agents / "skills.json").write_text(
            json.dumps({"entries": entries}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        subagents_tuple = tuple(profile.get("subagents", ()))
        if subagents_tuple:
            repo_agent_roots = [repo_dir / "agents", *base_roots] if (repo_dir / "agents").is_dir() else base_roots
            sync_config_agents_fn(repo_agent_roots, dot_agents / "agents", allowed_files=subagents_tuple)
        configured_repos += 1
    return configured_repos
