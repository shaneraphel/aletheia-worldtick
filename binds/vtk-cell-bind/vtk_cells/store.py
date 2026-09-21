"""A VTK leftover: every cell lands in one unsigned list."""

from __future__ import annotations

CELLS: dict[str, list] = {}


def register(ncell, vtk_id: str | None = None) -> None:
    if not vtk_id:
        raise ValueError("vtk cell requires a vtk id")
    CELLS.setdefault(vtk_id, []).append({"ncell": ncell})
