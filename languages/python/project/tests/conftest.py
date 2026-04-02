"""Shared test fixtures."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture()
def tmp_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Override HOME to a temporary directory for config isolation."""
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path


@pytest.fixture()
def isolated_config(tmp_home: Path) -> Path:
    """Return the expected config path under a temporary HOME."""
    return tmp_home / ".config" / "__PROJECT_NAME__" / "config.yaml"
