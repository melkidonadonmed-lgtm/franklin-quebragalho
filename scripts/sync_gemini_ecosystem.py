"""
sync_gemini_ecosystem.py
Sincroniza fisicamente (sem junctions/symlinks) as Skills, Subagentes de UI (Topologia 3+1),
Planos DAG, Biblioteca Compartilhada (lib) e Documentação (doc/docs/plugins) entre o
repositório canônico `franklin-quebragalho`, `.agents/` e `C:\\Users\\melki\\.gemini\\`.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

GEMINI_ROOT = Path(r"C:\Users\melki\.gemini")
CONFIG_PLUGIN_ROOT = GEMINI_ROOT / "config" / "plugins" / "franklin-skills"
CONFIG_SKILLS_ROOT = GEMINI_ROOT / "config" / "skills"


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
            shutil.copy2(item, target)
            count += 1
    return count


def _prepare_and_clean_dirs() -> None:
    """Cria diretórios exigidos e remove pastas legadas redundantes ou backups órfãos."""
    required_gemini_dirs = (
        GEMINI_ROOT / "lib",
        GEMINI_ROOT / "doc",
        GEMINI_ROOT / "docs",
        GEMINI_ROOT / "agents",
        GEMINI_ROOT / "config" / "agents",
        GEMINI_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "skills",
        CONFIG_PLUGIN_ROOT / "agents",
        CONFIG_PLUGIN_ROOT / "plans",
        CONFIG_PLUGIN_ROOT / "lib",
        CONFIG_PLUGIN_ROOT / "doc",
        CONFIG_PLUGIN_ROOT / "hooks",
        ROOT_DIR / ".well-known",
    )
    for d in required_gemini_dirs:
        d.mkdir(parents=True, exist_ok=True)

    for legacy_dir in (
        GEMINI_ROOT / "plugins",
        GEMINI_ROOT / "skills",
        ROOT_DIR / ".agents",
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
    adk_bin = ROOT_DIR.parent / "adk-tests" / "bin"
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


def _sync_and_deduplicate_skills() -> tuple[int, int, int]:
    """Sincroniza skills para o plugin global e remove duplicatas em .gemini/config/skills e .agents."""
    skills_src = ROOT_DIR / "skills"
    plugin_skills_dst = CONFIG_PLUGIN_ROOT / "skills"
    if plugin_skills_dst.exists() and skills_src.exists():
        valid_skill_dirs = {p.name for p in skills_src.iterdir() if p.is_dir()}
        for existing_dir in list(plugin_skills_dst.iterdir()):
            if existing_dir.is_dir() and existing_dir.name not in valid_skill_dirs:
                shutil.rmtree(existing_dir)
    skills_plugin_count = _copy_tree(skills_src, plugin_skills_dst)

    deduplicated = _deduplicate_config_skills(skills_src)
    synced_agents_skills = _sync_user_agents_root()
    return skills_plugin_count, deduplicated, synced_agents_skills


def _deduplicate_config_skills(skills_src: Path) -> int:
    """Remove de .gemini/config/skills qualquer skill que já exista no catálogo canônico ou em plugins."""
    if not CONFIG_SKILLS_ROOT.exists() or not skills_src.exists():
        return 0
    canonical_names = {p.name for p in skills_src.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    plugins_dir = GEMINI_ROOT / "config" / "plugins"
    if plugins_dir.exists():
        canonical_names.update(p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md"))

    deduplicated = 0
    for name in canonical_names:
        dup_dir = CONFIG_SKILLS_ROOT / name
        if dup_dir.is_dir():
            shutil.rmtree(dup_dir)
            deduplicated += 1
    return deduplicated


def _sync_user_agents_root() -> int:
    """Mantém .agents/skills sincronizado com dev/skills e espelha skills não-plugin em .gemini/config/skills."""
    user_agents_root = Path(r"C:\Users\melki\.agents")
    user_agents_skills = user_agents_root / "skills"
    dev_skills_root = ROOT_DIR.parent.parent / "skills"
    if dev_skills_root.exists():
        _copy_tree(dev_skills_root, user_agents_skills)

    synced_agents_skills = 0
    if user_agents_skills.exists():
        plugins_dir = GEMINI_ROOT / "config" / "plugins"
        plugin_names = {p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md")} if plugins_dir.exists() else set()
        for s_dir in [d for d in user_agents_skills.iterdir() if d.is_dir()]:
            if s_dir.name in plugin_names:
                shutil.rmtree(s_dir)
            elif (s_dir / "SKILL.md").exists():
                _copy_tree(s_dir, CONFIG_SKILLS_ROOT / s_dir.name)
                synced_agents_skills += 1

    cli_skills_dir = GEMINI_ROOT / "antigravity-cli" / "skills"
    if cli_skills_dir.exists():
        for entry in list(cli_skills_dir.iterdir()):
            if entry.is_symlink() and not entry.exists():
                entry.unlink(missing_ok=True)

    mem_proto_dst = user_agents_root / "rules" / "memory-protocol.md"
    if mem_proto_dst.exists():
        mem_proto_dst.unlink()
    return synced_agents_skills


def _sync_docs_and_agent_card() -> int:
    """Sincroniza documentação Markdown, regenera o AgentCard assinado e copia manifestos."""
    doc_files = (
        ROOT_DIR / "AGENTS.md",
        ROOT_DIR / "MY_AGENTS.md",
        ROOT_DIR / "MY_SKILLS.md",
        ROOT_DIR / "README.md",
        ROOT_DIR / "SPEC.md",
        ROOT_DIR / "CONTEXT.md",
        ROOT_DIR / "GEMINI.md",
        ROOT_DIR / "skills" / "nav-x-func" / "references" / "taxonomia_subagentes_ui_6_camadas.md",
    )
    doc_copied = 0
    for df in doc_files:
        if df.exists():
            shutil.copy2(df, GEMINI_ROOT / "doc" / df.name)
            shutil.copy2(df, GEMINI_ROOT / "docs" / df.name)
            shutil.copy2(df, CONFIG_PLUGIN_ROOT / "doc" / df.name)
            doc_copied += 1

    from shared.a2a_bridge import build_franklin_agent_card

    card = build_franklin_agent_card(skills_dir=ROOT_DIR / "skills", sign=True)
    card_json = json.dumps(card, indent=2, ensure_ascii=False) + "\n"
    for target_card in (
        ROOT_DIR / "agent_card.json",
        ROOT_DIR / ".well-known" / "agent-card.json",
        GEMINI_ROOT / "doc" / "agent_card.json",
        GEMINI_ROOT / "docs" / "agent_card.json",
        CONFIG_PLUGIN_ROOT / "doc" / "agent_card.json",
    ):
        target_card.parent.mkdir(parents=True, exist_ok=True)
        target_card.write_text(card_json, encoding="utf-8")

    hooks_src = ROOT_DIR / "hooks"
    if hooks_src.exists():
        _copy_tree(hooks_src, CONFIG_PLUGIN_ROOT / "hooks")

    plugin_manifest_src = ROOT_DIR / "plugin.json"
    if plugin_manifest_src.exists():
        shutil.copy2(plugin_manifest_src, CONFIG_PLUGIN_ROOT / "plugin.json")
    # Evita duplicar franklin-skills_franklin-skills no Antigravity (já registrado em ~/.gemini/config/mcp_config.json)
    (CONFIG_PLUGIN_ROOT / "mcp_config.json").write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")
    return doc_copied


def _sync_gemini_cli_agents(src: Path, dst: Path) -> int:
    """Sincroniza subagentes para ~/.gemini/agents adaptando o frontmatter ao schema estrito do Gemini CLI."""
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
        cli_md = (
            f"---\n"
            f"name: {spec['name']}\n"
            f"description: {desc_escaped}\n"
            f"tools:\n"
            f'  - "*"\n'
            f"---\n\n"
            f"{body}\n"
        )
        (dst / item.name).write_text(cli_md, encoding="utf-8")
        count += 1
    return count


def sync_ecosystem() -> dict[str, int | str | bool]:
    """Executa a sincronização completa, higieniza duplicatas e regenera o AgentCard assinado."""
    _prepare_and_clean_dirs()
    skills_plugin_count, deduplicated_config_skills, synced_agents_skills = _sync_and_deduplicate_skills()

    agents_src = ROOT_DIR / "agents"
    agents_plugin_count = _copy_tree(agents_src, CONFIG_PLUGIN_ROOT / "agents")
    agents_gemini_count = _sync_gemini_cli_agents(agents_src, GEMINI_ROOT / "agents")
    agents_config_count = _copy_tree(agents_src, GEMINI_ROOT / "config" / "agents")

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
        "skills_synced_to_agents": synced_agents_skills,
        "skills_synced_to_plugin": skills_plugin_count,
        "deduplicated_config_skills": deduplicated_config_skills,
        "agents_synced": agents_gemini_count,
        "agents_config_synced": agents_config_count,
        "plans_synced": plans_gemini_count,
        "lib_files_synced": lib_gemini_count,
        "doc_files_synced": doc_copied,
        "agent_card_local_check": (agents_gemini_count == agents_plugin_count),
    }


if __name__ == "__main__":
    summary = sync_ecosystem()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
