"""A PCD leftover: every cloud lands in one unsigned list."""

from __future__ import annotations

CLOUDS: dict[str, list] = {}


def register(path: str, pcd_id: str | None = None) -> None:
    if not pcd_id:
        raise ValueError("pcd cloud requires a pcd id")
    CLOUDS.setdefault(pcd_id, []).append({"path": path})
