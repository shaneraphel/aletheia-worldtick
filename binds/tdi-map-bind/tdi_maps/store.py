"""An TDI leftover: every row lands in one unsigned list."""

from __future__ import annotations

MAPS: dict[str, list] = {}


def register(tdi, tdi_id: str | None = None) -> None:
    if not tdi_id:
        raise ValueError("tdi map requires a tdi id")
    MAPS.setdefault(tdi_id, []).append({"tdi": tdi})
