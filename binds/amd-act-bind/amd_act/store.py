"""Open leftover: every amd act kernel lands in one unsigned list."""

from __future__ import annotations

KERNELS: dict[str, list] = {}


def register(op: str, act_id: str | None = None) -> None:
    if not act_id:
        raise ValueError("amd act kernel requires an act id")
    KERNELS.setdefault(act_id, []).append({"op": op})
