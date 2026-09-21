"""Open leftover: every emma node lands in one unsigned list."""

from __future__ import annotations

NODES: dict[str, list] = {}


def register(shape: str, cloud_id: str | None = None) -> None:
    if not cloud_id:
        raise ValueError("emma node requires a cloud id")
    NODES.setdefault(cloud_id, []).append({"shape": shape})
