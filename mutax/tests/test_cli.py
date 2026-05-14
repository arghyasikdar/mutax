"""CLI tests."""

from __future__ import annotations

import json

from typer.testing import CliRunner

from mutax.cli.app import app

runner = CliRunner()


def test_cli_json_output() -> None:
    """CLI should emit structured JSON when requested."""

    result = runner.invoke(app, ["-p", "../../etc/passwd", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["seed"] == "../../etc/passwd"
    assert payload["total"] > 0


def test_cli_writes_text_output(tmp_path) -> None:
    """CLI should export payloads to a text file."""

    output = tmp_path / "payloads.txt"
    result = runner.invoke(app, ["-p", "../../etc/passwd", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    assert "..%2f..%2fetc%2fpasswd" in output.read_text(encoding="utf-8")


def test_cli_lists_profiles() -> None:
    """CLI should list bundled profiles."""

    result = runner.invoke(app, ["profiles"])
    assert result.exit_code == 0
    assert "apache" in result.stdout
    assert "nginx" in result.stdout

