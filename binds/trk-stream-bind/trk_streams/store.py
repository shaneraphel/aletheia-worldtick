"""A TRK leftover: every stream lands in one unsigned list."""

from __future__ import annotations

STREAMS: dict[str, list] = {}


def register(npts, trk_id: str | None = None) -> None:
    if not trk_id:
        raise ValueError("trk stream requires a trk id")
    STREAMS.setdefault(trk_id, []).append({"npts": npts})
