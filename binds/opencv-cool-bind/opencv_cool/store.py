"""Open leftover: every cool tile lands in one unsigned list."""

from __future__ import annotations

PIXELS: dict[str, list] = {}


def register(tile: str, graviton_id: str | None = None) -> None:
    if not graviton_id:
        raise ValueError("opencv cool tile requires a graviton id")
    PIXELS.setdefault(graviton_id, []).append({"tile": tile})
