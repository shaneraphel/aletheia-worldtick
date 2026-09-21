"""Open leftover: every vultr rush run lands in one unsigned list."""

from __future__ import annotations

RUNS: dict[str, list] = {}


def register(job: str, rush_id: str | None = None) -> None:
    if not rush_id:
        raise ValueError("vultr rush run requires a rush id")
    RUNS.setdefault(rush_id, []).append({"job": job})
