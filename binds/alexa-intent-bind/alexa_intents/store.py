"""Open leftover: every alexa utterance lands in one unsigned list."""

from __future__ import annotations

UTTERANCES: dict[str, list] = {}


def register(text: str, intent_id: str | None = None) -> None:
    if not intent_id:
        raise ValueError("alexa utterance requires an intent id")
    UTTERANCES.setdefault(intent_id, []).append({"text": text})
