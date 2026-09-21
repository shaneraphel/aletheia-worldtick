"""A GIFTI leftover: every surface lands in one unsigned list."""

from __future__ import annotations

SURFS: dict[str, list] = {}


def register(nvert, gifti_id: str | None = None) -> None:
    if not gifti_id:
        raise ValueError("gifti surf requires a gifti id")
    SURFS.setdefault(gifti_id, []).append({"nvert": nvert})
