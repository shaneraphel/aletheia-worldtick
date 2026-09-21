"""An FDC leftover: every row lands in one unsigned list."""

from __future__ import annotations

FDCS: dict[str, list] = {}


def register(fdc, fdc_id: str | None = None) -> None:
    if not fdc_id:
        raise ValueError("fdc metric requires an fdc id")
    FDCS.setdefault(fdc_id, []).append({"fdc": fdc})
