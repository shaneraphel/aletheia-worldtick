"""Open leftover: every opencv vision action lands in one unsigned list."""

from __future__ import annotations

ACTIONS: dict[str, list] = {}


def register(act: str, vision_id: str | None = None) -> None:
    if not vision_id:
        raise ValueError("opencv vision action requires a vision id")
    ACTIONS.setdefault(vision_id, []).append({"act": act})
