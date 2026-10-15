#!/usr/bin/env python3
"""
standardize_skills_metadata.py
Sincroniza metadados YAML e espelha de forma física e paritária as skills
canônicas entre .agents/skills/, skills/ e o plugin global franklin-skills.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any, Dict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.tools.frontmatter_parser import parse_frontmatter

AGENTS_SKILLS_DIR = ROOT_DIR / ".agents" / "skills"
MIRROR_SKILLS_DIR = ROOT_DIR / "skills"
GLOBAL_PLUGIN_DIR = Path.home() / ".gemini" / "config" / "plugins" / "franklin-skills" / "skills"


def sync_directory_tree(src_root: Path, dst_root: Path) -> int:
    """Sincroniza fisicamente todas as pastas de skills de src_root para dst_root e remove órfãs."""
    dst_root.mkdir(parents=True, exist_ok=True)
    src_names = {d.name for d in src_root.iterdir() if d.is_dir()}

    for existing in dst_root.iterdir():
        if existing.is_dir() and existing.name not in src_names:
            shutil.rmtree(existing)

    count = 0
    for skill_dir in sorted(src_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        target_dir = dst_root / skill_dir.name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(skill_dir, target_dir)
        count += 1
    return count


def main() -> int:
    print("=== SINCRONIZANDO E VALIDANDO METADADOS DO CATÁLOGO DE SKILLS ===")
    if not AGENTS_SKILLS_DIR.exists():
        print(f"[FAIL] Diretório canônico não encontrado: {AGENTS_SKILLS_DIR}")
        return 1

    checked = 0
    for skill_dir in sorted(AGENTS_SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        version = meta.get("version", "1.0.0")
        checked += 1
        print(f"[OK] {skill_dir.name:<45} (v{version})")

    mirror_count = sync_directory_tree(AGENTS_SKILLS_DIR, MIRROR_SKILLS_DIR)
    plugin_count = sync_directory_tree(AGENTS_SKILLS_DIR, GLOBAL_PLUGIN_DIR)

    print("-" * 65)
    print(
        f"Sucesso: {checked} skills verificadas | "
        f"skills/ sincronizadas ({mirror_count}) | "
        f"plugin global sincronizado ({plugin_count})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
