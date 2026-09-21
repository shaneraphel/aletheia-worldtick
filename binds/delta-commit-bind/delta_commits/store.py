"""A Delta leftover: every commit lands in one unsigned list."""

from __future__ import annotations

COMMITS: dict[str, list] = {}


def register(ver, delta_id: str | None = None) -> None:
    if not delta_id:
        raise ValueError("delta commit requires a delta id")
    COMMITS.setdefault(delta_id, []).append({"ver": ver})
