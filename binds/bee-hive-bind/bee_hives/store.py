"""Bee leftover: every note lands in one unsigned list."""

from __future__ import annotations

HIVES: dict[str, list] = {}


def log(note: str, hive_id: str | None = None) -> None:
    if not hive_id:
        raise ValueError("bee note requires a hive id")
    HIVES.setdefault(hive_id, []).append({"note": note})
