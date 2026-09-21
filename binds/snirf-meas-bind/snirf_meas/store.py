"""A SNIRF leftover: every measurement lands in one unsigned list."""

from __future__ import annotations

MEAS: dict[str, list] = {}


def register(wl, snirf_id: str | None = None) -> None:
    if not snirf_id:
        raise ValueError("snirf meas requires a snirf id")
    MEAS.setdefault(snirf_id, []).append({"wl": wl})
