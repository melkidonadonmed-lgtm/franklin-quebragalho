# Matriz dos 5 Pilares Técnicos (Padrão 2026) e Orquestração do Trio de Projetos

Referência técnica de Tier 3 para `antigravity-project-auditor` (`v2.0.0`), detalhando os critérios de avaliação de 2026 e a fronteira operacional com `organizador-projetos-ideias` e `auditoria-projetos-sistema`.

---

## 1. Fluxo Canônico do Trio de Projetos no Ecossistema Antigravity (2026)

| Etapa | Skill Canônica | Modo / Escopo | Papel Exato (Sem Sobreposição) |
| :---: | :--- | :--- | :--- |
| **1** | **`organizador-projetos-ideias`** | `Modo 1: ideation_to_v1` | **Concepção do Zero:** Triagem de intenção/objetivo, protocolo inteligente quando o usuário responde *"não sei"* às funções (sugerindo o MVP mínimo), definição de design/estrutura e geração da `v1.0.0` datada. |
| **2** | **`antigravity-project-auditor`** | `autonomous_scan` \| `targeted_focus` | **Diagnóstico Executivo Read-Only:** Varredura de `CONTEXT.md`, `AGENTS.md`, `SPEC.md`, `README.md` e memória; diagnóstico do que falta para o MVP com justificativa causal (`Por quê:`), matriz nos 5 pilares (`[PRIORIDADE \| MODERADO \| EXTRA]`) e Plano em 3 Fases. |
| **3** | **`organizador-projetos-ideias`** | `Modo 2: project_organizer_sync` | **Saneamento e Sincronização Ativa:** Criação/atualização dos documentos-chave (`README.md` 100% fiel ao disco, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`), diagrama Mermaid, contratos (`tools.json` MCP, FastAPI, RPC com métodos), limpeza segura da raiz (*Dry-Run*) e memória. |
| **4** | **`auditoria-projetos-sistema`** | `v3.0.0` (7 Módulos) | **Homologação Profunda (0–100 pts):** Confronto `[IMPLEMENTADO_FUNCIONAL]` vs. `[CÓDIGO_FANTASMA]`, scripts AST (`frontiercode_maintainability_guardrail.py`, `ai_ready_data_pipeline.py`), auditoria de propósito visual (`preferencias_estilo_e_temas.md`) e inspeção dinâmica via `agent-browser` (`@eX`). |

---

## 2. Critérios de Referência 2026 nos 5 Pilares Obrigatórios

| Pilar | Referência Técnica 2026 (`[PRIORIDADE]` se violado no caminho crítico) |
| :--- | :--- |
| **1. Design e UI/UX** | Seleção de atmosfera guiada pelo propósito do projeto (`preferencias_estilo_e_temas.md` e `minimal-impact-ui`: *Ad Lucem* `#F3F3F5`, *Cinza Monolítico* `#57545d` + menus `#8e8999` com tinta `#16151A`, *Preto Terminal IBM* `#070709` + `IBM Plex`, *AETHER 2027*), WCAG 2.1 AA/AAA, `tabular-nums`, alvos $\ge 44\times44\text{px}$ e zero transparências/contornos alarmistas destoantes. |
| **2. Segurança (AppSec & IA)** | Segredos exclusivamente em `.env` (com `.env.example` limpo e `.gitignore` estrito), validação de fronteira (`Pydantic v2` `extra="forbid"`, `Zod`), sanitização anti-XSS (`DOMPurify`) e isolamento Zero-Trust contra Prompt Injection em ferramentas e agentes. |
| **3. Atualização Temporal (2026)** | Runtimes e SDKs vigentes em Outubro/2026: Python `3.13–3.15` gerenciado via `uv`, SDK oficial `google-genai`, `FastMCP` / MCP Spec `2026-07-28`, `a2a-sdk` `1.2+` (assinatura JCS/JWS), Node `22–26+`, Go `1.27+`. |
| **4. Qualidade de Código** | Modularidade por coesão (funções $\le 40\text{–}60$ linhas `ARCH001`, McCabe $M \le 10$, $\le 3$ níveis de indentação), tipagem estrita (zero `any`, `dataclass(frozen=True)` / `BaseModel`), proibição de `except: pass` ou `catch` vazio, e remoção de código órfão. |
| **5. Árvore & Componentes** | Raiz limpa (apenas manifestos e documentos-chave), separação clara entre `src/components/`, `src/api/` (FastAPI/REST), `src/contracts/` (MCP `tools.json` e métodos RPC), `scripts/` e `tests/`. |
