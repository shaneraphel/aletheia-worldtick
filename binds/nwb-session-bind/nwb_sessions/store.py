"""An NWB leftover: every session lands in one unsigned list."""

from __future__ import annotations

SESSIONS: dict[str, list] = {}


def register(path, nwb_id: str | None = None) -> None:
    if not nwb_id:
        raise ValueError("nwb session requires an nwb id")
    SESSIONS.setdefault(nwb_id, []).append({"path": path})
