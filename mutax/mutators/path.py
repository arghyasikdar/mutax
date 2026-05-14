"""Path and normalization bypass mutators."""

from __future__ import annotations

from collections.abc import Iterable

from mutax.core.models import MutationCategory
from mutax.core.mutator import Mutator


class SlashVariantMutator(Mutator):
    """Generate slash duplication and encoded slash variants."""

    name = "slash-variants"
    description = "Expands path separators into duplicate and encoded separator forms."
    category = MutationCategory.PATH_NORMALIZATION
    weight = 1.4

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield slash-centric normalization bypass variants."""

        replacements = ("//", "/./", "%2f", "%2F", "\\")
        for replacement in replacements:
            yield payload.replace("/", replacement)


class DotNormalizationMutator(Mutator):
    """Generate dot-segment normalization variants."""

    name = "dot-normalization"
    description = "Alters dot segments to probe inconsistent path normalization."
    category = MutationCategory.PATH_NORMALIZATION
    weight = 1.5

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield dot normalization bypass variants."""

        yield payload.replace("../", "..././")
        yield payload.replace("..", ".%2e")
        yield payload.replace("../", "..;/")
        yield payload.replace("../", "..%00/")
        yield payload.replace("../", "./../")


class PathSeparatorMutator(Mutator):
    """Generate platform-specific path separator variants."""

    name = "path-separators"
    description = "Mixes POSIX and Windows path separators."
    category = MutationCategory.DIRECTORY_TRAVERSAL
    weight = 1.3

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield separator variants."""

        yield payload.replace("/", "\\")
        yield payload.replace("/", "\\/")
        yield payload.replace("/", "/\\")
        yield payload.replace("/", "%5c")

