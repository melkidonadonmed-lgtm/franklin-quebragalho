"""Unit and adversarial tests for SOTA 4-tier verdict ranking in vault_palace_search."""

from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "obsidian-vault-curator"
    / "scripts"
    / "vault_palace_search.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("vault_palace_search", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_sota_veredito_ranking_orders_recomendado_above_contraindicado(tmp_path: Path, monkeypatch) -> None:
    """Verify recomendado outscores casos-especificos, nao-recomendado, and contraindicacao-total."""
    mod = _load_module()
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "sections_cache.json")

    proj_dir = tmp_path / "Projetos"
    proj_dir.mkdir(parents=True)
    body = "# Design Tokens OKLCH\n\n## Guia de Tokens de Cor\n\nGuia canônico de tokens de cor para projetos frontend modernos com contraste calibrado e acessibilidade verificável.\n"

    notes = {
        "a_recomendado.md": "---\ntitle: Tokens OKLCH\ndate: 2026-11-20\nstatus: ativo\nveredito: recomendado\ntags:\n  - design\n  - sota/recomendado\n---\n\n" + body,
        "b_casos.md": "---\ntitle: Tokens OKLCH\ndate: 2026-11-20\nstatus: ativo\nveredito: casos-especificos\ntags:\n  - design\n  - sota/casos-especificos\n---\n\n" + body,
        "c_nao_rec.md": "---\ntitle: Tokens OKLCH\ndate: 2026-11-20\nstatus: ativo\nveredito: nao-recomendado\ntags:\n  - design\n  - sota/nao-recomendado\n---\n\n" + body,
        "d_contra.md": "---\ntitle: Tokens OKLCH\ndate: 2026-11-20\nstatus: ativo\nveredito: contraindicacao-total\ntags:\n  - design\n  - sota/contraindicacao-total\n---\n\n" + body,
    }
    for fname, content in notes.items():
        (proj_dir / fname).write_text(content, encoding="utf-8")

    resp = mod.search_vault_and_palace(
        query="tokens cor oklch",
        vault_path=tmp_path,
        room="",
        mode="fast",
        limit=10,
        force_rebuild=True,
    )
    ordered = [h.veredito for h in resp.hits]
    assert ordered == ["recomendado", "casos-especificos", "nao-recomendado", "contraindicacao-total"]
    assert resp.hits[0].score > resp.hits[1].score > resp.hits[2].score > resp.hits[3].score


def test_adversarial_contraindicado_demoted_out_of_projetos_room(tmp_path: Path, monkeypatch) -> None:
    """Adversarial: even if mislabeled status: ativo inside Projetos/, contraindicacao-total is demoted to arquivo."""
    mod = _load_module()
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "sections_cache.json")

    proj_dir = tmp_path / "Projetos"
    proj_dir.mkdir(parents=True)
    (proj_dir / "bad_palette.md").write_text(
        "---\ntitle: Paleta Hex Antiga\ndate: 2026-10-05\nstatus: ativo\nveredito: contraindicacao-total\ntags:\n  - design\n---\n\n"
        "# Paleta Hex Antiga\n\nPaleta fixa em Hex e HSL de Tailwind v3 que viola a arquitetura OKLCH e induz viés de ancoragem em interfaces.\n",
        encoding="utf-8",
    )

    scoped = mod.search_vault_and_palace(
        query="paleta hex antiga",
        vault_path=tmp_path,
        room="projetos",
        mode="fast",
        limit=5,
        force_rebuild=True,
    )
    assert scoped.hits == []

    archived = mod.search_vault_and_palace(
        query="paleta hex antiga",
        vault_path=tmp_path,
        room="arquivo",
        mode="fast",
        limit=5,
        force_rebuild=False,
    )
    assert len(archived.hits) == 1
    assert archived.hits[0].room == "arquivo"
    assert archived.hits[0].veredito == "contraindicacao-total"


def test_private_phi_notes_never_indexed(tmp_path: Path, monkeypatch) -> None:
    """Adversarial: notes marked phi: true must be excluded completely from search results."""
    mod = _load_module()
    monkeypatch.setattr(mod, "CACHE_PATH", tmp_path / "sections_cache.json")

    med_dir = tmp_path / "Medicina"
    med_dir.mkdir(parents=True)
    (med_dir / "caso_privado.md").write_text(
        "---\ntitle: Caso Privado\ndate: 2026-11-20\nphi: true\nveredito: recomendado\ntags:\n  - medicina\n---\n\n"
        "# Caso Privado\n\nConteúdo clínico confidencial que nunca pode ser indexado ou devolvido em buscas de memória.\n",
        encoding="utf-8",
    )

    resp = mod.search_vault_and_palace(
        query="caso privado confidencial",
        vault_path=tmp_path,
        room="all",
        mode="fast",
        limit=5,
        force_rebuild=True,
    )
    assert resp.hits == []
