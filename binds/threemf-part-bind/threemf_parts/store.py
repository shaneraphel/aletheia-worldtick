"""A 3MF leftover: every part lands in one unsigned list."""

from __future__ import annotations

PARTS: dict[str, list] = {}


def register(nobj, threemf_id: str | None = None) -> None:
    if not threemf_id:
        raise ValueError("threemf part requires a threemf id")
    PARTS.setdefault(threemf_id, []).append({"nobj": nobj})
