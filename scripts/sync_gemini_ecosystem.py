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
    )
    for d in required_gemini_dirs:
        d.mkdir(parents=True, exist_ok=True)

    for legacy_dir in (GEMINI_ROOT / "plugins", GEMINI_ROOT / "skills", ROOT_DIR / ".agents" / "skills"):
        if legacy_dir.exists():
            shutil.rmtree(legacy_dir)
    for stale_bak in list(GEMINI_ROOT.glob("*.bak")) + list(GEMINI_ROOT.glob("*.rea.backup*")):
        if stale_bak.is_file():
            stale_bak.unlink()


def _sync_and_deduplicate_skills() -> tuple[int, int]:
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
    _sync_user_agents_root()
    return skills_plugin_count, deduplicated


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


def _sync_user_agents_root() -> None:
    """Mantém C:\\Users\\melki\\.agents\\ sincronizado sem duplicatas de plugins."""
    user_agents_root = Path(r"C:\Users\melki\.agents")
    user_agents_skills = user_agents_root / "skills"
    if user_agents_skills.exists():
        plugins_dir = GEMINI_ROOT / "config" / "plugins"
        plugin_names = {p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md")} if plugins_dir.exists() else set()
        migrated_or_dup = plugin_names | {"microsoft-foundry", "reverse-engineer-anything"}
        for s_dir in [d for d in user_agents_skills.iterdir() if d.is_dir()]:
            if s_dir.name in migrated_or_dup:
                shutil.rmtree(s_dir)
            elif (CONFIG_SKILLS_ROOT / s_dir.name).exists():
                _copy_tree(CONFIG_SKILLS_ROOT / s_dir.name, s_dir)

    mem_proto_src = GEMINI_ROOT / "config" / "plugins" / "mempalace" / "rules" / "memory-protocol.md"
    mem_proto_dst = user_agents_root / "rules" / "memory-protocol.md"
    if mem_proto_src.exists() and mem_proto_dst.parent.exists():
        shutil.copy2(mem_proto_src, mem_proto_dst)


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
        ROOT_DIR / "skills" / "arquitetura-design-implementacao-sistema" / "references" / "taxonomia_subagentes_ui_6_camadas.md",
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
        GEMINI_ROOT / "doc" / "agent_card.json",
        GEMINI_ROOT / "docs" / "agent_card.json",
        CONFIG_PLUGIN_ROOT / "doc" / "agent_card.json",
    ):
        target_card.write_text(card_json, encoding="utf-8")

    for manifest_name in ("plugin.json", "mcp_config.json"):
        manifest_src = ROOT_DIR / manifest_name
        if manifest_src.exists():
            shutil.copy2(manifest_src, CONFIG_PLUGIN_ROOT / manifest_name)
    return doc_copied


def sync_ecosystem() -> dict[str, int | str | bool]:
    """Executa a sincronização completa, higieniza duplicatas e regenera o AgentCard assinado."""
    _prepare_and_clean_dirs()
    skills_plugin_count, deduplicated_config_skills = _sync_and_deduplicate_skills()

    agents_src = ROOT_DIR / "agents"
    agents_local_count = _copy_tree(agents_src, ROOT_DIR / ".agents" / "agents")
    agents_plugin_count = _copy_tree(agents_src, CONFIG_PLUGIN_ROOT / "agents")
    agents_gemini_count = _copy_tree(agents_src, GEMINI_ROOT / "agents")
    agents_config_count = _copy_tree(agents_src, GEMINI_ROOT / "config" / "agents")

    plans_src = ROOT_DIR / "plans"
    _copy_tree(plans_src, CONFIG_PLUGIN_ROOT / "plans")
    plans_gemini_count = _copy_tree(plans_src, GEMINI_ROOT / "plans")

    shared_src = ROOT_DIR / "shared"
    lib_gemini_count = _copy_tree(shared_src, GEMINI_ROOT / "lib" / "shared")
    _copy_tree(shared_src, CONFIG_PLUGIN_ROOT / "lib" / "shared")

    loader_src = ROOT_DIR / "skills" / "aprimoramento-expansibilidade-agentes-skills" / "scripts" / "agent_spec_loader.py"
    if loader_src.exists():
        shutil.copy2(loader_src, GEMINI_ROOT / "lib" / "agent_spec_loader.py")
        shutil.copy2(loader_src, CONFIG_PLUGIN_ROOT / "lib" / "agent_spec_loader.py")

    doc_copied = _sync_docs_and_agent_card()
    return {
        "status": "SYNCHRONIZED",
        "skills_synced_to_agents": 0,
        "skills_synced_to_plugin": skills_plugin_count,
        "deduplicated_config_skills": deduplicated_config_skills,
        "agents_synced": agents_gemini_count,
        "agents_config_synced": agents_config_count,
        "plans_synced": plans_gemini_count,
        "lib_files_synced": lib_gemini_count,
        "doc_files_synced": doc_copied,
        "agent_card_local_check": (agents_local_count == agents_plugin_count),
    }


if __name__ == "__main__":
    summary = sync_ecosystem()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
