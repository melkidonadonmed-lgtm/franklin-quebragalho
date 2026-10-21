#!/usr/bin/env python3
"""
prompt_entropy_auditor.py
Motor determinístico de auditoria de prompts, modulação de entropia (Fluidez vs. Baixa Entropia),
isolamento Zero-Trust, parede de complexidade (IFEval) e buffer autorregressivo (_pre_flight_check).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

EntropyRegimeType = Literal["AUTO", "COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"]
PromptRuleIdType = Literal[
    "PR-SEC-01",
    "PR-WALL-01",
    "PR-REF-01",
    "PR-FLUID-01",
    "PR-ENT-01",
    "PR-SCRAPE-01",
]
SeverityType = Literal["CRÍTICO", "ALTO", "MÉDIO", "BAIXO"]

RULE_PENALTIES: Dict[PromptRuleIdType, float] = {
    "PR-SEC-01": 15.0,
    "PR-WALL-01": 15.0,
    "PR-REF-01": 25.0,
    "PR-FLUID-01": 15.0,
    "PR-ENT-01": 20.0,
    "PR-SCRAPE-01": 10.0,
}

NEGATIVE_RULE_REGEX = re.compile(
    r"(?:^|\n)\s*(?:[-*•]|\d+\.)?\s*(?:nunca|jamais|proibido|n[aã]o\s+use|never|do\s+not|don't|forbidden)\b",
    re.IGNORECASE,
)
XML_ISOLATION_REGEX = re.compile(
    r"<(untrusted_user_input|untrusted_data|source_code|raw_notes|error_log|file_list|user_data)>",
    re.IGNORECASE,
)
BLIND_SELF_REFINE_REGEX = re.compile(
    r"(revis\S+\s+(?:tudo\s+)?silencios\S+|auto[- ]?refin\S+\s+silencios\S+|"
    r"silencios\S+\s+antes\s+de\s+(?:responder|escrever))",
    re.IGNORECASE,
)
AUTOREGRESSIVE_BUFFER_REGEX = re.compile(
    r"(_pre_flight_check|_internal_audit|_audit_check|<thinking>|bloco\s+de\s+pensamento|racioc[ií]nio\s+nativo)",
    re.IGNORECASE,
)
RIGID_TEMPLATE_COLLAPSE_REGEX = re.compile(
    r"(sempre\s+em\s+exatamente\s+\d+\s+t[oó]picos|no\s+m[aá]ximo\s+\d+\s+palavras\s+por\s+t[oó]pico|"
    r"termine\s+sempre\s+com\s+conclus[aã]o:|use\s+sempre\s+os\s+cabe[cç]alhos\s+introdu[cç][aã]o:)",
    re.IGNORECASE,
)
ESCAPE_TOKEN_REGEX = re.compile(
    r"(\[N[AÃ]O\s+INFORMADO|\[PENDENTE|missing_required_fields|zero\s+infer[eê]ncia)",
    re.IGNORECASE,
)
SCRAPE_NOISE_REGEX = re.compile(
    r"\b(cards_star|audio_magic_eraser|stacked_bar_chart|Gerando\s+apresenta[cç][aã]o)\b",
    re.IGNORECASE,
)
LOW_ENTROPY_HINTS_REGEX = re.compile(
    r"(<task_contract>|baixa\s+entropia|output_schema|output_format|responda\s+exclusivamente\s+em\s+json)",
    re.IGNORECASE,
)


class PromptViolation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rule_id: PromptRuleIdType
    severity: SeverityType
    penalty: float = Field(ge=0.0)
    message: str
    recommendation: str


class PromptEntropyReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_name: str
    detected_regime: Literal["COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"]
    negative_constraints_count: int = Field(ge=0)
    has_xml_isolation: bool
    has_autoregressive_buffer: bool
    has_escape_tokens: bool
    readiness_score: float = Field(ge=0.0, le=100.0)
    status: Literal["APPROVED", "REJECTED"]
    deterministic_markers: List[str] = Field(default_factory=list)
    violations: List[PromptViolation] = Field(default_factory=list)


def _infer_regime(text: str, requested: EntropyRegimeType) -> Literal["COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"]:
    if requested in ("COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"):
        return requested
    if LOW_ENTROPY_HINTS_REGEX.search(text):
        return "LOW_ENTROPY_CONTRACT"
    return "COGNITIVE_FLUID"


def _make_violation(
    rule_id: PromptRuleIdType,
    severity: SeverityType,
    message: str,
    recommendation: str,
) -> PromptViolation:
    return PromptViolation(
        rule_id=rule_id,
        severity=severity,
        penalty=RULE_PENALTIES[rule_id],
        message=message,
        recommendation=recommendation,
    )


def _collect_prompt_violations(
    prompt_text: str,
    effective_regime: Literal["COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"],
    neg_count: int,
    max_negative_constraints: int,
    has_xml: bool,
    has_buffer: bool,
    has_escape: bool,
    require_xml_isolation: bool,
) -> List[PromptViolation]:
    """Avalia as 6 invariantes determinísticas de entropia, fluidez e segurança."""
    checks = [
        (
            require_xml_isolation and not has_xml,
            "PR-SEC-01",
            "ALTO",
            "Ausência de delimitadores XML Zero-Trust para dados externos.",
            "Isole a entrada em <untrusted_user_input>, <raw_notes> ou <untrusted_data>.",
        ),
        (
            neg_count > max_negative_constraints,
            "PR-WALL-01",
            "ALTO",
            f"Prompt Complexity Wall: {neg_count} restrições negativas (limite: {max_negative_constraints}).",
            "Desmembre restrições excessivas em sub-skills (SKILL.md) ou contratos estruturados.",
        ),
        (
            bool(BLIND_SELF_REFINE_REGEX.search(prompt_text)) and not has_buffer,
            "PR-REF-01",
            "CRÍTICO",
            "Exigência de Self-Refine silencioso sem buffer autorregressivo (_pre_flight_check/Thinking).",
            "Adicione o campo '_pre_flight_check' antes da resposta final ou habilite Thinking tokens.",
        ),
        (
            effective_regime == "COGNITIVE_FLUID" and bool(RIGID_TEMPLATE_COLLAPSE_REGEX.search(prompt_text)),
            "PR-FLUID-01",
            "MÉDIO",
            "Colapso de Modo Induzido por Prompt (template fixo engessado ou rótulo Conclusão:).",
            "Aplique Why-First e roteamento dinâmico de formato (prosa, tabela 3+ itens, lista).",
        ),
        (
            effective_regime == "LOW_ENTROPY_CONTRACT" and not has_escape,
            "PR-ENT-01",
            "ALTO",
            "Contrato de baixa entropia sem token de escape para dados ausentes.",
            "Exija [NÃO INFORMADO: dado], [PENDENTE: dado] ou 'missing_required_fields'.",
        ),
        (
            bool(SCRAPE_NOISE_REGEX.search(prompt_text)),
            "PR-SCRAPE-01",
            "BAIXO",
            "Resíduos espúrios de scraping de UI detectados no texto do prompt.",
            "Expurgue artefatos visuais copiados de interfaces (cards_star, audio_magic_eraser).",
        ),
    ]
    return [
        _make_violation(rule_id, sev, msg, rec)  # type: ignore[arg-type]
        for cond, rule_id, sev, msg, rec in checks
        if cond
    ]


def audit_prompt_text(
    prompt_text: str,
    source_name: str = "<inline>",
    regime: EntropyRegimeType = "AUTO",
    max_negative_constraints: int = 15,
    require_xml_isolation: bool = False,
) -> PromptEntropyReport:
    """Executa auditoria determinística de entropia, fluidez e segurança em um prompt."""
    effective_regime = _infer_regime(prompt_text, regime)
    neg_count = len(NEGATIVE_RULE_REGEX.findall(prompt_text))
    has_xml = bool(XML_ISOLATION_REGEX.search(prompt_text))
    has_buffer = bool(AUTOREGRESSIVE_BUFFER_REGEX.search(prompt_text))
    has_escape = bool(ESCAPE_TOKEN_REGEX.search(prompt_text))

    violations = _collect_prompt_violations(
        prompt_text=prompt_text,
        effective_regime=effective_regime,
        neg_count=neg_count,
        max_negative_constraints=max_negative_constraints,
        has_xml=has_xml,
        has_buffer=has_buffer,
        has_escape=has_escape,
        require_xml_isolation=require_xml_isolation,
    )

    score = round(max(0.0, 100.0 - sum(v.penalty for v in violations)), 2)
    critical_count = sum(1 for v in violations if v.severity == "CRÍTICO")
    approved = critical_count == 0 and score >= 75.0
    status: Literal["APPROVED", "REJECTED"] = "APPROVED" if approved else "REJECTED"

    markers = [f"[FAIL: {v.rule_id}]" for v in violations]
    markers.append("[PASS]" if approved else "[FAIL: PROMPT_ENTROPY_GATE_REJECTED]")

    return PromptEntropyReport(
        source_name=source_name,
        detected_regime=effective_regime,
        negative_constraints_count=neg_count,
        has_xml_isolation=has_xml,
        has_autoregressive_buffer=has_buffer,
        has_escape_tokens=has_escape,
        readiness_score=score,
        status=status,
        deterministic_markers=markers,
        violations=violations,
    )


def run_self_test() -> int:
    """Executa bateria de auto-validação determinística do motor."""
    valid_low_entropy = (
        "<task_contract>Converta as notas brutas sob regime de baixa entropia. "
        "Zero inferência: use [NÃO INFORMADO: dado] para lacunas.</task_contract>"
        "<raw_notes>Paciente lúcido.</raw_notes>"
    )
    rep_ok = audit_prompt_text(valid_low_entropy, "valid_low_entropy", "LOW_ENTROPY_CONTRACT", require_xml_isolation=True)

    flawed_prompt = (
        "Responda sempre em exatamente 3 tópicos, termine sempre com Conclusão: "
        "e faça uma revisão silenciosa antes de responder."
    )
    rep_fail = audit_prompt_text(flawed_prompt, "flawed_prompt", "COGNITIVE_FLUID")

    passed = rep_ok.status == "APPROVED" and rep_ok.readiness_score == 100.0 and rep_fail.status == "REJECTED"
    summary = {
        "self_test": "PASS" if passed else "FAIL",
        "valid_case_score": rep_ok.readiness_score,
        "flawed_case_score": rep_fail.readiness_score,
        "flawed_markers": rep_fail.deterministic_markers,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if passed else 1


def _resolve_input_text(file_arg: Optional[str], text_arg: Optional[str]) -> tuple[str, str]:
    if file_arg:
        path = Path(file_arg)
        return path.read_text(encoding="utf-8", errors="replace"), str(path)
    return text_arg or "", "<inline_text>"


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor Determinístico de Entropia e Fluidez de Prompts (v3.2)")
    parser.add_argument("--file", type=str, help="Caminho de arquivo Markdown/XML/TXT contendo o prompt")
    parser.add_argument("--text", type=str, help="Texto inline do prompt para auditar")
    parser.add_argument(
        "--regime",
        type=str,
        choices=["AUTO", "COGNITIVE_FLUID", "LOW_ENTROPY_CONTRACT"],
        default="AUTO",
        help="Regime operacional de entropia",
    )
    parser.add_argument("--require-xml", action="store_true", help="Exigir tags XML de isolamento Zero-Trust")
    parser.add_argument("--self-test", action="store_true", help="Executar auto-teste determinístico")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.file and not args.text:
        parser.print_help()
        return 0

    content, src_name = _resolve_input_text(args.file, args.text)
    regime_val: EntropyRegimeType = args.regime  # type: ignore[assignment]
    report = audit_prompt_text(content, src_name, regime=regime_val, require_xml_isolation=args.require_xml)
    print(report.model_dump_json(indent=2))
    return 0 if report.status == "APPROVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
