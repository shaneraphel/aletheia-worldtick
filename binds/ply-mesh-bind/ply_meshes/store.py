"""A PLY leftover: every face lands in one unsigned list."""

from __future__ import annotations

FACES: dict[str, list] = {}


def register(n, ply_id: str | None = None) -> None:
    if not ply_id:
        raise ValueError("ply mesh requires a ply id")
    FACES.setdefault(ply_id, []).append({"n": n})
