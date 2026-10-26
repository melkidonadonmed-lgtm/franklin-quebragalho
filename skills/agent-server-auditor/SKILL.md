---
name: agent-server-auditor
description: >-
  Audita estaticamente sistemas agênticos, servidores MCP (Model Context Protocol 2026-07-28) e nós A2A (Agent-to-Agent v1.0) em Go, TypeScript e Python. Use para inspecionar higiene de binários, STDIO stdout, AgentCard JWS, travas max_steps em loops ReAct/StateGraph/ADK e persistir memories/audit_report.json; não use para testes dinâmicos de UI ou suítes unitárias AAA.
version: "1.0.0"
date: "2026-10-26"
updated_at: "2026-10-26"
license: MIT
author: "SkillCraft, Franklin-Main & Melki"
category: "Agent Architecture, Protocol Compliance & Static Code Auditing"
compatibility: Python 3.11+, TypeScript 5+, Go 1.22+, MCP Spec 2026-07-28, A2A v1.0, Google ADK 2.x, LangGraph, CrewAI
metadata:
  version: "1.0.0"
  author: "SkillCraft, Franklin-Main & Melki"
  category: "Agent Architecture, Protocol Compliance & Static Code Auditing"
  updated_at: "2026-10-26"
  protocols: "MCP (Model Context Protocol), A2A (Agent-to-Agent Protocol), JSON-RPC 2.0"
  supported_languages: "Go, TypeScript, Python"
  standards: "Agent Skills (SKILL.md), Zero-Trust Agent Architecture, OWASP GenAI 2026"
  tags:
    - "agent-server-auditor"
    - "mcp-2026-07-28"
    - "a2a-protocol"
    - "agent-card-jws"
    - "stdio-hygiene"
    - "max-steps"
    - "binary-hygiene"
    - "audit-report"
---

# 🕵️‍♂️ Skill: `agent-server-auditor` — Auditoria Arquitetural de Agentes e Servidores (`v1.0.0`)

## 1. Objetivo e Missão Arquitetural
A Skill **`agent-server-auditor`** fornece uma esteira determinística e padronizada de inspeção estática, conformidade de protocolos e validação estrutural para ecossistemas de agentes autônomos.

Atuando a partir da raiz do projeto (`root_dir`), esta Skill resolve os seguintes gargalos críticos da engenharia de IA:
1. **Desorganização Estrutural e Dispersão de Contexto:** Falta de separação canônica entre orquestradores, subagentes especialistas, manifestos de skills (`SKILL.md`) e artefatos compilados.
2. **Quebra de Protocolos em Servidores (MCP & A2A):** Poluição do canal `stdout` em servidores MCP via STDIO, ausência de descoberta estruturada, omissão de schemas estritos ou ausência de Cartões de Agente A2A (`agent-card.json`) assinados.
3. **Loops Cognitivos Desgovernados:** Agentes configurados sem travas de profundidade (`max_steps`), sem critérios objetivos de parada verificáveis e sem correspondência fidedigna entre a descrição da função e sua implementação real.
4. **Falta de Memória Auditável:** Execuções efêmeras sem registro de metadados estruturados para rastreabilidade e governança corporativa (`memories/audit_report.json`).

---

## 2. Gatilhos de Ativação (Quando Usar)

### ✅ Quando Ativar (Gatilhos Positivos)
- Solicitação explícita para auditar a raiz da pasta de um sistema agêntico, validar agentes, inspecionar servidores MCP ou verificar conformidade A2A (`agent-card.json`).
- Pré-deploy ou homologação de novas skills e agentes nas linguagens **Go, TypeScript ou Python**.
- Diagnóstico de falhas de comunicação entre clientes e servidores de ferramentas (ex: `"JSON-RPC parser error"`, `"Tool call timeout"`, poluição de `stdout` em transporte `STDIO`).
- Auditoria de segurança de contratos de dados (`Pydantic`, `Zod`, `JSON Schema`) e verificação de travas de loop (`max_steps`, `max_turns`, `recursion_limit`).

---

## 3. Entradas, Pré-requisitos e Parâmetros

- **`--root` / `target_root` (obrigatório):** Diretório raiz do projeto agêntico a ser inspecionado (padrão: `.`).
- **`--persist` (opcional):** Quando ativado, grava o relatório JSON estruturado em `<target_root>/memories/audit_report.json` (ou no caminho indicado por `--output`).
- **`--output` (opcional):** Caminho customizado para gravação do snapshot JSON da auditoria.
- **`--self-test` (opcional):** Executa a bateria de auto-validação determinística sobre fixtures sintéticas em diretório temporário isolado.
- **Ambiente:** Python `3.11+` com `pydantic>=2.0`.

---

## 4. Procedimento Operacional Passo a Passo e Matriz de Dimensões

```text
                    ┌─────────────────────────────────────────────────────────┐
                    │          RAIZ DO PROJETO (VARREDURA RECURSIVA)          │
                    └────────────────────────────┬────────────────────────────┘
                                                 │
         ┌──────────────────────────────┬────────┴──────────────┬──────────────────────────────┐
         ▼                              ▼                       ▼                              ▼
┌──────────────────┐          ┌──────────────────┐    ┌──────────────────┐          ┌──────────────────┐
│ 1. HIGIENE &     │          │ 2. AGENTES &     │    │ 3. SERVIDORES    │    ┌─────┤ 4. CONTRATOS &   │
│    BINÁRIOS      │          │    LOOPS         │    │    MCP & A2A     │    │     │    MEMÓRIA       │
├──────────────────┤          ├──────────────────┤    ├──────────────────┤    │     ├──────────────────┤
│• .gitignore      │          │• Go / TS / Py    │    │• MCP 2026-07-28  │    │     │• JSON Schema     │
│• .env.example    │          │• ReAct / CoT     │    │• Higiene STDIO   │    │     │• Zod / Pydantic  │
│• bin/ / dist/    │          │• StateGraph/ADK  │    │• A2A Agent Card  │    │     │• max_steps       │
│• Sem blobs soltos│          │• Skills próprios │    │• Task Lifecycle  │    │     │• audit_report    │
└──────────────────┘          └──────────────────┘    └──────────────────┘    │     └──────────────────┘
                                                                              ▼
                                                               ┌───────────────────────────────┐
                                                               │ RELATÓRIO & SNAPSHOT MEMÓRIA  │
                                                               └───────────────────────────────┘
```

### Dimensão 1: Higiene da Raiz e Organização de Binários
- **Proteção de Segredos:** Verificação da presença de `.gitignore`, `.env.example` e ausência de chaves de API commitadas.
- **Segregação de Artefatos Compilados:** Binários nativos (`ELF`, `Mach-O`, `.exe`, `.dll`, `.so`, `.dylib`), pacotes Electron (`.asar`) ou bundles compilados devem residir estritamente em pastas designadas (`bin/`, `dist/`, `build/`), jamais dispersos no diretório raiz ou de código-fonte.

### Dimensão 2: Agentes Próprios e Skills Modulares
- **Estrutura Canônica de Skills (`SKILL.md`):**
  - Existência obrigatória do manifesto `SKILL.md` em `skills/<nome>/` ou `.claude/skills/<nome>/`.
  - Frontmatter YAML válido contendo `name`, `description` e `version` / `compatibility`.
  - Separação modular de recursos: pasta `scripts/` para código executável determinístico, `references/` para documentação contextual e `evals/evals.json` para baterias de testes.
- **Topologia de Agentes (Go, TypeScript, Python):**
  - Identificação de orquestradores centrais e subagentes especialistas.
  - Verificação de bibliotecas reais: Google ADK 2.x (`google.golang.org/adk`, `google.adk`), LangGraph (`StateGraph`), CrewAI, Anthropic Claude SDK, OpenAI Agents SDK, FastMCP.
  - Mapeamento da correlação semântica entre descrição do papel, prompt do agente e ferramentas atribuídas.

### Dimensão 3: Protocolos de Comunicação (MCP e A2A)
- **Servidores MCP (Model Context Protocol 2026-07-28):**
  - **Stateless Core:** Cada requisição carrega versão em `_meta` (`io.modelcontextprotocol/protocolVersion`).
  - **Higiene Crítica no Transporte STDIO:** O canal `stdout` é reservado **exclusivamente** para mensagens JSON-RPC. O uso de `print()`, `console.log()` ou `fmt.Println()` para depuração no fluxo de servidor STDIO corrompe o parser do host; logs devem ser canalizados para `stderr` (`sys.stderr`, `console.error`, `os.Stderr`) ou drivers de log estruturados.
  - **Primitivas Expostas:** Declaração explícita de `tools`, `resources` e `prompts`.
  - **Segurança de Transporte HTTP/SSE:** Validação de OAuth 2.1, Resource Indicators e proteção contra SSRF e DNS Rebinding.
- **Nós e Servidores A2A (Agent-to-Agent Protocol v1.0):**
  - **Cartão de Agente (`/.well-known/agent-card.json` ou `agent_card.json`):** Campos obrigatórios: `name`, `description`, `version`, `supportedInterfaces` (com `protocolBinding: "JSONRPC"` ou `"gRPC"`), `defaultInputModes`, `defaultOutputModes` e catálogo de `skills`.
  - **Segurança e Identidade:** Suporte a `signatures` JWS (RFC 7515 sobre RFC 8785) ou `securitySchemes` para prevenir falsificação de identidade (*impersonation*).
  - **Máquina de Estados de Tarefas:** Transições canônicas (`TASK_STATE_SUBMITTED` $\rightarrow$ `WORKING` $\rightarrow$ `INPUT_REQUIRED` $\rightarrow$ `COMPLETED` / `FAILED` / `REJECTED`).
  - **Preservação da Opacidade:** Blindagem de raciocínio interno (Chain-of-Thought privado e ferramentas internas opacas ao chamador externo).

### Dimensão 4: Loops Cognitivos, Grafos e Contratos
- **Padrões de Raciocínio Suportados:**
  - **ReAct (Reasoning + Acting):** Ciclo iterativo `pensamento` $\rightarrow$ `ação (tool_use)` $\rightarrow$ `observação (tool_result)`.
  - **Chain-of-Thought (CoT) & Tree of Thoughts:** Decomposição em etapas sequenciais com nós de avaliação.
  - **Grafos de Estado e Workflows Cíclicos:** Definição formal de nós de processamento, arestas condicionais e pontos de intervenção humana (*Human-in-the-Loop* - HITL).
- **Travas Operacionais e Critérios de Parada:**
  - Parâmetro limitador de iterações (`max_steps`, `max_turns`, `max_retries`, `max_iterations` ou `recursion_limit`).
  - Detector de repetições/loops infinitos sem progresso de observação.
  - Critério de parada verificável (pós-condição testada via *Read-After-Write* ou estado terminal explícito).
- **Contratos de Dados Estritos:**
  - Pydantic v2: proibição de propriedades soltas via `model_config = ConfigDict(extra="forbid")`.
  - Zod: aplicação estrita de `.strict()`.
  - JSON Schema: `additionalProperties: false`.

### Fluxo de Execução Passo a Passo e Comandos (`pwsh`)
1. **Passo 1 — Varredura da Raiz e Detecção Poliglota:** O script [`scripts/agent_server_auditor.py`](scripts/agent_server_auditor.py) inspeciona a raiz do repositório, cataloga arquivos de dependências (`pyproject.toml`, `package.json`, `go.mod`) e define as pilhas ativas.
2. **Passo 2 — Inventário de Skills e Agentes:** Mapeia recursivamente todas as subpastas contendo `SKILL.md` e cataloga classes e funções construtoras de agentes.
3. **Passo 3 — Inspeção de Servidores e Contratos:** Examina manipuladores de transporte JSON-RPC para MCP e endpoints de Cartões A2A, verificando vazamentos de streams e rigidez de esquemas.
4. **Passo 4 — Diagnóstico de Gaps e Emissão de Alertas:** Classifica as inconformidades em **CRÍTICO**, **ALTO** e **MÉDIO**.
5. **Passo 5 — Serialização com Metadados e Persistência em Memória:** Compila o relatório técnico completo e persiste o snapshot estruturado em `memories/audit_report.json`.

```powershell
# 1. Auditar um repositório e exibir o relatório JSON
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --root . --json

# 2. Auditar e persistir o snapshot em memories/audit_report.json
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --root . --persist --json

# 3. Executar auto-teste determinístico (Self-Test)
uv run python skills/agent-server-auditor/scripts/agent_server_auditor.py --self-test
```

---

## 5. Estrutura Canônica Esperada (Diagrama Arquitetural)

```text
projeto-agentico-raiz/
├── .gitignore                         # Bloqueio estrito de segredos, venv e caches
├── .env.example                       # Template público de variáveis de ambiente
├── .geminiignore                      # Isolamento contra indexação de credenciais locais
├── pyproject.toml / go.mod / package.json # Lockfiles de dependências travados
├── bin/                               # Destino exclusivo de executáveis e binários compilados
├── agents/                            # Módulos de agentes autônomos (orchestrator, subagents)
├── skills/                            # Catálogo modular de Skills autocontidas
│   └── agent-server-auditor/
│       ├── SKILL.md                   # Manifesto declarativo com YAML frontmatter
│       ├── rules/
│       │   └── criterios_auditoria.md # Critérios determinísticos [PASS] / [FAIL]
│       ├── scripts/
│       │   └── agent_server_auditor.py # Motor estático poliglota (Go, TS, Py, MCP, A2A)
│       ├── references/
│       │   └── protocol_matrix.md     # Rubricas de protocolos MCP 2026-07-28 e A2A v1.0
│       └── evals/
│           └── evals.json             # Baterias de teste automatizadas
├── mcp_servers/                       # Servidores de ferramentas (Model Context Protocol)
├── .well-known/
│   └── agent-card.json                # Cartão de identidade pública A2A v1.0 assinado com JWS
├── memories/
│   └── audit_report.json              # Snapshot persistente da última auditoria
└── tests/                             # Suíte de testes determinísticos
```

---

## 6. Saídas, Entregáveis e Esquema Persistido em Memória

A saída gerada e gravada em `memories/audit_report.json` segue rigorosamente este contrato de dados:

```json
{
  "timestamp": "2026-10-26T10:15:00Z",
  "audit_version": "1.0.0",
  "target_root": "/workspace/meu-projeto",
  "summary": {
    "compliance_score": 88.5,
    "status": "CONFORME_COM_RESSALVAS",
    "detected_languages": ["Python", "TypeScript", "Go"],
    "total_agents": 3,
    "total_skills": 2,
    "total_mcp_servers": 1,
    "total_a2a_cards": 1
  },
  "binary_hygiene": {
    "has_dedicated_bin_dir": true,
    "compiled_artifacts_count": 0,
    "status": "APPROVED"
  },
  "audit_details": {
    "agents": [
      {
        "name": "orchestrator",
        "file": "agents/orchestrator.py",
        "language": "Python",
        "framework": "Google ADK 2.x",
        "reasoning_pattern": "ReAct (Reasoning + Acting)",
        "has_max_steps": true,
        "has_stop_condition": true,
        "type_safety": true,
        "missing_elements": []
      }
    ],
    "skills": [
      {
        "name": "agent-server-auditor",
        "path": "skills/agent-server-auditor",
        "has_frontmatter": true,
        "has_scripts": true,
        "has_references": true,
        "has_evals": true,
        "missing_elements": []
      }
    ],
    "mcp_servers": [
      {
        "name": "db_connector",
        "file": "mcp_servers/db_connector/server.py",
        "transport": "STDIO",
        "stdout_hygiene": "CLEAN",
        "strict_contracts": true,
        "missing_elements": []
      }
    ],
    "a2a_nodes": [
      {
        "card_path": ".well-known/agent-card.json",
        "name": "finance-analyst",
        "has_supported_interfaces": true,
        "has_skills_catalog": true,
        "has_jws_signatures": true,
        "missing_elements": []
      }
    ]
  },
  "gap_analysis": {
    "critical_missing_structures": [],
    "warnings": [
      "Subagente 'intent_diagnostician.py' não declara timeout explícito para chamadas de ferramentas."
    ]
  }
}
```

---

## 7. Limites, Exceções, Guardrails e Quality Gates (Quando NÃO Usar)

### ❌ Exclusões e Quando NÃO Usar
- **Não executar testes dinâmicos invasivos:** Não executa chamadas externas descontroladas ou comandos de rede que causem mutações sem aprovação prévia.
- **Não usar para substituir suítes de testes unitários sob o padrão AAA:** Para auditar falsificabilidade de testes (`pytest`, `vitest`, `testing.T`) e *Green Build Illusion*, delegue para `test-quality-auditor`.
- **Não usar para auditoria de contraste visual, DOM ou CSS frontend:** Para auditoria visual de interfaces web, delegue para `frontend-testing-auditor` ou `frontend-ui-ux-auditor`.

### 🛡️ Critérios de Aceite e Quality Gates
1. **Gate de Segurança de Protocolo (`AUD-MCP-01`):** Servidores MCP STDIO que utilizem `print()`, `console.log()` ou `fmt.Println()` no canal de dados `stdout` são automaticamente reprovados (`REJECTED`).
2. **Gate de Contratos de Dados (`AUD-CNT-01`):** Nenhuma ferramenta de agente deve aceitar parâmetros arbitrários sem esquema tipado (`extra="forbid"`, `.strict()` ou `additionalProperties: false`).
3. **Gate de Resiliência de Loop (`AUD-AGT-01`):** Todo agente baseado em ReAct ou Grafo de Estados deve possuir limite superior de passos (`max_steps`, `max_retries`, `recursion_limit` ou equivalente) configurado.
4. **Gate de Transparência e Memória (`AUD-MEM-01`):** O relatório final deve ser emitido acompanhado do snapshot JSON salvo no armazenamento de memória (`memories/audit_report.json`) com carimbo temporal UTC.
