#!/usr/bin/env python3
"""
deterministic_scorer.py
Wrapper/Script executável para `franklin_run_skill_script` e CLI direta da skill
`arquitetura-design-implementacao-sistema` (v2.0.0).
Importa e delega para `../modules/deterministic_scorer.py`.
"""

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from modules.deterministic_scorer import (  # noqa: E402
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
    "calculate_architecture_score",
    "generate_resolution_html",
    "scan_project_tree",
    "run_self_test",
    "main",
]

if __name__ == "__main__":
    sys.exit(main())
