"""A BVAL leftover: every shell lands in one unsigned list."""

from __future__ import annotations

BVALS: dict[str, list] = {}


def register(nb, bval_id: str | None = None) -> None:
    if not bval_id:
        raise ValueError("bval shell requires a bval id")
    BVALS.setdefault(bval_id, []).append({"nb": nb})
