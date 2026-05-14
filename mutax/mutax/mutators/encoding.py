"""Encoding mutators for traversal payloads."""

from __future__ import annotations

from collections.abc import Iterable

from mutax.core.models import MutationCategory
from mutax.core.mutator import Mutator
from mutax.encoders.url import (
    double_encode_selected,
    double_full_url_encode,
    encode_selected,
    overlong_slash,
)


class UrlEncodeMutator(Mutator):
    """Encode traversal-significant path characters."""

    name = "url-encoding"
    description = "Percent-encodes traversal-significant characters."
    category = MutationCategory.WAF_BYPASS
    weight = 1.6

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield URL-encoded variants."""

        yield encode_selected(payload, {"/"})
        yield encode_selected(payload, {".", "/"})
        yield encode_selected(payload, {".", "/", "\\"})


class DoubleUrlEncodeMutator(Mutator):
    """Double-encode traversal-significant characters."""

    name = "double-url-encoding"
    description = "Double percent-encodes dots, slashes, and backslashes."
    category = MutationCategory.WAF_BYPASS
    weight = 2.0

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield double URL-encoded variants."""

        yield double_encode_selected(payload, {".", "/"})
        yield double_encode_selected(payload, {"/"})
        yield double_full_url_encode(payload)


class UnicodeSlashMutator(Mutator):
    """Generate Unicode and encoded slash substitutions."""

    name = "unicode-slashes"
    description = "Substitutes path separators with Unicode slash-like code points."
    category = MutationCategory.WAF_BYPASS
    weight = 1.8

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield Unicode slash variants."""

        for slash in ("%u2215", "%u2044", "\u2215", "\u2044"):
            yield payload.replace("/", slash)


class MixedEncodingMutator(Mutator):
    """Blend encoded dots, separators, and raw characters."""

    name = "mixed-encodings"
    description = "Combines encoded dot segments with encoded or raw separators."
    category = MutationCategory.WAF_BYPASS
    weight = 2.2

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield mixed-encoding variants."""

        yield payload.replace("../", "%2e%2e/")
        yield payload.replace("../", "..%2f")
        yield payload.replace("../", "%2e./")
        yield payload.replace("../", ".%2e%2f")
        yield payload.replace("/", "%2f").replace(".", "%2e", 1)


class Utf8OverlongMutator(Mutator):
    """Generate historical UTF-8 overlong separator encodings."""

    name = "utf8-overlong"
    description = "Uses historical overlong UTF-8 encodings for path separators."
    category = MutationCategory.WAF_BYPASS
    weight = 2.1

    def mutate(self, payload: str) -> Iterable[str]:
        """Yield overlong separator variants."""

        yield overlong_slash(payload)
        yield payload.replace("/", "%e0%80%af")

