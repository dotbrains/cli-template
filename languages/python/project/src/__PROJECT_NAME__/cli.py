"""CLI entry point using Click.

Mirrors the Go cmd/root.go pattern: thin command wrappers around internal logic.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click

from __PROJECT_NAME__ import __version__
from __PROJECT_NAME__.config import Config, default_config, load_config, save_config


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(__version__, prog_name="__PROJECT_NAME__")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """__PROJECT_DESCRIPTION_LONG__"""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.group()
def config() -> None:
    """Manage configuration."""


@config.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing config.")
def config_init(force: bool) -> None:
    """Create default config file."""
    cfg_path = _config_path()

    if not force and cfg_path.exists():
        click.echo(f"Error: config already exists at {cfg_path} (use --force to overwrite)", err=True)
        sys.exit(1)

    save_config(default_config(), cfg_path)

    display = _shorten_path(cfg_path)
    click.echo(f"\u2713 Wrote default config to {display}")
    click.echo("Edit the file to customize settings.")


def _config_path() -> Path:
    """Return the config file path (mirrors config.ConfigPath)."""
    home = Path.home()
    return home / ".config" / "__PROJECT_NAME__" / "config.yaml"


def _shorten_path(path: Path) -> str:
    """Shorten path using ~/ prefix if under home directory."""
    try:
        home = Path.home()
        return "~/" + str(path.relative_to(home))
    except ValueError:
        return str(path)


def main(version: str = __version__) -> None:
    """Entry point for the CLI."""
    cli(max_content_width=100)


if __name__ == "__main__":
    main()
