"""Open leftover: every kiro crew task lands in one unsigned list."""

from __future__ import annotations

CREWS: dict[str, list] = {}


def register(task: str, kiro_id: str | None = None) -> None:
    if not kiro_id:
        raise ValueError("kiro crew task requires a kiro id")
    CREWS.setdefault(kiro_id, []).append({"task": task})
