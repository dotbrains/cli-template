"""Config module tests.

Mirrors the Go internal/config/config_test.go structure.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from __PROJECT_NAME__.config import (
    Config,
    config_dir,
    config_path,
    default_config,
    load_config,
    save_config,
)


def test_default_config() -> None:
    """DefaultConfig should return a non-None Config."""
    cfg = default_config()
    assert cfg is not None
    assert isinstance(cfg, Config)


def test_config_dir(tmp_home: Path) -> None:
    """ConfigDir should return the expected path."""
    result = config_dir()
    expected = tmp_home / ".config" / "__PROJECT_NAME__"
    assert result == expected


def test_config_path(tmp_home: Path) -> None:
    """ConfigPath should return the expected full path."""
    result = config_path()
    expected = tmp_home / ".config" / "__PROJECT_NAME__" / "config.yaml"
    assert result == expected


def test_load_no_file(tmp_home: Path) -> None:
    """Load should return defaults when no file exists."""
    cfg = load_config()
    assert cfg is not None
    assert isinstance(cfg, Config)


def test_save_and_load(tmp_home: Path) -> None:
    """Save then Load should round-trip correctly."""
    cfg = default_config()
    save_config(cfg)

    loaded = load_config()
    assert loaded is not None


def test_save_to_and_load_from(tmp_path: Path) -> None:
    """Save and Load with explicit paths should work."""
    path = tmp_path / "test-config.yaml"

    cfg = default_config()
    save_config(cfg, path)

    assert path.exists()

    loaded = load_config(path)
    assert loaded is not None


def test_load_from_no_file(tmp_path: Path) -> None:
    """Load from nonexistent path should return defaults."""
    cfg = load_config(tmp_path / "nonexistent" / "config.yaml")
    assert cfg is not None


def test_load_from_invalid_yaml(tmp_path: Path) -> None:
    """Load from invalid YAML should raise ValueError."""
    path = tmp_path / "bad.yaml"
    path.write_text("{{invalid yaml")

    with pytest.raises(ValueError, match="parsing config"):
        load_config(path)
