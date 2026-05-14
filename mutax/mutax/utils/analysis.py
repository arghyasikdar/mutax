"""Analysis helpers for generated payloads."""

from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from math import log2


def shannon_entropy(value: str) -> float:
    """Compute Shannon entropy for a string."""

    if not value:
        return 0.0
    counts = Counter(value)
    length = len(value)
    return round(-sum((count / length) * log2(count / length) for count in counts.values()), 4)


def similarity(left: str, right: str) -> float:
    """Return a normalized similarity ratio between two payloads."""

    return SequenceMatcher(None, left, right).ratio()

