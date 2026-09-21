"""A dataset leftover: every card lands in one unsigned list."""

from __future__ import annotations

CARDS: dict[str, list] = {}


def register(doi: str, card_id: str | None = None) -> None:
    if not card_id:
        raise ValueError("dataset card requires a card id")
    CARDS.setdefault(card_id, []).append({"doi": doi})
