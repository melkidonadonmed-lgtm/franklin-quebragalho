"""
harness2_engine.py
Reconstrução nativo-determinística dos algoritmos recursivos do Google Research Harness²
(arXiv:2610.14224) para o ecossistema Franklin Quebra-Galho (Windows 11 / Python 3.12+).

Componentes:
1. RecursionLedger (Budget Identity: R = 4k rollouts, P = 3k sessions)
2. Contrastive Task-Level Recursion (Propose-Probe-Compose: parallel 'agg' & sequential 'seq')
3. Anonymized Candidate Pool & ExperienceLibrary (cue, lesson, evidence, INDEX.md)
"""

from __future__ import annotations

import hashlib
import random
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from shared.harness2_tree import (
    FRANKLIN_SURFACE,
    SurfaceSpec,
    Tree,
     always_on_text,
    assert_tree_has_no_grader_verdicts,
    autotrigger_skills,
    diff_summary,
    is_allowed_path,
    normalize_rel,
    skill_names,
    tree_diversity,
    validate_harness_tree,
)

__all__ = [
    "FRANKLIN_SURFACE",
    "ExperienceLibrary",
    "LedgerEntry",
    "RecursionLedger",
    "SurfaceSpec",
    "Tree",
    "always_on_text",
    "assert_tree_has_no_grader_verdicts",
    "assign_anonymous_ids",
    "autotrigger_skills",
    "diff_summary",
    "is_allowed_path",
    "normalize_rel",
    "simulate_propose_probe_compose",
    "skill_names",
    "tree_diversity",
    "validate_harness_tree",
]


@dataclass
class LedgerEntry:
    kind: str
    label: str
    usd: float = 0.0
    attempts: int = 1


@dataclass
class RecursionLedger:
    """Contabilidade de orçamento R = 4k rollouts e P = 3k estágios de proposição."""

    mode: str
    task_id: str
    k: int
    entries: List[LedgerEntry] = field(default_factory=list)

    def rollout(self, label: str, usd: float = 0.0) -> None:
        self.entries.append(LedgerEntry("rollout", label, usd))

    def session(self, label: str, usd: float = 0.0, attempts: int = 1) -> None:
        self.entries.append(LedgerEntry("session", label, usd, attempts))

    @property
    def R(self) -> int:
        return sum(1 for e in self.entries if e.kind == "rollout")

    @property
    def P(self) -> int:
        return sum(1 for e in self.entries if e.kind == "session")

    def assert_identity(self) -> None:
        want_r, want_p = 4 * self.k, 3 * self.k
        rl = [e.label for e in self.entries if e.kind == "rollout"]
        sl = [e.label for e in self.entries if e.kind == "session"]
        dupes = sorted({x for x in rl if rl.count(x) > 1} | {x for x in sl if sl.count(x) > 1})
        if dupes or self.R != want_r or self.P != want_p:
            raise AssertionError(
                f"Budget identity violated for {self.mode}-{self.k}: R={self.R}/{want_r}, P={self.P}/{want_p}, dupes={dupes}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "task_id": self.task_id,
            "k": self.k,
            "R": self.R,
            "expected_R": 4 * self.k,
            "P": self.P,
            "expected_P": 3 * self.k,
            "usd": round(sum(e.usd for e in self.entries), 6),
        }


def assign_anonymous_ids(labels: Sequence[str], *, task_id: str, k: int, mode: str) -> Dict[str, str]:
    """Mapeia IDs anônimos (A, B, C...) para labels de candidatos via SHA-1 determinístico."""
    seed = int(hashlib.sha1(f"{task_id}|{k}|{mode}".encode("utf-8")).hexdigest()[:12], 16)
    ordered = sorted(labels)
    random.Random(seed).shuffle(ordered)
    return {chr(ord("A") + i): lbl for i, lbl in enumerate(ordered)}


def _execute_recursion_step(
    label: str,
    dim: str,
    fallback: Tree,
    surface: SurfaceSpec,
    prop: Callable[[str, str, Tree], Tuple[Tree, str]],
    ledger: RecursionLedger,
    trees: Dict[str, Tree],
    stages: List[Dict[str, Any]],
) -> Tree:
    """Executa um estágio individual de proposição, reparo autotrigger e validação Answer-Free."""
    proposed, notes = prop(label, dim, dict(fallback))
    autotrigger_skills(surface, proposed)
    try:
        validate_harness_tree(surface, proposed)
        fell_back, err = False, ""
        chosen_tree = proposed
    except ValueError as exc:
        fell_back, err = True, str(exc)
        chosen_tree = dict(fallback)
    delta = diff_summary(surface, fallback, chosen_tree)
    kept_base = not (delta["added"] or delta["removed"] or delta["modified"])
    ledger.session(label)
    trees[label] = chosen_tree
    stages.append(
        {
            "label": label,
            "dim": dim,
            "kept_base": kept_base,
            "fell_back": fell_back,
            "notes": notes,
            "error": err,
        }
    )
    return chosen_tree


def simulate_propose_probe_compose(
    task_id: str,
    base_tree: Tree,
    *,
    mode: str = "agg",
    k: int = 1,
    surface: SurfaceSpec = FRANKLIN_SURFACE,
    proposer_fn: Optional[Callable[[str, str, Tree], Tuple[Tree, str]]] = None,
) -> Dict[str, Any]:
    """Executa o loop contrastivo Propose-Probe-Compose (R=4k, P=3k) com reparo e validação."""
    if mode not in ("agg", "seq"):
        raise ValueError("mode must be 'agg' (parallel) or 'seq' (sequential)")
    k = max(1, int(k))
    ledger = RecursionLedger(mode=mode, task_id=task_id, k=k)
    for i in range(1, k + 1):
        ledger.rollout(f"base{i}")

    def _default_proposer(label: str, dim: str, current: Tree) -> Tuple[Tree, str]:
        cand = dict(current)
        a_file = surface.always_on[0]
        cand[a_file] = cand.get(a_file, "").rstrip() + f"\n<!-- [{dim}:{label}] verified invariant -->\n"
        return cand, f"Applied {dim} refinement in {label}"

    prop = proposer_fn or _default_proposer
    trees: Dict[str, Tree] = {}
    stages: List[Dict[str, Any]] = []
    finals: List[str] = []

    if mode == "agg":
        for i in range(1, k + 1):
            for d in ("INV", "DOM"):
                lbl = f"{d.lower()}{i}"
                _execute_recursion_step(lbl, d, base_tree, surface, prop, ledger, trees, stages)
                ledger.rollout(lbl)
        for i in range(1, k + 1):
            lbl = f"agg{i}"
            _execute_recursion_step(lbl, "AGG", trees.get(f"inv{i}", base_tree), surface, prop, ledger, trees, stages)
            ledger.rollout(lbl)
            finals.append(lbl)
    else:
        cur = dict(base_tree)
        for t in range(1, k + 1):
            for d in ("INV", "DOM"):
                lbl = f"{d.lower()}{t}"
                _execute_recursion_step(lbl, d, cur, surface, prop, ledger, trees, stages)
                ledger.rollout(lbl)
            ck = f"c{t}"
            cur = _execute_recursion_step(ck, "COMPOSE", trees.get(f"inv{t}", cur), surface, prop, ledger, trees, stages)
            ledger.rollout(ck)
            finals.append(ck)

    ledger.assert_identity()
    return {
        "mode": mode, "task_id": task_id, "k": k, "finals": finals,
        "anonymous_pool": assign_anonymous_ids(finals, task_id=task_id, k=k, mode=mode),
        "stages": stages, "diversity": tree_diversity({f: trees[f] for f in finals}),
        "ledger": ledger.to_dict(),
    }


@dataclass
class ExperienceLibrary:
    """Biblioteca de experiência evolutiva por domínio (Harnessing-Level Recursion)."""

    root: Path
    domain: str
    surface: SurfaceSpec = FRANKLIN_SURFACE

    @property
    def domain_dir(self) -> Path:
        clean = re.sub(r"\s*[/\\]\s*", "__", self.domain).strip() or "general"
        return Path(self.root) / clean

    def add_experience(
        self,
        task_id: str,
        harness: Tree,
        *,
        cue: str,
        lesson: str,
        evidence: str,
        why: str = "",
    ) -> Path:
        """Persiste o harness adotado + lição verificada (cue, lesson, evidence) e reconstrói INDEX.md."""
        if not (cue.strip() and lesson.strip() and evidence.strip()):
            raise ValueError("Experience requires non-empty 'cue', 'lesson', and 'evidence'")
        assert_tree_has_no_grader_verdicts(harness)
        assert_tree_has_no_grader_verdicts({"EXPERIENCE.md": f"{cue} {lesson} {evidence} {why}"})

        slug = task_id.replace("/", "__")
        entry_dir = self.domain_dir / "harnesses" / slug
        h_dir = entry_dir / "harness"
        if h_dir.exists():
            shutil.rmtree(h_dir)
        h_dir.mkdir(parents=True, exist_ok=True)
        for rel, content in harness.items():
            p = h_dir / normalize_rel(rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

        exp_md = "\n".join(
            [
                f"# {task_id}",
                "",
                "## Why this was chosen",
                why.strip() or "Selected via anonymous behavioral contrast.",
                "",
                "## Transferable lesson",
                f"- **cue**: {cue.strip()}",
                f"- **lesson**: {lesson.strip()}",
                f"- **evidence**: {evidence.strip()}",
                "",
            ]
        )
        (entry_dir / "EXPERIENCE.md").write_text(exp_md, encoding="utf-8")
        self._rebuild_index()
        return entry_dir

    def _rebuild_index(self) -> Path:
        h_root = self.domain_dir / "harnesses"
        entries = sorted(p.name for p in h_root.iterdir() if p.is_dir()) if h_root.is_dir() else []
        lines = [f"# Library — {self.domain}", ""]
        for name in entries:
            lines.append(f"- `harnesses/{name}/` -> `EXPERIENCE.md`")
        self.domain_dir.mkdir(parents=True, exist_ok=True)
        idx = self.domain_dir / "INDEX.md"
        idx.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return idx
