"""A BVEC leftover: every direction lands in one unsigned list."""

from __future__ import annotations

BVECS: dict[str, list] = {}


def register(nd, bvec_id: str | None = None) -> None:
    if not bvec_id:
        raise ValueError("bvec dir requires a bvec id")
    BVECS.setdefault(bvec_id, []).append({"nd": nd})
