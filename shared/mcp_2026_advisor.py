"""
Consultor e Gerador de Arquitetura MCP 2026-07-28 (`build-with-agent-skills`).
Implementa as 3 Agent Skills oficiais (`build-mcp-server`, `build-mcp-app`, `build-mcpb`),
roteamento Elicitation vs MCP App Widget (`text/html;profile=mcp-app`), Pattern A vs Pattern B
(`search_actions` + `execute_action`), aviso de depreciação SEP-2577 e manifesto `.mcpb` v0.4.
Mantido abaixo de 300 linhas conforme diretrizes de arquitetura modular.
"""

from __future__ import annotations

from typing import Any, Dict, List


MCP_APP_MIME_TYPE = "text/html;profile=mcp-app"
SUPPORTED_MCP_SPECS = [
    "2026-07-28",
    "2025-11-25",
    "2025-06-18",
    "2025-03-26",
    "2024-11-05",
]

SDK_CATALOG_2026: Dict[str, Dict[str, Any]] = {
    "typescript": {
        "language": "typescript",
        "packages": ["@modelcontextprotocol/server", "@modelcontextprotocol/client", "zod/v4"],
        "spec_version": "2026-07-28 (v2 split packages + Standard Schema)",
        "middleware": ["@modelcontextprotocol/node", "@modelcontextprotocol/express", "@modelcontextprotocol/hono"],
    },
    "python": {
        "language": "python",
        "packages": ["mcp[cli]", "fastmcp>=3.0"],
        "spec_version": "2026-07-28 (MCPServer / FastMCP 3.x + Client structured_content)",
        "cli_commands": ["uv run mcp dev server.py", "uv run mcp run server.py --transport streamable-http"],
    },
    "go": {
        "language": "go",
        "packages": [
            "github.com/modelcontextprotocol/go-sdk/mcp",
            "github.com/modelcontextprotocol/go-sdk/jsonrpc",
            "github.com/modelcontextprotocol/go-sdk/auth",
            "github.com/modelcontextprotocol/go-sdk/oauthex",
        ],
        "spec_version": "2026-07-28 (go-sdk v1.7.0+ com tipagem genérica Input/Output)",
    },
}


def _resolve_deployment_and_skill(conn: str, aud: str, inter: str) -> tuple[str, str]:
    """Determina o modelo de deploy e a skill oficial correspondente."""
    if inter == "rich_interactive_ui" or aud == "desktop_ui_users":
        return "mcp-app", "build-mcp-app"
    if conn == "hardware_or_os":
        return "mcpb", "build-mcpb"
    if conn == "local_process_or_fs":
        if aud == "public_distribution":
            return "mcpb", "build-mcpb"
        return "local-stdio", "build-mcp-server"
    return "remote-streamable-http", "build-mcp-server"


def _resolve_interaction_and_auth(inter: str, auth: str) -> tuple[str, str]:
    """Determina o mecanismo de interação mid-call e a estratégia de autenticação."""
    if inter == "simple_structured_input":
        interaction_mechanism = "elicitation-with-capability-fallback"
    elif inter == "rich_interactive_ui":
        interaction_mechanism = "mcp-app-ui-widget"
    else:
        interaction_mechanism = "plain-tool-response"

    if auth == "oauth2":
        auth_strategy = (
            "OAuth 2.0 sobre Streamable HTTP com Client ID Metadata Document (CIMD) "
            "preferencial ou Dynamic Client Registration (DCR)"
        )
    elif auth == "api_key":
        auth_strategy = "API Key via .env local ou user_config (sensitive: true no OS Keychain do MCPB)"
    else:
        auth_strategy = "Authless (none) — apto para submissão direta ao diretório público de conectores"
    return interaction_mechanism, auth_strategy


def _build_mcpb_manifest_v04(lang: str, srv: str) -> Dict[str, Any]:
    """Gera o manifesto empacotado MCPB v0.4 para a linguagem e nome do servidor."""
    entry_map = {
        "typescript": ("node", "server/index.js", "node", ["${__dirname}/server/index.js"]),
        "python": ("python", "server/server.py", "python", ["${__dirname}/server/server.py"]),
        "go": ("binary", f"server/{srv}.exe", f"${{__dirname}}/server/{srv}.exe", []),
    }
    srv_type, entry_pt, cmd, cmd_args = entry_map.get(lang, entry_map["python"])
    return {
        "$schema": "https://raw.githubusercontent.com/anthropics/mcpb/main/schemas/mcpb-manifest-v0.4.schema.json",
        "manifest_version": "0.4",
        "name": srv,
        "version": "1.0.0",
        "description": f"Servidor MCP local empacotado ({srv}) seguindo o padrão MCPB v0.4.",
        "author": {"name": "Franklin Quebra-Galho Ecosystem"},
        "server": {
            "type": srv_type,
            "entry_point": entry_pt,
            "mcp_config": {"command": cmd, "args": cmd_args, "env": {"ROOT_DIR": "${user_config.rootDir}"}},
        },
        "user_config": {
            "rootDir": {
                "type": "directory",
                "title": "Workspace Root",
                "description": "Diretório raiz confinado com validação anti-path-traversal.",
                "default": "${HOME}/Documents",
                "required": True,
            }
        },
        "compatibility": {"claude_desktop": ">=1.0.0", "platforms": ["darwin", "win32", "linux"]},
    }


def evaluate_mcp_2026_architecture(
    connects_to: str = "cloud_api",
    audience: str = "personal_or_team",
    action_count: int = 10,
    interaction_needs: str = "plain_text_or_json",
    upstream_auth: str = "none",
    preferred_language: str = "python",
    server_name: str = "franklin-mcp-service",
) -> Dict[str, Any]:
    """Executa a Fase de Descoberta de 5 perguntas da especificação MCP 2026-07-28 (`build-with-agent-skills`)."""
    conn = connects_to.strip().lower() or "cloud_api"
    aud = audience.strip().lower() or "personal_or_team"
    inter = interaction_needs.strip().lower() or "plain_text_or_json"
    auth = upstream_auth.strip().lower() or "none"
    lang = preferred_language.strip().lower() or "python"
    srv = server_name.strip() or "franklin-mcp-service"

    deployment_model, active_skill = _resolve_deployment_and_skill(conn, aud, inter)
    tool_pattern = "one-per-action" if action_count < 15 else "search-and-execute"
    interaction_mechanism, auth_strategy = _resolve_interaction_and_auth(inter, auth)
    selected_sdk = SDK_CATALOG_2026.get(lang, SDK_CATALOG_2026["python"])

    return {
        "specVersion": "2026-07-28",
        "supportedSpecs": SUPPORTED_MCP_SPECS,
        "activeSkillRoute": active_skill,
        "deploymentModel": deployment_model,
        "toolDesignPattern": tool_pattern,
        "interactionMechanism": interaction_mechanism,
        "authStrategy": auth_strategy,
        "sdkRecommendation": selected_sdk,
        "sep2577DeprecationNotice": (
            "SEP-2577: roots, sampling e logging estão depreciados a partir da versão 2026-07-28 "
            "(mantidos por janela de compatibilidade de 12 meses)."
        ),
        "mcpAppWidgetConfig": {
            "resourceUri": f"ui://widgets/{srv}.html",
            "mimeType": MCP_APP_MIME_TYPE,
            "requiredAnnotations": ["title", "readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"],
        },
        "mcpbManifestV04": _build_mcpb_manifest_v04(lang, srv),
    }
