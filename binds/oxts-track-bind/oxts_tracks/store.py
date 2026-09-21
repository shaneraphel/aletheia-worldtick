"""An OXTS leftover: every fix lands in one unsigned list."""

from __future__ import annotations

FIXES: dict[str, list] = {}


def register(lla: str, oxts_id: str | None = None) -> None:
    if not oxts_id:
        raise ValueError("oxts track requires an oxts id")
    FIXES.setdefault(oxts_id, []).append({"lla": lla})
