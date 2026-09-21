"""A FIXEL leftover: every direction lands in one unsigned list."""

from __future__ import annotations

FIXELS: dict[str, list] = {}


def register(ndir, fixel_id: str | None = None) -> None:
    if not fixel_id:
        raise ValueError("fixel dir requires a fixel id")
    FIXELS.setdefault(fixel_id, []).append({"ndir": ndir})
