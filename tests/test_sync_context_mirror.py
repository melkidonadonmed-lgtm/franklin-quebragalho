"""Unit tests for canonical .context/ migration and root mirror removal."""

from pathlib import Path

from scripts.sync_gemini_ecosystem import (
    ROOT_DIR,
    UI_SUBAGENTS,
    _format_antigravity_agent_markdown,
    _mirror_context_to_root,
    _sync_antigravity_config_agents,
)


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


def test_agent_markdown_format_is_idempotent_across_franklin_and_shredded_shape(tmp_path: Path) -> None:
    """Ensure _format_antigravity_agent_markdown and _sync_antigravity_config_agents preserve byte parity."""
    assert _sync_antigravity_config_agents(tmp_path / "missing_src", tmp_path / "dst") == 0

    for agent_file in sorted((ROOT_DIR / "agents").glob("*.md")):
        raw_lf = agent_file.read_text(encoding="utf-8").replace("\r\n", "\n")
        formatted = _format_antigravity_agent_markdown(agent_file)
        assert formatted == raw_lf, f"{agent_file.name} drifted from canonical _format_antigravity_agent_markdown()"

    shredded_agents_dir = ROOT_DIR.parent / "shredded-shape" / "agents"
    if shredded_agents_dir.is_dir():
        dst_dir = tmp_path / ".agents" / "agents"
        dst_dir.mkdir(parents=True)
        (dst_dir / "stale-agent.md").write_text("stale\n", encoding="utf-8")
        synced = _sync_antigravity_config_agents([shredded_agents_dir], dst_dir, allowed_files=UI_SUBAGENTS)
        assert synced == len(UI_SUBAGENTS)
        assert not (dst_dir / "stale-agent.md").exists()
        for fname in UI_SUBAGENTS:
            src_lf = (shredded_agents_dir / fname).read_text(encoding="utf-8").replace("\r\n", "\n")
            dst_lf = (dst_dir / fname).read_text(encoding="utf-8").replace("\r\n", "\n")
            assert _format_antigravity_agent_markdown(shredded_agents_dir / fname) == src_lf
            assert dst_lf == src_lf

    repo_dir = tmp_path / "folded_repo"
    repo_agents = repo_dir / "agents"
    repo_dot_agents = repo_dir / ".agents" / "agents"
    repo_agents.mkdir(parents=True)
    folded_src = (
        "---\nname: ui-analyst\ndescription: >-\n"
        "  Folded YAML description for Stage 0 analyst. Do NOT use for mutating code.\n"
        "subagent: true\nmainAgent: false\nmodel: inherit\ncommandExecutionPolicy: sandbox\n"
        "inheritMcp: true\ninheritCustomizations: true\nmax_steps: 10\nstop_condition: \"DONE\"\n"
        "tools:\n  - read_file\n  - send_message\n---\n\n# Folded Agent\nRespond in pt-BR.\n"
    )
    (repo_agents / "ui-analyst.md").write_text(folded_src, encoding="utf-8", newline="\n")
    assert _sync_antigravity_config_agents([repo_agents], repo_dot_agents, allowed_files=("ui-analyst.md",)) == 1
    assert (repo_dot_agents / "ui-analyst.md").read_text(encoding="utf-8") == folded_src

