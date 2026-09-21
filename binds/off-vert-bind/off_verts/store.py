"""An OFF leftover: every vertex count lands in one unsigned list."""

from __future__ import annotations

VERTS: dict[str, list] = {}


def register(nv, off_id: str | None = None) -> None:
    if not off_id:
        raise ValueError("off vert requires an off id")
    VERTS.setdefault(off_id, []).append({"nv": nv})
