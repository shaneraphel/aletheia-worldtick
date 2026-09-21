"""Open leftover: every cds message lands in one unsigned list."""

from __future__ import annotations

MESSAGES: dict[str, list] = {}


def register(text: str, contact_id: str | None = None) -> None:
    if not contact_id:
        raise ValueError("cds message requires a contact id")
    MESSAGES.setdefault(contact_id, []).append({"text": text})
