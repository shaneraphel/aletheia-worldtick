"""An Arrow leftover: every batch lands in one unsigned list."""

from __future__ import annotations

BATCHES: dict[str, list] = {}


def register(ncols, arrow_id: str | None = None) -> None:
    if not arrow_id:
        raise ValueError("arrow batch requires an arrow id")
    BATCHES.setdefault(arrow_id, []).append({"ncols": ncols})
