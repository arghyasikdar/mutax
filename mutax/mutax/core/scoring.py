"""Payload scoring heuristics."""

from __future__ import annotations

from mutax.core.mutator import MutationScorer
from mutax.utils.analysis import shannon_entropy


class HeuristicScorer(MutationScorer):
    """Score payloads by encoded density, traversal signal, entropy, and chaining depth."""

    def entropy(self, payload: str) -> float:
        """Return Shannon entropy for a payload."""

        return shannon_entropy(payload)

    def score(self, payload: str, weight: float, history: tuple[str, ...]) -> float:
        """Return a stable research-oriented priority score."""

        encoded_density = payload.count("%") * 0.8 + payload.count("\\") * 0.4
        traversal_signal = payload.count("..") * 0.7 + payload.lower().count("%2e") * 0.35
        separator_signal = payload.count("/") * 0.15 + payload.count("\\") * 0.25
        chain_bonus = min(len(history), 4) * 0.3
        entropy_bonus = min(self.entropy(payload), 6.0) * 0.18
        return round(
            weight
            + encoded_density
            + traversal_signal
            + separator_signal
            + chain_bonus
            + entropy_bonus,
            3,
        )
