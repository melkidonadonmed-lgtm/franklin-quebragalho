"""
sync_gemini_ecosystem.py
Sincroniza o ecossistema com separação estrita entre Escopo Global Enxuto (~12 skills core +
3 subagentes universais em `C:\\Users\\melki\\.gemini\\config`) e Escopo por Projeto
(`.agents/skills.json` e `.agents/agents/` em cada repositório de `C:\\Users\\melki\\dev\\repos`).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

GEMINI_ROOT = Path(r"C:\Users\melki\.gemini")
REPOS_ROOT = ROOT_DIR.parent
CONFIG_PLUGIN_ROOT = GEMINI_ROOT / "config" / "plugins" / "franklin-skills"
CONFIG_SKILLS_ROOT = GEMINI_ROOT / "config" / "skills"

GLOBAL_CORE_FRANKLIN_SKILLS: tuple[str, ...] = (
    "auditoria-projetos-sistema",
    "audit-skills-antigravity",
    "code-acceptability-auditor",
    "test-quality-auditor",
    "gap-analyzer-auditor",
    "organizador-projetos-ideias",
)

GLOBAL_CORE_USER_SKILLS: tuple[str, ...] = (
    "adk-go-mcp-router",
    "agent-0meia",
    "agent-browser",
    "find-skills",
    "obsidian-vault",
    "reverse-engineer-anything",
    "review-squad",
)

GLOBAL_CORE_SUBAGENTS: tuple[str, ...] = (
    "adk-go-operator.md",
    "read-after-write-verifier.md",
    "vault-memory-retriever.md",
)

UI_SUBAGENTS: tuple[str, ...] = (
    "ui-shell-navigator.md",
    "ui-controls-data.md",
    "ui-motion-interaction.md",
    "ui-deterministic-observer.md",
)

GOV_SUBAGENTS: tuple[str, ...] = (
    "review-squad.md",
    "intent-hitl-mediator.md",
    "dev-workspace-publisher.md",
)


def _remove_dir_or_link(target: Path) -> None:
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


def _copy_tree(src: Path, dst: Path) -> int:
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


def _prepare_and_clean_dirs() -> None:
    """Cria diretórios exigidos e remove pastas legadas redundantes ou backups órfãos."""
    required_gemini_dirs = (
        GEMINI_ROOT / "lib",
        GEMINI_ROOT / "doc",
        GEMINI_ROOT / "agents",
        GEMINI_ROOT / "config" / "agents",
        GEMINI_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "skills",
        CONFIG_PLUGIN_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "lib",
        CONFIG_PLUGIN_ROOT / "doc",
        CONFIG_PLUGIN_ROOT / "assets",
        ROOT_DIR / ".well-known",
    )
    for d in required_gemini_dirs:
        d.mkdir(parents=True, exist_ok=True)

    for legacy_dir in (
        GEMINI_ROOT / "plugins",
        GEMINI_ROOT / "skills",
        GEMINI_ROOT / "docs",
        GEMINI_ROOT / "extensions",
        GEMINI_ROOT / "staging",
        CONFIG_PLUGIN_ROOT / "agents",
        CONFIG_PLUGIN_ROOT / "hooks",
        ROOT_DIR / ".agents" / "skills",
        ROOT_DIR / ".sessions" / "temp_plans",
    ):
        if legacy_dir.exists():
            shutil.rmtree(legacy_dir)

    stale_patterns = (
        list(GEMINI_ROOT.glob("*.bak*"))
        + list(GEMINI_ROOT.glob("*.rea.backup*"))
        + list((GEMINI_ROOT / "config").glob("*.bak*"))
        + list((GEMINI_ROOT / "config").glob("*.rea.backup*"))
        + (list(CONFIG_SKILLS_ROOT.rglob("*.rea.backup*")) if CONFIG_SKILLS_ROOT.exists() else [])
    )
    adk_bin = REPOS_ROOT / "adk-tests" / "bin"
    if adk_bin.exists():
        stale_patterns.extend(list(adk_bin.glob("*.exe.old")))
        stale_patterns.extend(list(adk_bin.glob("*.old.exe")))
        stale_patterns.extend(list(adk_bin.glob("*.exe~")))
    for stale_bak in stale_patterns:
        if stale_bak.is_file():
            try:
                stale_bak.unlink(missing_ok=True)
            except OSError as exc:
                _ignored_err = str(exc)


def _sync_global_core_plugin_skills(skills_src: Path, plugin_skills_dst: Path) -> int:
    """Sincroniza apenas as 6 skills core universais para o plugin global franklin-skills."""
    if not skills_src.exists():
        return 0
    plugin_skills_dst.mkdir(parents=True, exist_ok=True)
    allowed = set(GLOBAL_CORE_FRANKLIN_SKILLS)
    for existing_dir in list(plugin_skills_dst.iterdir()):
        if existing_dir.is_dir() and existing_dir.name not in allowed:
            shutil.rmtree(existing_dir)
    copied_files = 0
    for skill_name in GLOBAL_CORE_FRANKLIN_SKILLS:
        src_dir = skills_src / skill_name
        if src_dir.is_dir():
            copied_files += _copy_tree(src_dir, plugin_skills_dst / skill_name)
    return copied_files


def _sync_global_skills_json() -> None:
    """Garante que ~/.gemini/config/skills.json carregue apenas as 7 skills core globais."""
    global_skills_json = GEMINI_ROOT / "config" / "skills.json"
    payload = {
        "entries": [
            {
                "path": "C:/Users/melki/.agents/skills",
                "include_only": list(GLOBAL_CORE_USER_SKILLS),
            }
        ]
    }
    global_skills_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sync_and_deduplicate_skills() -> tuple[int, int, int]:
    """Sincroniza skills core para o plugin global e remove duplicatas em .gemini/config/skills."""
    skills_src = ROOT_DIR / "skills"
    plugin_skills_dst = CONFIG_PLUGIN_ROOT / "skills"
    skills_plugin_count = _sync_global_core_plugin_skills(skills_src, plugin_skills_dst)
    _sync_global_skills_json()
    deduplicated = _deduplicate_config_skills(skills_src)
    synced_agents_skills = _sync_user_agents_root()
    return skills_plugin_count, deduplicated, synced_agents_skills


def _deduplicate_config_skills(skills_src: Path) -> int:
    """Remove de .gemini/config/skills qualquer skill que já exista no catálogo canônico, em plugins ou em .agents/skills."""
    if not CONFIG_SKILLS_ROOT.exists() or not skills_src.exists():
        return 0
    canonical_names = {p.name for p in skills_src.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    plugins_dir = GEMINI_ROOT / "config" / "plugins"
    if plugins_dir.exists():
        canonical_names.update(p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md"))
    user_agents_skills = Path(r"C:\Users\melki\.agents\skills")
    if user_agents_skills.exists():
        canonical_names.update(p.name for p in user_agents_skills.iterdir() if p.is_dir() and (p / "SKILL.md").exists())

    deduplicated = 0
    for name in canonical_names:
        dup_dir = CONFIG_SKILLS_ROOT / name
        if dup_dir.exists() or dup_dir.is_symlink():
            _remove_dir_or_link(dup_dir)
            deduplicated += 1
    return deduplicated


def _clean_redundant_skill_links(user_agents_skills: Path) -> None:
    """Remove junctions/symlinks redundantes em antigravity-cli/skills e antigravity/skills."""
    for redundant_skills_dir in (
        GEMINI_ROOT / "antigravity-cli" / "skills",
        GEMINI_ROOT / "antigravity" / "skills",
    ):
        if not redundant_skills_dir.exists():
            continue
        for entry in list(redundant_skills_dir.iterdir()):
            is_link = entry.is_symlink() or (hasattr(entry, "is_junction") and entry.is_junction())
            if is_link or (user_agents_skills / entry.name).exists():
                _remove_dir_or_link(entry)


def _sync_user_agents_root() -> int:
    """Mantém .agents/skills higienizado sem duplicar cópias em .gemini/config/skills."""
    user_agents_root = Path(r"C:\Users\melki\.agents")
    user_agents_skills = user_agents_root / "skills"
    canonical_franklin = {p.name for p in (ROOT_DIR / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").exists()}

    synced_agents_skills = 0
    if user_agents_skills.exists():
        plugins_dir = GEMINI_ROOT / "config" / "plugins"
        plugin_names = {p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md")} if plugins_dir.exists() else set()
        plugin_names.update(canonical_franklin)
        for s_dir in [d for d in user_agents_skills.iterdir() if d.is_dir()]:
            if s_dir.name in plugin_names:
                _remove_dir_or_link(s_dir)
            elif (s_dir / "SKILL.md").exists():
                synced_agents_skills += 1

    _clean_redundant_skill_links(user_agents_skills)
    mem_proto_dst = user_agents_root / "rules" / "memory-protocol.md"
    if mem_proto_dst.exists():
        mem_proto_dst.unlink()
    return synced_agents_skills


CONTEXT_MIRRORS: tuple[tuple[str, Path], ...] = (
    ("CONTEXT.md", Path(".context") / "context.md"),
    ("SPEC.md", Path(".context") / "spec.md"),
)


def _mirror_context_to_root(repo_dir: Path) -> list[str]:
    """[LOCK-03] .context/ é a fonte; CONTEXT.md/SPEC.md da raiz são espelhos sobrescritos a cada sync.

    Sem .context/, a cópia da raiz semeia o destino (repositórios legados). Retorna os arquivos gravados.
    """
    written: list[str] = []
    for root_name, ctx_rel in CONTEXT_MIRRORS:
        root_f, ctx_f = repo_dir / root_name, repo_dir / ctx_rel
        if ctx_f.is_file():
            if not root_f.is_file() or root_f.read_bytes() != ctx_f.read_bytes():
                shutil.copy2(ctx_f, root_f)
                written.append(root_name)
        elif root_f.is_file():
            ctx_f.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root_f, ctx_f)
            written.append(ctx_rel.as_posix())
    return written


def _sync_local_triad_and_plugin_assets() -> None:
    """Sincroniza a Tríade de Governança v2.0 (.agents/ e .context/), rules/, SSOT global, hooks e assets do plugin."""
    ssot_rule = ROOT_DIR / "rules" / "diretrizes-qualidade-eficiencia.md"
    if ssot_rule.exists():
        raw_ssot = ssot_rule.read_text(encoding="utf-8")
        lines = raw_ssot.splitlines()
        body_ssot = raw_ssot
        if lines and lines[0].strip() == "---":
            end_fm = next((i for i in range(1, min(15, len(lines))) if lines[i].strip() == "---"), 0)
            if end_fm > 0:
                body_ssot = "\n".join(lines[end_fm + 1 :]).lstrip() + "\n"
        for global_agents_md in (
            Path(r"C:\Users\melki\AGENTS.md"),
            Path(r"C:\Users\melki\.agents\AGENTS.md"),
        ):
            global_agents_md.parent.mkdir(parents=True, exist_ok=True)
            global_agents_md.write_text(body_ssot, encoding="utf-8")

    for repo_dir in REPOS_ROOT.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        src_f = repo_dir / "AGENTS.md"
        dst_f = repo_dir / ".agents" / "AGENTS.md"
        if src_f.exists() and (not dst_f.exists() or repo_dir.name in ("franklin-quebragalho", "adk-tests")):
            dst_f.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_f, dst_f)
        _mirror_context_to_root(repo_dir)

    for src_dir, dst_dir in (
        (ROOT_DIR / "rules", GEMINI_ROOT / "config" / "rules"),
        (ROOT_DIR / "assets", CONFIG_PLUGIN_ROOT / "assets"),
    ):
        if src_dir.exists():
            _copy_tree(src_dir, dst_dir)

    for src_file, dst_file in (
        (ROOT_DIR / "hooks" / "hooks.json", CONFIG_PLUGIN_ROOT / "hooks.json"),
        (ROOT_DIR / "plugin.json", CONFIG_PLUGIN_ROOT / "plugin.json"),
    ):
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
    (CONFIG_PLUGIN_ROOT / "mcp_config.json").write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")


def _sync_docs_and_agent_card() -> int:
    """Sincroniza documentação Markdown, rules/, regenera o AgentCard assinado e atualiza audit_report.json."""
    doc_files = (
        ROOT_DIR / "AGENTS.md",
        ROOT_DIR / "MY_AGENTS.md",
        ROOT_DIR / "MY_SKILLS.md",
        ROOT_DIR / "README.md",
        ROOT_DIR / "SPEC.md",
        ROOT_DIR / "CONTEXT.md",
        ROOT_DIR / "CURRENT_STATE.md",
        ROOT_DIR / "skills" / "auditoria-projetos-sistema" / "references" / "taxonomia_subagentes_ui_6_camadas.md",
    )
    allowed_doc_names = {df.name for df in doc_files} | {"agent_card.json"}
    for doc_dir in (GEMINI_ROOT / "doc", CONFIG_PLUGIN_ROOT / "doc"):
        if doc_dir.exists():
            for existing_doc in list(doc_dir.iterdir()):
                if existing_doc.is_file() and existing_doc.name not in allowed_doc_names:
                    existing_doc.unlink(missing_ok=True)

    doc_copied = 0
    for df in doc_files:
        if df.exists():
            shutil.copy2(df, GEMINI_ROOT / "doc" / df.name)
            shutil.copy2(df, CONFIG_PLUGIN_ROOT / "doc" / df.name)
            doc_copied += 1

    _sync_local_triad_and_plugin_assets()

    from shared.a2a_bridge import build_franklin_agent_card

    card = build_franklin_agent_card(skills_dir=ROOT_DIR / "skills", sign=True)
    card_json = json.dumps(card, indent=2, ensure_ascii=False) + "\n"
    for target_card in (
        ROOT_DIR / "agent_card.json",
        ROOT_DIR / ".well-known" / "agent-card.json",
        GEMINI_ROOT / "doc" / "agent_card.json",
        CONFIG_PLUGIN_ROOT / "doc" / "agent_card.json",
    ):
        target_card.parent.mkdir(parents=True, exist_ok=True)
        target_card.write_text(card_json, encoding="utf-8")

    auditor_script_dir = ROOT_DIR / "skills" / "agent-server-auditor" / "scripts"
    if auditor_script_dir.exists():
        if str(auditor_script_dir) not in sys.path:
            sys.path.insert(0, str(auditor_script_dir))
        from agent_server_auditor import audit_repository

        audit_repository(ROOT_DIR, persist=True)
    return doc_copied


def _format_antigravity_agent_markdown(item: Path) -> str:
    """Converte um arquivo declarativo de subagente para o frontmatter YAML oficial do Antigravity."""
    from shared.agent_spec_loader import _extract_yaml_and_body, load_agent_spec

    raw = item.read_text(encoding="utf-8")
    _, body = _extract_yaml_and_body(raw)
    spec = load_agent_spec(str(item), verbose=False)
    desc_escaped = json.dumps(spec["description"], ensure_ascii=False)
    tools_list = spec.get("tools") or ["read_file", "call_mcp_tool"]
    tools_yaml = "\n".join(f"  - {t}" for t in tools_list)
    return (
        f"---\n"
        f"name: {spec['name']}\n"
        f"description: {desc_escaped}\n"
        f"subagent: true\n"
        f"mainAgent: false\n"
        f"commandExecutionPolicy: {spec.get('commandExecutionPolicy', 'auto')}\n"
        f"tools:\n"
        f"{tools_yaml}\n"
        f"---\n\n"
        f"{body}\n"
    )


def _sync_gemini_cli_agents(src: Path, dst: Path) -> int:
    """Sincroniza todos os 10 subagentes para ~/.gemini/agents (referência e Gemini CLI)."""
    if not src.exists():
        return 0
    from shared.agent_spec_loader import _extract_yaml_and_body, load_agent_spec

    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.glob("*.md"):
        raw = item.read_text(encoding="utf-8")
        _, body = _extract_yaml_and_body(raw)
        spec = load_agent_spec(str(item), verbose=False)
        desc_escaped = json.dumps(spec["description"], ensure_ascii=False)
        cli_md = f"---\nname: {spec['name']}\ndescription: {desc_escaped}\ntools:\n  - \"*\"\n---\n\n{body}\n"
        (dst / item.name).write_text(cli_md, encoding="utf-8")
        count += 1
    return count


def _sync_antigravity_config_agents(src: Path, dst: Path, allowed_files: tuple[str, ...] = GLOBAL_CORE_SUBAGENTS) -> int:
    """Sincroniza apenas os subagentes autorizados para o diretório de destino do Antigravity."""
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    allowed_set = set(allowed_files)
    for existing in list(dst.glob("*.md")):
        if existing.name not in allowed_set:
            existing.unlink(missing_ok=True)

    count = 0
    for filename in sorted(allowed_set):
        item = src / filename
        if item.is_file():
            (dst / item.name).write_text(_format_antigravity_agent_markdown(item), encoding="utf-8")
            count += 1
    return count


def _build_project_customization_profiles() -> dict[str, dict[str, Any]]:
    """Retorna o mapa de skills e subagentes específicos de cada repositório em dev/repos."""
    ui_f = ["design-md", "frontend-code-architect", "frontend-testing-auditor", "frontend-ui-ux-auditor", "plan-uiux", "complex-zero"]
    ui_u = ["vercel-react-best-practices", "web-design-guidelines", "ai-sdk", "live-api-function-auditor"]
    mcp_f = ["agent-server-auditor", "audit-skills-antigravity", "high-level-context-planner", "skill-orquestrador-planos-encadeados", "refine-prompt", "context-sentinel"]
    mcp_u = ["api-auditor", "build-mcp-server", "build-mcp-app", "build-mcpb", "mcp-use-app-builder", "live-api-function-auditor"]
    adk_local_skills = ["backend-architecture-skill", "backfront-stress", "code-quality-validation", "context-architecture-skill", "estante", "gatekeeper-eval", "temperea", "weather-skill"]
    ui_profile = {"franklin_skills": ui_f, "user_skills": ui_u, "subagents": UI_SUBAGENTS}
    mcp_profile = {"franklin_skills": mcp_f, "user_skills": mcp_u, "subagents": GOV_SUBAGENTS}
    all_franklin = sorted(p.name for p in (ROOT_DIR / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").exists())

    profiles: dict[str, dict[str, Any]] = {
        name: dict(ui_profile) for name in ("frontcraft-studio", "scoreboard", "mytts", "astral-pet-assist", "android-auto-first-app", "skills-web")
    }
    for name in ("mcp-web-agents", "webmcp", "google-auth-mcp", "caveman-agent", "epic-volta"):
        profiles[name] = dict(mcp_profile)

    profiles.update({
        "GoSTylo": {
            "franklin_skills": [*ui_f, *mcp_f],
            "user_skills": [*ui_u, *mcp_u, "developing-genkit-go"],
            "subagents": (*UI_SUBAGENTS, *GOV_SUBAGENTS),
        },
        "PCM": {
            "franklin_skills": ["design-interface-medica-minimalista", "conversor-html-pdf", "redator-tecnico-markdown", *ui_f],
            "user_skills": ["clinical-change-safety", "ui-pdf-validation", *ui_u],
            "plugin_skills": [("firebase", ["firebase_firestore", "firebase_auth_basics", "firebase_hosting_basics", "firestore_rules_creation", "firebase_security_rules_auditor"])],
            "subagents": (*UI_SUBAGENTS, "review-squad.md"),
        },
        "appmy": {
            "franklin_skills": ["android-agy-projects", "re-a-ndroid", "design-md", "plan-uiux", "code-quality-audit-3d-physics"],
            "user_skills": [
                "agp-9-upgrade", "android-cli", "android-intent-security", "android-permissions-security", "android-profiler",
                "android-ui-audit", "anr-audit-and-fix", "appfunctions", "camerax", "edge-to-edge", "glance-appwidget-updates-and-memory",
                "glance-canonical-layouts", "jetpack-compose-performance", "litert-lm", "litert-runtime", "ml-kit-genai-prompt-api",
                "mlkit-agent-api", "navigation-3", "navigation-event", "play-billing-library-version-upgrade", "play-policy-insights",
                "r8-analyzer", "restore-credentials", "testing-setup", "verified-email",
            ],
            "plugin_skills": [("android-cli-plugin", ["compose-preview", "device-hub"])],
            "subagents": (*UI_SUBAGENTS, "review-squad.md"),
        },
        "adk-tests": {
            "franklin_skills": [*mcp_f, "design-md", "frontend-code-architect", "frontend-testing-auditor", "frontend-ui-ux-auditor"],
            "user_skills": [*mcp_u, "google-agents-cli-adk-code", "google-agents-cli-deploy", "google-agents-cli-eval", "google-agents-cli-observability", "google-agents-cli-publish", "google-agents-cli-scaffold", "google-agents-cli-workflow"],
            "plugin_skills": [("data-agent-kit-plugin", ["bigquery-ai-ml", "bigquery-observability", "bigquery-optimization", "bigquery-troubleshooting", "building-data-apps", "enforcing-resource-attribution"])],
            "local_skills": [("go_agent/skills", adk_local_skills)],
            "subagents": (*UI_SUBAGENTS, *GOV_SUBAGENTS, *GLOBAL_CORE_SUBAGENTS),
        },
        "franklin-quebragalho": {
            "franklin_skills": all_franklin,
            "user_skills": ["agent-skill-evaluator", "skill-repair", "build-mcp-server", "api-auditor", "live-api-function-auditor"],
            "local_skills": [("../adk-tests/go_agent/skills", adk_local_skills)],
            "subagents": (*UI_SUBAGENTS, *GOV_SUBAGENTS),
        },
        "workspace-mcp": {"franklin_skills": [*mcp_f, "gdrive-auditoria-limpeza", "gdrive-taxonomia-organizacao"], "user_skills": mcp_u, "subagents": GOV_SUBAGENTS},
        "genkit-app": {"franklin_skills": mcp_f, "user_skills": [*mcp_u, "developing-genkit-js", "developing-genkit-go", "developing-genkit-python"], "subagents": GOV_SUBAGENTS},
    })
    return profiles


def _sync_project_scoped_customizations(agents_src: Path) -> int:
    """Gera .agents/skills.json e .agents/agents/*.md sob medida dentro de cada repositório de dev/repos."""
    profiles = _build_project_customization_profiles()
    franklin_skills_path = (ROOT_DIR / "skills").as_posix()
    user_skills_path = Path(r"C:\Users\melki\.agents\skills").as_posix()
    plugins_base = (GEMINI_ROOT / "config" / "plugins").as_posix()
    configured_repos = 0

    for repo_name, profile in profiles.items():
        repo_dir = REPOS_ROOT / repo_name
        if not repo_dir.is_dir():
            continue
        dot_agents = repo_dir / ".agents"
        dot_agents.mkdir(parents=True, exist_ok=True)
        entries: list[dict[str, Any]] = []
        if profile.get("franklin_skills"):
            entries.append({"path": franklin_skills_path, "include_only": profile["franklin_skills"]})
        if profile.get("user_skills"):
            entries.append({"path": user_skills_path, "include_only": profile["user_skills"]})
        for plugin_name, p_skills in profile.get("plugin_skills", []):
            entries.append({"path": f"{plugins_base}/{plugin_name}/skills", "include_only": p_skills})
        for rel_dir, l_skills in profile.get("local_skills", []):
            entries.append({"path": (repo_dir / rel_dir).resolve().as_posix(), "include_only": l_skills})

        (dot_agents / "skills.json").write_text(
            json.dumps({"entries": entries}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        subagents_tuple = tuple(profile.get("subagents", ()))
        if subagents_tuple:
            _sync_antigravity_config_agents(agents_src, dot_agents / "agents", allowed_files=subagents_tuple)
        configured_repos += 1
    return configured_repos


def sync_ecosystem() -> dict[str, int | str | bool]:
    """Executa a sincronização completa com Global Enxuto e customizações isoladas por projeto."""
    _prepare_and_clean_dirs()
    skills_plugin_count, deduplicated_config_skills, synced_agents_skills = _sync_and_deduplicate_skills()

    agents_src = ROOT_DIR / "agents"
    agents_gemini_count = _sync_gemini_cli_agents(agents_src, GEMINI_ROOT / "agents")
    agents_config_count = _sync_antigravity_config_agents(
        agents_src, GEMINI_ROOT / "config" / "agents", allowed_files=GLOBAL_CORE_SUBAGENTS
    )
    project_repos_synced = _sync_project_scoped_customizations(agents_src)

    plans_src = ROOT_DIR / "plans"
    _copy_tree(plans_src, CONFIG_PLUGIN_ROOT / "plans")
    plans_gemini_count = _copy_tree(plans_src, GEMINI_ROOT / "plans")

    shared_src = ROOT_DIR / "shared"
    lib_gemini_count = _copy_tree(shared_src, GEMINI_ROOT / "lib" / "shared")
    _copy_tree(shared_src, CONFIG_PLUGIN_ROOT / "lib" / "shared")

    loader_src = ROOT_DIR / "shared" / "agent_spec_loader.py"
    if loader_src.exists():
        shutil.copy2(loader_src, GEMINI_ROOT / "lib" / "agent_spec_loader.py")
        shutil.copy2(loader_src, CONFIG_PLUGIN_ROOT / "lib" / "agent_spec_loader.py")

    doc_copied = _sync_docs_and_agent_card()
    return {
        "status": "SYNCHRONIZED",
        "global_core_franklin_skills": len(GLOBAL_CORE_FRANKLIN_SKILLS),
        "global_core_user_skills": len(GLOBAL_CORE_USER_SKILLS),
        "global_core_subagents": agents_config_count,
        "project_repos_scoped": project_repos_synced,
        "skills_synced_to_agents": synced_agents_skills,
        "skills_synced_to_plugin": skills_plugin_count,
        "deduplicated_config_skills": deduplicated_config_skills,
        "agents_synced": agents_gemini_count,
        "agents_config_synced": agents_config_count,
        "plans_synced": plans_gemini_count,
        "lib_files_synced": lib_gemini_count,
        "doc_files_synced": doc_copied,
        "agent_card_local_check": (agents_config_count == len(GLOBAL_CORE_SUBAGENTS)),
    }


if __name__ == "__main__":
    summary = sync_ecosystem()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
