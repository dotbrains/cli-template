"""Executor module tests.

Mirrors the Go internal/exec/executor_test.go structure.
"""

from __future__ import annotations

import subprocess

import pytest

from __PROJECT_NAME__.executor import MockExecutor, RealExecutor


def test_real_executor_run() -> None:
    """RealExecutor.run should capture stdout."""
    e = RealExecutor()
    out = e.run("echo", "hello")
    assert "hello" in out


def test_real_executor_run_error() -> None:
    """RealExecutor.run should raise for nonexistent commands."""
    e = RealExecutor()
    with pytest.raises (FileNotFoundError):
        e.run("nonexistent-command-abc123")


def test_real_executor_run_with_stdin() -> None:
    """RealExecutor.run_with_stdin should pass stdin to command."""
    e = RealExecutor()
    out = e.run_with_stdin("hello from stdin", "cat")
    assert "hello from stdin" in out


def test_mock_executor() -> None:
    """MockExecutor should use the provided callback."""
    mock = MockExecutor(run_func=lambda name, *args: "mocked output")

    out = mock.run("anything")
    assert out == "mocked output"


def test_mock_executor_defaults() -> None:
    """MockExecutor with no callbacks should return empty strings."""
    mock = MockExecutor()

    out = mock.run("anything")
    assert out == ""

    out = mock.run_with_stdin("stdin", "anything")
    assert out == ""
