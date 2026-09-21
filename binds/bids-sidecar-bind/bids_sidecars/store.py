"""A BIDS leftover: every sidecar lands in one unsigned list."""

from __future__ import annotations

SIDECARS: dict[str, list] = {}


def register(suffix, bids_id: str | None = None) -> None:
    if not bids_id:
        raise ValueError("bids sidecar requires a bids id")
    SIDECARS.setdefault(bids_id, []).append({"suffix": suffix})
