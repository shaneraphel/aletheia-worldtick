"""An ORC leftover: every stripe lands in one unsigned list."""

from __future__ import annotations

STRIPES: dict[str, list] = {}


def register(rid, orc_id: str | None = None) -> None:
    if not orc_id:
        raise ValueError("orc stripe requires an orc id")
    STRIPES.setdefault(orc_id, []).append({"rid": rid})
