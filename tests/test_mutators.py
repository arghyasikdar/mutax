"""Mutator behavior tests."""

from __future__ import annotations

import pytest

from mutax.mutators import BUILTIN_MUTATORS
from mutax.mutators.encoding import DoubleUrlEncodeMutator, UrlEncodeMutator, Utf8OverlongMutator
from mutax.mutators.path import PathSeparatorMutator, SlashVariantMutator
from mutax.mutators.text import NullByteMutator


@pytest.mark.parametrize("mutator_type", BUILTIN_MUTATORS)
def test_every_mutator_generates_variants(mutator_type: type) -> None:
    """All built-in mutators should produce at least one changed variant."""

    mutator = mutator_type()
    variants = list(mutator.mutate("../../etc/passwd"))
    assert variants
    assert any(variant != "../../etc/passwd" for variant in variants)


def test_url_encoding_matches_expected_slash_payload() -> None:
    """URL encoding should preserve dots and encode separators for the common case."""

    assert "..%2f..%2fetc%2fpasswd" in list(UrlEncodeMutator().mutate("../../etc/passwd"))


def test_double_url_encoding_matches_expected_payload() -> None:
    """Double URL encoding should generate fully encoded traversal markers."""

    assert "%252e%252e%252f%252e%252e%252fetc%252fpasswd" in list(
        DoubleUrlEncodeMutator().mutate("../../etc/passwd")
    )


def test_slash_variants_include_duplicate_slashes() -> None:
    """Slash variants should include duplicate separator payloads."""

    assert "..//..//etc//passwd" in list(SlashVariantMutator().mutate("../../etc/passwd"))


def test_utf8_overlong_generates_legacy_separator_encoding() -> None:
    """UTF-8 overlong mutator should replace slashes with overlong encodings."""

    assert "..%c0%af..%c0%afetc%c0%afpasswd" in list(
        Utf8OverlongMutator().mutate("../../etc/passwd")
    )


def test_path_separator_generates_windows_payload() -> None:
    """Path separator mutator should generate Windows-style traversal strings."""

    assert "..\\..\\etc\\passwd" in list(PathSeparatorMutator().mutate("../../etc/passwd"))


def test_null_byte_generates_encoded_suffixes() -> None:
    """Null-byte mutator should append encoded terminators."""

    variants = list(NullByteMutator().mutate("../../etc/passwd"))
    assert "../../etc/passwd%00" in variants
    assert "../../etc/passwd%2500" in variants

