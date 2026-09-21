"""An OBJ leftover: every face lands in one unsigned list."""

from __future__ import annotations

FACES: dict[str, list] = {}


def register(nface, obj_id: str | None = None) -> None:
    if not obj_id:
        raise ValueError("obj face requires an obj id")
    FACES.setdefault(obj_id, []).append({"nface": nface})
