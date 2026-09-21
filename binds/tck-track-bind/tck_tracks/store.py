"""A TCK leftover: every track lands in one unsigned list."""

from __future__ import annotations

TRACKS: dict[str, list] = {}


def register(nsl, tck_id: str | None = None) -> None:
    if not tck_id:
        raise ValueError("tck track requires a tck id")
    TRACKS.setdefault(tck_id, []).append({"nsl": nsl})
