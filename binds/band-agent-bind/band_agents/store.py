"""Open leftover: every band agent lands in one unsigned list."""

from __future__ import annotations

AGENTS: dict[str, list] = {}


def register(goal: str, band_id: str | None = None) -> None:
    if not band_id:
        raise ValueError("band agent requires a band id")
    AGENTS.setdefault(band_id, []).append({"goal": goal})
