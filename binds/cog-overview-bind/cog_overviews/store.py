"""A COG leftover: every overview lands in one unsigned list."""

from __future__ import annotations

OVERVIEWS: dict[str, list] = {}


def register(lvl, cog_id: str | None = None) -> None:
    if not cog_id:
        raise ValueError("cog overview requires a cog id")
    OVERVIEWS.setdefault(cog_id, []).append({"lvl": lvl})
