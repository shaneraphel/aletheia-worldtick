"""A PEAK leftover: every peak lands in one unsigned list."""

from __future__ import annotations

PEAKS: dict[str, list] = {}


def register(npeak, peak_id: str | None = None) -> None:
    if not peak_id:
        raise ValueError("peak dir requires a peak id")
    PEAKS.setdefault(peak_id, []).append({"npeak": npeak})
