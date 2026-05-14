"""Abstract mutator interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from mutax.core.models import Mutation, MutationCategory


class Mutator(ABC):
    """Base class for every payload mutation strategy."""

    name: str = "mutator"
    description: str = ""
    category: MutationCategory = MutationCategory.WAF_BYPASS
    weight: float = 1.0

    @abstractmethod
    def mutate(self, payload: str) -> Iterable[str]:
        """Yield payload variants for the supplied input."""

    def transform(self, mutation: Mutation, scorer: MutationScorer) -> list[Mutation]:
        """Convert raw string variants into full mutation records."""

        variants: list[Mutation] = []
        for variant in self.mutate(mutation.payload):
            if variant == mutation.payload:
                continue
            score = scorer.score(variant, self.weight, mutation.history)
            variants.append(
                mutation.with_transform(
                    payload=variant,
                    mutator=self.name,
                    score=score,
                    entropy=scorer.entropy(variant),
                    category=self.category,
                    metadata={"description": self.description, "category": self.category.value},
                )
            )
        return variants


class MutationScorer(ABC):
    """Protocol-like scoring base used to avoid circular imports."""

    @abstractmethod
    def score(self, payload: str, weight: float, history: tuple[str, ...]) -> float:
        """Return a numeric usefulness score for a payload."""

    @abstractmethod
    def entropy(self, payload: str) -> float:
        """Return Shannon entropy for a payload."""
