"""
compass_topology.py
Serviço de Topologia Multi-Repo (5 Camadas), Subagentes de UI (Topologia 3+1)
e Bússola Cognitiva (franklin_smart_compass) do Franklin Quebra-Galho.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from shared.catalog_service import AGENTS_MD_PATH, ROOT_DIR, SHREDDED_SHAPE_ROOT, _get_all_skills_data

UI_SUBAGENT_ALIASES: Dict[str, str] = {
    "analyst": "ui-analyst",
    "ui-analyst": "ui-analyst",
    "ui_analyst": "ui-analyst",
    "stage0": "ui-analyst",
    "planner": "ui-planner",
    "ui-planner": "ui-planner",
    "ui_planner": "ui-planner",
    "stage1": "ui-planner",
    "shell": "ui-planner",
    "navigator": "ui-planner",
    "onda1": "ui-planner",
    "wave1": "ui-planner",
    "ui_shell_navigator": "ui-planner",
    "worker": "ui-worker",
    "ui-worker": "ui-worker",
    "ui_worker": "ui-worker",
    "stage2": "ui-worker",
    "controls": "ui-worker",
    "data": "ui-worker",
    "onda2a": "ui-worker",
    "wave2a": "ui-worker",
    "ui_controls_data": "ui-worker",
    "motion": "ui-worker",
    "interaction": "ui-worker",
    "onda2b": "ui-worker",
    "wave2b": "ui-worker",
    "ui_motion_interaction": "ui-worker",
    "judge": "ui-judge",
    "ui-judge": "ui-judge",
    "ui_judge": "ui-judge",
    "stage3": "ui-judge",
    "observer": "ui-judge",
    "gatekeeper": "ui-judge",
    "onda3": "ui-judge",
    "wave3": "ui-judge",
    "ui_deterministic_observer": "ui-judge",
    "memory": "vault-memory-retriever",
    "retriever": "vault-memory-retriever",
    "vault-retriever": "vault-memory-retriever",
    "vault_memory_retriever": "vault-memory-retriever",
    "palace": "vault-memory-retriever",
    "onda0": "vault-memory-retriever",
    "wave0": "vault-memory-retriever",
    "mediator": "intent-hitl-mediator",
    "hitl-mediator": "intent-hitl-mediator",
    "intent_hitl_mediator": "intent-hitl-mediator",
    "attribution": "intent-hitl-mediator",
    "verifier": "read-after-write-verifier",
    "raw-verifier": "read-after-write-verifier",
    "read_after_write_verifier": "read-after-write-verifier",
    "publisher": "dev-workspace-publisher",
    "workspace-publisher": "dev-workspace-publisher",
    "dev-publisher": "dev-workspace-publisher",
    "dev_workspace_publisher": "dev-workspace-publisher",
}

PERSONA_ALIASES: Dict[str, str] = {
    "franklin": "Franklin-Main",
    "franklin-main": "Franklin-Main",
    "main": "Franklin-Main",
    "drivemaster": "DriveMaster",
    "drive": "DriveMaster",
    "subagent-drive-master": "DriveMaster",
    "fileopslocal": "FileOpsLocal",
    "fileops": "FileOpsLocal",
    "subagent-file-ops-local": "FileOpsLocal",
    "docmaker": "DocMaker",
    "subagent-doc-maker": "DocMaker",
    "skillcraft": "SkillCraft",
    "subagent-skill-craft": "SkillCraft",
    "ui-architect": "UI-Architect",
    "uiarchitect": "UI-Architect",
    "subagent-ui-architect": "UI-Architect",
    "vaultmaster": "VaultMaster",
    "subagent-vault-master": "VaultMaster",
    "loopplanner": "LoopPlanner",
    "subagent-loop-planner": "LoopPlanner",
}

COMPASS_PROFILE_RULES: List[Tuple[Tuple[str, ...], str, List[str], List[Tuple[str, str, str]], str, str]] = [
    (
        ("3d", "fisica", "physics", "three", "webgl", "babylon", "shader", "quaternion", "fps"),
        "📐 Física 3D, Computação Gráfica & Simulação Numérica",
        ["code-quality-audit-3d-physics", "system-project-auditor"],
        [
            ("code-quality-audit-3d-physics", "state_checker_observer.py", "Roda as 3 ondas (AST + Testes Pass@10 + Observador Pydantic Snorm)"),
            ("code-quality-audit-3d-physics", "static_ast_parser.py", "Analisador AST Python (12 regras + 5 sub-dimensões de física)"),
            ("code-quality-audit-3d-physics", "js_ts_ast_parser.js", "Analisador JS/TS para Three.js/WebGL (alocação em loop, dt, Euler)"),
            ("code-quality-audit-3d-physics", "physics_test_runner.py", "Runner de 5 baterias dinâmicas (60 vs 120Hz, Energia, NaN, CCD, Pass@10)"),
        ],
        "plans/physics_code_audit_dag.json",
        "Foco em zero alocação no hot-loop (GC), multiplicação por dt e guarda contra NaN (sem burocracia de docstrings em helpers matemáticos).",
    ),
    (
        ("medic", "saude", "clin", "prontuario", "receit", "calculadora", "paciente", "appmy", "scoreboard", "atlas", "hexagonal", "sofa"),
        "🩺 Software Médico, Atlas 3D (`appmy`) & Scoreboard Hexagonal (`clinical_preceptor_orchestrator`)",
        ["clinical-minimalist-ui", "system-project-auditor", "ui-brand-ux-planner", "ui-quality-judge"],
        [
            ("system-project-auditor", "frontiercode_maintainability_guardrail.py", "Auditoria adaptativa FrontierCode (Tipagem, Bare Except, Segurança)"),
        ],
        "../shredded-shape/plans/ui_actor_critic_dag.json",
        "Coordenador clínico unificado (clinical_preceptor_orchestrator em adk-py-agents/py_agent/pipelines/clinical_coordinator.py) com AgentTools separados: anatomy_3d_inspector (appmy) + hexagonal_score_calculator (scoreboard) e suíte UI federada em shredded-shape.",
    ),
    (
        ("ui", "ux", "front", "tela", "botao", "menu", "css", "tailwind", "react", "design", "sombra", "tatil", "tactile", "elevacao"),
        "🎨 Suíte UI/UX Separada (`shredded-shape` • Analista -> Planejador -> Worker <-> Judge)",
        ["ui-frontend-analyst", "ui-brand-ux-planner", "ui-clean-worker", "ui-quality-judge", "system-project-auditor"],
        [
            ("ui-frontend-analyst", "frontend_inventory_and_slop_scanner.py", "Inventário total de tokens/cores/fontes/menus + Chrome DevTools probe + AI Slop"),
            ("ui-brand-ux-planner", "ui_dag_compiler.py", "Branding OKLCH, estilos Soft..Clinical, Stitch/Figma/Fonts/3D e DAG <= 5 regras/nó"),
            ("ui-clean-worker", "verify_raw_frontend.py", "Verificador físico Read-After-Write SHA-256 + tsc --noEmit + anti-stub"),
            ("ui-quality-judge", "ui_judge_gatekeeper.py", "Juiz Read-Only WCAG 2.2 OKLCH (FNR < 0.001) + Actor-Critic Self-Refine"),
        ],
        "../shredded-shape/plans/ui_actor_critic_dag.json",
        "Suíte UI federada no repositório dedicado shredded-shape: Analista DevTools -> Planejador Brand/Estilos -> Worker RAW -> Judge WCAG 2.2 OKLCH (zero neon, fosco superior, rim light no escuro).",
    ),
    (
        ("rag", "dado", "chunk", "jsonl", "vetor", "memoria", "obsidian", "nota", "vault"),
        "🧠 Dados AI-Ready, RAG & Curadoria Obsidian Vault",
        ["obsidian-vault-curator", "context-sentinel", "system-project-auditor"],
        [
            ("obsidian-vault-curator", "vault_hygiene_scanner.py", "Scanner determinístico de Active Drift, Open Loops, Monólitos (>25KB) e Wikilinks"),
        ],
        "N/A (Execução direta via script)",
        "Preservação de parágrafos lógicos, metadados source_id + byte_range e proteção absoluta da pasta .obsidian/.",
    ),
    (
        ("prompt", "refin", "entropia", "desengess", "fluidez", "zero-trust", "socratic", "epistem"),
        "🎯 Engenharia de Prompts, Fluidez Cognitiva & Contratos de Baixa Entropia (`refine-prompt` v3.2)",
        ["refine-prompt", "solution-content-architect", "context-sentinel"],
        [
            ("refine-prompt", "prompt_entropy_auditor.py", "Auditor determinístico AST/Pydantic de entropia, rigidez burocrática e ancoragem 2026"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Portão AST de segurança e tipagem Python (Quality Score >= 75)"),
        ],
        "N/A (Execução direta via refine-prompt + prompt_entropy_auditor.py)",
        "Determinismo na borda (schemas/contratos de ferramentas) e fluidez cognitiva no núcleo (zero engessamento conversacional).",
    ),
    (
        ("revers", "binario", "binary", "decompil", "ghidra", "sqlite", "bundle", "macho", "objdump", "frida", "rizin"),
        "🔬 Engenharia Reversa Baseada em Evidências (`REA` • Binários Go/PE, SQLite & Bundles JS)",
        ["system-project-auditor", "gap-analyzer-auditor", "code-acceptability-auditor"],
        [
            ("system-project-auditor", "frontiercode_maintainability_guardrail.py", "Auditoria estrutural e de segurança pós-inspeção de artefatos"),
            ("obsidian-vault-curator", "vault_palace_search.py", "Busca híbrida (~35ms) e sincronização do Grafo de Conhecimento SQLite"),
        ],
        "N/A (Inspeção via MCP rea: inspect_go_binary, inspect_sqlite_database, analyze_javascript_application)",
        "Separação estrita entre [FATO OBSERVADO] (com evidence_id ev_...), [INFERÊNCIA] e [DESCONHECIDO].",
    ),
    (
        ("projeto", "repo", "organizar", "ideia", "mvp", "sincronizar", "readme", "estrutura", "auditar", "android", "kotlin", "compose", "gradle", "agp"),
        "📦 Organização de Projetos, Refinamento de Ideias, Auditoria Integrada 3-em-1 (`system-project-auditor` v6.1) & Engenharia Android (`android-agy-projects`)",
        ["system-project-auditor", "project-idea-organizer", "android-agy-projects"],
        [
            ("system-project-auditor", "project_structure_and_code_auditor.py", "Scanner físico AST e árvore real (órfãos, paridade README/SPEC vs disco, placebos e 60-30-10 OKLCH)"),
            ("system-project-auditor", "deterministic_scorer.py", "Scanner determinístico SGA + TIF (adaptativo por stack: Backend/CLI vs UI 3 Camadas)"),
            ("system-project-auditor", "frontiercode_maintainability_guardrail.py", "Auditoria Python adaptativa (SRP, Tipagem Pydantic, Segurança)"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Portão AST pré-commit de segurança e tipagem Python (Score >= 75)"),
        ],
        "plans/distributed_agent_mediation_dag.json | ../shredded-shape/plans/ui_actor_critic_dag.json",
        "Fluxo coerente: (1) Bootstrap MVP proporcional sem pastas vazias ('project-idea-organizer' v1.3) -> (2) Implementação tipada mínima ('solution-content-architect' v2.6) -> (3) Auditoria read-only adaptativa à stack ('system-project-auditor' v6.1).",
    ),
    (
        ("agente", "skill", "yaml", "mcp", "plano", "dag", "orquestra", "test", "auditor", "rca", "converge", "gap", "intencao", "cognitiv", "kahn", "a2a", "stdio"),
        "🤖 Esteira de Qualidade (AST • Testes/Evals • Servidores MCP/A2A • RCA/Convergência), Planejamento Cognitivo Não-Linear & Orquestração DAG (21 Skills Canônicas + 6 UI em shredded-shape)",
        ["agent-server-auditor", "code-acceptability-auditor", "test-quality-auditor", "gap-analyzer-auditor", "high-level-context-planner", "chained-plan-orchestrator"],
        [
            ("agent-server-auditor", "agent_server_auditor.py", "Auditor arquitetural poliglota (Go/TS/Py) de agentes, higiene STDIO MCP, A2A JWS, binários e max_steps"),
            ("high-level-context-planner", "cognitive_plan_builder.py", "Motor Cognitivo: 4 quadrantes, CLAREZA/CREATE + CoT/ReAct/ToT/Self-Refine e Parede <= 5 regras/nó"),
            ("chained-plan-orchestrator", "dag_chain_validator.py", "Compilador de Ondas DAG (Kahn), detector de colisão de arquivos [P] e validador de Context Fork"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Portão 1 AST + Pydantic v2 (12 regras: Segurança, Tipagem, McCabe <= 10, Score >= 75)"),
            ("test-quality-auditor", "test_quality_auditor.py", "Portão 2 de qualidade de suítes de testes em 5 módulos (Py/TS/Go/MCP/Harness + PerfKit)"),
            ("workspace", "validate_skills.py", "Validador determinístico das 21 skills canônicas"),
        ],
        "../shredded-shape/plans/ui_actor_critic_dag.json | plans/physics_code_audit_dag.json | plans/distributed_agent_mediation_dag.json",
        "Planejamento Não-Linear ('high-level-context-planner' v3.0 <=5 regras/nó) -> Compilação de Ondas Kahn ('chained-plan-orchestrator' v3.0) -> Esteira em 3 Portões ('code-acceptability-auditor' -> 'test-quality-auditor' -> 'gap-analyzer-auditor').",
    ),
]


def _resolve_agent_dirs() -> List[Path]:
    """Localiza os diretórios de contratos de subagentes (franklin + shredded-shape federado)."""
    candidates = [
        ROOT_DIR / "agents",
        SHREDDED_SHAPE_ROOT / "agents",
        Path(r"C:\Users\melki\.gemini\config\plugins\franklin-skills\agents"),
        Path(r"C:\Users\melki\.gemini\config\agents"),
        Path(r"C:\Users\melki\.gemini\agents"),
    ]
    return [c for c in candidates if c.exists() and c.is_dir()]


def _resolve_agents_dir() -> Path:
    """Mantém compatibilidade retornando o diretório primário de agentes."""
    dirs = _resolve_agent_dirs()
    return dirs[0] if dirs else (ROOT_DIR / "agents")


def _render_ecosystem_topology() -> str:
    """Renderiza a topologia interativa de agentes em 5 camadas e 21 skills (+ 6 UI em shredded-shape)."""
    skills = _get_all_skills_data()
    by_persona: Dict[str, List[str]] = {}
    for s in skills:
        by_persona.setdefault(s["persona"], []).append(s["name"])
    lines = [
        "# ⚡ Topologia Interativa de Agentes Multi-Repo (5 Camadas • Workspace Multi-Repo)\n",
        "## 1. Camadas de Execução e Custo Cognitivo",
        "- **Camada 0 (Bússola & Heartbeat Zero-LLM — 0 tokens)**: `franklin_smart_compass()`, `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1`, `POST /rpc` (`mesh/heartbeat` em `adk-go-mcp`).",
        "- **Camada 1 (Orquestração & Loop Fechado)**: `Franklin-Main` (Execução Direta) e `LoopPlanner` (`high-level-context-planner` Fase 0 -> `chained-plan-orchestrator` -> `gap-analyzer-auditor`).",
        "- **Camada 2 (Esquadrão Frontend Separado — `shredded-shape` Actor-Critic)**: `UI-Architect` -> `ui-analyst` (DevTools/Slop) -> `ui-planner` (Brand/Estilos/DAG<=5) -> `ui-worker` (ReAct/RAW) <-> `ui-judge` (WCAG 2.2 OKLCH `FNR<0.001`).",
        "- **Camada 3 (Gatekeepers Determinísticos AST/Pass@k — 0 tokens)**: `SkillCraft` (`code-acceptability-auditor` Score >= 75, `test-quality-auditor`), `3D Physics Auditor` (`franklin_execute_dag('physics')`) e `dispatch_skill_deterministic_tests` (Go Eval Harness).",
        "- **Camada 4 (Malha Multiagente Cloud/Web & Clínica)**: `adk-go-mcp` + `adk-py-agents` + `adk-ts-agent` (`mesh_hybrid_orchestrator`, `self_healing_specialist`, `customer_issue_reviewer`, `AgyCalcCluster`, `clinical_preceptor_orchestrator` -> `anatomy_3d_inspector` [`appmy`] + `hexagonal_score_calculator` [`scoreboard`]), `epic-volta` (`DAGEngine` Kahn + `MCPBridgeAgent` + `ContextSentinel`), `mcp-web-agents` (Gateway 4+1 + `watchdogBridge.ts`) e `PCM`/`scoreboard` (`prescmed-clinical-reviewer`).\n",
        "## 2. Personas Especialistas & Skills Vinculadas (`franklin-quebragalho`)",
    ]
    for p_name, s_list in sorted(by_persona.items()):
        lines.append(f"- **`{p_name}`** ({len(s_list)} skills): `{', '.join(sorted(s_list))}`")
    lines.extend([
        "\n## 3. Comandos Interativos de 1 Clique",
        "- **Terminal Hub Interativo**: `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1`",
        "- **Executar DAG UI (3 Ondas)**: `franklin_execute_dag(plan_path_or_json='ui')`",
        "- **Executar DAG Física 3D (3 Ondas)**: `franklin_execute_dag(plan_path_or_json='physics')`",
        "- **Auditar Código Python (AST)**: `franklin_run_skill_script(skill_name='code-auditor', script_name='code_acceptability_auditor.py', args=['--self-test'])`",
    ])
    return "\n".join(lines)


def _extract_persona_details(canonical_persona: str) -> str:
    """Extrai a seção dedicada de uma persona de MY_AGENTS.md e anexa suas skills ativas."""
    my_agents_path = ROOT_DIR / "MY_AGENTS.md"
    section_text = ""
    if my_agents_path.exists():
        raw = my_agents_path.read_text(encoding="utf-8", errors="replace")
        header_term = "Franklin Quebra-Galho" if canonical_persona == "Franklin-Main" else canonical_persona
        for ch in re.split(r"\n---\n", raw):
            if header_term.lower() in ch.lower() and "## " in ch:
                section_text = ch.strip()
                break
    skills = [s["name"] for s in _get_all_skills_data() if s["persona"].lower() == canonical_persona.lower()]
    skills_block = f"\n\n### Skills Vinculadas a `{canonical_persona}` ({len(skills)}):\n- `" + "`, `".join(sorted(skills)) + "`" if skills else ""
    return (section_text or f"## Persona: {canonical_persona}") + skills_block


def get_agents_impl(agent_name: str = "") -> str:
    """Implementação da recuperação de topologia de agentes, personas e contratos de subagentes de UI."""
    clean = agent_name.strip().lower()
    if not clean:
        return AGENTS_MD_PATH.read_text(encoding="utf-8", errors="replace") if AGENTS_MD_PATH.exists() else "Arquivo AGENTS.md não encontrado na raiz do workspace."
    if clean in ("ecosystem", "topology", "matrix", "all", "multi-repo", "repos"):
        return _render_ecosystem_topology()

    agent_dirs = _resolve_agent_dirs()
    if clean in ("ui", "3+1", "all-ui", "subagentes-ui", "shredded-shape"):
        ordered = ("ui-analyst.md", "ui-planner.md", "ui-worker.md", "ui-judge.md")
        parts = ["# Esquadrão de Subagentes de UI (`shredded-shape` • Topologia Actor-Critic em 4 Estágios)\n"]
        for fname in ordered:
            for adir in agent_dirs:
                fpath = adir / fname
                if fpath.exists():
                    parts.extend([fpath.read_text(encoding="utf-8", errors="replace"), "\n" + ("=" * 60) + "\n"])
                    break
        return "\n".join(parts)

    target_stem = UI_SUBAGENT_ALIASES.get(clean, clean.removesuffix(".md"))
    for adir in agent_dirs:
        target_file = adir / f"{target_stem}.md"
        if target_file.exists():
            return target_file.read_text(encoding="utf-8", errors="replace")
    if clean in PERSONA_ALIASES:
        return _extract_persona_details(PERSONA_ALIASES[clean])
    return f"Erro: Subagente '{agent_name}' não encontrado em {[str(d) for d in agent_dirs]}."


def _resolve_compass_profile(q: str) -> Tuple[str, List[str], List[Tuple[str, str, str]], str, str]:
    """Seleciona o perfil cognitivo, skills recomendadas, scripts prontos e plano DAG conforme a intenção."""
    for keywords, title, rec_skills, scripts, dag_plan, guardrail in COMPASS_PROFILE_RULES:
        if any(k in q for k in keywords):
            return title, rec_skills, scripts, dag_plan, guardrail
    return (
        "🧭 Visão Geral Rápida do Ecossistema Franklin (Multi-Projeto • 21 Skills + 6 UI em shredded-shape)",
        ["project-idea-organizer", "system-project-auditor", "solution-content-architect", "code-acceptability-auditor", "ui-brand-ux-planner", "ui-clean-worker"],
        [
            ("system-project-auditor", "frontiercode_maintainability_guardrail.py", "Auditoria Python adaptativa (detecta sozinho se é código Geral ou 3D)"),
            ("code-acceptability-auditor", "code_acceptability_auditor.py", "Portão AST pré-commit de segurança e tipagem Python (Score >= 75)"),
            ("code-quality-audit-3d-physics", "state_checker_observer.py", "Observador Pydantic com filtro anti-alucinação AST e nota Snorm"),
            ("ui-quality-judge", "ui_judge_gatekeeper.py", "Juiz Read-Only WCAG 2.2 OKLCH e FSM em shredded-shape"),
        ],
        "../shredded-shape/plans/ui_actor_critic_dag.json | plans/physics_code_audit_dag.json | plans/distributed_agent_mediation_dag.json",
        "Portão gradual: bloqueia apenas falhas críticas/altas (Hard Gate) e trata estilo/docstrings como sugestões leves (Soft Advisory).",
    )


def smart_compass_impl(
    intent_or_path: str = "",
    auto_dispatch_dag: bool = False,
    target_dir: str = "",
    dag_executor: Callable[[str, str], str] | None = None,
) -> str:
    """Implementação da Bússola Cognitiva do Franklin."""
    skills = _get_all_skills_data()
    q = intent_or_path.strip().lower()
    profile_title, recommended_skills, ready_scripts, dag_plan, linear_guardrail = _resolve_compass_profile(q)

    lines = [f"## 🧭 Bússola Cognitiva Franklin — {profile_title}", "", "### 1. Skills Prontas para Ativar neste Contexto:"]
    for s_name in recommended_skills:
        s_obj = next((x for x in skills if x["name"] == s_name or x["directory"] == s_name), None)
        if s_obj:
            lines.append(f"- **`{s_obj['name']}`** (`{s_obj['persona']}`): {s_obj['description'][:140]}...")

    lines.append("\n### 2. Scripts Executáveis Prontos (Sem precisar recriar do zero):")
    for sk, sc_name, desc in ready_scripts:
        lines.append(f"- **`{sc_name}`** (Skill: `{sk}`) — {desc}")
        lines.append(f"  ↳ Disparo rápido: `franklin_run_skill_script(skill_name='{sk}', script_name='{sc_name}', args=['--self-test'])`")

    candidate_path = intent_or_path.strip()
    target_arg = target_dir.strip() or (candidate_path if candidate_path and Path(candidate_path).exists() else "")
    dag_line = f"### 3. Planos DAG Disponíveis: `{dag_plan}`"
    has_dag_plan = dag_plan.startswith(("plans/", "../shredded-shape/plans/"))
    if target_arg and has_dag_plan:
        primary_plan = dag_plan.split("|")[0].strip()
        dag_line += f"\n- Disparo com alvo: `franklin_execute_dag(plan_path_or_json=\"{primary_plan}\", target_dir=\"{target_arg}\")`"

    lines.extend([
        "", dag_line,
        "### 4. Qualidade Linear Sem Engessar (Regra de Bolso):",
        f"> {linear_guardrail}", "",
        "### 5. Central Interativa no Terminal (1-Clique):",
        "- `pwsh C:\\Users\\melki\\dev\\tools\\agent-hub.ps1` (Menu interativo de agentes, portas e repositórios do workspace)",
        "- `franklin_get_agents(agent_name='ecosystem')` (Mapa completo das 5 camadas de agentes)",
    ])
    if auto_dispatch_dag and has_dag_plan and dag_executor is not None:
        primary_plan = dag_plan.split("|")[0].strip()
        dag_out = dag_executor(primary_plan, target_arg)
        lines.extend(["", "### 6. Execução Automática do DAG Recomendado:", f"```json\n{dag_out}\n```"])
    return "\n".join(lines)
