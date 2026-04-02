"""CLI command tests.

Mirrors the Go cmd/cmd_test.go test structure.
"""

from __future__ import annotations

import os
from pathlib import Path

from click.testing import CliRunner

from __PROJECT_NAME__.cli import cli, config_init


def test_version() -> None:
    """Test --version flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "__PROJECT_NAME__" in result.output


def test_help() -> None:
    """Test --help output contains project name and subcommands."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "__PROJECT_NAME__" in result.output
    assert "config" in result.output


def test_no_args_shows_help() -> None:
    """Test that running with no args shows help."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "config" in result.output


def test_config_init(tmp_home: Path) -> None:
    """Test config init creates config file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "init"])

    assert result.exit_code == 0
    assert "Wrote default config" in result.output

    config_path = tmp_home / ".config" / "__PROJECT_NAME__" / "config.yaml"
    assert config_path.exists()


def test_config_init_already_exists(tmp_home: Path) -> None:
    """Test config init fails when config already exists."""
    # Pre-create config.
    config_dir = tmp_home / ".config" / "__PROJECT_NAME__"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "config.yaml").write_text("existing")

    runner = CliRunner()
    result = runner.invoke(cli, ["config", "init"])

    assert result.exit_code != 0
    assert "already exists" in result.output


def test_config_init_force(tmp_home: Path) -> None:
    """Test config init --force overwrites existing config."""
    # Pre-create config.
    config_dir = tmp_home / ".config" / "__PROJECT_NAME__"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "config.yaml").write_text("existing")

    runner = CliRunner()
    result = runner.invoke(cli, ["config", "init", "--force"])

    assert result.exit_code == 0
    assert "Wrote default config" in result.output
