"""An FOD leftover: every SH order lands in one unsigned list."""

from __future__ import annotations

FODS: dict[str, list] = {}


def register(lmax, fod_id: str | None = None) -> None:
    if not fod_id:
        raise ValueError("fod sh requires a fod id")
    FODS.setdefault(fod_id, []).append({"lmax": lmax})
