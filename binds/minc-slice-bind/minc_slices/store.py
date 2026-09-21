"""A MINC leftover: every slice lands in one unsigned list."""

from __future__ import annotations

SLICES: dict[str, list] = {}


def register(z, minc_id: str | None = None) -> None:
    if not minc_id:
        raise ValueError("minc slice requires a minc id")
    SLICES.setdefault(minc_id, []).append({"z": z})
