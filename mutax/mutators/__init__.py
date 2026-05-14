"""Built-in mutator registry."""

from mutax.core.mutator import Mutator
from mutax.mutators.encoding import (
    DoubleUrlEncodeMutator,
    MixedEncodingMutator,
    UnicodeSlashMutator,
    UrlEncodeMutator,
    Utf8OverlongMutator,
)
from mutax.mutators.path import DotNormalizationMutator, PathSeparatorMutator, SlashVariantMutator
from mutax.mutators.text import CaseMutationMutator, NullByteMutator

BUILTIN_MUTATORS: tuple[type[Mutator], ...] = (
    UrlEncodeMutator,
    DoubleUrlEncodeMutator,
    UnicodeSlashMutator,
    SlashVariantMutator,
    DotNormalizationMutator,
    MixedEncodingMutator,
    NullByteMutator,
    CaseMutationMutator,
    Utf8OverlongMutator,
    PathSeparatorMutator,
)

__all__ = [
    "BUILTIN_MUTATORS",
    "CaseMutationMutator",
    "DotNormalizationMutator",
    "DoubleUrlEncodeMutator",
    "MixedEncodingMutator",
    "Mutator",
    "NullByteMutator",
    "PathSeparatorMutator",
    "SlashVariantMutator",
    "UnicodeSlashMutator",
    "UrlEncodeMutator",
    "Utf8OverlongMutator",
]

