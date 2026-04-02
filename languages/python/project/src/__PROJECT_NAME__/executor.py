"""Command execution abstraction for testability.

Mirrors the Go internal/exec package: CommandExecutor interface + RealExecutor.
"""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod


class CommandExecutor(ABC):
    """Abstract command executor for testability."""

    @abstractmethod
    def run(self, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute a command and return combined stdout output.

        Raises:
            subprocess.CalledProcessError: If the command fails.
            subprocess.TimeoutExpired: If the command times out.
        """

    @abstractmethod
    def run_with_stdin(self, stdin: str, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute a command with stdin and return stdout.

        Raises:
            subprocess.CalledProcessError: If the command fails.
            subprocess.TimeoutExpired: If the command times out.
        """


class RealExecutor(CommandExecutor):
    """Shells out to real commands."""

    def run(self, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute a command and return stdout."""
        try:
            result = subprocess.run(
                [name, *args],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.strip() if e.stderr else ""
            msg = f"{e}: {stderr}"
            raise subprocess.CalledProcessError(e.returncode, e.cmd, output=e.stdout, stderr=msg) from e

    def run_with_stdin(self, stdin: str, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute a command with stdin and return stdout."""
        try:
            result = subprocess.run(
                [name, *args],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.strip() if e.stderr else ""
            msg = f"{e}: {stderr}"
            raise subprocess.CalledProcessError(e.returncode, e.cmd, output=e.stdout, stderr=msg) from e


class MockExecutor(CommandExecutor):
    """Mock executor for testing. Use callbacks to control behavior."""

    def __init__(
        self,
        run_func: callable | None = None,  # type: ignore[type-arg]
        run_with_stdin_func: callable | None = None,  # type: ignore[type-arg]
    ) -> None:
        self._run_func = run_func
        self._run_with_stdin_func = run_with_stdin_func

    def run(self, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute mock command."""
        if self._run_func is not None:
            return self._run_func(name, *args)  # type: ignore[operator]
        return ""

    def run_with_stdin(self, stdin: str, name: str, *args: str, timeout: int | None = None) -> str:
        """Execute mock command with stdin."""
        if self._run_with_stdin_func is not None:
            return self._run_with_stdin_func(stdin, name, *args)  # type: ignore[operator]
        return ""
