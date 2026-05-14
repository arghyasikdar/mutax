"""Encoding primitives used by mutators."""

from __future__ import annotations

from urllib.parse import quote


def encode_selected(value: str, characters: set[str]) -> str:
    """Percent-encode selected characters and leave the rest intact."""

    return "".join(f"%{ord(char):02x}" if char in characters else char for char in value)


def double_encode_selected(value: str, characters: set[str]) -> str:
    """Apply percent-encoding twice to selected characters."""

    once = encode_selected(value, characters)
    return once.replace("%", "%25")


def full_url_encode(value: str) -> str:
    """Percent-encode every non-alphanumeric payload character."""

    return quote(value, safe="")


def double_full_url_encode(value: str) -> str:
    """Double URL-encode a payload."""

    return quote(full_url_encode(value), safe="")


def overlong_slash(value: str) -> str:
    """Replace slashes with historical overlong UTF-8 slash encodings."""

    return value.replace("/", "%c0%af").replace("\\", "%c1%9c")

