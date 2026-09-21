"""An MGZ leftover: every volume lands in one unsigned list."""

from __future__ import annotations

MGHS: dict[str, list] = {}


def register(sz, mgz_id: str | None = None) -> None:
    if not mgz_id:
        raise ValueError("mgz vol requires a mgz id")
    MGHS.setdefault(mgz_id, []).append({"sz": sz})
