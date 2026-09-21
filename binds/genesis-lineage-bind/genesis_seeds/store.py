"""Genesis leftover: every seed lands in one unsigned list."""

from __future__ import annotations

SEEDS: dict[str, list] = {}


def plant(prompt: str, lineage_id: str | None = None) -> None:
    if not lineage_id:
        raise ValueError("genesis seed requires a lineage id")
    SEEDS.setdefault(lineage_id, []).append({"prompt": prompt})
