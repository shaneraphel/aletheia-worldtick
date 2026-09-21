"""A DWI leftover: every series lands in one unsigned list."""

from __future__ import annotations

DWIS: dict[str, list] = {}


def register(nb0, dwi_id: str | None = None) -> None:
    if not dwi_id:
        raise ValueError("dwi series requires a dwi id")
    DWIS.setdefault(dwi_id, []).append({"nb0": nb0})
