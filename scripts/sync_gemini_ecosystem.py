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
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1
    return count


def sync_ecosystem() -> dict[str, int | str]:
    """Executa a sincronização completa, higieniza duplicatas e regenera o AgentCard assinado."""
    # 1. Criar diretórios solicitados em C:\Users\melki\.gemini e no plugin franklin-skills
    required_gemini_dirs = [
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
    ]
    for d in required_gemini_dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Remover pastas legadas redundantes caso existam (.gemini/plugins, .gemini/skills e .agents/skills local)
    for legacy_dir in (GEMINI_ROOT / "plugins", GEMINI_ROOT / "skills", ROOT_DIR / ".agents" / "skills"):
        if legacy_dir.exists():
            shutil.rmtree(legacy_dir)

    # 2. Sincronizar Skills: skills/ -> config/plugins/franklin-skills/skills/
    skills_src = ROOT_DIR / "skills"
    skills_agents_count = 0
    skills_plugin_count = _copy_tree(skills_src, CONFIG_PLUGIN_ROOT / "skills")

    # 2.1 Remover de .gemini/config/skills qualquer skill que já exista em franklin-quebragalho/skills/ ou em plugins
    deduplicated_config_skills = 0
    if CONFIG_SKILLS_ROOT.exists() and skills_src.exists():
        canonical_skill_names = {
            p.name for p in skills_src.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
        }
        plugins_dir = GEMINI_ROOT / "config" / "plugins"
        if plugins_dir.exists():
            for p_skill in plugins_dir.glob("*/skills/*/SKILL.md"):
                canonical_skill_names.add(p_skill.parent.name)
        for name in canonical_skill_names:
            dup_dir = CONFIG_SKILLS_ROOT / name
            if dup_dir.exists() and dup_dir.is_dir():
                shutil.rmtree(dup_dir)
                deduplicated_config_skills += 1

    # 2.2 Manter C:\Users\melki\.agents\ sincronizado sem duplicatas de plugins ou skills migradas
    user_agents_root = Path(r"C:\Users\melki\.agents")
    user_agents_skills = user_agents_root / "skills"
    if user_agents_skills.exists():
        plugins_dir = GEMINI_ROOT / "config" / "plugins"
        plugin_skill_names = (
            {p.parent.name for p in plugins_dir.glob("*/skills/*/SKILL.md")}
            if plugins_dir.exists()
            else set()
        )
        migrated_or_dup = plugin_skill_names | {"microsoft-foundry", "reverse-engineer-anything"}
        for s_dir in list(user_agents_skills.iterdir()):
            if not s_dir.is_dir():
                continue
            if s_dir.name in migrated_or_dup:
                shutil.rmtree(s_dir)
            elif (CONFIG_SKILLS_ROOT / s_dir.name).exists():
                _copy_tree(CONFIG_SKILLS_ROOT / s_dir.name, s_dir)
    mem_proto_src = GEMINI_ROOT / "config" / "plugins" / "mempalace" / "rules" / "memory-protocol.md"
    mem_proto_dst = user_agents_root / "rules" / "memory-protocol.md"
    if mem_proto_src.exists() and mem_proto_dst.parent.exists():
        shutil.copy2(mem_proto_src, mem_proto_dst)

    # 3. Sincronizar Subagentes (Topologia 3+1): agents/ -> .agents/agents/, plugin/agents/, .gemini/agents/ e .gemini/config/agents/
    agents_src = ROOT_DIR / "agents"
    agents_local_count = _copy_tree(agents_src, ROOT_DIR / ".agents" / "agents")
    agents_plugin_count = _copy_tree(agents_src, CONFIG_PLUGIN_ROOT / "agents")
    agents_gemini_count = _copy_tree(agents_src, GEMINI_ROOT / "agents")
    agents_config_count = _copy_tree(agents_src, GEMINI_ROOT / "config" / "agents")

    # 4. Sincronizar Planos DAG: plans/ -> plugin/plans/ e .gemini/plans/
    plans_src = ROOT_DIR / "plans"
    plans_plugin_count = _copy_tree(plans_src, CONFIG_PLUGIN_ROOT / "plans")
    plans_gemini_count = _copy_tree(plans_src, GEMINI_ROOT / "plans")

    # 5. Sincronizar Biblioteca Compartilhada (lib): shared/ + agent_spec_loader.py -> .gemini/lib e plugin/lib
    shared_src = ROOT_DIR / "shared"
    lib_gemini_count = _copy_tree(shared_src, GEMINI_ROOT / "lib" / "shared")
    lib_plugin_count = _copy_tree(shared_src, CONFIG_PLUGIN_ROOT / "lib" / "shared")

    loader_src = (
        ROOT_DIR
        / "skills"
        / "aprimoramento-expansibilidade-agentes-skills"
        / "scripts"
        / "agent_spec_loader.py"
    )
    if loader_src.exists():
        shutil.copy2(loader_src, GEMINI_ROOT / "lib" / "agent_spec_loader.py")
        shutil.copy2(loader_src, CONFIG_PLUGIN_ROOT / "lib" / "agent_spec_loader.py")

    # 6. Sincronizar Documentação (doc e docs)
    doc_files = [
        ROOT_DIR / "AGENTS.md",
        ROOT_DIR / "MY_AGENTS.md",
        ROOT_DIR / "MY_SKILLS.md",
        ROOT_DIR / "README.md",
        ROOT_DIR / "SPEC.md",
        ROOT_DIR / "CONTEXT.md",
        ROOT_DIR / "GEMINI.md",
        ROOT_DIR
        / "skills"
        / "arquitetura-design-implementacao-sistema"
        / "references"
        / "taxonomia_subagentes_ui_6_camadas.md",
    ]
    doc_copied = 0
    for df in doc_files:
        if df.exists():
            shutil.copy2(df, GEMINI_ROOT / "doc" / df.name)
            shutil.copy2(df, GEMINI_ROOT / "docs" / df.name)
            shutil.copy2(df, CONFIG_PLUGIN_ROOT / "doc" / df.name)
            doc_copied += 1

    # 7. Regenerar e assinar agent_card.json
    from shared.a2a_bridge import build_franklin_agent_card

    card = build_franklin_agent_card(skills_dir=ROOT_DIR / "skills", sign=True)
    card_json = json.dumps(card, indent=2, ensure_ascii=False) + "\n"
    (ROOT_DIR / "agent_card.json").write_text(card_json, encoding="utf-8")
    (GEMINI_ROOT / "doc" / "agent_card.json").write_text(card_json, encoding="utf-8")
    (GEMINI_ROOT / "docs" / "agent_card.json").write_text(card_json, encoding="utf-8")
    (CONFIG_PLUGIN_ROOT / "doc" / "agent_card.json").write_text(card_json, encoding="utf-8")

    # 8. Sincronizar manifestos do plugin (plugin.json e mcp_config.json)
    for manifest_name in ("plugin.json", "mcp_config.json"):
        manifest_src = ROOT_DIR / manifest_name
        if manifest_src.exists():
            shutil.copy2(manifest_src, CONFIG_PLUGIN_ROOT / manifest_name)

    return {
        "status": "SYNCHRONIZED",
        "skills_synced_to_agents": skills_agents_count,
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
