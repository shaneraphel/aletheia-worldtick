"""An SIFT leftover: every row lands in one unsigned list."""

from __future__ import annotations

WEIGHTS: dict[str, list] = {}


def register(mu, sift_id: str | None = None) -> None:
    if not sift_id:
        raise ValueError("sift weight requires a sift id")
    WEIGHTS.setdefault(sift_id, []).append({"mu": mu})
