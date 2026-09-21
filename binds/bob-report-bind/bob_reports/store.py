"""Open leftover: every bob report lands in one unsigned list."""

from __future__ import annotations

REPORTS: dict[str, list] = {}


def register(note: str, bob_id: str | None = None) -> None:
    if not bob_id:
        raise ValueError("bob report requires a bob id")
    REPORTS.setdefault(bob_id, []).append({"note": note})
