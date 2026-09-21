"""An MIF leftover: every image lands in one unsigned list."""

from __future__ import annotations

MIFS: dict[str, list] = {}


def register(dw, mif_id: str | None = None) -> None:
    if not mif_id:
        raise ValueError("mif image requires a mif id")
    MIFS.setdefault(mif_id, []).append({"dw": dw})
