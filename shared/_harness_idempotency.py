"""
_harness_idempotency.py
Deterministic MCP idempotency ledger and RFC 8693 Intent-Bound Token validator
extracted from shared.harness to keep modules concise (<= 600 lines).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from shared.harness import SecurityViolationError, SemanticGuard, _utc_now_iso


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
    """Validador determinístico de Troca de Tokens vinculada à Intenção Registrada (RFC 8693 / MCP 2026)."""

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
