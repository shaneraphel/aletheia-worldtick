"""A TRX leftover: every group lands in one unsigned list."""

from __future__ import annotations

GROUPS: dict[str, list] = {}


def register(ng, trx_id: str | None = None) -> None:
    if not trx_id:
        raise ValueError("trx group requires a trx id")
    GROUPS.setdefault(trx_id, []).append({"ng": ng})
