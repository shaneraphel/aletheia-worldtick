"""A TDT leftover: every tank lands in one unsigned list."""

from __future__ import annotations

TANKS: dict[str, list] = {}


def register(fs, tdt_id: str | None = None) -> None:
    if not tdt_id:
        raise ValueError("tdt tank requires a tdt id")
    TANKS.setdefault(tdt_id, []).append({"fs": fs})
