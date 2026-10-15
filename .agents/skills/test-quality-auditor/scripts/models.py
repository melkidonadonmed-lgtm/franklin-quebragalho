#!/usr/bin/env python3
"""
models.py
Camada de Domínio: Contratos Estritos (Dataclasses) e Régua de Classificação (Níveis 1 a 4)
para o Auditor Determinístico de Qualidade de Testes (Python, TS/JS, Go e MCP).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class AuditIssue:
    id: str
    title: str
    category: str
    severity: str
    file: str
    test_name: str
    line: int
    col: int
    penalty: int
    description: str
    recommendation: str


@dataclass
class TestDossierRecord:
    __test__ = False
    test_name: str
    file: str
    line: int
    assertion_count: int
    score: int
    level: str
    status: str
    issues: List[str] = field(default_factory=list)
    evidence: str = ""
    domain: str = "general"


@dataclass
class FileAuditReport:
    aprovado: bool
    filename: str
    total_tests: int
    score_medio: float
    nivel_espectro: str
    total_inconformidades: int
    dossiers: List[TestDossierRecord] = field(default_factory=list)
    issues: List[AuditIssue] = field(default_factory=list)
    language: str = "python"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aprovado": self.aprovado,
            "filename": self.filename,
            "language": self.language,
            "total_tests": self.total_tests,
            "score_medio": round(self.score_medio, 2),
            "nivel_espectro": self.nivel_espectro,
            "total_inconformidades": self.total_inconformidades,
            "dossiers": [asdict(d) for d in self.dossiers],
            "issues": [asdict(i) for i in self.issues],
        }


def classify_quality_level(score: float) -> str:
    """Classifica a pontuação (0-100) nos 4 níveis canônicos do Dossiê de Qualidade."""
    if score <= 25:
        return "NÍVEL 1: ILUSÓRIO / PLACEBO"
    if score <= 50:
        return "NÍVEL 2: SUPERFICIAL / FRÁGIL"
    if score <= 80:
        return "NÍVEL 3: FUNCIONAL RÍGIDO"
    return "NÍVEL 4: DETERMINÍSTICO & RESILIENTE"
