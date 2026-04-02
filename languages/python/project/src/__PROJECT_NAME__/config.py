"""YAML configuration management.

Mirrors the Go internal/config package: Load, Save, defaults.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Config:
    """Top-level configuration.

    Add your project-specific config fields here.

    Example:
        default_agent: str = "claude-cli"
        agents: dict[str, Any] = field(default_factory=dict)
    """

    # Add your project-specific config fields here.
    pass


def default_config() -> Config:
    """Return the built-in default configuration."""
    return Config()


def config_dir() -> Path:
    """Return the configuration directory path."""
    return Path.home() / ".config" / "__PROJECT_NAME__"


def config_path() -> Path:
    """Return the full path to the config file."""
    return config_dir() / "config.yaml"


def load_config(path: Path | None = None) -> Config:
    """Read config from disk, falling back to defaults if no file exists."""
    if path is None:
        path = config_path()

    if not path.exists():
        return default_config()

    try:
        data = path.read_text(encoding="utf-8")
    except OSError as e:
        msg = f"reading config: {e}"
        raise OSError(msg) from e

    try:
        raw: dict[str, Any] = yaml.safe_load(data) or {}
    except yaml.YAMLError as e:
        msg = f"parsing config {path}: {e}"
        raise ValueError(msg) from e

    cfg = default_config()
    for key, value in raw.items():
        if hasattr(cfg, key):
            setattr(cfg, key, value)
    return cfg


def save_config(cfg: Config, path: Path | None = None) -> None:
    """Write config to disk, creating directories as needed."""
    if path is None:
        path = config_path()

    path.parent.mkdir(parents=True, exist_ok=True)

    data = _config_to_dict(cfg)
    try:
        path.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False), encoding="utf-8")
    except OSError as e:
        msg = f"writing config: {e}"
        raise OSError(msg) from e


def _config_to_dict(cfg: Config) -> dict[str, Any]:
    """Convert a Config dataclass to a dict for YAML serialization."""
    result: dict[str, Any] = {}
    for f in cfg.__dataclass_fields__:
        value = getattr(cfg, f)
        if value != getattr(default_config(), f):
            result[f] = value
    return result
