"""An Iceberg leftover: every snapshot lands in one unsigned list."""

from __future__ import annotations

SNAPSHOTS: dict[str, list] = {}


def register(sid, iceberg_id: str | None = None) -> None:
    if not iceberg_id:
        raise ValueError("iceberg snapshot requires an iceberg id")
    SNAPSHOTS.setdefault(iceberg_id, []).append({"sid": sid})
