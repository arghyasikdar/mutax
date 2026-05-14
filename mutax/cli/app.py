"""Typer-powered command line interface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from mutax import __version__
from mutax.core.config import load_config
from mutax.core.engine import MutationEngine
from mutax.output.exporters import batch_to_dict, export_json, export_text
from mutax.output.rich_renderer import render_batch
from mutax.profiles.registry import PROFILES

app = typer.Typer(
    name="mutax",
    help="MutaX: modular payload mutation engine for authorized offensive security research.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"MutaX {__version__}")
        raise typer.Exit


@app.callback(invoke_without_command=True)
def main(
    payload: Annotated[
        str | None,
        typer.Option(
            "-p",
            "--payload",
            help="Seed payload to mutate, for example ../../etc/passwd.",
        ),
    ] = None,
    profile: Annotated[
        str,
        typer.Option("--profile", help=f"Mutation profile: {', '.join(sorted(PROFILES))}."),
    ] = "generic",
    chain: Annotated[bool, typer.Option("--chain", help="Enable chained transformations.")] = False,
    json_output: Annotated[bool, typer.Option("--json", help="Print JSON output.")] = False,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Write payloads to a file. Use .json for metadata export.",
        ),
    ] = None,
    config: Annotated[
        Path | None,
        typer.Option(
            "--config",
            "-c",
            exists=True,
            file_okay=True,
            dir_okay=False,
            help="YAML config file.",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show scores, entropy, and history."),
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
) -> None:
    """Generate mutation variants for a payload."""

    _ = version
    if payload is None:
        return

    try:
        runtime_config = load_config(config)
        batch = MutationEngine().run(
            payload,
            profile_name=profile,
            chain=chain,
            config=runtime_config,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix.lower() == ".json":
            export_json(batch, output)
        else:
            export_text(batch, output)

    if json_output:
        console.print_json(json.dumps(batch_to_dict(batch)))
        return

    render_batch(console, batch, verbose=verbose)


@app.command("profiles")
def list_profiles() -> None:
    """List available mutation profiles."""

    for name, profile in sorted(PROFILES.items()):
        console.print(f"[cyan]{name}[/cyan]: {profile.description}")
