"""A NRRD leftover: every axis lands in one unsigned list."""

from __future__ import annotations

AXES: dict[str, list] = {}


def register(spc, nrrd_id: str | None = None) -> None:
    if not nrrd_id:
        raise ValueError("nrrd axis requires a nrrd id")
    AXES.setdefault(nrrd_id, []).append({"spc": spc})
