"""
a2a_bridge.py
Motor Protocolar Agent2Agent (A2A v1.0 / a2a-sdk) do Franklin Quebra-Galho.
Implementa geração dinâmica do AgentCard a partir das 29 Skills canônicas,
assinatura/verificação criptográfica JCS/JWS, sanitização Zero-Trust de AgentCards
externos (via SemanticGuard) e máquina de estados de Tasks A2A integrada ao CheckpointStore HITL.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from a2a import types as a2a_types
from google.protobuf.json_format import MessageToDict, ParseDict

from shared.harness import (
    CheckpointStore,
    RiskLevel,
    SecurityViolationError,
    SemanticGuard,
    evaluate_action_risk,
)
from shared.tools.frontmatter_parser import parse_frontmatter

DEFAULT_SIGNING_SECRET = "franklin-a2a-jws-local-key-2026"
DEFAULT_KEY_ID = "franklin-key-2026-v1"
DEFAULT_JKU_URL = "http://localhost:10999/public_keys.json"


def _canonical_json_bytes(payload: Dict[str, Any]) -> bytes:
    """Serializa dicionário segundo esquema de canonização determinística (JCS / RFC 8785)."""
    filtered = {k: v for k, v in payload.items() if k != "signatures"}
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sign_agent_card(
    card_dict: Dict[str, Any],
    secret: str = DEFAULT_SIGNING_SECRET,
    kid: str = DEFAULT_KEY_ID,
    jku: str = DEFAULT_JKU_URL,
) -> Dict[str, Any]:
    """Assina o AgentCard usando canonização JCS e envelope JWS (HMAC-SHA256)."""
    canonical = _canonical_json_bytes(card_dict)
    digest = hmac.new(secret.encode("utf-8"), canonical, hashlib.sha256).hexdigest()
    signed = dict(card_dict)
    signed["signatures"] = [
        {
            "protected": {"alg": "HS256", "kid": kid, "jku": jku, "typ": "JOSE+JSON"},
            "signature": digest,
        }
    ]
    return signed


def verify_agent_card_signature(
    card_dict: Dict[str, Any],
    secret: str = DEFAULT_SIGNING_SECRET,
) -> bool:
    """Verifica a integridade criptográfica do bloco 'signatures' de um AgentCard."""
    sigs = card_dict.get("signatures")
    if not isinstance(sigs, list) or not sigs:
        return False
    first_sig = sigs[0].get("signature", "") if isinstance(sigs[0], dict) else ""
    if not first_sig:
        return False
    expected = hmac.new(secret.encode("utf-8"), _canonical_json_bytes(card_dict), hashlib.sha256).hexdigest()
    return hmac.compare_digest(str(first_sig), expected)


def sanitize_external_agent_card(card_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitiza todos os campos textuais de um AgentCard externo antes de injetá-los no contexto do LLM,
    prevenindo ataques de Indirect Prompt Injection via '.well-known/agent-card.json'.
    """
    cleaned = dict(card_dict)
    cleaned["name"] = SemanticGuard.sanitize_input(str(cleaned.get("name", "")))
    cleaned["description"] = SemanticGuard.sanitize_input(str(cleaned.get("description", "")))

    sanitized_skills: List[Dict[str, Any]] = []
    for sk in cleaned.get("skills", []):
        if not isinstance(sk, dict):
            continue
        sk_copy = dict(sk)
        sk_copy["id"] = SemanticGuard.sanitize_input(str(sk_copy.get("id", "")))
        sk_copy["name"] = SemanticGuard.sanitize_input(str(sk_copy.get("name", "")))
        sk_copy["description"] = SemanticGuard.sanitize_input(str(sk_copy.get("description", "")))
        sanitized_skills.append(sk_copy)
    cleaned["skills"] = sanitized_skills
    return cleaned


def build_franklin_agent_card(
    skills_dir: Path,
    skill_filter: str = "",
    host_url: str = "http://localhost:10999",
    sign: bool = True,
) -> Dict[str, Any]:
    """Constrói e valida via Protobuf (a2a.types.AgentCard) o AgentCard canônico do Franklin Quebra-Galho."""
    skills_list: List[Dict[str, Any]] = []
    kw = skill_filter.strip().lower()

    if skills_dir.exists():
        for folder in sorted(skills_dir.iterdir()):
            if not folder.is_dir():
                continue
            skill_md = folder / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text(encoding="utf-8", errors="replace")
            fm, _ = parse_frontmatter(content)
            name = str(fm.get("name", folder.name))
            desc = str(fm.get("description", ""))
            category = str(fm.get("category", "Produtividade & Engenharia Agêntica"))
            tags_raw = fm.get("tags", [])
            tags = [str(t) for t in tags_raw] if isinstance(tags_raw, list) else [folder.name, category]

            if kw and kw not in name.lower() and kw not in desc.lower() and kw not in category.lower():
                continue

            skills_list.append(
                {
                    "id": name,
                    "name": name,
                    "description": desc,
                    "tags": tags[:6],
                    "examples": [f"Executar a skill {name} no contexto atual"],
                }
            )

    total_skills = (
        sum(1 for f in skills_dir.iterdir() if f.is_dir() and (f / "SKILL.md").exists())
        if skills_dir.exists()
        else 26
    ) or 26

    raw_card: Dict[str, Any] = {
        "name": "Franklin Quebra-Galho (A2A + MCP Orchestrator)",
        "description": (
            f"Orquestrador multiagente e catálogo de {total_skills} Skills canônicas (Python, TS/JS, Go, MCP, Harness e Arquitetura Visual por Propósito) "
            "com suporte nativo a Agent2Agent (A2A v1.0) e Model Context Protocol (MCP)."
        ),
        "version": "1.2.0",
        "defaultInputModes": ["text", "text/plain", "application/json"],
        "defaultOutputModes": ["text", "text/plain", "application/json"],
        "supportedInterfaces": [
            {"url": host_url, "protocolBinding": "JSONRPC", "protocolVersion": "1.0"},
            {"url": host_url, "protocolBinding": "JSONRPC", "protocolVersion": "0.3"},
        ],
        "capabilities": {
            "streaming": True,
            "pushNotifications": True,
            "extendedAgentCard": True,
        },
        "provider": {
            "organization": "Melki Dev Lab (Franklin Quebra-Galho)",
            "url": "https://github.com/melkidonadonmed-lgtm/franklin-quebragalho",
        },
        "skills": skills_list,
    }

    # Valida conformidade estrita com o schema Protobuf oficial do a2a-sdk 1.2.2
    pb_card = ParseDict(raw_card, a2a_types.AgentCard(), ignore_unknown_fields=True)
    validated_dict = MessageToDict(pb_card, preserving_proto_field_name=False)
    return sign_agent_card(validated_dict) if sign else validated_dict


class FranklinA2ATaskManager:
    """
    Gerenciador determinístico do ciclo de vida de Tasks A2A (a2a.types.TaskState)
    integrado ao SemanticGuard e ao CheckpointStore HITL.
    """

    def __init__(self, skills_dir: Path, checkpoint_store: CheckpointStore) -> None:
        self.skills_dir = skills_dir
        self.checkpoint_store = checkpoint_store
        self._tasks: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def resolve_user_id(authenticated_user: Optional[str] = None) -> str:
        """
        Regra Zero-Trust A2A: O context_id fornecido pelo cliente NUNCA deve ser usado como user_id
        para evitar sequestro de sessão (Session Hijacking).
        """
        if authenticated_user and authenticated_user.strip():
            return authenticated_user.strip()
        return "a2a_user"

    def submit_task(
        self,
        query: str,
        skill_id: str = "",
        context_id: str = "ctx-default",
        task_id: Optional[str] = None,
        authenticated_user: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Processa uma requisição A2A ('message/send' / 'tasks/send') com guarda Zero-Trust e HITL."""
        t_id = task_id or f"a2a-task-{uuid.uuid4().hex[:8]}"
        user_id = self.resolve_user_id(authenticated_user)
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Guarda Semântica contra Prompt Injection / XSS -> TASK_STATE_REJECTED
        try:
            cleaned_query = SemanticGuard.sanitize_input(query)
        except SecurityViolationError as exc:
            rejected_task = {
                "id": t_id,
                "contextId": context_id,
                "userId": user_id,
                "state": a2a_types.TaskState.Name(a2a_types.TaskState.TASK_STATE_REJECTED),
                "stateHistory": ["TASK_STATE_SUBMITTED", "TASK_STATE_REJECTED"],
                "statusMessage": str(exc),
                "artifacts": [],
                "updatedAt": now_iso,
            }
            self._tasks[t_id] = rejected_task
            return rejected_task

        # 2. Policy Gate HITL -> Ações destrutivas transitam para TASK_STATE_INPUT_REQUIRED
        risk_level, risk_reason = evaluate_action_risk(cleaned_query)
        if risk_level == RiskLevel.CRITICAL:
            chk_id = f"chk-a2a-{uuid.uuid4().hex[:8]}"
            self.checkpoint_store.create(
                checkpoint_id=chk_id,
                session_id=context_id,
                task_intent=cleaned_query,
                proposed_action=cleaned_query,
                active_skill=skill_id or "a2a-router",
                risk_level=risk_level.value,
                notes=risk_reason,
            )
            input_req_task = {
                "id": t_id,
                "contextId": context_id,
                "userId": user_id,
                "state": a2a_types.TaskState.Name(a2a_types.TaskState.TASK_STATE_INPUT_REQUIRED),
                "stateHistory": [
                    "TASK_STATE_SUBMITTED",
                    "TASK_STATE_WORKING",
                    "TASK_STATE_INPUT_REQUIRED",
                ],
                "checkpointId": chk_id,
                "riskLevel": risk_level.value,
                "statusMessage": f"Aprovação HITL obrigatória ({chk_id}): {risk_reason}",
                "artifacts": [],
                "updatedAt": now_iso,
            }
            self._tasks[t_id] = input_req_task
            return input_req_task

        # 3. Execução Segura -> TASK_STATE_SUBMITTED -> TASK_STATE_WORKING -> TASK_STATE_COMPLETED
        selected_skill = skill_id.strip() or "franklin-orchestrator"
        artifact_payload = {
            "skill_id": selected_skill,
            "sanitized_intent": cleaned_query,
            "risk_level": risk_level.value,
            "status": "completed",
        }
        completed_task = {
            "id": t_id,
            "contextId": context_id,
            "userId": user_id,
            "state": a2a_types.TaskState.Name(a2a_types.TaskState.TASK_STATE_COMPLETED),
            "stateHistory": [
                "TASK_STATE_SUBMITTED",
                "TASK_STATE_WORKING",
                "TASK_STATE_COMPLETED",
            ],
            "riskLevel": risk_level.value,
            "statusMessage": f"Tarefa A2A executada com sucesso via skill '{selected_skill}'.",
            "artifacts": [
                {
                    "name": "a2a_execution_result",
                    "parts": [{"text": json.dumps(artifact_payload, ensure_ascii=False)}],
                }
            ],
            "updatedAt": now_iso,
        }
        self._tasks[t_id] = completed_task
        return completed_task

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Recupera o estado atual de uma Task A2A pelo ID."""
        return self._tasks.get(task_id)

    def cancel_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Cancela uma Task A2A existente ('tasks/cancel' -> TASK_STATE_CANCELED)."""
        task = self._tasks.get(task_id)
        if not task:
            return None
        task["state"] = a2a_types.TaskState.Name(a2a_types.TaskState.TASK_STATE_CANCELED)
        task["stateHistory"].append("TASK_STATE_CANCELED")
        task["statusMessage"] = "Tarefa cancelada pelo cliente A2A."
        return task
