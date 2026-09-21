"""An SIFT2 leftover: every row lands in one unsigned list."""

from __future__ import annotations

STREAM_W: dict[str, list] = {}


def register(sift2, sift2_id: str | None = None) -> None:
    if not sift2_id:
        raise ValueError("sift2 weight requires a sift2 id")
    STREAM_W.setdefault(sift2_id, []).append({"sift2": sift2})
