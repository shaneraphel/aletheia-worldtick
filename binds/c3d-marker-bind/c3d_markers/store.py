"""A C3D leftover: every marker lands in one unsigned list."""

from __future__ import annotations

MARKERS: dict[str, list] = {}


def register(lab, c3d_id: str | None = None) -> None:
    if not c3d_id:
        raise ValueError("c3d marker requires a c3d id")
    MARKERS.setdefault(c3d_id, []).append({"lab": lab})
