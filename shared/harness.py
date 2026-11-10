"""
harness.py
Harness de Governança Determinística, Sanitização Semântica e Checkpoints Human-in-the-Loop (HITL)
para o ecossistema Franklin Quebra-Galho.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


class RiskLevel(str, Enum):
    """Nível de risco operacional determinístico."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    CRITICAL = "CRITICAL"


class RootCauseCategory(str, Enum):
    """Taxonomia determinística de causa-raiz para falhas na 1ª tentativa e Self-Refine."""

    PREMATURE_RETURN_NO_WAIT = "PREMATURE_RETURN_NO_WAIT"
    STUCK_IN_LOOP = "STUCK_IN_LOOP"
    WRONG_ROUTE_CHOICE = "WRONG_ROUTE_CHOICE"
    POST_CONDITION_FAILED = "POST_CONDITION_FAILED"
    SCHEMA_OR_GUARD_VIOLATION = "SCHEMA_OR_GUARD_VIOLATION"


class SecurityViolationError(Exception):
    """Exceção acionada quando o SemanticGuard detecta tentativa de injeção ou comando proibido."""


class SemanticGuard:
    """Guardião determinístico de sanitização de entradas antes do processamento de ferramentas."""

    _INJECTION_PATTERNS = [
        (re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE), "Prompt Injection (Ignore Instructions)"),
        (re.compile(r"system\s*prompt\s*override", re.IGNORECASE), "Prompt Injection (System Override)"),
        (re.compile(r"<\s*script\b", re.IGNORECASE), "XSS / Script Tag Injection"),
        (re.compile(r"(?:\b(?:eval|exec)\s*\(|;\s*rm\s+-rf\b|\|\|\s*curl\b)", re.IGNORECASE), "Code / Shell Injection"),
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

    @classmethod
    def evaluate_corpus_metrics(cls, corpus: List[Tuple[str, bool]]) -> Dict[str, Any]:
        """Calcula Matriz de Confusão (TP, FP, TN, FN, Precision, Recall, FNR) sobre corpus rotulado."""
        tp = fp = tn = fn = 0
        for text, is_malicious in corpus:
            blocked = False
            try:
                cleaned = cls.sanitize_input(text)
                risk, _ = evaluate_action_risk(cleaned)
                if risk == RiskLevel.CRITICAL:
                    blocked = True
            except SecurityViolationError:
                blocked = True

            if is_malicious and blocked:
                tp += 1
            elif is_malicious and not blocked:
                fn += 1
            elif not is_malicious and blocked:
                fp += 1
            else:
                tn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        fnr = fn / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        return {
            "TP": tp,
            "FP": fp,
            "TN": tn,
            "FN": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "fnr": round(fnr, 4),
            "f1_score": round(f1, 4),
        }


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


# Re-exportação dos motores recursivos Harness² (Google Research arXiv:2610.14224)
from shared.harness2_engine import (  # noqa: E402, F401
    FRANKLIN_SURFACE,
    ExperienceLibrary,
    RecursionLedger,
    SurfaceSpec,
    assert_tree_has_no_grader_verdicts,
    assign_anonymous_ids,
    autotrigger_skills,
    diff_summary,
    is_allowed_path,
    normalize_rel,
    simulate_propose_probe_compose,
    tree_diversity,
    validate_harness_tree,
)


def _dispatch_telemetry_report(sessions_dir: Path) -> str:
    """Consolida o relatório de telemetria pós-refinamento e candidatos de Evals."""
    store = RefinementTelemetryStore(sessions_dir=sessions_dir)
    records = [r.to_dict() for r in store.load_records()]
    by_cause: Dict[str, int] = {}
    for r in records:
        rc = str(r.get("root_cause", "UNKNOWN"))
        by_cause[rc] = by_cause.get(rc, 0) + 1
    evals: List[Dict[str, Any]] = []
    if store.evals_candidates_path.exists():
        try:
            evals = json.loads(store.evals_candidates_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            evals = []
    return json.dumps(
        {
            "status": "OK",
            "total_refinement_events": len(records),
            "by_root_cause": by_cause,
            "recent_records": records[-10:],
            "eval_regression_candidates_count": len(evals),
            "eval_regression_candidates": evals[-10:],
        },
        indent=2,
        ensure_ascii=False,
    )


def _dispatch_record_refinement(sessions_dir: Path, payload: Dict[str, Any]) -> str:
    """Registra um evento de refinamento determinístico no ledger e na ExperienceLibrary."""
    store = RefinementTelemetryStore(sessions_dir=sessions_dir, domain=str(payload.get("domain", "orchestration")))
    rec = RefinementTelemetryRecord(
        run_id=str(payload.get("run_id", f"run-{uuid.uuid4().hex[:6]}")),
        step_id=str(payload.get("step_id", "step-manual")),
        attempt=int(payload.get("attempt", 2)),
        root_cause=str(payload.get("root_cause", RootCauseCategory.POST_CONDITION_FAILED.value)),
        why_failed_first_time=str(payload.get("why_failed_first_time", "Falha reportada via MCP")),
        chosen_path=str(payload.get("chosen_path", "mcp_tool")),
        recovery_action=str(payload.get("recovery_action", "Refinamento determinístico aplicado")),
        post_condition_verified=bool(payload.get("post_condition_verified", True)),
        duration_ms=float(payload.get("duration_ms", 0.0)),
    )
    dest = store.record_refinement(rec, user_query=str(payload.get("user_query", "")))
    return json.dumps({"status": "RECORDED", "record": rec.to_dict(), "destinations": dest}, indent=2, ensure_ascii=False)


def dispatch_harness2_action(action: str, notes_json: str, sessions_dir: Path) -> Optional[str]:
    """Despacha sub-ações do Harness² ('validate_tree', 'evolve', 'record_experience', 'telemetry_report', 'record_refinement')."""
    act = action.strip().lower()
    if act not in ("validate_tree", "evolve", "record_experience", "telemetry_report", "record_refinement"):
        return None
    try:
        payload = json.loads(notes_json) if notes_json.strip().startswith("{") else {}
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Payload JSON inválido em notes: {exc}"}, ensure_ascii=False)
    if act == "telemetry_report":
        return _dispatch_telemetry_report(sessions_dir)
    if act == "record_refinement":
        return _dispatch_record_refinement(sessions_dir, payload)
    tree = payload.get("tree") or {"AGENTS.md": "# Franklin Agent\nFollow core rules.\n"}
    if act == "validate_tree":
        try:
            repaired = autotrigger_skills(FRANKLIN_SURFACE, tree)
            census = validate_harness_tree(FRANKLIN_SURFACE, tree)
            return json.dumps({"status": "VALID", "repaired_triggers": repaired, "census": census, "tree": tree}, indent=2, ensure_ascii=False)
        except ValueError as exc:
            return json.dumps({"status": "INVALID", "error": str(exc)}, indent=2, ensure_ascii=False)
    if act == "evolve":
        task_id, mode, k = str(payload.get("task_id", "task-default")), str(payload.get("mode", "agg")), int(payload.get("k", 1))
        try:
            res = simulate_propose_probe_compose(task_id, tree, mode=mode, k=k)
            return json.dumps({"status": "COMPLETED", **res}, indent=2, ensure_ascii=False)
        except (ValueError, AssertionError) as exc:
            return json.dumps({"status": "FAILED", "error": str(exc)}, indent=2, ensure_ascii=False)
    domain, task_id = str(payload.get("domain", "general")), str(payload.get("task_id", "task-default"))
    lib = ExperienceLibrary(root=sessions_dir / "experience_library", domain=domain)
    try:
        entry_dir = lib.add_experience(
            task_id, tree, cue=str(payload.get("cue", "")), lesson=str(payload.get("lesson", "")),
            evidence=str(payload.get("evidence", "")), why=str(payload.get("why", "")),
        )
        return json.dumps({"status": "RECORDED", "domain": domain, "entry_dir": str(entry_dir)}, indent=2, ensure_ascii=False)
    except ValueError as exc:
        return json.dumps({"status": "REJECTED", "error": str(exc)}, indent=2, ensure_ascii=False)


def classify_failure_root_cause(
    error_or_critique: str,
    data_payload: Dict[str, Any],
    *,
    attempt: int = 1,
    max_retries: int = 3,
    expected_keys: Optional[List[str]] = None,
) -> Tuple[RootCauseCategory, str]:
    """Classifica deterministicamente por que a execução falhou na tentativa atual."""
    msg_low = (error_or_critique or "").lower()
    if "violação de segurança" in msg_low or "schema" in msg_low or "extra_forbidden" in msg_low:
        return (
            RootCauseCategory.SCHEMA_OR_GUARD_VIOLATION,
            f"Violação de contrato Pydantic ou SemanticGuard: {error_or_critique}",
        )
    if "timeout" in msg_low or "loop" in msg_low or "max_steps" in msg_low or attempt >= max_retries:
        return (
            RootCauseCategory.STUCK_IN_LOOP,
            f"Agente atingiu limite de passos/tentativas ({attempt}/{max_retries}) ou timeout: {error_or_critique}",
        )
    if not data_payload or "vazia" in msg_low or "no_wait" in msg_low or "pending" in str(data_payload.get("job_status", "")).lower():
        return (
            RootCauseCategory.PREMATURE_RETURN_NO_WAIT,
            "Retorno prematuro sem aguardar conclusão do job ou sem artefato verificável no payload.",
        )
    if expected_keys and any(k not in data_payload for k in expected_keys):
        missing = [k for k in expected_keys if k not in data_payload]
        return (
            RootCauseCategory.WRONG_ROUTE_CHOICE,
            f"Rota/ferramenta escolhida não produziu as chaves exigidas pelo plano: {missing}",
        )
    return (
        RootCauseCategory.POST_CONDITION_FAILED,
        f"Artefato gerado reprovou na verificação Read-After-Write / pós-condição: {error_or_critique}",
    )


@dataclass
class RefinementTelemetryRecord:
    """Registro estruturado de falha na 1ª tentativa, diagnóstico de causa-raiz e correção pós-Self-Refine."""

    run_id: str
    step_id: str
    attempt: int
    root_cause: str
    why_failed_first_time: str
    chosen_path: str
    recovery_action: str
    post_condition_verified: bool
    duration_ms: float = 0.0
    created_at: str = field(default_factory=_utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RefinementTelemetryStore:
    """Roteia telemetria pós-refinamento para JSONL, ExperienceLibrary e candidatos de regressão Evals."""

    def __init__(self, sessions_dir: Path, domain: str = "orchestration") -> None:
        self.sessions_dir = Path(sessions_dir)
        self.domain = domain
        self.ledger_path = self.sessions_dir / "refinement_ledger.jsonl"
        self.evals_candidates_path = self.sessions_dir / "eval_regression_candidates.json"
        self.experience_lib = ExperienceLibrary(root=self.sessions_dir / "experience_library", domain=domain)

    def record_refinement(
        self,
        record: RefinementTelemetryRecord,
        *,
        user_query: str = "",
        harness_tree: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Persiste o trace no ledger JSONL e, se recuperado com sucesso, alimenta ExperienceLibrary e Evals."""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

        destinations: Dict[str, Any] = {"ledger_jsonl": str(self.ledger_path)}
        if record.post_condition_verified:
            tree = harness_tree or {
                "AGENTS.md": (
                    f"# Franklin Closed-Loop Guard\n"
                    f"- Prevent {record.root_cause} on route {record.chosen_path}.\n"
                )
            }
            exp_dir = self.experience_lib.add_experience(
                f"{record.run_id}__{record.step_id}",
                tree,
                cue=f"When executing '{record.chosen_path}' for query '{user_query or record.step_id}'",
                lesson=f"Avoid {record.root_cause}: {record.recovery_action}",
                evidence=f"Attempt {record.attempt} verified post-condition after initial failure ({record.why_failed_first_time})",
                why=f"First attempt failed due to {record.root_cause}; deterministic refinement recovered execution.",
            )
            destinations["experience_library_dir"] = str(exp_dir)
            eval_case = self._append_eval_candidate(record, user_query)
            destinations["eval_candidate_id"] = eval_case["id"]
        return destinations

    def _append_eval_candidate(self, record: RefinementTelemetryRecord, user_query: str) -> Dict[str, Any]:
        existing: List[Dict[str, Any]] = []
        if self.evals_candidates_path.exists():
            try:
                raw = json.loads(self.evals_candidates_path.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    existing = raw
            except (OSError, json.JSONDecodeError):
                existing = []

        case_entry = {
            "id": f"eval-reg-{record.run_id}-{record.step_id}",
            "prompt": user_query or f"Execute step {record.step_id} via {record.chosen_path}",
            "root_cause": record.root_cause,
            "why_failed_first_time": record.why_failed_first_time,
            "recovery_action": record.recovery_action,
            "expected_assertions": [
                "post_condition_verified == True",
                f"no_{record.root_cause.lower()}",
            ],
            "created_at": record.created_at,
        }
        existing.append(case_entry)
        self.evals_candidates_path.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return case_entry

    def load_records(self) -> List[RefinementTelemetryRecord]:
        if not self.ledger_path.exists():
            return []
        out: List[RefinementTelemetryRecord] = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(RefinementTelemetryRecord(**json.loads(line)))
        return out


def execute_with_idempotency(
    sessions_dir: Path,
    idempotency_key: str,
    tool_name: str,
    compute_fn: Callable[[], str],
) -> str:
    """Garante execução idempotente determinística em tools MCP de mutação (Spec 2026-07-28)."""
    key = (idempotency_key or "").strip()
    if not key:
        return compute_fn()

    sessions_dir.mkdir(parents=True, exist_ok=True)
    ledger_file = sessions_dir / "mcp_idempotency_ledger.json"
    compound_key = f"{tool_name}::{key}"

    ledger: Dict[str, Any] = {}
    if ledger_file.exists():
        try:
            raw = json.loads(ledger_file.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                ledger = raw
        except (OSError, json.JSONDecodeError):
            ledger = {}

    if compound_key in ledger:
        cached_entry = ledger[compound_key]
        cached_raw = str(cached_entry.get("response", ""))
        try:
            parsed = json.loads(cached_raw)
            if isinstance(parsed, dict):
                parsed["idempotent_replay"] = True
                parsed["idempotency_key"] = key
                parsed["payload_sha256"] = cached_entry.get("payload_sha256", "")
                return json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as exc:
            _ = exc
        return cached_raw

    result_str = compute_fn()
    digest = hashlib.sha256(result_str.encode("utf-8")).hexdigest()
    ledger[compound_key] = {
        "tool_name": tool_name,
        "idempotency_key": key,
        "payload_sha256": digest,
        "recorded_at": _utc_now_iso(),
        "response": result_str,
    }
    ledger_file.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    return result_str


class IntentBoundTokenValidator:
    """Validador determinístico de Troca de Tokens vinculada à Intenção Registrada (RFC 8693 / MCP 2026).

    Garante que o token efêmero emitido pelo servidor MCP só possa acionar exatamente a ferramenta
    (tool_name) e o recurso alvo (target_resource) declarados e assinados previamente pelo agente,
    bloqueando desvios de intenção induzidos por Prompt Injection e ataques de replay fora do TTL.
    """

    def __init__(
        self,
        secret_key: bytes | str | None = None,
        max_age_seconds: int = 300,
    ) -> None:
        raw_secret = secret_key or os.getenv("FRANKLIN_MCP_INTENT_SECRET", "mcp-auth-secret-key-2026")
        self.secret_key: bytes = raw_secret.encode("utf-8") if isinstance(raw_secret, str) else raw_secret
        self.max_age_seconds: int = max(1, int(max_age_seconds))

    def _sign_statement(self, statement: Dict[str, Any]) -> str:
        statement_bytes = json.dumps(statement, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hmac.new(self.secret_key, statement_bytes, hashlib.sha256).hexdigest()

    def create_intent_statement(
        self,
        agent_id: str,
        tool_name: str,
        target_resource: str,
        timestamp: Optional[int] = None,
    ) -> str:
        """Assina formalmente a declaração de intenção antes de solicitar acesso à ferramenta MCP."""
        clean_agent = SemanticGuard.sanitize_input(agent_id)
        clean_tool = SemanticGuard.sanitize_input(tool_name)
        clean_res = SemanticGuard.sanitize_input(target_resource)
        statement: Dict[str, Any] = {
            "agent_id": clean_agent,
            "tool_name": clean_tool,
            "target_resource": clean_res,
            "timestamp": int(time.time()) if timestamp is None else int(timestamp),
        }
        sig = self._sign_statement(statement)
        return json.dumps({"statement": statement, "sig": sig}, ensure_ascii=False)

    def validate_and_exchange(
        self,
        intent_token_str: str,
        actual_tool_call: str,
        actual_resource: str,
        now_ts: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Valida criptograficamente se a chamada real bate com a intenção registrada e emite token efêmero."""
        try:
            clean_tool = SemanticGuard.sanitize_input(actual_tool_call)
            clean_res = SemanticGuard.sanitize_input(actual_resource)
            data = json.loads(intent_token_str)
            stmt = data["statement"]
            provided_sig = str(data["sig"])
            expected_sig = self._sign_statement(stmt)

            if not hmac.compare_digest(provided_sig, expected_sig):
                return {"permitido": False, "motivo": "Assinatura de intenção forjada."}

            current_ts = int(time.time()) if now_ts is None else int(now_ts)
            stmt_ts = int(stmt.get("timestamp", 0))
            if abs(current_ts - stmt_ts) > self.max_age_seconds:
                return {
                    "permitido": False,
                    "motivo": f"Declaração de intenção expirada (TTL > {self.max_age_seconds}s).",
                }

            if stmt.get("tool_name") != clean_tool or stmt.get("target_resource") != clean_res:
                return {
                    "permitido": False,
                    "motivo": (
                        f"Desvio de intenção detectado: Declarou '{stmt.get('tool_name')}' em "
                        f"'{stmt.get('target_resource')}', mas tentou '{clean_tool}' em '{clean_res}'."
                    ),
                }

            ephemeral_digest = hmac.new(
                self.secret_key,
                f"{stmt.get('agent_id')}:{clean_tool}:{clean_res}:{stmt_ts}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()[:24]
            return {
                "permitido": True,
                "token_efemero": f"mcp_token_autorizado_{self.max_age_seconds}s_{ephemeral_digest}",
                "scope": f"mcp:tool:{clean_tool}:{clean_res}",
                "expires_in": self.max_age_seconds,
            }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, SecurityViolationError) as exc:
            return {"permitido": False, "motivo": str(exc)}





