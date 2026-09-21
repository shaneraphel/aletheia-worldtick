"""Agent-week leftover: every booking lands in one unsigned list."""

from __future__ import annotations

SLOTS: dict[str, list] = {}


def book(agent: str, week_id: str | None = None) -> None:
    if not week_id:
        raise ValueError("agent week slot requires a week id")
    SLOTS.setdefault(week_id, []).append({"agent": agent})
