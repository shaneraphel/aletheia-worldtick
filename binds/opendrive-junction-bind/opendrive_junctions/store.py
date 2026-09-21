"""An OpenDRIVE leftover: every junction lands in one unsigned list."""

from __future__ import annotations

JUNCTIONS: dict[str, list] = {}


def register(rid: str, xodr_id: str | None = None) -> None:
    if not xodr_id:
        raise ValueError("opendrive junction requires an xodr id")
    JUNCTIONS.setdefault(xodr_id, []).append({"rid": rid})
