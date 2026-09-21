"""A NEV leftover: every unit lands in one unsigned list."""

from __future__ import annotations

UNITS: dict[str, list] = {}


def register(uid, nev_id: str | None = None) -> None:
    if not nev_id:
        raise ValueError("nev unit requires a nev id")
    UNITS.setdefault(nev_id, []).append({"uid": uid})
