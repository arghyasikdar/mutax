"""Mutation pipeline orchestration."""

from __future__ import annotations

from collections.abc import Iterable

from mutax.core.models import Mutation, MutationCategory
from mutax.core.mutator import Mutator
from mutax.core.scoring import HeuristicScorer
from mutax.utils.analysis import similarity


class MutationPipeline:
    """Apply mutators directly or as chained transformation stages."""

    def __init__(
        self,
        mutators: Iterable[Mutator],
        *,
        similarity_threshold: float | None = None,
        max_chain_depth: int = 2,
    ) -> None:
        self.mutators = tuple(mutators)
        self.similarity_threshold = similarity_threshold
        self.max_chain_depth = max_chain_depth
        self.scorer = HeuristicScorer()

    def direct(self, seed: str) -> tuple[list[Mutation], int]:
        """Apply each mutator to the original seed payload only."""

        base = self._base(seed)
        return self._dedupe(self._apply_mutators([base]))

    def chained(self, seed: str) -> tuple[list[Mutation], int]:
        """Apply mutators breadth-first to build chained transformations."""

        frontier = [self._base(seed)]
        generated: list[Mutation] = []
        for _depth in range(self.max_chain_depth):
            next_frontier = self._apply_mutators(frontier)
            unique, _removed = self._dedupe(next_frontier, existing=generated)
            generated.extend(unique)
            frontier = unique
            if not frontier:
                break
        return self._dedupe(generated)

    def _apply_mutators(self, inputs: Iterable[Mutation]) -> list[Mutation]:
        output: list[Mutation] = []
        for mutation in inputs:
            for mutator in self.mutators:
                output.extend(mutator.transform(mutation, self.scorer))
        return output

    def _base(self, seed: str) -> Mutation:
        return Mutation(
            payload=seed,
            category=MutationCategory.DIRECTORY_TRAVERSAL,
            mutator="seed",
            score=0.0,
            entropy=self.scorer.entropy(seed),
            history=(),
            metadata={"description": "Original seed payload"},
        )

    def _dedupe(
        self,
        mutations: Iterable[Mutation],
        *,
        existing: Iterable[Mutation] = (),
    ) -> tuple[list[Mutation], int]:
        seen = {mutation.payload for mutation in existing}
        unique: list[Mutation] = []
        removed = 0
        for mutation in sorted(mutations, key=lambda item: item.score, reverse=True):
            if mutation.payload in seen or self._too_similar(mutation.payload, unique):
                removed += 1
                continue
            seen.add(mutation.payload)
            unique.append(mutation)
        return unique, removed

    def _too_similar(self, payload: str, existing: list[Mutation]) -> bool:
        if self.similarity_threshold is None:
            return False
        return any(
            similarity(payload, candidate.payload) >= self.similarity_threshold
            for candidate in existing
        )
