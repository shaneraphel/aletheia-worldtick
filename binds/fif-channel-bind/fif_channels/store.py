"""A FIF leftover: every channel lands in one unsigned list."""

from __future__ import annotations

CHANNELS: dict[str, list] = {}


def register(ch, fif_id: str | None = None) -> None:
    if not fif_id:
        raise ValueError("fif channel requires a fif id")
    CHANNELS.setdefault(fif_id, []).append({"ch": ch})
