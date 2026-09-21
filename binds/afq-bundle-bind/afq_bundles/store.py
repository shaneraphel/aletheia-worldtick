"""An AFQ leftover: every bundle lands in one unsigned list."""

from __future__ import annotations

BUNDLES: dict[str, list] = {}


def register(ntr, afq_id: str | None = None) -> None:
    if not afq_id:
        raise ValueError("afq bundle requires an afq id")
    BUNDLES.setdefault(afq_id, []).append({"ntr": ntr})
