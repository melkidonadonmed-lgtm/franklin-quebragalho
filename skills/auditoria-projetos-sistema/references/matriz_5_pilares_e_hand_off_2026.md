# Matriz dos 5 Pilares Técnicos (Padrão 2026), Regra 60-30-10 OKLCH e Orquestração de Projetos

Referência técnica de Tier 3 para `auditoria-projetos-sistema` (`v6.0.0` — fusão canônica de `auditoria-projetos-sistema`, `antigravity-project-auditor` e `nav-x-func`), detalhando os critérios de avaliação de 2026 e a fronteira operacional com `organizador-projetos-ideias` e `android-agy-projects`.

---

## 1. Fluxo Canônico da Dupla de Projetos + Módulo Android no Ecossistema Antigravity (2026)

| Etapa | Skill Canônica | Modo / Escopo | Papel Exato (Zero Sobreposição) |
| :---: | :--- | :--- | :--- |
| **1** | **`organizador-projetos-ideias`** | `Modo 1: ideation_to_v1` \| `Modo 2: project_organizer_sync` | **Concepção e Saneamento Ativo:** Triagem de intenção/MVP do zero (`ideation_to_v1`) ou criação/sincronização 1:1 dos documentos-chave (`README.md` fiel ao disco, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `DESIGN.md`), contratos (`MCP`/`FastAPI`/`RPC`) e limpeza da raiz. |
| **2** | **`auditoria-projetos-sistema`** | `Modo 1: mvp_and_plan` \| `Modo 2: deep_code_and_nav_audit` \| `Modo 3: live_dom_inspection` | **Auditoria Unificada de Projeto, Código Real, Navegação & UI (0–100 pts + SGA/TIF):** Executa `project_structure_and_code_auditor.py`, `deterministic_scorer.py` e `frontiercode_maintainability_guardrail.py`; diagnostica bloqueios de MVP (`Por quê:`), confronta `README.md`/`SPEC.md` vs. código real (`[IMPLEMENTADO_FUNCIONAL]` vs. `[INEXISTENTE_DOCUMENTADO]`), audita Navegação em 3 Camadas (`X ativa Y`), Regra `60-30-10 OKLCH` e DOM via `agent-browser` (`@eX`). |
| **2B** | **[`android-agy-projects`](../../android-agy-projects/SKILL.md)** | `MODO GREEN \| COT \| AUDIT` | **Módulo Especialista Android:** Criação de MVP Android 2026 (`libs.versions.toml`, AGP 9.x Built-in Kotlin, KSP2 `2.3.12`, Compose BOM `2026.09.00`, Navigation 3), RCA em 5 eixos (ANR, Memory Leaks, *Phase Deferral*, *Strong Skipping Mode*) e auditoria R8 Full Mode / Baseline Profiles. |

---

## 2. Critérios de Referência 2026 nos 5 Pilares Obrigatórios

| Pilar | Referência Técnica 2026 (`[PRIORIDADE]` se violado no caminho crítico) |
| :--- | :--- |
| **1. Design, UI/UX, Regra `60-30-10` & Cores `OKLCH`** | Identidade própria guiada pelo propósito do projeto (`design-md` v7.0 / SSOT): **Proporção Cromática `60-30-10`** (`60%` superfície dominante `--bg-canvas`/`--surface-canvas`, `30%` estrutura secundária `--bg-surface-1`/`--surface-card` e `--bg-surface-2`/`--surface-elevated`, `10%` acento cirúrgico `--brand-primary` ou contraste acromático), **Cores Perceptuais `OKLCH`** (`oklch(L C H / alpha)`, `light-dark()`, `color-mix(in oklab, ...)`), Dark Mode sem `#000000` puro ($L = 0.16 \to 0.22 \to 0.27$), **Iluminação Zenital (90°–120° com `inset 0 1px 0 0`)**, **Sombras Multi-Camadas em 3 Níveis** (`--shadow-elevation-1..3`: Umbra + Penumbra com `spread` negativo + Borda Especular), **6 Arquétipos Espaciais** + `@container`, **Navegação em 3 Camadas** (`<= 3 <nav>`, menus `>= 13px`, `X ativa Y`), travas anti-borrão (`antialiased`, `font-synthesis: none`, zero `scale()` fracionário em texto), `tabular-nums`, WCAG 2.1 AA ($\ge 4.5:1$), alvos $\ge 44\times44\text{px}$ e Engenharia Real-State (zero placebos). |
| **2. Segurança (AppSec & IA)** | Segredos exclusivamente em `.env` (com `.env.example` limpo e `.gitignore` estrito), validação de fronteira (`Pydantic v2` `extra="forbid"`, `Zod`), sanitização anti-XSS (`DOMPurify`) e isolamento Zero-Trust contra Prompt Injection em ferramentas e agentes. |
| **3. Atualização Temporal** | Runtimes e SDKs vigentes conforme contexto da sessão e docs/MCP oficiais: Python `3.12+` gerenciado via `uv`, SDK oficial `google-genai` (modelos atuais configurados pelo projeto, ex.: família Gemini 4), `FastMCP` / MCP Spec `2026-07-28`, `a2a-sdk` `1.0+` (assinatura JCS/JWS), TypeScript `5+` / Node LTS, Go `1.24+`. Consulta condicional via `gemini_search_docs` e `audit-websocket-jsonrpc.md` quando aplicável. |
| **4. Qualidade de Código Real (AST)** | Verificação obrigatória no código-fonte real (`project_structure_and_code_auditor.py` + `frontiercode_maintainability_guardrail.py`): modularidade por coesão (funções $\le 60$ linhas, McCabe $M \le 10$), tipagem estrita (zero `any`, `dataclass(frozen=True)` / `BaseModel`), proibição de `except:` genérico ou funções placebo (`pass`, `onClick={() => {}}`), e zero arquivos órfãos. |
| **5. Árvore Física, Navegação & Componentes** | Raiz limpa (apenas manifestos e documentos-chave `README.md`, `AGENTS.md`, `.context/spec.md`, `.context/context.md`, `CURRENT_STATE.md`), pasta `rules/` versionada, separação clara em `src/`, `scripts/`, `tests/` e governança de abas em UI (permitidas para domínios distintos; proibidas abas de função duplicada, sub-abas aninhadas ou componentes de backend expostos em abas). |

