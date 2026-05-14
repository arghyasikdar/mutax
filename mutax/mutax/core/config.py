"""Configuration loading for mutator selection and engine options."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class MutaXConfig:
    """Runtime configuration for a mutation run."""

    enabled_mutators: tuple[str, ...] = ()
    disabled_mutators: tuple[str, ...] = ()
    similarity_threshold: float | None = None
    max_chain_depth: int = 2
    profile: str = "generic"
    metadata: dict[str, Any] = field(default_factory=dict)


def load_config(path: Path | None) -> MutaXConfig:
    """Load optional YAML config from disk."""

    if path is None:
        return MutaXConfig()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return MutaXConfig(
        enabled_mutators=tuple(raw.get("enabled_mutators", ()) or ()),
        disabled_mutators=tuple(raw.get("disabled_mutators", ()) or ()),
        similarity_threshold=raw.get("similarity_threshold"),
        max_chain_depth=int(raw.get("max_chain_depth", 2)),
        profile=str(raw.get("profile", "generic")),
        metadata=dict(raw.get("metadata", {}) or {}),
    )

