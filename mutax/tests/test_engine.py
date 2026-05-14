"""Engine and pipeline tests."""

from __future__ import annotations

from mutax.core.engine import MutationEngine
from mutax.core.mutator import Mutator


class DuplicateMutator(Mutator):
    """Test mutator that intentionally emits duplicates."""

    name = "duplicate"
    description = "test duplicate mutator"

    def mutate(self, payload: str) -> list[str]:
        """Return duplicate variants."""

        return [f"{payload}%00", f"{payload}%00"]


def test_engine_deduplicates_payloads() -> None:
    """Engine should remove duplicate payload strings automatically."""

    batch = MutationEngine([DuplicateMutator()]).run("../../etc/passwd")
    assert batch.total == 1
    assert batch.duplicates_removed == 1


def test_engine_supports_chained_transformations() -> None:
    """Chained mode should preserve transformation history."""

    batch = MutationEngine().run("../../etc/passwd", profile_name="apache", chain=True)
    assert batch.total > 10
    assert any(len(mutation.history) > 1 for mutation in batch.mutations)


def test_profile_changes_mutator_selection() -> None:
    """IIS profile should prioritize Windows path separators."""

    batch = MutationEngine().run("../../etc/passwd", profile_name="iis")
    assert "path-separators" in batch.by_mutator
    assert any("\\etc\\passwd" in mutation.payload for mutation in batch.mutations)

