"""Rich terminal rendering for MutaX."""

from __future__ import annotations

from collections import defaultdict

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from mutax.core.models import MutationBatch


def render_banner(console: Console) -> None:
    """Render a restrained professional banner."""

    title = Text("MutaX", style="bold cyan")
    subtitle = Text("Payload Mutation Engine", style="white")
    console.print(
        Panel.fit(
            Text.assemble(title, "  ", subtitle),
            border_style="cyan",
            box=box.SQUARE,
        )
    )


def render_batch(console: Console, batch: MutationBatch, *, verbose: bool = False) -> None:
    """Render grouped mutation output with statistics."""

    render_banner(console)
    console.print(_stats_table(batch))
    console.print(_mutator_tree(batch, verbose=verbose))


def _stats_table(batch: MutationBatch) -> Table:
    table = Table(title="Run Statistics", box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="cyan")
    table.add_row("Seed", batch.seed)
    table.add_row("Profile", batch.profile)
    table.add_row("Chained", "yes" if batch.chained else "no")
    table.add_row("Unique payloads", str(batch.total))
    table.add_row("Duplicates removed", str(batch.duplicates_removed))
    return table


def _mutator_tree(batch: MutationBatch, *, verbose: bool) -> Tree:
    root = Tree("[bold]Mutation Groups[/bold]")
    grouped: dict[str, list[str]] = defaultdict(list)
    meta: dict[str, list[tuple[float, float, tuple[str, ...]]]] = defaultdict(list)
    for mutation in batch.mutations:
        grouped[mutation.mutator].append(mutation.payload)
        meta[mutation.mutator].append((mutation.score, mutation.entropy, mutation.history))

    for mutator, payloads in grouped.items():
        branch = root.add(f"[cyan]{mutator}[/cyan] [dim]({len(payloads)})[/dim]")
        for index, payload in enumerate(payloads[:25], start=1):
            if verbose:
                score, entropy, history = meta[mutator][index - 1]
                branch.add(
                    f"[bold]{index:02d}[/bold] {payload} "
                    f"[dim]score={score:.2f} entropy={entropy:.2f} "
                    f"chain={' > '.join(history)}[/dim]"
                )
            else:
                branch.add(f"[bold]{index:02d}[/bold] {payload}")
        if len(payloads) > 25:
            branch.add(f"[dim]... {len(payloads) - 25} more[/dim]")
    return root
