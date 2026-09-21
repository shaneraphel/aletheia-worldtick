"""Open leftover: every aviation leg lands in one unsigned list."""

from __future__ import annotations

LEGS: dict[str, list] = {}


def register(route: str, flight_id: str | None = None) -> None:
    if not flight_id:
        raise ValueError("aviation leg requires a flight id")
    LEGS.setdefault(flight_id, []).append({"route": route})
