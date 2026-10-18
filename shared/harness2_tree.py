"""
harness2_tree.py
Reconstrução nativo-determinística da Árvore de Componentes c1..c8 e Validador Answer-Free
do Google Research Harness² (arXiv:2610.14224) para o ecossistema Franklin Quebra-Galho.

Componentes:
1. SurfaceSpec (c1..c8: always_on, skills, sub_agents, scripts, hooks)
2. Autotrigger (reparo automático de gatilho de skill em always-on respeitando cap)
3. Validador determinístico (validate_harness_tree + assert_tree_has_no_grader_verdicts)
4. Diff estrutural (diff_summary) e Diversidade Line-Jaccard (tree_diversity)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Tuple

Tree = Dict[str, str]
_NAME_RX = r"[a-z0-9][a-z0-9_\-]*"
_GRADER_VERDICT_RX = re.compile(
    r"\b(grader_verdict|ground_truth_score|reference_answer_key|the grader expects)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SurfaceSpec:
    """Superfície editável de um framework de agentes (c1..c8)."""

    name: str = "franklin"
    always_on: Tuple[str, ...] = ("AGENTS.md",)
    always_on_max: int = 16_000
    skill_dir: str = ".agents/skills"
    skill_name_rule: str = "must_match"
    autotrigger_file: str = "AGENTS.md"
    trigger_line: str = "- When {desc}, load the `{name}` skill.\n"
    subagent_requires_mode: bool = False
    hooks_file: Optional[str] = ".codex/hooks.json"
    hook_events: FrozenSet[str] = frozenset({"PreToolUse", "PostToolUse", "SessionStart", "Stop"})
    compile_skill_scripts: bool = True
    reject_empty_always_on: bool = True


FRANKLIN_SURFACE = SurfaceSpec()


def normalize_rel(rel: str) -> str:
    """Normaliza caminho relativo e bloqueia path traversal ('..')."""
    r = str(rel).strip().replace("\\", "/")
    if r.startswith("/") or ".." in r.split("/"):
        raise ValueError(f"Path escapes the harness surface: {rel!r}")
    while r.startswith("./"):
        r = r[2:]
    return r.strip("/")


def _surface_regexes(surface: SurfaceSpec) -> Dict[str, re.Pattern[str]]:
    sd = re.escape(surface.skill_dir)
    return {
        "skill": re.compile(rf"{sd}/({_NAME_RX})/SKILL\.md"),
        "skill_script": re.compile(rf"{sd}/{_NAME_RX}/scripts/[A-Za-z0-9_.\-]+"),
        "subagent": re.compile(rf"sub_agents/({_NAME_RX})/AGENT\.md"),
        "script": re.compile(r"scripts/[a-z0-9_][a-z0-9_]*\.py"),
        "script_ref": re.compile(rf"(?:python3?\s+)((?:{sd}/[\w\-]+/)?scripts/[\w.\-]+\.py)"),
    }


def is_allowed_path(surface: SurfaceSpec, rel: str) -> bool:
    """Verifica se um arquivo relativo pertence à superfície editável c1..c8."""
    try:
        norm = normalize_rel(rel)
    except ValueError:
        return False
    if norm in surface.always_on or (surface.hooks_file and norm == surface.hooks_file):
        return True
    rxs = _surface_regexes(surface)
    return any(rxs[k].fullmatch(norm) for k in ("skill", "skill_script", "subagent", "script"))


def always_on_text(surface: SurfaceSpec, tree: Tree) -> str:
    """Concatena o texto always-on da árvore."""
    return "\n\n".join(tree.get(a, "") for a in surface.always_on)


def skill_names(surface: SurfaceSpec, tree: Tree) -> List[str]:
    """Extrai nomes ordenados das skills presentes na árvore."""
    rx = _surface_regexes(surface)["skill"]
    return sorted({m.group(1) for rel in tree if (m := rx.fullmatch(normalize_rel(rel)))})


def autotrigger_skills(surface: SurfaceSpec, tree: Tree) -> List[str]:
    """Injeta linha de gatilho no arquivo always-on para skills órfãs respeitando always_on_max."""
    body = always_on_text(surface, tree)
    repaired: List[str] = []
    for name in skill_names(surface, tree):
        if name in body:
            continue
        fm = tree.get(f"{surface.skill_dir}/{name}/SKILL.md", "")[:600]
        m = re.search(r"^description:\s*(.+)$", fm, re.M)
        desc = m.group(1).strip().rstrip(".") if m else f"the {name} workflow applies"
        line = surface.trigger_line.format(name=name, desc=desc)
        cur = tree.get(surface.autotrigger_file, "")
        if len(always_on_text(surface, tree)) + len(line) + 2 > surface.always_on_max:
            continue
        tree[surface.autotrigger_file] = (cur.rstrip() + "\n" + line) if cur.strip() else line
        body = always_on_text(surface, tree)
        repaired.append(name)
    return repaired


def assert_tree_has_no_grader_verdicts(tree: Mapping[str, str]) -> None:
    """Garante invariante Answer-Free: bloqueia vazamento de vereditos de avaliador ou gabarito."""
    for rel, content in tree.items():
        if _GRADER_VERDICT_RX.search(content):
            raise ValueError(f"Grader verdict or answer-key leak detected in {rel!r}")


def validate_harness_tree(surface: SurfaceSpec, tree: Tree) -> Dict[str, Any]:
    """Valida invariantes da árvore c1..c8 (cap, frontmatter, triggers, compilação AST e scripts)."""
    errs: List[str] = []
    rxs = _surface_regexes(surface)
    norm_tree: Tree = {}
    for k, v in tree.items():
        norm_k = normalize_rel(k)
        if not is_allowed_path(surface, norm_k):
            errs.append(f"File off editable surface: {norm_k}")
        norm_tree[norm_k] = v

    body = always_on_text(surface, norm_tree)
    if len(body) > surface.always_on_max:
        errs.append(f"Always-on content ({len(body)} chars) exceeds cap ({surface.always_on_max})")
    if surface.reject_empty_always_on and not body.strip():
        errs.append(f"{surface.always_on[0]} cannot be empty")

    skills = skill_names(surface, norm_tree)
    for sname in skills:
        s_path = f"{surface.skill_dir}/{sname}/SKILL.md"
        fm = norm_tree.get(s_path, "")[:600]
        if not re.search(r"^description:\s*\S", fm, re.M):
            errs.append(f"{s_path} missing `description:` in frontmatter")
        m_name = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
        if surface.skill_name_rule == "must_match" and not (m_name and m_name.group(1) == sname):
            errs.append(f"{s_path} needs frontmatter `name: {sname}`")
        if sname not in body:
            errs.append(f"Skill '{sname}' is untriggered in always-on text")

    have_scripts = {
        rel for rel in norm_tree if rxs["script"].fullmatch(rel) or rxs["skill_script"].fullmatch(rel)
    }
    for rel, src in norm_tree.items():
        if rel.endswith(".py") and (rxs["script"].fullmatch(rel) or rxs["skill_script"].fullmatch(rel)):
            try:
                compile(src, rel, "exec")
            except SyntaxError as exc:
                errs.append(f"{rel} does not compile: {exc.msg} (line {exc.lineno})")
        if rxs["skill"].fullmatch(rel) or rel in surface.always_on:
            for ref in rxs["script_ref"].findall(src):
                if ref not in have_scripts:
                    errs.append(f"{rel} invokes `{ref}` which is missing from harness tree")

    assert_tree_has_no_grader_verdicts(norm_tree)
    if errs:
        raise ValueError(" | ".join(errs))

    return {
        "always_on_chars": len(body),
        "n_files": len(norm_tree),
        "skills": len(skills),
        "scripts": len(have_scripts),
    }


def diff_summary(surface: SurfaceSpec, before: Tree, after: Tree) -> Dict[str, Any]:
    """Calcula delta determinístico entre duas árvores de harness."""
    b_keys, a_keys = set(before), set(after)
    return {
        "added": sorted(a_keys - b_keys),
        "removed": sorted(b_keys - a_keys),
        "modified": sorted(k for k in (b_keys & a_keys) if before[k] != after[k]),
        "always_on_char_delta": len(always_on_text(surface, after)) - len(always_on_text(surface, before)),
    }


def tree_diversity(trees: Mapping[str, Tree]) -> Dict[str, Any]:
    """Calcula a similaridade par-a-par Line-Jaccard entre árvores candidatas."""
    names = sorted(trees)
    if len(names) < 2:
        return {"n": len(names), "n_distinct": len(names), "mean_line_jaccard": 1.0}
    line_sets = {
        n: {f"{rel}:{ln}" for rel, c in trees[n].items() for ln in c.splitlines() if ln.strip()}
        for n in names
    }
    sims: List[float] = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            union = line_sets[a] | line_sets[b]
            sims.append(len(line_sets[a] & line_sets[b]) / len(union) if union else 1.0)
    distinct = len({tuple(sorted(t.items())) for t in trees.values()})
    return {"n": len(names), "n_distinct": distinct, "mean_line_jaccard": round(sum(sims) / len(sims), 4)}
