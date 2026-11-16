"""
trigger_eval_suite.py
Deterministic Level 1 Trigger Evaluation Suite (Should-Trigger vs. Near-Misses)
for all 28 Canonical Agent Skills of Franklin Quebra-Galho (Bilingual PT-BR + EN).

Objective:
Mathematically validate that Level 1 descriptions (<available_skills>), bilingual tags,
and the ranking engine (rank_skills_for_query) achieve 100% Top-1 Accuracy on
should-trigger cases and 100% rejection on near-misses (including negative clauses).
"""

from __future__ import annotations

from typing import Dict, List, Literal
from pydantic import BaseModel, ConfigDict, Field

from shared.catalog_service import rank_skills_for_query


class TriggerEvalCase(BaseModel):
    """Caso individual de avaliação Should-Trigger e Near-Miss."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    case_id: str
    cluster: str
    query: str
    expected_skill: str
    near_miss_skills: List[str] = Field(default_factory=list)
    case_type: Literal["should_trigger", "negative_clause_near_miss"] = "should_trigger"
    rationale: str


class TriggerCaseOutcome(BaseModel):
    """Resultado determinístico da execução de um TriggerEvalCase."""

    model_config = ConfigDict(extra="forbid")

    case_id: str
    query: str
    expected_skill: str
    top1_skill: str
    top1_score: int
    expected_skill_score: int
    top3_skills: List[str]
    near_miss_scores: Dict[str, int]
    passed_top1: bool
    passed_near_miss: bool


class TriggerEvalReport(BaseModel):
    """Relatório consolidado de precisão, recall, F1 e rejeição de near-misses."""

    model_config = ConfigDict(extra="forbid")

    total_cases: int
    covered_skills_count: int
    top1_hits: int
    top3_hits: int
    near_miss_rejections: int
    top1_accuracy: float = Field(ge=0.0, le=1.0)
    top3_recall: float = Field(ge=0.0, le=1.0)
    near_miss_rejection_rate: float = Field(ge=0.0, le=1.0)
    f1_score: float = Field(ge=0.0, le=1.0)
    status: Literal["[PASS]", "[FAIL]"]
    outcomes: List[TriggerCaseOutcome]
    failures: List[str]


CANONICAL_TRIGGER_EVAL_CASES: List[TriggerEvalCase] = [
    # Cluster 1: Prompts, Entropia, Soluções & Sentinela de Contexto
    TriggerEvalCase(
        case_id="TRG-01",
        cluster="Prompts & Context",
        query="auditar factibilidade FATO INFERÊNCIA LACUNA, modular entropia e refinar prompt sob Zero-Trust XML OWASP LLM 2026",
        expected_skill="refine-prompt",
        near_miss_skills=["solution-content-architect", "context-sentinel"],
        rationale="Direct trigger for epistemic prompt audit, entropy modulation, and Zero-Trust XML.",
    ),
    TriggerEvalCase(
        case_id="TRG-02",
        cluster="Prompts & Context",
        query="desenhar soluções técnicas, biblioteca de prompts enterprise, código tipado e roadmaps em 4 modos com 7 Módulos de Guardrails",
        expected_skill="solution-content-architect",
        near_miss_skills=["refine-prompt", "high-level-context-planner"],
        rationale="End-to-end solution architecture, enterprise prompts, and 4-mode roadmaps.",
    ),
    TriggerEvalCase(
        case_id="TRG-03",
        cluster="Prompts & Context",
        query="auditoria epistêmica isolada de prompt e modulação de entropia socrática",
        expected_skill="refine-prompt",
        near_miss_skills=["solution-content-architect"],
        case_type="negative_clause_near_miss",
        rationale="Negative clause in solution-content-architect ('Do not use for isolated epistemic prompt audits') penalizes it in favor of refine-prompt.",
    ),
    TriggerEvalCase(
        case_id="TRG-04",
        cluster="Prompts & Context",
        query="auditar integridade da janela de contexto em conversas multi-turn e extrair estado estruturado da sessão em SQLite ou JSON",
        expected_skill="context-sentinel",
        near_miss_skills=["refine-prompt", "obsidian-vault-curator"],
        rationale="Multi-turn context window integrity sentinel vs. isolated prompt refiner.",
    ),
    # Cluster 2: Frontend Engineering, UI/UX, DESIGN.md & Clinical UI
    TriggerEvalCase(
        case_id="TRG-05",
        cluster="Frontend & UI",
        query="criar ou atualizar o contrato DESIGN.md na raiz do projeto definindo tokens semânticos e escala tipográfica modular",
        expected_skill="design-md",
        near_miss_skills=["frontend-code-architect", "frontend-ui-ux-auditor"],
        rationale="Authoring DESIGN.md contract vs. implementing UI components.",
    ),
    TriggerEvalCase(
        case_id="TRG-06",
        cluster="Frontend & UI",
        query="implementar e refatorar interfaces web React Next.js Tailwind consumindo o contrato DESIGN.md com estados finitos FSM",
        expected_skill="frontend-code-architect",
        near_miss_skills=["design-md", "frontend-testing-auditor", "system-project-auditor"],
        rationale="Frontend code implementation/refactoring (system-project-auditor excludes code refactoring).",
    ),
    TriggerEvalCase(
        case_id="TRG-07",
        cluster="Frontend & UI",
        query="auditar qualidade de interfaces web via audit_tactile_ui.py verificando WAI-ARIA, zero emojis, zero bloat Base64 e anti-XSS",
        expected_skill="frontend-testing-auditor",
        near_miss_skills=["frontend-ui-ux-auditor", "frontend-code-architect"],
        rationale="Deterministic UI gate via audit_tactile_ui.py (Base64, XSS, WAI-ARIA).",
    ),
    TriggerEvalCase(
        case_id="TRG-08",
        cluster="Frontend & UI",
        query="auditar com precisão matemática densidade de nós DOM, contraste WCAG 2.1 AA, luz zenital 90-120 e elevação por sombras",
        expected_skill="frontend-ui-ux-auditor",
        near_miss_skills=["frontend-testing-auditor", "design-md"],
        rationale="Optical/mathematical UI/UX audit of DOM density, zenith light 90-120, and elevation shadows.",
    ),
    TriggerEvalCase(
        case_id="TRG-09",
        cluster="Frontend & UI",
        query="arquitetura para interfaces clínicas, prontuários eletrônicos PEP, receituários laudos A4 .sus-grid e calculadoras médicas",
        expected_skill="clinical-minimalist-ui",
        near_miss_skills=["design-md", "frontend-code-architect"],
        rationale="Specialist for clinical EHR/PEP interfaces, .sus-grid A4 print, and medical dosing safeguards.",
    ),
    # Cluster 3: Google Drive, Local Windows Disk & Obsidian Vault
    TriggerEvalCase(
        case_id="TRG-10",
        cluster="Drive, Disk & Vault",
        query="auditar e higienizar Google Drive detectando arquivos pesados >100MB, duplicatas por hash e pastas vazias órfãs com Dry-run",
        expected_skill="gdrive-cleanup-auditor",
        near_miss_skills=["gdrive-taxonomy-organizer", "windows-disk-maintenance"],
        rationale="Cleaning heavy/duplicate files on Google Drive vs. folder taxonomy or local Windows disk.",
    ),
    TriggerEvalCase(
        case_id="TRG-11",
        cluster="Drive, Disk & Vault",
        query="estruturar e categorizar pastas no Google Drive aplicando taxonomia canônica numerada e padronização de datas ISO YYYY-MM-DD",
        expected_skill="gdrive-taxonomy-organizer",
        near_miss_skills=["gdrive-cleanup-auditor", "flow-filetree-organizer"],
        rationale="Canonical numbered folder taxonomy and ISO YYYY-MM-DD naming on Google Drive.",
    ),
    TriggerEvalCase(
        case_id="TRG-12",
        cluster="Drive, Disk & Vault",
        query="manutenção de arquivos locais no Windows 11 Downloads e Desktop isolando instaladores antigos e resíduos temporários",
        expected_skill="windows-disk-maintenance",
        near_miss_skills=["gdrive-cleanup-auditor", "refine-prompt"],
        case_type="negative_clause_near_miss",
        rationale="Local Windows file maintenance (refine-prompt explicitly excludes local file maintenance).",
    ),
    TriggerEvalCase(
        case_id="TRG-13",
        cluster="Drive, Disk & Vault",
        query="auditar e higienizar o cofre do Obsidian validando frontmatter YAML, links bidirecionais Wikilinks e MemPalace wing notes",
        expected_skill="obsidian-vault-curator",
        near_miss_skills=["technical-markdown-writer", "windows-disk-maintenance"],
        rationale="Structural Obsidian vault curation and MemPalace synchronization.",
    ),
    # Cluster 4: Code AST Quality, Test Suites & 3D Physics
    TriggerEvalCase(
        case_id="TRG-14",
        cluster="Code, Tests & 3D",
        query="auditar estaticamente arquivos Python via AST contra eval/exec, shell=True, ausência de type hints e funções longas >60 linhas",
        expected_skill="code-acceptability-auditor",
        near_miss_skills=["test-quality-auditor", "system-project-auditor"],
        rationale="Python static AST acceptability gatekeeper (Quality Score 0-100).",
    ),
    TriggerEvalCase(
        case_id="TRG-15",
        cluster="Code, Tests & 3D",
        query="auditoria de suítes de testes em 5 módulos Python TS Go MCP e Harness detectando Green Build Illusion e falhas AAA",
        expected_skill="test-quality-auditor",
        near_miss_skills=["code-acceptability-auditor", "code-quality-audit-3d-physics"],
        rationale="5-module test quality auditor (Green Build Illusion, AAA, grading.json).",
    ),
    TriggerEvalCase(
        case_id="TRG-16",
        cluster="Code, Tests & 3D",
        query="auditar e sanitizar código de Física 3D, Computação Gráfica WebGL Three.js Babylon.js, shaders, colisões e nota Snorm Pass@10",
        expected_skill="code-quality-audit-3d-physics",
        near_miss_skills=["code-acceptability-auditor", "test-quality-auditor"],
        rationale="Specialized auditor for 3D physics engines, shaders, collisions, and Pass@10 simulation.",
    ),
    # Cluster 5: Phase 0 Planning, Gap Analysis (RCA) & DAG Orchestration
    TriggerEvalCase(
        case_id="TRG-17",
        cluster="Planning & Closed Loop",
        query="planejador de contexto de alto nível decompondo metas em fases numeradas com Fase 0, tasks paralelizáveis e Complexity Tracking",
        expected_skill="high-level-context-planner",
        near_miss_skills=["chained-plan-orchestrator", "gap-analyzer-auditor"],
        rationale="Strategic Phase 0 decomposition and Complexity Tracking.",
    ),
    TriggerEvalCase(
        case_id="TRG-18",
        cluster="Planning & Closed Loop",
        query="analista de brechas RCA e convergência Spec-to-Code inspecionando logs e traces para emitir Hand-off Payload YAML",
        expected_skill="gap-analyzer-auditor",
        near_miss_skills=["high-level-context-planner", "system-project-auditor"],
        rationale="Root-cause gap analysis (RCA) over logs/traces and YAML hand-off payload.",
    ),
    TriggerEvalCase(
        case_id="TRG-19",
        cluster="Planning & Closed Loop",
        query="orquestrador executivo de planos encadeados DAG mapeando dependências entre skills especialistas e executando ondas sequenciais",
        expected_skill="chained-plan-orchestrator",
        near_miss_skills=["high-level-context-planner", "gap-analyzer-auditor"],
        rationale="Chained DAG wave compilation and execution with Context Fork isolation.",
    ),
    # Cluster 6: Project Organization, MVP Diagnosis & Islands Architecture (3-in-1 Fusion)
    TriggerEvalCase(
        case_id="TRG-20",
        cluster="Projects, MVP & Architecture",
        query="auditoria integrada 3-em-1 de projetos, sistemas, MVP e navegabilidade com project_structure_and_code_auditor.py e Plano de Evolução em 3 Fases",
        expected_skill="system-project-auditor",
        near_miss_skills=["project-idea-organizer", "frontend-testing-auditor"],
        rationale="MVP diagnostics, AST physical tree, and 3-phase evolution plan in system-project-auditor.",
    ),
    TriggerEvalCase(
        case_id="TRG-21",
        cluster="Projects, MVP & Architecture",
        query="auditar integridade estrutural de repositórios, código órfão e esteira dinâmica via agent-browser @eX com nota de 0 a 100",
        expected_skill="system-project-auditor",
        near_miss_skills=["project-idea-organizer", "frontend-testing-auditor"],
        rationale="0-100 structural repo audit combined with agent-browser (@eX) inspection.",
    ),
    TriggerEvalCase(
        case_id="TRG-22",
        cluster="Projects, MVP & Architecture",
        query="organizar ideias do zero com perguntas guiadas e sugestão de MVP ou reestruturar README.md fiel ao disco e contratos MCP tools.json",
        expected_skill="project-idea-organizer",
        near_miss_skills=["system-project-auditor", "flow-filetree-organizer"],
        rationale="Guided ideation from scratch or README.md / MCP tools.json synchronization.",
    ),
    TriggerEvalCase(
        case_id="TRG-23",
        cluster="Projects, MVP & Architecture",
        query="auditoria de navegação em 3 camadas, Ilhas Funcionais, Clicar em X ativa Y, Dead Ends, suficiência funcional e score determinístico SGA V1 vs V2 com deterministic_scorer.py",
        expected_skill="system-project-auditor",
        near_miss_skills=["design-md", "project-idea-organizer"],
        rationale="3-layer navigation, functional islands (X activates Y), and SGA V1 vs V2 scoring.",
    ),
    # Cluster 7: Markdown Docs, PDF Conversion & Mermaid Flows
    TriggerEvalCase(
        case_id="TRG-24",
        cluster="Documents & Diagrams",
        query="redigir relatórios executivos, notas técnicas e atas de decisão em Markdown com caixas de alerta GitHub e Google Style Guides",
        expected_skill="technical-markdown-writer",
        near_miss_skills=["html-pdf-converter", "obsidian-vault-curator"],
        rationale="Technical Markdown writing with GitHub alerts and Google Style Guides.",
    ),
    TriggerEvalCase(
        case_id="TRG-25",
        cluster="Documents & Diagrams",
        query="converter documentos Markdown e HTML para arquivos PDF profissionais via Microsoft Edge ou Chrome headless com CSS de impressão",
        expected_skill="html-pdf-converter",
        near_miss_skills=["technical-markdown-writer", "flow-filetree-organizer"],
        rationale="Deterministic Markdown/HTML to PDF conversion via headless Edge/Chrome.",
    ),
    TriggerEvalCase(
        case_id="TRG-26",
        cluster="Documents & Diagrams",
        query="transformar ideias brutas e requisitos de apps em fluxos visuais Mermaid e árvores de diretórios comentadas",
        expected_skill="flow-filetree-organizer",
        near_miss_skills=["project-idea-organizer", "technical-markdown-writer"],
        rationale="Mermaid flowcharts and commented directory trees from raw app ideas.",
    ),
    TriggerEvalCase(
        case_id="TRG-27",
        cluster="Code, Tests & 3D",
        query="auditar sistemas agênticos, servidores MCP 2026-07-28 STDIO stdout, nós A2A agent-card JWS, higiene de binários, travas max_steps e persistir memories/audit_report.json",
        expected_skill="agent-server-auditor",
        near_miss_skills=["system-project-auditor", "test-quality-auditor", "code-acceptability-auditor"],
        rationale="Agentic architecture, MCP STDIO, A2A agent-card JWS, and audit_report.json auditing.",
    ),
    TriggerEvalCase(
        case_id="TRG-28",
        cluster="Frontend & UI",
        query="auditar via ciclo ReAct CDP DevTools e AST aplicações frontend complexas com canvas infinito @xyflow/react WebSocket Chokidar, detecção de nós fantasmas funções falsas e Next.js 15 async params",
        expected_skill="complex-zero",
        near_miss_skills=["frontend-code-architect", "frontend-testing-auditor", "frontend-ui-ux-auditor"],
        rationale="ReAct + CDP + AST anti-fake auditing for @xyflow/react, WebSocket/Chokidar, and Next.js 15+.",
    ),
    TriggerEvalCase(
        case_id="TRG-29",
        cluster="Frontend & UI",
        query="análise minuciosa e global de frontend UI/UX com REA Reverse Engineer Anything, proporção 60-30-10 OKLCH e propostas de mutação Antes Depois plan-uiux",
        expected_skill="plan-uiux",
        near_miss_skills=["frontend-ui-ux-auditor", "design-md", "frontend-code-architect"],
        rationale="Frontend UI/UX reverse engineering with REA and Before/After mutation plans.",
    ),
    TriggerEvalCase(
        case_id="TRG-30",
        cluster="Projects, MVP & Architecture",
        query="criar app Android do zero ou auditar gargalos de build Gradle AGP 9 Built-in Kotlin KSP2 Jetpack Compose Navigation 3 R8 ANR e memory leaks com android-agy-projects",
        expected_skill="android-agy-projects",
        near_miss_skills=["system-project-auditor", "frontend-code-architect"],
        rationale="Android app engineering and Gradle/AGP9/Compose/ANR auditing.",
    ),
    TriggerEvalCase(
        case_id="TRG-31",
        cluster="Code, Tests & 3D",
        query="engenharia reversa e auditoria de APKs Android com re-a-ndroid REA e ADB descompilando DEX .so assinaturas v1-v3.1 funções placebo latência de rotas e alvos 48dp",
        expected_skill="re-a-ndroid",
        near_miss_skills=["android-agy-projects", "plan-uiux"],
        rationale="Binary/dynamic APK reverse engineering with REA and ADB.",
    ),
    TriggerEvalCase(
        case_id="TRG-32",
        cluster="Bilingual English Verification",
        query="Audit repository AST code health, MVP diagnosis, 3-layer navigation SGA score, and agent-browser DOM without refactoring code",
        expected_skill="system-project-auditor",
        near_miss_skills=["project-idea-organizer", "frontend-code-architect"],
        case_type="negative_clause_near_miss",
        rationale="English query must select system-project-auditor and reject project-idea-organizer / frontend-code-architect.",
    ),
    TriggerEvalCase(
        case_id="TRG-33",
        cluster="Bilingual English Verification",
        query="Convert technical Markdown reports to A4 PDF using headless Edge or Chrome print CSS",
        expected_skill="html-pdf-converter",
        near_miss_skills=["technical-markdown-writer", "flow-filetree-organizer"],
        rationale="English query must route PDF conversion to html-pdf-converter.",
    ),
    TriggerEvalCase(
        case_id="TRG-34",
        cluster="Bilingual English Verification",
        query="Clean up Google Drive heavy files over 100MB, SHA-256 duplicates, and orphan empty folders with dry-run",
        expected_skill="gdrive-cleanup-auditor",
        near_miss_skills=["gdrive-taxonomy-organizer", "windows-disk-maintenance"],
        rationale="English query must route Drive cleanup to gdrive-cleanup-auditor.",
    ),
]


def _evaluate_single_case(case: TriggerEvalCase) -> TriggerCaseOutcome:
    """Executa o ranqueamento Nível 1 para um caso e verifica Top-1 e rejeição de near-misses."""
    ranked = rank_skills_for_query(case.query, limit=50)
    score_by_name: Dict[str, int] = {item[1]["name"]: item[0] for item in ranked}
    top3_names = [item[1]["name"] for item in ranked[:3]]
    top1_name = top3_names[0] if top3_names else ""
    top1_score = ranked[0][0] if ranked else 0
    expected_score = score_by_name.get(case.expected_skill, 0)

    near_miss_scores = {nm: score_by_name.get(nm, 0) for nm in case.near_miss_skills}
    passed_top1 = top1_name == case.expected_skill and expected_score > 0
    passed_near_miss = all(expected_score > nm_score for nm_score in near_miss_scores.values())

    return TriggerCaseOutcome(
        case_id=case.case_id,
        query=case.query,
        expected_skill=case.expected_skill,
        top1_skill=top1_name,
        top1_score=top1_score,
        expected_skill_score=expected_score,
        top3_skills=top3_names,
        near_miss_scores=near_miss_scores,
        passed_top1=passed_top1,
        passed_near_miss=passed_near_miss,
    )


def run_trigger_eval_suite(cases: List[TriggerEvalCase] | None = None) -> TriggerEvalReport:
    """Executa toda a bateria Should-Trigger vs. Near-Miss e calcula métricas determinísticas."""
    active_cases = cases if cases is not None else CANONICAL_TRIGGER_EVAL_CASES
    outcomes: List[TriggerCaseOutcome] = []
    failures: List[str] = []
    top1_hits = 0
    top3_hits = 0
    nm_rejections = 0

    for c in active_cases:
        out = _evaluate_single_case(c)
        outcomes.append(out)
        if out.passed_top1:
            top1_hits += 1
        else:
            failures.append(
                f"[{c.case_id}] Top-1 incorreto para '{c.expected_skill}': obteve '{out.top1_skill}' ({out.top1_score} pts vs {out.expected_skill_score} pts)"
            )
        if c.expected_skill in out.top3_skills:
            top3_hits += 1
        if out.passed_near_miss:
            nm_rejections += 1
        else:
            failures.append(
                f"[{c.case_id}] Falha de separação Near-Miss para '{c.expected_skill}' ({out.expected_skill_score} pts): {out.near_miss_scores}"
            )

    total = max(1, len(active_cases))
    precision = round(top1_hits / total, 4)
    recall = round(top3_hits / total, 4)
    nm_rate = round(nm_rejections / total, 4)
    f1 = round((2 * precision * nm_rate) / (precision + nm_rate), 4) if (precision + nm_rate) > 0 else 0.0
    covered_skills = len({c.expected_skill for c in active_cases})
    status: Literal["[PASS]", "[FAIL]"] = "[PASS]" if not failures else "[FAIL]"

    return TriggerEvalReport(
        total_cases=len(active_cases),
        covered_skills_count=covered_skills,
        top1_hits=top1_hits,
        top3_hits=top3_hits,
        near_miss_rejections=nm_rejections,
        top1_accuracy=precision,
        top3_recall=recall,
        near_miss_rejection_rate=nm_rate,
        f1_score=f1,
        status=status,
        outcomes=outcomes,
        failures=failures,
    )
