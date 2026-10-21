#!/usr/bin/env python3
"""
mcp_test_auditor.py
Módulo Determinístico de Auditoria de Qualidade de Testes para Servidores e Clientes MCP
(Model Context Protocol — JSON-RPC 2.0, FastMCP Python, Go StdioServer e TypeScript MCP).
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from go_test_auditor import _extract_go_test_blocks, audit_go_test_file
from models import AuditIssue, FileAuditReport, classify_quality_level
from python_ast_auditor import audit_python_test_file
from ts_js_auditor import audit_ts_js_test_file

MCP_MARKERS = (
    "jsonrpc",
    "tools/list",
    "tools/call",
    "notifications/initialized",
    "FastMCP",
    "StdioServer",
    "McpStdioServer",
    "mcpserver",
    "probe_mcp_server",
    "franklin_skills_",
    "franklin_harness_",
    "franklin_execute_dag",
    "franklin_run_skill_script",
    "McpBridgeAgent",
)


def is_mcp_test_content(code_str: str, filename: str = "") -> bool:
    """Detecta se o arquivo ou código de teste exercita servidores, ferramentas ou transporte MCP."""
    lower_name = filename.lower()
    if "mcp" in lower_name or "test_server" in lower_name or "stdio_server" in lower_name:
        return True
    return any(marker in code_str for marker in MCP_MARKERS)


def _extract_python_test_blocks(code_str: str, lines: List[str]) -> List[Tuple[str, int, str]]:
    """Extrai funções de teste Python (`test_*` / `_test_*`) via AST."""
    import ast

    blocks: List[Tuple[str, int, str]] = []
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        is_fn = isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        if is_fn and (node.name.startswith("test_") or node.name.startswith("_test_")):
            end_ln = getattr(node, "end_lineno", node.lineno)
            fn_text = "\n".join(lines[node.lineno - 1 : end_ln])
            blocks.append((node.name, node.lineno, fn_text))
    return blocks


def _find_ts_block_end(lines: List[str], start_idx: int) -> int:
    """Encontra o índice da linha final de um bloco `{ ... }` em TypeScript/JavaScript."""
    depth = 0
    started = False
    for j in range(start_idx, len(lines)):
        clean = re.sub(r"//.*$", "", lines[j])
        opens = clean.count("{")
        closes = clean.count("}")
        if opens > 0:
            started = True
        depth += opens - closes
        if started and depth <= 0:
            return j
    return len(lines) - 1


def _extract_ts_test_blocks(lines: List[str]) -> List[Tuple[str, int, str]]:
    """Extrai blocos `test(...)` e `it(...)` de arquivos TypeScript/JavaScript."""
    blocks_ts: List[Tuple[str, int, str]] = []
    test_pat = re.compile(r"^\s*(?:test|it)\s*\(\s*(['\"`])(.*?)\1\s*,")
    i = 0
    while i < len(lines):
        m = test_pat.match(lines[i])
        if not m:
            i += 1
            continue
        end_i = _find_ts_block_end(lines, i)
        blocks_ts.append((m.group(2), i + 1, "\n".join(lines[i : end_i + 1])))
        i = end_i + 1
    return blocks_ts


def _extract_test_blocks_generic(code_str: str, language: str) -> List[Tuple[str, int, str]]:
    """Extrai (test_name, start_line, block_text) independente da linguagem (Python, Go ou TS/JS)."""
    lines = code_str.splitlines()
    if language == "go":
        return [(name, s_ln, "\n".join(b_lines)) for name, s_ln, _e_ln, b_lines in _extract_go_test_blocks(lines)]
    if language == "python":
        return _extract_python_test_blocks(code_str, lines)
    return _extract_ts_test_blocks(lines)


def _make_mcp_issue(
    issue_id: str,
    title: str,
    severity: str,
    filename: str,
    test_name: str,
    start_line: int,
    penalty: int,
    desc: str,
    rec: str,
) -> AuditIssue:
    """Cria uma instância padronizada de AuditIssue para testes MCP."""
    return AuditIssue(
        id=issue_id,
        title=title,
        category="Contrato & Protocolo MCP (JSON-RPC 2.0)",
        severity=severity,
        file=filename,
        test_name=test_name,
        line=start_line,
        col=1,
        penalty=penalty,
        description=desc,
        recommendation=rec,
    )


def _check_mcp_handshake_and_json_parse(
    block_text: str,
    filename: str,
    test_name: str,
    start_line: int,
) -> List[AuditIssue]:
    """Verifica handshake JSON-RPC stdio e decodificação de resposta JSON."""
    found: List[AuditIssue] = []
    if '"jsonrpc"' in block_text and '"tools/call"' in block_text:
        if '"initialize"' not in block_text:
            found.append(
                _make_mcp_issue(
                    "MCP_INCOMPLETE_STDIO_HANDSHAKE",
                    "Teste JSON-RPC MCP Sem Handshake 'initialize' Prévio",
                    "Alta", filename, test_name, start_line, 30,
                    f"[FATO] O teste MCP '{test_name}' dispara 'tools/call' via JSON-RPC sem validar o handshake 'initialize'.",
                    "Inclua a requisição 'initialize' (id=1) e 'notifications/initialized' antes de invocar 'tools/call'.",
                )
            )
        if re.search(
            r'"id"\s*:\s*\d+[^}]*"notifications/initialized"|"notifications/initialized"[^}]*"id"\s*:\s*\d+',
            block_text,
        ):
            found.append(
                _make_mcp_issue(
                    "MCP_INCOMPLETE_STDIO_HANDSHAKE",
                    "Violação JSON-RPC 2.0: Notificação 'notifications/initialized' Contendo 'id'",
                    "Alta", filename, test_name, start_line, 30,
                    f"[FATO] O teste MCP '{test_name}' envia 'notifications/initialized' com campo 'id', violando a especificação JSON-RPC 2.0.",
                    "Remova o campo 'id' de 'notifications/initialized' e valide que o servidor não emite resposta para notificações.",
                )
            )

    calls_json_mcp_tool = any(
        tok in block_text
        for tok in ('format="json"', "franklin_execute_dag(", "franklin_harness_guard(", "get_mcp_topology(")
    )
    has_json_parse = any(p in block_text for p in ("json.loads(", "json.Unmarshal(", "JSON.parse("))
    if calls_json_mcp_tool and not has_json_parse:
        found.append(
            _make_mcp_issue(
                "MCP_TAUTOLOGICAL_RAW_RESPONSE",
                "Tool MCP JSON Testada Sem Decodificação (json.loads / json.Unmarshal)",
                "Crítica", filename, test_name, start_line, 55,
                f"[FATO] O teste MCP '{test_name}' invoca uma tool que retorna payload JSON estruturado, mas não faz parse do JSON para validar o schema de saída.",
                "Decodifique o retorno com json.loads/json.Unmarshal e valide chaves contratuais exatas (ex: status, results, error).",
            )
        )
    return found


def _check_mcp_discovery_error_and_security(
    block_text: str,
    filename: str,
    test_name: str,
    start_line: int,
) -> List[AuditIssue]:
    """Verifica descoberta tools/list, código de erro JSON-RPC (-32601) e fronteira Zero-Trust."""
    found: List[AuditIssue] = []
    known_tools = (
        "go_fast_dispatch", "analyze_issue_triage", "list_workspace",
        "fetch_url", "search_files", "franklin_skills_list",
        "drive_list_files", "node_runtime_inspector", "design_mcp_with_agent_skills",
    )
    if ('"tools/list"' in block_text or "probe_mcp_server(" in block_text) and not any(
        tool_tok in block_text for tool_tok in known_tools
    ):
        found.append(
            _make_mcp_issue(
                "MCP_WEAK_TOOLS_LIST_DISCOVERY",
                "Descoberta MCP 'tools/list' Superficial (Sem Validar Nomes Canônicos de Tools)",
                "Média", filename, test_name, start_line, 25,
                f"[FATO] O teste MCP '{test_name}' inspeciona 'tools/list' ou probe de servidor sem validar o nome de nenhuma ferramenta registrada.",
                "Valide explicitamente a presença das tools críticas no manifesto retornado por 'tools/list'.",
            )
        )
    if any(err_tok in block_text for err_tok in ("nonexistent_tool", "unknown_tool", "tool_inexistente")):
        if not any(c in block_text for c in ("-32601", "Error.Code", 'error["code"]', "errResp.Error", "Erro:")):
            found.append(
                _make_mcp_issue(
                    "MCP_UNVERIFIED_ERROR_CODE_CONTRACT",
                    "Teste de Tool MCP Inexistente Sem Validar Erro JSON-RPC (-32601)",
                    "Alta", filename, test_name, start_line, 30,
                    f"[FATO] O teste MCP '{test_name}' invoca uma ferramenta inexistente mas não verifica o código JSON-RPC -32601 (Method not found).",
                    "Desempacote a resposta de erro e valide 'errResp.Error != nil && errResp.Error.Code == -32601'.",
                )
            )
    if any(sec_tok in block_text for sec_tok in ("../", "Ignore all previous instructions", "drop database")):
        if not any(v in block_text for v in ("Erro de Segurança", "BLOCKED", "APPROVAL_REQUIRED", "SecurityViolation")):
            found.append(
                _make_mcp_issue(
                    "MCP_WEAK_SECURITY_GUARD_ASSERT",
                    "Payload Adversarial MCP Sem Asserção Explícita de Bloqueio Zero-Trust",
                    "Alta", filename, test_name, start_line, 35,
                    f"[FATO] O teste MCP '{test_name}' envia payload de Path Traversal ou Prompt Injection sem validar se o status foi BLOCKED / Erro de Segurança.",
                    "Adicione asserção estrita exigindo status == 'BLOCKED' ou mensagem 'Erro de Segurança'.",
                )
            )
    return found


def _inspect_single_mcp_block(
    test_name: str,
    start_line: int,
    raw_block_text: str,
    report: FileAuditReport,
    dossier_map: Dict[str, int],
) -> None:
    """Inspeciona um único bloco de teste quanto às invariantes MCP e atualiza o dossiê."""
    meta_fns = ("audit_mcp_test_file(", "audit_go_test_file(", "audit_test_file(")
    block_text = (
        re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', '""', raw_block_text)
        if any(fn in raw_block_text for fn in meta_fns)
        else raw_block_text
    )
    if not is_mcp_test_content(block_text, ""):
        return

    candidates = _check_mcp_handshake_and_json_parse(
        block_text, report.filename, test_name, start_line
    ) + _check_mcp_discovery_error_and_security(
        block_text, report.filename, test_name, start_line
    )

    mcp_issues: List[AuditIssue] = []
    for cand in candidates:
        if not any(existing.id == cand.id and existing.test_name == test_name for existing in report.issues):
            report.issues.append(cand)
            mcp_issues.append(cand)

    if test_name in dossier_map:
        d = report.dossiers[dossier_map[test_name]]
        d.domain = f"mcp/{report.language}"
        if mcp_issues:
            for m_iss in mcp_issues:
                d.issues.append(m_iss.id)
                d.score = max(0, d.score - m_iss.penalty)
            d.level = classify_quality_level(d.score)
            d.status = "[PASS]" if len(d.issues) == 0 and d.score >= 81 else "[FAIL]"
            d.evidence = "; ".join(f"{i_id}" for i_id in d.issues)


def enrich_with_mcp_audit(report: FileAuditReport, code_str: str) -> FileAuditReport:
    """Inspeciona invariantes de protocolo MCP (JSON-RPC 2.0, Descoberta, Erros e Zero-Trust) por teste."""
    if not is_mcp_test_content(code_str, report.filename):
        return report

    blocks = _extract_test_blocks_generic(code_str, report.language)
    dossier_map: Dict[str, int] = {d.test_name: idx for idx, d in enumerate(report.dossiers)}

    for test_name, start_line, raw_block_text in blocks:
        _inspect_single_mcp_block(test_name, start_line, raw_block_text, report, dossier_map)

    report.total_inconformidades = len(report.issues)
    report.score_medio = (
        sum(d.score for d in report.dossiers) / len(report.dossiers) if report.dossiers else report.score_medio
    )
    report.nivel_espectro = classify_quality_level(report.score_medio)
    report.aprovado = report.total_inconformidades == 0 and report.score_medio >= 81.0
    return report



def audit_mcp_test_file(code_str: str, filename: str = "test_mcp_suite.py") -> FileAuditReport:
    """Ponto de entrada direto para auditar qualquer suíte de teste MCP (Python, Go ou TS/JS)."""
    if filename.endswith(".go"):
        base_report = audit_go_test_file(code_str, filename)
    elif filename.endswith((".ts", ".js", ".tsx", ".jsx")):
        base_report = audit_ts_js_test_file(code_str, filename)
    else:
        base_report = audit_python_test_file(code_str, filename)
    return enrich_with_mcp_audit(base_report, code_str)
