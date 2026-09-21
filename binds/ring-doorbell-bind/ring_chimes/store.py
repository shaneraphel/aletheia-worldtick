"""Ring leftover: every chime lands in one unsigned list."""

from __future__ import annotations

CHIMES: dict[str, list] = {}


def ring(event: str, doorbell_id: str | None = None) -> None:
    if not doorbell_id:
        raise ValueError("ring chime requires a doorbell id")
    CHIMES.setdefault(doorbell_id, []).append({"event": event})
