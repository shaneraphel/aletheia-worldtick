"""An EDF leftover: every signal lands in one unsigned list."""

from __future__ import annotations

SIGNALS: dict[str, list] = {}


def register(label, edf_id: str | None = None) -> None:
    if not edf_id:
        raise ValueError("edf signal requires an edf id")
    SIGNALS.setdefault(edf_id, []).append({"label": label})
