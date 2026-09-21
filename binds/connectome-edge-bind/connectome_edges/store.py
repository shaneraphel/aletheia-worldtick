"""An CONNECTOME leftover: every row lands in one unsigned list."""

from __future__ import annotations

EDGES: dict[str, list] = {}


def register(w, connectome_id: str | None = None) -> None:
    if not connectome_id:
        raise ValueError("connectome edge requires a connectome id")
    EDGES.setdefault(connectome_id, []).append({"w": w})
