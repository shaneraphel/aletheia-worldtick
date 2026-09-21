"""A URDF leftover: every joint lands in one unsigned list."""

from __future__ import annotations

JOINTS: dict[str, list] = {}


def register(name: str, urdf_id: str | None = None) -> None:
    if not urdf_id:
        raise ValueError("urdf joint requires a urdf id")
    JOINTS.setdefault(urdf_id, []).append({"name": name})
