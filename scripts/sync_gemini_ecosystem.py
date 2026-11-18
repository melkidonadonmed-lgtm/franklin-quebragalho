"""
sync_gemini_ecosystem.py
Sincroniza o ecossistema com separação estrita entre Escopo Global Enxuto (~12 skills core +
3 subagentes universais em `C:\\Users\\melki\\.gemini\\config`) e Escopo por Projeto
(`.agents/skills.json` e `.agents/agents/` em cada repositório de `C:\\Users\\melki\\dev\\repos`).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts._sync_project_profiles import (  # noqa: E402
    CONTEXT_MIRRORS,
    build_base_ui_and_mcp_profiles,
    build_project_customization_profiles,
    build_repo_skill_entries,
    copy_tree as _copy_tree,
    list_skill_dir_names as _list_skill_dir_names,
    mirror_context_to_root as _mirror_context_to_root,
    remove_dir_or_link as _remove_dir_or_link,
    sync_project_scoped_customizations,
)

# Raiz do usuário; os testes redirecionam USER_HOME/GEMINI_ROOT/REPOS_ROOT para tmp_path.
USER_HOME = Path(r"C:\Users\melki")
GEMINI_ROOT = USER_HOME / ".gemini"
REPOS_ROOT = ROOT_DIR.parent
CONFIG_PLUGIN_ROOT = GEMINI_ROOT / "config" / "plugins" / "franklin-skills"
CONFIG_SKILLS_ROOT = GEMINI_ROOT / "config" / "skills"

GLOBAL_CORE_FRANKLIN_SKILLS: tuple[str, ...] = (
    "system-project-auditor", "code-acceptability-auditor",
    "test-quality-auditor", "gap-analyzer-auditor", "project-idea-organizer",
)
GLOBAL_CORE_USER_SKILLS: tuple[str, ...] = (
    "adk-go-mcp-router", "agent-0meia", "agent-browser", "find-skills",
    "obsidian-vault", "reverse-engineer-anything",
)
GLOBAL_CORE_SUBAGENTS: tuple[str, ...] = (
    "adk-go-operator.md", "read-after-write-verifier.md", "vault-memory-retriever.md",
)
UI_SUBAGENTS: tuple[str, ...] = (
    "ui-analyst.md", "ui-planner.md", "ui-worker.md", "ui-judge.md",
)
GOV_SUBAGENTS: tuple[str, ...] = (
    "intent-hitl-mediator.md", "dev-workspace-publisher.md",
)

GLOBAL_ONLY_RULES: tuple[str, ...] = ("quality-efficiency-guidelines.md",)


# Local filesystem helpers (_remove_dir_or_link, _copy_tree, _mirror_context_to_root) extracted to scripts/_sync_project_profiles.py


def _prepare_and_clean_dirs() -> None:
    """Cria diretórios exigidos e remove pastas legadas redundantes ou backups órfãos."""
    required_gemini_dirs = (
        GEMINI_ROOT / "lib",
        GEMINI_ROOT / "doc",
        GEMINI_ROOT / "agents",
        GEMINI_ROOT / "config" / "agents",
        GEMINI_ROOT / "config" / "rules",
        GEMINI_ROOT / "config" / "specs-cache",
        GEMINI_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "skills",
        CONFIG_PLUGIN_ROOT / "rules",
        CONFIG_PLUGIN_ROOT / "scripts",
        CONFIG_PLUGIN_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "lib",
        CONFIG_PLUGIN_ROOT / "doc",
        CONFIG_PLUGIN_ROOT / "assets",
        ROOT_DIR / ".well-known",
    )
    for d in required_gemini_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # ~/.gemini/skills e ~/.gemini/extensions NÃO são legados: o Gemini CLI instala skills e extensões
    # (ex.: wt-agent-hooks do Windows Terminal) ali. Apagá-los quebra o CLI e eles voltam na reinstalação.
    for legacy_dir in (
        GEMINI_ROOT / "plugins",
        GEMINI_ROOT / "docs",
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
    adk_bin = REPOS_ROOT / "adk-go-mcp" / "bin"
    if adk_bin.exists():
        stale_patterns.extend(list(adk_bin.glob("*.exe.old")))
        stale_patterns.extend(list(adk_bin.glob("*.old.exe")))
        stale_patterns.extend(list(adk_bin.glob("*.exe~")))
    for legacy_agent in ("review-squad.md",):
        (GEMINI_ROOT / "agents" / legacy_agent).unlink(missing_ok=True)
        (GEMINI_ROOT / "config" / "agents" / legacy_agent).unlink(missing_ok=True)
    for stale_bak in stale_patterns:
        if stale_bak.is_file():
            try:
                stale_bak.unlink(missing_ok=True)
            except OSError as exc:
                _ignored_err = str(exc)


def _sync_global_core_plugin_skills(skills_src: Path, plugin_skills_dst: Path) -> int:
    """Sincroniza apenas as 5 skills core universais para o plugin global franklin-skills."""
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
        dst_dir = plugin_skills_dst / skill_name
        if src_dir.is_dir():
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            copied_files += _copy_tree(src_dir, dst_dir)
    return copied_files


def _sync_global_skills_json() -> None:
    """Garante que ~/.gemini/config/skills.json carregue apenas as 7 skills core globais."""
    global_skills_json = GEMINI_ROOT / "config" / "skills.json"
    payload = {
        "entries": [
            {
                "path": (USER_HOME / ".agents" / "skills").as_posix(),
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
    canonical_names = _list_skill_dir_names(skills_src)
    canonical_names.update(_list_skill_dir_names(USER_HOME / ".agents" / "skills"))
    canonical_names.update(_list_skill_dir_names(GEMINI_ROOT / "skill-catalog" / "user-skills"))
    plugins_dir = GEMINI_ROOT / "config" / "plugins"
    if plugins_dir.exists():
        canonical_names.update(p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md"))

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


def _triage_single_user_agent_skill(
    s_dir: Path, plugin_names: set[str], core_user_set: set[str], catalog_user_skills: Path
) -> int:
    """Roteia uma pasta em .agents/skills (remove duplicata de plugin, mantém core ou move para o catálogo)."""
    if s_dir.name in plugin_names:
        _remove_dir_or_link(s_dir)
        return 0
    if not (s_dir / "SKILL.md").exists():
        return 0
    if s_dir.name in core_user_set:
        return 1
    dst_cat = catalog_user_skills / s_dir.name
    if dst_cat.exists():
        _remove_dir_or_link(dst_cat)
    _copy_tree(s_dir, dst_cat)
    _remove_dir_or_link(s_dir)
    return 1


def _sync_user_agents_root() -> int:
    """Mantém .agents/skills enxuto (apenas GLOBAL_CORE_USER_SKILLS) e move demais skills para skill-catalog/user-skills."""
    user_agents_root = USER_HOME / ".agents"
    user_agents_skills = user_agents_root / "skills"
    catalog_user_skills = GEMINI_ROOT / "skill-catalog" / "user-skills"
    catalog_user_skills.mkdir(parents=True, exist_ok=True)
    plugin_names = _list_skill_dir_names(ROOT_DIR / "skills")
    plugins_dir = GEMINI_ROOT / "config" / "plugins"
    if plugins_dir.exists():
        plugin_names.update(p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md"))
    core_user_set = set(GLOBAL_CORE_USER_SKILLS)

    synced_agents_skills = 0
    if user_agents_skills.exists():
        for s_dir in [d for d in user_agents_skills.iterdir() if d.is_dir()]:
            synced_agents_skills += _triage_single_user_agent_skill(s_dir, plugin_names, core_user_set, catalog_user_skills)

    _clean_redundant_skill_links(user_agents_skills)
    (user_agents_root / "rules" / "memory-protocol.md").unlink(missing_ok=True)
    return synced_agents_skills


def _eol_normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def _cleanup_ssot_home_duplicates() -> None:
    """Remove duplicatas SSOT em ~/AGENTS.md, ~/.agents/AGENTS.md e franklin/.agents/AGENTS.md."""
    ssot_markers = (
        "Kernel Operacional, Criação de Projetos e Governança",
        "Operational Kernel, Project Bootstrapping, and Governance",
    )
    for dup_agents in (USER_HOME / "AGENTS.md", USER_HOME / ".agents" / "AGENTS.md"):
        if dup_agents.is_file():
            content = dup_agents.read_text(encoding="utf-8", errors="ignore")
            if any(m in content for m in ssot_markers):
                dup_agents.unlink(missing_ok=True)
    repo_dup = ROOT_DIR / ".agents" / "AGENTS.md"
    if repo_dup.is_file() and (ROOT_DIR / "AGENTS.md").is_file():
        repo_dup.unlink(missing_ok=True)


def _prune_unlisted_md(folder: Path, allowed: set[str]) -> None:
    """Remove arquivos .md em folder cujo nome não esteja em allowed."""
    if not folder.exists():
        return
    for existing in list(folder.glob("*.md")):
        if existing.name not in allowed:
            existing.unlink(missing_ok=True)


def _sync_rules_and_plugin_bundle() -> None:
    """Distribui rules/ sem duplicação (always_on em config/rules, demais no plugin) e empacota scripts/manifest."""
    rules_src = ROOT_DIR / "rules"
    rules_dst = GEMINI_ROOT / "config" / "rules"
    plugin_rules_dst = CONFIG_PLUGIN_ROOT / "rules"
    if rules_src.exists():
        global_names = set(GLOBAL_ONLY_RULES)
        plugin_names = {p.name for p in rules_src.glob("*.md") if p.name not in global_names}
        _prune_unlisted_md(rules_dst, global_names)
        _prune_unlisted_md(plugin_rules_dst, plugin_names)
        for rule_file in rules_src.glob("*.md"):
            target_dir = rules_dst if rule_file.name in global_names else plugin_rules_dst
            shutil.copy2(rule_file, target_dir / rule_file.name)

    assets_src = ROOT_DIR / "assets"
    if assets_src.exists():
        _copy_tree(assets_src, CONFIG_PLUGIN_ROOT / "assets")

    for src_file, dst_file in (
        (ROOT_DIR / "hooks" / "hooks.json", CONFIG_PLUGIN_ROOT / "hooks.json"),
        (ROOT_DIR / "hooks" / "antigravity_harness_hook.py", CONFIG_PLUGIN_ROOT / "scripts" / "antigravity_harness_hook.py"),
        (ROOT_DIR / "plugin.json", CONFIG_PLUGIN_ROOT / "plugin.json"),
    ):
        if src_file.exists():
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)

    (CONFIG_PLUGIN_ROOT / "mcp_config.json").unlink(missing_ok=True)
    plugin_readme = (
        "# franklin-skills\n\n"
        f"Plugin enxuto gerado automaticamente por `sync_gemini_ecosystem.py`: {len(GLOBAL_CORE_FRANKLIN_SKILLS)} "
        "skills core universais (`skills/`), regras modulares (`rules/`), hook harness portátil (`hooks.json` + "
        "`scripts/antigravity_harness_hook.py`), planos DAG (`plans/`) e biblioteca compartilhada (`lib/`).\n"
    )
    (CONFIG_PLUGIN_ROOT / "README.md").write_text(plugin_readme, encoding="utf-8")


def _sync_local_triad_and_plugin_assets() -> None:
    """Sincroniza a Tríade de Governança v2.0 (.context/), rules/ sem duplicata, hooks e bundle do plugin."""
    _cleanup_ssot_home_duplicates()

    for repo_dir in REPOS_ROOT.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue
        root_agents = repo_dir / "AGENTS.md"
        nested_agents = repo_dir / ".agents" / "AGENTS.md"
        if root_agents.is_file() and nested_agents.is_file():
            nested_agents.unlink(missing_ok=True)
        _mirror_context_to_root(repo_dir)

    _sync_rules_and_plugin_bundle()


def _clean_doc_dir(doc_dir: Path, allowed_doc_names: set[str]) -> None:
    """Remove arquivos obsoletos de um diretório doc/ preservando apenas allowed_doc_names."""
    if not doc_dir.exists():
        return
    for existing_doc in list(doc_dir.iterdir()):
        if existing_doc.is_file() and existing_doc.name not in allowed_doc_names:
            existing_doc.unlink(missing_ok=True)
    for legacy_doc in ("SPEC.md", "CONTEXT.md"):
        (doc_dir / legacy_doc).unlink(missing_ok=True)


def _sync_docs_and_agent_card() -> int:
    """Sincroniza documentação Markdown, rules/, regenera o AgentCard assinado e atualiza audit_report.json."""
    doc_files = (
        ROOT_DIR / "AGENTS.md",
        ROOT_DIR / "MY_AGENTS.md",
        ROOT_DIR / "MY_SKILLS.md",
        ROOT_DIR / "README.md",
        ROOT_DIR / ".context" / "spec.md",
        ROOT_DIR / ".context" / "context.md",
        ROOT_DIR / "CURRENT_STATE.md",
        ROOT_DIR / "skills" / "system-project-auditor" / "references" / "ui_subagent_taxonomy_6_layers.md",
    )
    allowed_doc_names = {df.name for df in doc_files} | {"agent_card.json"}
    for doc_dir in (GEMINI_ROOT / "doc", CONFIG_PLUGIN_ROOT / "doc"):
        _clean_doc_dir(doc_dir, allowed_doc_names)
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
    tools_list = [t for t in (spec.get("tools") or []) if t not in ("*", "call_mcp_tool")]
    tools_block = "tools:\n" + "\n".join(f"  - {t}" for t in tools_list) + "\n" if tools_list else ""
    skills_list = spec.get("skills") or []
    skills_block = "skills:\n" + "\n".join(f"  - {s}" for s in skills_list) + "\n" if skills_list else ""
    raw_policy = str(spec.get("commandExecutionPolicy", "sandbox"))
    policy_yaml = '"off"' if raw_policy == "off" else raw_policy
    guardrails = spec.get("guardrails") or {}
    max_steps_val = spec.get("max_steps") or guardrails.get("max_steps", 10)
    stop_cond_val = spec.get("stop_condition") or guardrails.get("stop_condition", "TASK_STATE_COMPLETED")
    stop_escaped = json.dumps(str(stop_cond_val), ensure_ascii=False)
    return (
        f"---\nname: {spec['name']}\ndescription: {desc_escaped}\nsubagent: true\nmainAgent: false\n"
        f"model: {spec.get('model', 'inherit')}\n"
        f"commandExecutionPolicy: {policy_yaml}\n"
        f"inheritMcp: {str(bool(spec.get('inheritMcp', True))).lower()}\n"
        f"inheritCustomizations: {str(bool(spec.get('inheritCustomizations', True))).lower()}\n"
        f"max_steps: {int(max_steps_val)}\n"
        f"stop_condition: {stop_escaped}\n"
        f"{tools_block}{skills_block}---\n\n{body}\n"
    )


def _sync_gemini_cli_agents(src: Path, dst: Path) -> int:
    """Sincroniza todos os 10 subagentes para ~/.gemini/agents sem injetar wildcard tools: '*'."""
    if not src.exists():
        return 0

    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.glob("*.md"):
        (dst / item.name).write_text(_format_antigravity_agent_markdown(item), encoding="utf-8", newline="\n")
        count += 1
    return count


def _resolve_agent_sync_content(item: Path, dst: Path) -> str:
    """Valida o manifesto do subagente e preserva cópia LF literal quando sincronizado no próprio repositório."""
    formatted = _format_antigravity_agent_markdown(item)
    if dst.parent.name == ".agents" and item.parent.resolve() == (dst.parent.parent / "agents").resolve():
        return item.read_text(encoding="utf-8").replace("\r\n", "\n")
    return formatted


def _sync_antigravity_config_agents(
    src_dirs: Path | list[Path], dst: Path, allowed_files: tuple[str, ...] = GLOBAL_CORE_SUBAGENTS
) -> int:
    """Sincroniza apenas os subagentes autorizados a partir de um ou mais diretórios de origem."""
    roots = [src_dirs] if isinstance(src_dirs, Path) else list(src_dirs)
    if not any(r.exists() for r in roots):
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    allowed_set = set(allowed_files)
    _prune_unlisted_md(dst, allowed_set)
    count = 0
    for filename in sorted(allowed_set):
        for r in roots:
            item = r / filename
            if item.is_file():
                (dst / item.name).write_text(_resolve_agent_sync_content(item, dst), encoding="utf-8", newline="\n")
                count += 1
                break
    return count


def _sync_shredded_shape_plugin() -> tuple[int, int]:
    """Sincroniza o repositório separado shredded-shape para plugins/shredded-shape, agents/ e plans/."""
    shredded_dir = REPOS_ROOT / "shredded-shape"
    if not shredded_dir.is_dir():
        return 0, 0
    plugin_dst = GEMINI_ROOT / "config" / "plugins" / "shredded-shape"
    if plugin_dst.exists():
        shutil.rmtree(plugin_dst)
    copied = 0
    for sub in ("skills", "rules", "plans", "assets", "agents"):
        copied += _copy_tree(shredded_dir / sub, plugin_dst / sub)
    for fname in ("plugin.json", "README.md"):
        src_f = shredded_dir / fname
        if src_f.is_file():
            plugin_dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_f, plugin_dst / fname)
            copied += 1
    _copy_tree(shredded_dir / "plans", GEMINI_ROOT / "plans")
    (GEMINI_ROOT / "plans" / "ui_composition_dag.json").unlink(missing_ok=True)
    for legacy_agent in ("ui-shell-navigator.md", "ui-controls-data.md", "ui-motion-interaction.md", "ui-deterministic-observer.md"):
        (GEMINI_ROOT / "agents" / legacy_agent).unlink(missing_ok=True)
    agents_count = _sync_gemini_cli_agents(shredded_dir / "agents", GEMINI_ROOT / "agents")
    return copied, agents_count


def _build_base_ui_and_mcp_profiles(ui_u: list[str], mcp_f: list[str], mcp_u: list[str]) -> dict[str, dict[str, Any]]:
    """Constrói os perfis base de UI, mobile e servidores MCP."""
    return build_base_ui_and_mcp_profiles(ui_u, mcp_f, mcp_u, UI_SUBAGENTS, GOV_SUBAGENTS)


def _build_project_customization_profiles() -> dict[str, dict[str, Any]]:
    """Retorna o mapa de skills e subagentes específicos de cada repositório em dev/repos."""
    return build_project_customization_profiles(ROOT_DIR, UI_SUBAGENTS, GOV_SUBAGENTS)


def _build_repo_skill_entries(
    repo_name: str, repo_dir: Path, profile: dict[str, Any],
    franklin_skills_path: str, user_skills_path: str, plugins_base: str,
) -> list[dict[str, Any]]:
    """Monta a lista de entradas para .agents/skills.json de um repositório específico."""
    return build_repo_skill_entries(
        repo_name, repo_dir, profile, franklin_skills_path, user_skills_path, plugins_base,
        ROOT_DIR.name, GLOBAL_CORE_FRANKLIN_SKILLS, GLOBAL_CORE_USER_SKILLS,
    )


def _sync_project_scoped_customizations(agents_src: Path | list[Path]) -> int:
    """Gera .agents/skills.json e .agents/agents/*.md sob medida sem duplicar skills core globais."""
    return sync_project_scoped_customizations(
        agents_src,
        root_dir=ROOT_DIR,
        repos_root=REPOS_ROOT,
        gemini_root=GEMINI_ROOT,
        user_home=USER_HOME,
        ui_subagents=UI_SUBAGENTS,
        gov_subagents=GOV_SUBAGENTS,
        core_franklin=GLOBAL_CORE_FRANKLIN_SKILLS,
        core_user=GLOBAL_CORE_USER_SKILLS,
        sync_config_agents_fn=_sync_antigravity_config_agents,
    )


def sync_ecosystem() -> dict[str, int | str | bool]:
    """Executa a sincronização completa com Global Enxuto e customizações isoladas por projeto."""
    _prepare_and_clean_dirs()
    shredded_files_synced, shredded_agents_synced = _sync_shredded_shape_plugin()
    skills_plugin_count, deduplicated_config_skills, synced_agents_skills = _sync_and_deduplicate_skills()

    agents_src = ROOT_DIR / "agents"
    shredded_agents = REPOS_ROOT / "shredded-shape" / "agents"
    agent_sources = [agents_src, shredded_agents] if shredded_agents.is_dir() else [agents_src]
    agents_gemini_count = _sync_gemini_cli_agents(agents_src, GEMINI_ROOT / "agents") + shredded_agents_synced
    agents_config_count = _sync_antigravity_config_agents(
        agents_src, GEMINI_ROOT / "config" / "agents", allowed_files=GLOBAL_CORE_SUBAGENTS
    )
    project_repos_synced = _sync_project_scoped_customizations(agent_sources)

    plans_src = ROOT_DIR / "plans"
    _copy_tree(plans_src, CONFIG_PLUGIN_ROOT / "plans")
    plans_gemini_count = _copy_tree(plans_src, GEMINI_ROOT / "plans")

    shared_src = ROOT_DIR / "shared"
    lib_gemini_count = _copy_tree(shared_src, GEMINI_ROOT / "lib" / "shared")
    _copy_tree(shared_src, CONFIG_PLUGIN_ROOT / "lib" / "shared")

    for lib_root in (GEMINI_ROOT / "lib", CONFIG_PLUGIN_ROOT / "lib"):
        (lib_root / "agent_spec_loader.py").unlink(missing_ok=True)

    doc_copied = _sync_docs_and_agent_card()
    return {
        "status": "SYNCHRONIZED",
        "global_core_franklin_skills": len(GLOBAL_CORE_FRANKLIN_SKILLS),
        "global_core_user_skills": len(GLOBAL_CORE_USER_SKILLS),
        "global_core_subagents": agents_config_count,
        "shredded_shape_plugin_files": shredded_files_synced,
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


__all__ = [
    "CONTEXT_MIRRORS",
    "GLOBAL_CORE_FRANKLIN_SKILLS",
    "GLOBAL_CORE_SUBAGENTS",
    "GLOBAL_CORE_USER_SKILLS",
    "GLOBAL_ONLY_RULES",
    "GOV_SUBAGENTS",
    "UI_SUBAGENTS",
    "_build_base_ui_and_mcp_profiles",
    "_build_project_customization_profiles",
    "_build_repo_skill_entries",
    "_copy_tree",
    "_format_antigravity_agent_markdown",
    "_list_skill_dir_names",
    "_mirror_context_to_root",
    "_remove_dir_or_link",
    "_sync_antigravity_config_agents",
    "_sync_project_scoped_customizations",
    "sync_ecosystem",
]


if __name__ == "__main__":
    summary = sync_ecosystem()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
