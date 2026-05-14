"""High-level mutation engine."""

from __future__ import annotations

from collections.abc import Iterable

from mutax.core.config import MutaXConfig
from mutax.core.models import MutationBatch
from mutax.core.mutator import Mutator
from mutax.core.pipeline import MutationPipeline
from mutax.profiles.registry import get_profile, resolve_mutators


class MutationEngine:
    """Facade for profile-aware payload mutation."""

    def __init__(self, mutators: Iterable[Mutator] | None = None) -> None:
        self._explicit_mutators = tuple(mutators) if mutators is not None else None

    def run(
        self,
        payload: str,
        *,
        profile_name: str = "generic",
        chain: bool = False,
        config: MutaXConfig | None = None,
    ) -> MutationBatch:
        """Generate payload variants for a single seed payload."""

        runtime_config = config or MutaXConfig(profile=profile_name)
        effective_profile = profile_name or runtime_config.profile
        profile = get_profile(effective_profile)
        mutators = self._explicit_mutators or resolve_mutators(
            profile,
            enabled=runtime_config.enabled_mutators,
            disabled=runtime_config.disabled_mutators,
        )
        pipeline = MutationPipeline(
            mutators,
            similarity_threshold=runtime_config.similarity_threshold,
            max_chain_depth=runtime_config.max_chain_depth,
        )
        mutations, removed = pipeline.chained(payload) if chain else pipeline.direct(payload)
        return MutationBatch(
            seed=payload,
            mutations=tuple(mutations),
            duplicates_removed=removed,
            profile=profile.name,
            chained=chain,
        )

