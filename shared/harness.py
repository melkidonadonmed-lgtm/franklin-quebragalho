"""
harness.py
Harness de Governança Determinística, Sanitização Semântica e Checkpoints Human-in-the-Loop (HITL)
para o ecossistema Franklin Quebra-Galho.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class RiskLevel(str, Enum):
    """Nível de risco operacional determinístico."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    CRITICAL = "CRITICAL"


class SecurityViolationError(Exception):
    """Exceção acionada quando o SemanticGuard detecta tentativa de injeção ou comando proibido."""


class SemanticGuard:
    """Guardião determinístico de sanitização de entradas antes do processamento de ferramentas."""

    _INJECTION_PATTERNS = [
        (re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE), "Prompt Injection (Ignore Instructions)"),
        (re.compile(r"system\s*prompt\s*override", re.IGNORECASE), "Prompt Injection (System Override)"),
        (re.compile(r"<\s*script\b", re.IGNORECASE), "XSS / Script Tag Injection"),
    ]

    @classmethod
    def sanitize_input(cls, raw_text: str) -> str:
        """Remove caracteres de controle invisíveis e bloqueia padrões de injeção explícita."""
        if not raw_text:
            return ""

        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw_text).strip()
        for pattern, label in cls._INJECTION_PATTERNS:
            if pattern.search(cleaned):
                raise SecurityViolationError(f"Violação de segurança detectada pelo SemanticGuard: {label}")
        return cleaned


_CRITICAL_PATTERNS: List[Tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bremove-item\b.*(-recurse|-force)", re.IGNORECASE),
        "Exclusão recursiva/forçada em PowerShell (Remove-Item -Recurse/-Force)",
    ),
    (
        re.compile(r"\b(rm\s+-rf|del\s+/f|rmdir\s+/s|rd\s+/s|format\s+[a-z]:)", re.IGNORECASE),
        "Comando destrutivo de sistema de arquivos detectado",
    ),
    (
        re.compile(r"\b(drop\s+table|drop\s+database|truncate\s+table)\b", re.IGNORECASE),
        "Operação destrutiva de banco de dados (DROP/TRUNCATE)",
    ),
    (
        re.compile(r"\b(deletar\s+permanentemente|exclus[aã]o\s+definitiva|expurgo|apagar\s+tudo)\b", re.IGNORECASE),
        "Intenção de descarte ou exclusão permanente requer confirmação HITL e Dry-Run",
    ),
]


def evaluate_action_risk(action_text: str) -> Tuple[RiskLevel, str]:
    """Avalia deterministicamente o risco de uma intenção ou comando proposto."""
    for pattern, reason in _CRITICAL_PATTERNS:
        if pattern.search(action_text):
            return RiskLevel.CRITICAL, reason
    return RiskLevel.LOW, "Operação de leitura, diagnóstico ou mutação reversível segura."


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CheckpointRecord:
    """Registro imutável/tipado de checkpoint de governança HITL."""

    checkpoint_id: str
    session_id: str
    task_intent: str
    proposed_action: str
    active_skill: str
    risk_level: str
    status: str = "PENDING"
    notes: str = ""
    created_at: str = field(default_factory=_utc_now_iso)
    updated_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o registro para dicionário JSON."""
        return asdict(self)


class CheckpointStore:
    """Repositório local em JSON para persistência de checkpoints Human-in-the-Loop."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def _load_all(self) -> List[CheckpointRecord]:
        if not self.file_path.exists():
            return []
        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                return []
            return [CheckpointRecord(**item) for item in raw if isinstance(item, dict)]
        except (OSError, json.JSONDecodeError, TypeError):
            return []

    def _save_all(self, records: List[CheckpointRecord]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [r.to_dict() for r in records]
        self.file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def create(
        self,
        checkpoint_id: str,
        session_id: str,
        task_intent: str,
        proposed_action: str,
        active_skill: str,
        risk_level: str,
        notes: str = "",
    ) -> CheckpointRecord:
        """Cria e persiste um novo checkpoint pendente de aprovação humana."""
        records = self._load_all()
        rec = CheckpointRecord(
            checkpoint_id=checkpoint_id,
            session_id=session_id,
            task_intent=task_intent,
            proposed_action=proposed_action,
            active_skill=active_skill,
            risk_level=risk_level,
            status="PENDING",
            notes=notes,
        )
        records.append(rec)
        self._save_all(records)
        return rec

    def list(
        self,
        status: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> List[CheckpointRecord]:
        """Lista checkpoints filtrados opcionalmente por status e session_id."""
        records = self._load_all()
        if status:
            records = [r for r in records if r.status.upper() == status.upper()]
        if session_id:
            records = [r for r in records if r.session_id == session_id]
        return records

    def get(self, checkpoint_id: str) -> Optional[CheckpointRecord]:
        """Recupera um checkpoint pelo ID."""
        for rec in self._load_all():
            if rec.checkpoint_id == checkpoint_id:
                return rec
        return None

    def update_status(
        self,
        checkpoint_id: str,
        status: str,
        notes: str = "",
    ) -> Optional[CheckpointRecord]:
        """Atualiza o status ('APPROVED' ou 'REJECTED') de um checkpoint existente."""
        records = self._load_all()
        updated: Optional[CheckpointRecord] = None
        for rec in records:
            if rec.checkpoint_id == checkpoint_id:
                rec.status = status.upper()
                if notes:
                    rec.notes = notes
                rec.updated_at = _utc_now_iso()
                updated = rec
                break
        if updated:
            self._save_all(records)
        return updated

    def clear(self) -> int:
        """Remove todos os checkpoints armazenados e retorna a quantidade removida."""
        records = self._load_all()
        count = len(records)
        self._save_all([])
        return count
