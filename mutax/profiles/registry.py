"""Named mutation profiles."""

from __future__ import annotations

from dataclasses import dataclass

from mutax.core.mutator import Mutator
from mutax.mutators import BUILTIN_MUTATORS


@dataclass(frozen=True, slots=True)
class MutationProfile:
    """A prioritized set of mutators for a target normalization family."""

    name: str
    description: str
    mutators: tuple[str, ...]


PROFILES: dict[str, MutationProfile] = {
    "apache": MutationProfile(
        name="apache",
        description="Apache-style traversal and dot normalization research profile.",
        mutators=(
            "url-encoding",
            "double-url-encoding",
            "dot-normalization",
            "slash-variants",
            "mixed-encodings",
            "utf8-overlong",
            "null-byte",
            "case-mutation",
        ),
    ),
    "nginx": MutationProfile(
        name="nginx",
        description="nginx-oriented slash merge, encoded separator, and normalization profile.",
        mutators=(
            "slash-variants",
            "url-encoding",
            "mixed-encodings",
            "unicode-slashes",
            "dot-normalization",
            "double-url-encoding",
            "case-mutation",
        ),
    ),
    "iis": MutationProfile(
        name="iis",
        description="IIS/Windows-oriented separator and case normalization profile.",
        mutators=(
            "path-separators",
            "case-mutation",
            "url-encoding",
            "double-url-encoding",
            "unicode-slashes",
            "null-byte",
            "mixed-encodings",
        ),
    ),
    "waf": MutationProfile(
        name="waf",
        description="Generic WAF bypass research profile emphasizing mixed encodings.",
        mutators=(
            "mixed-encodings",
            "double-url-encoding",
            "utf8-overlong",
            "unicode-slashes",
            "url-encoding",
            "slash-variants",
            "null-byte",
            "dot-normalization",
        ),
    ),
    "generic": MutationProfile(
        name="generic",
        description="Balanced profile for traversal and LFI payload mutation.",
        mutators=tuple(mutator().name for mutator in BUILTIN_MUTATORS),
    ),
}


def get_profile(name: str) -> MutationProfile:
    """Return a profile by name."""

    try:
        return PROFILES[name.lower()]
    except KeyError as exc:
        available = ", ".join(sorted(PROFILES))
        raise ValueError(f"Unknown profile '{name}'. Available profiles: {available}") from exc


def resolve_mutators(
    profile: MutationProfile,
    *,
    enabled: tuple[str, ...] = (),
    disabled: tuple[str, ...] = (),
) -> tuple[Mutator, ...]:
    """Instantiate mutators for a profile with optional config overrides."""

    registry = {mutator().name: mutator for mutator in BUILTIN_MUTATORS}
    selected = tuple(enabled) if enabled else profile.mutators
    disabled_set = set(disabled)
    missing = [name for name in selected if name not in registry]
    if missing:
        raise ValueError(f"Unknown mutator(s): {', '.join(missing)}")
    return tuple(registry[name]() for name in selected if name not in disabled_set)

