"""Open leftover: every resource tape lands in one unsigned list."""

from __future__ import annotations

TAPES: dict[str, list] = {}


def register(uri: str, tape_id: str | None = None) -> None:
    if not tape_id:
        raise ValueError("resource tape requires a tape id")
    TAPES.setdefault(tape_id, []).append({"uri": uri})
