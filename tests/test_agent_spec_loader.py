"""Contratos de compatibilidade do loader de manifestos declarativos (max_steps legado)."""

import pytest
from pydantic import ValidationError

from shared.agent_spec_loader import DeclarativeAgentSpec, load_agent_spec


def test_top_level_max_steps_alimenta_guardrails() -> None:
    """`max_steps` no topo (formato legado) deve virar `guardrails.max_steps`."""
    spec = DeclarativeAgentSpec(name="compat", max_steps=7)
    assert spec.guardrails.max_steps == 7


def test_guardrails_aninhado_tem_precedencia() -> None:
    """Quando os dois existem, o valor aninhado vence o atalho."""
    spec = DeclarativeAgentSpec(name="compat", max_steps=7, guardrails={"max_steps": 12})
    assert spec.guardrails.max_steps == 12


def test_campo_desconhecido_continua_proibido() -> None:
    """O contrato segue fechado: campos desconhecidos continuam rejeitados."""
    with pytest.raises(ValidationError):
        DeclarativeAgentSpec(name="compat", campo_inexistente=1)


def test_manifesto_do_shredded_shape_carrega() -> None:
    """O manifesto que quebrava o pre-commit precisa carregar com max_steps e stop_condition aplicados."""
    from pathlib import Path

    target = Path(__file__).resolve().parents[1].parent / "shredded-shape" / "agents" / "ui-analyst.md"
    if not target.is_file():
        pytest.skip("shredded-shape ausente nesta maquina")
    spec = load_agent_spec(str(target), verbose=False)
    assert spec["guardrails"]["max_steps"] == 10
    assert spec["guardrails"]["stop_condition"] == "CLAREZA_REPORT_EMITTED"
    assert spec["enable_write_tools"] is False


def test_top_level_stop_condition_alimenta_guardrails() -> None:
    """`stop_condition` declarado no topo deve ser encaminhado para `guardrails.stop_condition`."""
    spec = DeclarativeAgentSpec(name="compat", max_steps=9, stop_condition="CUSTOM_DONE")
    assert spec.guardrails.max_steps == 9
    assert spec.guardrails.stop_condition == "CUSTOM_DONE"
