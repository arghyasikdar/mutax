"""Shared domain models for payload mutation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MutationCategory(StrEnum):
    """High-level payload category used for grouping and reporting."""

    DIRECTORY_TRAVERSAL = "directory-traversal"
    LFI_BYPASS = "lfi-bypass"
    PATH_NORMALIZATION = "path-normalization"
    WAF_BYPASS = "waf-bypass"


@dataclass(frozen=True, slots=True)
class Mutation:
    """A generated payload with provenance and scoring metadata."""

    payload: str
    category: MutationCategory
    mutator: str
    score: float
    entropy: float
    history: tuple[str, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_transform(
        self,
        payload: str,
        mutator: str,
        score: float,
        entropy: float,
        category: MutationCategory | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Mutation:
        """Return a copy extended with another transformation step."""

        merged_metadata = dict(self.metadata)
        if metadata:
            merged_metadata.update(metadata)
        return Mutation(
            payload=payload,
            category=category or self.category,
            mutator=mutator,
            score=score,
            entropy=entropy,
            history=(*self.history, mutator),
            metadata=merged_metadata,
        )


@dataclass(frozen=True, slots=True)
class MutationBatch:
    """A deduplicated collection returned by the mutation engine."""

    seed: str
    mutations: tuple[Mutation, ...]
    duplicates_removed: int
    profile: str
    chained: bool

    @property
    def total(self) -> int:
        """Return the number of unique generated payloads."""

        return len(self.mutations)

    @property
    def by_mutator(self) -> dict[str, int]:
        """Count mutations grouped by their final mutator."""

        counts: dict[str, int] = {}
        for mutation in self.mutations:
            counts[mutation.mutator] = counts.get(mutation.mutator, 0) + 1
        return counts

    @property
    def by_category(self) -> dict[str, int]:
        """Count mutations grouped by category."""

        counts: dict[str, int] = {}
        for mutation in self.mutations:
            key = mutation.category.value
            counts[key] = counts.get(key, 0) + 1
        return counts
