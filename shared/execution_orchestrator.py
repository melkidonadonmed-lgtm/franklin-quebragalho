"""
execution_orchestrator.py
Motor de execução segura de scripts de skills, planos DAG (Epic-Volta),
governança HITL (SemanticGuard / CheckpointStore / Harness²) e protocolo A2A v1.0.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shared.a2a_bridge import (
    FranklinA2ATaskManager,
    build_franklin_agent_card,
    verify_agent_card_signature,
)
from shared.catalog_service import (
    EPIC_VOLTA_DIR,
    ROOT_DIR,
    SKILLS_ROOT,
    _find_skill_dir,
    _get_all_skills_data,
)
from shared.harness import (
    CheckpointStore,
    RiskLevel,
    SecurityViolationError,
    SemanticGuard,
    dispatch_harness2_action,
    evaluate_action_risk,
)


def _build_script_command(script_path: Path, args: Optional[List[str]]) -> Optional[List[str]]:
    """Monta a lista de argumentos de comando segura conforme a extensão do script."""
    suffix = script_path.suffix.lower()
    if suffix == ".py":
        cmd = [sys.executable, str(script_path)]
    elif suffix == ".js":
        cmd = ["node", str(script_path)]
    elif suffix == ".ps1":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    elif suffix in (".cmd", ".bat"):
        cmd = ["cmd.exe", "/c", str(script_path)]
    else:
        return None
    if args:
        cmd.extend(args)
    return cmd


def run_skill_script_impl(
    skill_name: str,
    script_name: str,
    args: Optional[List[str]] = None,
    timeout_seconds: int = 60,
) -> str:
    """Executa de forma segura um script utilitário associado a uma skill ou ao workspace."""
    if ".." in script_name or "/" in script_name or "\\" in script_name:
        return "Erro de Segurança: Nome de script inválido (Path Traversal detectado)."

    if skill_name.lower() in ("workspace", "root", "global"):
        target_dir = ROOT_DIR / "scripts"
    else:
        skill_dir = _find_skill_dir(skill_name)
        if not skill_dir:
            return f"Erro: Skill '{skill_name}' não encontrada."
        target_dir = skill_dir / "scripts"

    script_path = target_dir / script_name
    if not script_path.exists():
        return f"Erro: Script '{script_name}' não existe em {target_dir}."

    cmd = _build_script_command(script_path, args)
    if not cmd:
        return f"Erro: Extensão de script '{script_path.suffix}' não suportada para execução direta."

    try:
        res = subprocess.run(
            cmd, capture_output=True, text=True, errors="replace",
            timeout=timeout_seconds, cwd=str(ROOT_DIR), shell=False,
        )
        out = res.stdout.strip()
        if res.stderr:
            out += "\n--- STDERR ---\n" + res.stderr.strip()
        return f"[Exit Code: {res.returncode}]\n{out if out else '(Script executado sem retorno textual)'}"
    except subprocess.TimeoutExpired:
        return f"Erro: Execução excedeu o tempo limite de {timeout_seconds} segundos."
    except (OSError, ValueError, RuntimeError) as e:
        return f"Erro ao executar script: {e}"


def _apply_target_dir_to_task(t_item: Any, clean_target: str) -> None:
    """Injeta target_dir no payload e input_data de um item de task do DAG."""
    if not isinstance(t_item, dict):
        return
    payload = t_item.setdefault("payload", {})
    if isinstance(payload, dict) and not payload.get("target_dir"):
        payload["target_dir"] = clean_target
    input_data = t_item.get("input_data")
    if isinstance(input_data, dict) and not input_data.get("target_dir"):
        input_data["target_dir"] = clean_target


def _inject_target_dir_into_plan(plan_dict: Dict[str, Any], target_dir: str) -> Tuple[Path, Path]:
    """Injeta target_dir nos payloads das tasks do DAG e persiste em arquivo temporário."""
    clean_target = target_dir.strip()
    if clean_target and isinstance(plan_dict.get("tasks"), list):
        for t_item in plan_dict["tasks"]:
            _apply_target_dir_to_task(t_item, clean_target)
    temp_dir = ROOT_DIR / ".sessions" / "temp_plans"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file = temp_dir / f"plan_{uuid.uuid4().hex[:8]}.json"
    temp_file.write_text(json.dumps(plan_dict, indent=2, ensure_ascii=False), encoding="utf-8")
    return temp_file.resolve(), temp_file


def _resolve_dag_plan_file(plan_str: str, target_dir: str = "") -> Tuple[Optional[Path], Optional[Path], Optional[str]]:
    """Resolve o arquivo de plano DAG por alias, caminho existente ou JSON inline temporário."""
    plan_aliases = {
        "ui": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "frontend": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "3+1": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition_dag": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "ui_composition_dag.json": ROOT_DIR / "plans" / "ui_composition_dag.json",
        "physics": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "3d": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "fisica": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit_dag": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "physics_code_audit_dag.json": ROOT_DIR / "plans" / "physics_code_audit_dag.json",
        "sample": EPIC_VOLTA_DIR / "examples" / "sample_dag_plan.json",
        "sample_dag_plan.json": EPIC_VOLTA_DIR / "examples" / "sample_dag_plan.json",
    }
    matched_file: Optional[Path] = None
    if plan_str.lower() in plan_aliases and plan_aliases[plan_str.lower()].is_file():
        matched_file = plan_aliases[plan_str.lower()].resolve()
    else:
        for cp in (
            Path(plan_str), ROOT_DIR / plan_str, ROOT_DIR / "plans" / plan_str,
            EPIC_VOLTA_DIR / plan_str, EPIC_VOLTA_DIR / "examples" / plan_str,
            Path(r"C:\Users\melki\.gemini\plans") / plan_str,
        ):
            if cp.exists() and cp.is_file():
                matched_file = cp.resolve()
                break

    if matched_file is not None:
        if target_dir.strip():
            parsed_file = json.loads(matched_file.read_text(encoding="utf-8"))
            resolved, tmp = _inject_target_dir_into_plan(parsed_file, target_dir)
            return resolved, tmp, None
        return matched_file, None, None

    try:
        parsed = json.loads(plan_str)
        if not isinstance(parsed, dict):
            return None, None, json.dumps({"status": "INVALID_PLAN", "error": "O payload JSON deve ser um objeto compatível com DAGExecutionPlan."}, ensure_ascii=False)
        resolved, tmp = _inject_target_dir_into_plan(parsed, target_dir)
        return resolved, tmp, None
    except json.JSONDecodeError as exc:
        return None, None, json.dumps({"status": "FILE_NOT_FOUND_OR_INVALID_JSON", "error": f"Não foi possível localizar o arquivo nem interpretar como JSON válido: {exc}"}, ensure_ascii=False)


def _build_dag_cli_cmd(resolved_plan_path: Path, run_id: str, resume: bool, timeout_seconds: float, db_path: str) -> List[str]:
    """Monta a lista de argumentos CLI para invocar o orchestrator.cli do Epic-Volta."""
    cmd = ["uv", "--directory", str(EPIC_VOLTA_DIR), "run", "python", "-m", "orchestrator.cli", str(resolved_plan_path), "--json"]
    if run_id.strip():
        cmd.extend(["--run-id", run_id.strip()])
    if resume:
        cmd.append("--resume")
    if timeout_seconds > 0:
        cmd.extend(["--timeout", str(timeout_seconds)])
    if db_path.strip():
        cmd.extend(["--db", db_path.strip()])
    return cmd


def execute_dag_impl(
    plan_path_or_json: str,
    run_id: str = "",
    resume: bool = False,
    timeout_seconds: float = 0,
    db_path: str = "",
    target_dir: str = "",
) -> str:
    """Executa um plano de orquestração em grafo acíclico dirigido (DAG) via motor do Epic-Volta."""
    if not EPIC_VOLTA_DIR.exists():
        return json.dumps({"status": "FAILED", "error": f"Repositório Epic-Volta não encontrado em {EPIC_VOLTA_DIR}."}, ensure_ascii=False)

    resolved_plan_path, temp_file, err_json = _resolve_dag_plan_file(plan_path_or_json.strip(), target_dir=target_dir)
    if err_json or not resolved_plan_path:
        return err_json or json.dumps({"status": "FAILED", "error": "Plano inválido."}, ensure_ascii=False)

    cmd = _build_dag_cli_cmd(resolved_plan_path, run_id, resume, timeout_seconds, db_path)
    try:
        res = subprocess.run(
            cmd, capture_output=True, text=True, errors="replace",
            timeout=timeout_seconds + 30 if timeout_seconds > 0 else 120,
            cwd=str(EPIC_VOLTA_DIR), shell=False,
        )
        stdout = res.stdout.strip()
        if res.returncode == 0:
            return stdout or json.dumps({"status": "COMPLETED", "note": "Sem saída stdout"}, ensure_ascii=False)
        return stdout if stdout.startswith("{") else json.dumps({"status": "FAILED", "exit_code": res.returncode, "stdout": stdout, "stderr": res.stderr.strip()}, ensure_ascii=False)
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "TIMEOUT", "error": f"Execução do DAG excedeu o limite de {timeout_seconds} segundos."}, ensure_ascii=False)
    except (OSError, ValueError, RuntimeError) as e:
        return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    finally:
        if temp_file:
            temp_file.unlink(missing_ok=True)


def _match_best_skill_for_harness(combined_query: str) -> Tuple[str, str]:
    """Identifica a skill e persona mais aderentes à intenção para o Harness HITL."""
    best_skill: Optional[Dict[str, Any]] = None
    max_score = 0
    for s in _get_all_skills_data():
        score = 20 if s["name"].lower() in combined_query else 0
        for tag in s.get("tags", []):
            if len(tag) > 3 and tag.lower() in combined_query:
                score += len(tag)
        if score > max_score:
            max_score = score
            best_skill = s
    if best_skill:
        return best_skill["name"], best_skill["persona"]
    return "franklin-main", "Franklin-Main"


def harness_guard_impl(
    harness_store: CheckpointStore,
    task_intent: str,
    proposed_tool_or_action: str = "",
    session_id: str = "default",
) -> str:
    """Aplica o Harness de Governança Determinística e Human-in-the-Loop antes de executar ações."""
    try:
        clean_intent = SemanticGuard.sanitize_input(task_intent)
        clean_action = SemanticGuard.sanitize_input(proposed_tool_or_action) if proposed_tool_or_action else ""
    except SecurityViolationError as e:
        return json.dumps({
            "status": "BLOCKED",
            "riskLevel": "CRITICAL",
            "reason": str(e),
            "instructions": "Execução terminantemente bloqueada pelo SemanticGuard fora da janela do LLM.",
        }, indent=2, ensure_ascii=False)

    active_skill_name, persona = _match_best_skill_for_harness(f"{clean_intent} {clean_action}".lower())
    risk_level, risk_reason = evaluate_action_risk(f"{clean_intent} {clean_action}")

    if risk_level == RiskLevel.CRITICAL:
        chk_id = f"chk-{uuid.uuid4().hex[:8]}"
        harness_store.create(
            checkpoint_id=chk_id, session_id=session_id, task_intent=clean_intent,
            proposed_action=clean_action or "Ação de mutação no sistema",
            active_skill=active_skill_name, risk_level="CRITICAL", notes=risk_reason,
        )
        return json.dumps({
            "status": "APPROVAL_REQUIRED", "riskLevel": "CRITICAL", "checkpointId": chk_id,
            "activeSkill": active_skill_name, "persona": persona, "reason": risk_reason,
            "instructions": (
                f"AÇÃO CRÍTICA DETECTADA: O Harness pausou a execução para proteger o sistema. "
                f"Checkpoint registrado sob o ID '{chk_id}'. "
                f"OBRIGATÓRIO: Apresente o plano / simulação (Dry-Run) com a lista dos itens impactados ao usuário e solicite "
                f"sua aprovação expressa antes de executar. Para aprovar, use 'franklin_harness_checkpoint(action=\"approve\", checkpoint_id=\"{chk_id}\")'."
            ),
        }, indent=2, ensure_ascii=False)

    return json.dumps({
        "status": "AUTHORIZED", "riskLevel": "LOW", "activeSkill": active_skill_name,
        "persona": persona, "reason": risk_reason,
        "instructions": f"Operação segura autorizada pelo Harness sob a persona {persona}. Siga os procedimentos e salvaguardas da skill '{active_skill_name}'.",
    }, indent=2, ensure_ascii=False)


def _mutate_checkpoint_status(harness_store: CheckpointStore, checkpoint_id: str, target_status: str, notes: str) -> str:
    """Aprova ou rejeita um checkpoint no CheckpointStore."""
    if not checkpoint_id:
        return json.dumps({"error": f"checkpoint_id é obrigatório para status '{target_status}'"}, ensure_ascii=False)
    default_note = "Aprovado pelo operador" if target_status == "APPROVED" else "Rejeitado pelo operador"
    rec = harness_store.update_status(checkpoint_id, status=target_status, notes=notes or default_note)
    if not rec:
        return json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
    msg = (
        f"Ação '{rec.proposed_action}' foi APROVADA pelo operador humano. A execução pode prosseguir."
        if target_status == "APPROVED"
        else f"Ação '{rec.proposed_action}' foi VETADA pelo operador humano. A execução está cancelada."
    )
    return json.dumps({"status": target_status, "checkpointId": checkpoint_id, "message": msg, "record": rec.to_dict()}, indent=2, ensure_ascii=False)


def harness_checkpoint_impl(
    harness_store: CheckpointStore,
    sessions_dir: Path,
    action: str = "list",
    session_id: str = "default",
    checkpoint_id: str = "",
    notes: str = "",
) -> str:
    """Gerencia checkpoints de governança HITL e sub-ações recursivas Harness²."""
    act = action.strip().lower()
    h2_res = dispatch_harness2_action(act, notes, sessions_dir)
    if h2_res is not None:
        return h2_res
    if act == "list":
        pending = harness_store.list(status="PENDING", session_id=session_id if session_id != "all" else None)
        return json.dumps({"totalPending": len(pending), "checkpoints": [r.to_dict() for r in pending]}, indent=2, ensure_ascii=False)
    if act == "get":
        if not checkpoint_id:
            return json.dumps({"error": "checkpoint_id é obrigatório para a ação 'get'"}, ensure_ascii=False)
        rec = harness_store.get(checkpoint_id)
        return json.dumps(rec.to_dict(), indent=2, ensure_ascii=False) if rec else json.dumps({"error": f"Checkpoint '{checkpoint_id}' não encontrado"}, ensure_ascii=False)
    if act == "approve":
        return _mutate_checkpoint_status(harness_store, checkpoint_id, "APPROVED", notes)
    if act == "reject":
        return _mutate_checkpoint_status(harness_store, checkpoint_id, "REJECTED", notes)
    if act == "clear":
        return json.dumps({"status": "CLEARED", "removedCount": harness_store.clear()}, indent=2, ensure_ascii=False)
    return json.dumps({"error": f"Ação '{action}' inválida. Use: list, get, approve, reject, clear, validate_tree, evolve ou record_experience."}, ensure_ascii=False)


def a2a_agent_card_impl(skill_filter: str = "", verify_signature: bool = True) -> str:
    """Gera e assina criptograficamente (JCS + JWS HMAC-SHA256) o AgentCard oficial A2A v1.0 do Franklin."""
    card = build_franklin_agent_card(skills_dir=SKILLS_ROOT, skill_filter=skill_filter, sign=True)
    card["signatureVerified"] = verify_agent_card_signature(card) if verify_signature else True
    return json.dumps(card, indent=2, ensure_ascii=False)


def a2a_dispatch_task_impl(
    a2a_task_manager: FranklinA2ATaskManager,
    query: str = "",
    skill_id: str = "",
    context_id: str = "ctx-default",
    task_id: str = "",
    action: str = "send",
    execute_dag: bool = False,
    target_dir: str = "",
) -> str:
    """Despacha, consulta ou cancela uma Task no protocolo Agent2Agent (A2A v1.0) acoplado ao Harness HITL."""
    act = action.strip().lower()
    if act == "send":
        task = a2a_task_manager.submit_task(query=query, skill_id=skill_id, context_id=context_id, task_id=task_id.strip() or None)
        if execute_dag and isinstance(task, dict):
            resolved_skill = str(task.get("metadata", {}).get("skillId") or skill_id).lower()
            dag_alias = "physics" if "physics" in resolved_skill or "3d" in query.lower() else "ui"
            dag_raw = execute_dag_impl(dag_alias, target_dir=target_dir)
            try:
                task["dagExecution"] = json.loads(dag_raw)
            except json.JSONDecodeError:
                task["dagExecution"] = {"raw": dag_raw}
        return json.dumps(task, indent=2, ensure_ascii=False)

    if act in ("get", "cancel"):
        if not task_id.strip():
            return json.dumps({"error": f"task_id é obrigatório para action='{act}'"}, ensure_ascii=False)
        found = a2a_task_manager.get_task(task_id.strip()) if act == "get" else a2a_task_manager.cancel_task(task_id.strip())
        if not found:
            return json.dumps({"error": f"Task A2A '{task_id}' não encontrada"}, ensure_ascii=False)
        return json.dumps(found, indent=2, ensure_ascii=False)

    return json.dumps({"error": f"Ação A2A '{action}' inválida. Use: send, get ou cancel."}, ensure_ascii=False)
