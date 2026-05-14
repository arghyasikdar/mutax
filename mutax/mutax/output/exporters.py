"""Export helpers for mutation batches."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mutax.core.models import Mutation, MutationBatch


def mutation_to_dict(mutation: Mutation) -> dict[str, Any]:
    """Serialize a mutation to a JSON-friendly dictionary."""

    return {
        "payload": mutation.payload,
        "category": mutation.category.value,
        "mutator": mutation.mutator,
        "score": mutation.score,
        "entropy": mutation.entropy,
        "history": list(mutation.history),
        "metadata": mutation.metadata,
    }


def batch_to_dict(batch: MutationBatch) -> dict[str, Any]:
    """Serialize a mutation batch to a JSON-friendly dictionary."""

    return {
        "seed": batch.seed,
        "profile": batch.profile,
        "chained": batch.chained,
        "total": batch.total,
        "duplicates_removed": batch.duplicates_removed,
        "by_mutator": batch.by_mutator,
        "by_category": batch.by_category,
        "mutations": [mutation_to_dict(mutation) for mutation in batch.mutations],
    }


def export_text(batch: MutationBatch, path: Path) -> None:
    """Write payloads only, one per line."""

    payloads = "\n".join(mutation.payload for mutation in batch.mutations)
    path.write_text(f"{payloads}\n", encoding="utf-8")


def export_json(batch: MutationBatch, path: Path) -> None:
    """Write full mutation metadata as formatted JSON."""

    path.write_text(json.dumps(batch_to_dict(batch), indent=2) + "\n", encoding="utf-8")
