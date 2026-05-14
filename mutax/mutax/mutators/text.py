"""Textual payload mutators."""

from __future__ import annotations

from collections.abc import Iterable

from mutax.core.models import MutationCategory
from mutax.core.mutator import Mutator


class NullByteMutator(Mutator):
    """Append null-byte terminator variants for legacy parser research."""

    name = "null-byte"
    description = "Appends encoded null-byte terminators."
    category = MutationCategory.LFI_BYPASS
    weight = 1.7

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield null-byte suffixed variants."""

        yield f"{payload}%00"
        yield f"{payload}%2500"
        yield f"{payload}\\x00"


class CaseMutationMutator(Mutator):
    """Generate stable case variants for path payloads."""

    name = "case-mutation"
    description = "Changes path segment casing while preserving traversal markers."
    category = MutationCategory.WAF_BYPASS
    weight = 1.0

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield case variants."""

        yield payload.upper()
        yield payload.lower()
        yield "".join(
            char.upper() if index % 2 == 0 else char.lower()
            for index, char in enumerate(payload)
        )
