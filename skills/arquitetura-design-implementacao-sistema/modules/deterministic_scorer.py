#!/usr/bin/env python3
"""
modules/deterministic_scorer.py
Fachada de re-exportação canônica (Zero Duplicação) para `scripts/deterministic_scorer.py`.
Mantém retrocompatibilidade com imports de `modules.deterministic_scorer` delegando à SSOT em `scripts/`.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from deterministic_scorer import (  # noqa: E402
    CODE_EXTENSIONS,
    IGNORED_DIRS,
    ArchitecturalEvidence,
    DeterministicScoreReport,
    calculate_architecture_score,
    generate_resolution_html,
    main,
    run_self_test,
    scan_project_tree,
)

__all__ = [
    "ArchitecturalEvidence",
    "DeterministicScoreReport",
    "CODE_EXTENSIONS",
    "IGNORED_DIRS",
    "calculate_architecture_score",
    "generate_resolution_html",
    "main",
    "run_self_test",
    "scan_project_tree",
]

if __name__ == "__main__":
    sys.exit(main())
