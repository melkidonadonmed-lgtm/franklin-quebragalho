"""Unit tests for canonical .context/ migration and root mirror removal."""

from pathlib import Path

from scripts.sync_gemini_ecosystem import _mirror_context_to_root


def test_context_removes_divergent_root_mirror_without_overwriting(tmp_path: Path) -> None:
    ctx_dir = tmp_path / ".context"
    ctx_dir.mkdir(parents=True)
    ctx_file = ctx_dir / "context.md"
    ctx_file.write_text("canonical state\n", encoding="utf-8")
    root_file = tmp_path / "CONTEXT.md"
    root_file.write_text("stale root mirror\n", encoding="utf-8")

    assert _mirror_context_to_root(tmp_path) == []
    assert not root_file.exists()
    assert ctx_file.read_text(encoding="utf-8") == "canonical state\n"


def test_legacy_root_seeds_context_and_unlinks_root(tmp_path: Path) -> None:
    legacy_ctx = tmp_path / "CONTEXT.md"
    legacy_spec = tmp_path / "SPEC.md"
    legacy_ctx.write_text("legacy context\n", encoding="utf-8")
    legacy_spec.write_text("legacy spec\n", encoding="utf-8")

    migrated = _mirror_context_to_root(tmp_path)

    assert migrated == [".context/context.md", ".context/spec.md"]
    assert not legacy_ctx.exists()
    assert not legacy_spec.exists()
    assert (tmp_path / ".context" / "context.md").read_text(encoding="utf-8") == "legacy context\n"
    assert (tmp_path / ".context" / "spec.md").read_text(encoding="utf-8") == "legacy spec\n"


def test_identical_root_mirror_is_removed(tmp_path: Path) -> None:
    ctx_dir = tmp_path / ".context"
    ctx_dir.mkdir(parents=True)
    (ctx_dir / "spec.md").write_text("# Spec\n", encoding="utf-8")
    root_spec = tmp_path / "SPEC.md"
    root_spec.write_text("# Spec\n", encoding="utf-8")

    assert _mirror_context_to_root(tmp_path) == []
    assert not root_spec.exists()
    assert (ctx_dir / "spec.md").read_text(encoding="utf-8") == "# Spec\n"


def test_canonical_only_repo_is_no_op(tmp_path: Path) -> None:
    ctx_dir = tmp_path / ".context"
    ctx_dir.mkdir(parents=True)
    (ctx_dir / "context.md").write_text("canonical\n", encoding="utf-8")
    (ctx_dir / "spec.md").write_text("spec\n", encoding="utf-8")

    assert _mirror_context_to_root(tmp_path) == []
    assert (ctx_dir / "context.md").read_text(encoding="utf-8") == "canonical\n"
    assert (ctx_dir / "spec.md").read_text(encoding="utf-8") == "spec\n"


def test_empty_repo_creates_nothing(tmp_path: Path) -> None:
    assert _mirror_context_to_root(tmp_path) == []
    assert not (tmp_path / ".context").exists()
    assert not (tmp_path / "CONTEXT.md").exists()
    assert not (tmp_path / "SPEC.md").exists()
