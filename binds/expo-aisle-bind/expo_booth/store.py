"""Expo booth leftover: every team lands in one unsigned list."""

from __future__ import annotations

BOOTHS: dict[str, list] = {}


def register(team: str, aisle: str | None = None) -> None:
    if not aisle:
        raise ValueError("expo booth requires an aisle")
    BOOTHS.setdefault(aisle, []).append({"team": team})
