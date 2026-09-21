"""An NSX leftover: every channel lands in one unsigned list."""

from __future__ import annotations

CHANS: dict[str, list] = {}


def register(sr, nsx_id: str | None = None) -> None:
    if not nsx_id:
        raise ValueError("nsx chan requires an nsx id")
    CHANS.setdefault(nsx_id, []).append({"sr": sr})
