"""A LAS leftover: every point lands in one unsigned list."""

from __future__ import annotations

POINTS: dict[str, list] = {}


def register(xyz, las_id: str | None = None) -> None:
    if not las_id:
        raise ValueError("las point requires a las id")
    POINTS.setdefault(las_id, []).append({"xyz": xyz})
