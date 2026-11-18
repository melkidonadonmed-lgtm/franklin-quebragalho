"""
_progressive_registry.py
3-Tier Progressive Disclosure registry (Tier 1 XML catalog, Tier 2 SKILL.md activation,
and Tier 3 Path-Traversal-safe resource reading) extracted from shared.modular_orchestrator.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from shared.tools.frontmatter_parser import parse_frontmatter

logger = logging.getLogger("AgentArchitecture")

BUNDLED_SUBDIRS: tuple[str, ...] = ("references", "scripts", "assets", "rules", "evals")


@dataclass(frozen=True)
class SkillMetadata:
    """Metadados do Nível 1 extraídos exclusivamente do frontmatter YAML."""

    name: str
    description: str
    location: Path
    base_dir: Path
    version: str = "1.0.0"
    persona: str = "Franklin-Main"
    compatibility: Optional[str] = None


@dataclass
class LoadedSkill:
    """Instruções do Nível 2 e catálogo de recursos do Nível 3."""

    metadata: SkillMetadata
    instructions_body: str
    available_resources: List[str] = field(default_factory=list)


class ProgressiveSkillRegistry:
    """Gerenciador de descoberta, ativação e isolamento progressivo de Skills em 3 níveis."""

    def __init__(self, search_paths: List[Path], persona_map: Optional[Dict[str, str]] = None) -> None:
        self.search_paths = search_paths
        self.persona_map = persona_map or {}
        self._skills_catalog: Dict[str, SkillMetadata] = {}
        self._active_skills: Dict[str, LoadedSkill] = {}

    @property
    def catalog(self) -> Dict[str, SkillMetadata]:
        return dict(self._skills_catalog)

    def discover_skills(self) -> None:
        """NÍVEL 1: Varre os diretórios com regra de precedência e compila o catálogo enxuto."""
        self._skills_catalog.clear()
        for base_path in self.search_paths:
            if not base_path.exists() or not base_path.is_dir():
                continue
            for item in sorted(base_path.iterdir()):
                skill_file = item / "SKILL.md"
                if item.is_dir() and skill_file.is_file():
                    self._parse_and_register_metadata(skill_file)

    def _parse_and_register_metadata(self, skill_file: Path) -> None:
        """Extrai apenas o frontmatter YAML entre delimitadores '---'."""
        try:
            content = skill_file.read_text(encoding="utf-8", errors="replace")
            parsed_meta, _ = parse_frontmatter(content)
            name = str(parsed_meta.get("name", "")).strip()
            description = str(parsed_meta.get("description", "")).strip()
            if not name or not description or name in self._skills_catalog:
                return
            folder_name = skill_file.parent.name
            persona = self.persona_map.get(folder_name, self.persona_map.get(name, "Franklin-Main"))
            self._skills_catalog[name] = SkillMetadata(
                name=name,
                description=description,
                location=skill_file.resolve(),
                base_dir=skill_file.parent.resolve(),
                version=str(parsed_meta.get("version", "1.0.0")),
                persona=persona,
                compatibility=str(parsed_meta["compatibility"]) if parsed_meta.get("compatibility") else None,
            )
        except OSError as exc:
            logger.error("Erro ao processar %s: %s", skill_file, exc)

    def render_catalog_prompt(self) -> str:
        """Gera a representação XML concisa do NÍVEL 1 (~60 tokens/skill)."""
        if not self._skills_catalog:
            self.discover_skills()
        if not self._skills_catalog:
            return ""
        xml_parts = ["<available_skills>"]
        for meta in self._skills_catalog.values():
            xml_parts.extend([
                f'  <skill name="{meta.name}" persona="{meta.persona}" version="{meta.version}">',
                f"    <description>{meta.description}</description>",
                f"    <location>{meta.location.as_posix()}</location>",
                "  </skill>",
            ])
        xml_parts.append("</available_skills>")
        return "\n".join(xml_parts)

    def _collect_bundled_files(self, base_dir: Path) -> List[str]:
        """Lista arquivos disponíveis nas subpastas sem carregar seu conteúdo."""
        bundled: List[str] = []
        valid_dirs = [base_dir / s for s in BUNDLED_SUBDIRS if (base_dir / s).is_dir()]
        for target_dir in valid_dirs:
            files = [f for f in sorted(target_dir.rglob("*")) if f.is_file() and "__pycache__" not in f.parts]
            bundled.extend(f.relative_to(base_dir).as_posix() for f in files)
        return bundled

    def activate_skill(self, skill_name: str) -> str:
        """NÍVEL 2: Carrega o corpo instrucional de SKILL.md sem frontmatter e enumera recursos."""
        if not self._skills_catalog:
            self.discover_skills()
        if skill_name not in self._skills_catalog:
            return f"Erro: Skill '{skill_name}' não encontrada no catálogo disponível."

        meta = self._skills_catalog[skill_name]
        try:
            raw_content = meta.location.read_text(encoding="utf-8", errors="replace")
            _, body_content = parse_frontmatter(raw_content)
            clean_body = body_content.strip() or re.sub(r"^---\s*\n.*?\n---\s*\n", "", raw_content, flags=re.DOTALL).strip()
            bundled_files = self._collect_bundled_files(meta.base_dir)
            self._active_skills[skill_name] = LoadedSkill(
                metadata=meta,
                instructions_body=clean_body,
                available_resources=bundled_files,
            )
            resources_xml = "\n".join(f"    <resource_file>{f}</resource_file>" for f in bundled_files)
            return (
                f'<skill_content name="{meta.name}" version="{meta.version}" persona="{meta.persona}">\n'
                f"{clean_body}\n\n"
                f"Diretório base: {meta.base_dir}\n"
                f"<available_resources>\n"
                f"{resources_xml}\n"
                f"</available_resources>\n"
                f"</skill_content>"
            )
        except OSError as exc:
            logger.error("Falha ao ativar skill %s: %s", skill_name, exc)
            return f"Erro interno ao carregar a skill: {exc}"

    def _validate_resource_target(self, base_dir: Path, relative_path: str) -> tuple[Optional[Path], str, Optional[str]]:
        """Validates relative_path against traversal escapes and resolves target Path."""
        clean_rel = relative_path.strip().lstrip("/\\")
        if not clean_rel or ".." in Path(clean_rel).parts:
            return None, clean_rel, f"Erro de segurança: Acesso negado ao caminho externo '{relative_path}'."
        target_path = (base_dir / clean_rel).resolve()
        if not target_path.is_relative_to(base_dir):
            return None, clean_rel, f"Erro de segurança: Acesso negado ao caminho externo '{relative_path}'."
        if not target_path.exists() or not target_path.is_file():
            return None, clean_rel, f"Erro: O recurso '{relative_path}' não existe na pasta da skill."
        return target_path, clean_rel, None

    def read_skill_resource(self, skill_name: str, relative_path: str) -> str:
        """NÍVEL 3: Lê sob demanda um recurso específico com proteção contra Path Traversal."""
        if not self._skills_catalog:
            self.discover_skills()
        if skill_name not in self._active_skills and skill_name in self._skills_catalog:
            self.activate_skill(skill_name)
        if skill_name not in self._active_skills:
            return f"Erro: A skill '{skill_name}' deve ser ativada antes de ler seus recursos."

        target_path, clean_rel, err_msg = self._validate_resource_target(self._active_skills[skill_name].metadata.base_dir, relative_path)
        if err_msg or target_path is None:
            return err_msg or "Erro desconhecido."
        try:
            content = target_path.read_text(encoding="utf-8")
            return f'<resource_content skill="{skill_name}" file="{clean_rel}">\n{content}\n</resource_content>'
        except UnicodeDecodeError:
            return f"Erro: O recurso '{relative_path}' é um binário e não pode ser lido como texto."
        except OSError as exc:
            return f"Erro ao ler recurso: {exc}"
