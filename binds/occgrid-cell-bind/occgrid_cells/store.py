"""An occupancy leftover: every cell lands in one unsigned list."""

from __future__ import annotations

CELLS: dict[str, list] = {}


def register(occ: str | int, grid_id: str | None = None) -> None:
    if not grid_id:
        raise ValueError("occupancy cell requires a grid id")
    CELLS.setdefault(grid_id, []).append({"occ": occ})
