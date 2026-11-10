"""[LOCK-03] Espelho .context/ -> raiz (CONTEXT.md/SPEC.md) do sync_gemini_ecosystem."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_gemini_ecosystem import _mirror_context_to_root  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_context_sobrescreve_raiz_divergente(tmp_path: Path) -> None:
    _write(tmp_path / ".context" / "context.md", "estado novo\n")
    _write(tmp_path / "CONTEXT.md", "estado antigo\n")
    assert _mirror_context_to_root(tmp_path) == ["CONTEXT.md"]
    assert (tmp_path / "CONTEXT.md").read_text(encoding="utf-8") == "estado novo\n"


def test_raiz_semeia_context_em_repo_legado(tmp_path: Path) -> None:
    _write(tmp_path / "SPEC.md", "spec legada\n")
    assert _mirror_context_to_root(tmp_path) == [".context/spec.md"]
    assert (tmp_path / ".context" / "spec.md").read_text(encoding="utf-8") == "spec legada\n"


def test_identicos_nao_regravam(tmp_path: Path) -> None:
    _write(tmp_path / ".context" / "spec.md", "igual\n")
    _write(tmp_path / "SPEC.md", "igual\n")
    os.utime(tmp_path / "SPEC.md", (1_000_000, 1_000_000))
    assert _mirror_context_to_root(tmp_path) == []
    assert (tmp_path / "SPEC.md").stat().st_mtime == 1_000_000


def test_diferenca_so_de_fim_de_linha_nao_regrava(tmp_path: Path) -> None:
    (tmp_path / ".context").mkdir()
    (tmp_path / ".context" / "context.md").write_bytes(b"linha 1\nlinha 2\n")
    (tmp_path / "CONTEXT.md").write_bytes(b"linha 1\r\nlinha 2\r\n")
    assert _mirror_context_to_root(tmp_path) == []


def test_raiz_nunca_sobrescreve_context(tmp_path: Path) -> None:
    """Adversarial: uma raiz editada à mão não pode vencer a fonte canônica."""
    _write(tmp_path / ".context" / "context.md", "canônico\n")
    _write(tmp_path / "CONTEXT.md", "edição manual na raiz\n")
    _mirror_context_to_root(tmp_path)
    assert (tmp_path / ".context" / "context.md").read_text(encoding="utf-8") == "canônico\n"


def test_sem_arquivos_nao_cria_nada(tmp_path: Path) -> None:
    assert _mirror_context_to_root(tmp_path) == []
    assert not any(tmp_path.iterdir())
