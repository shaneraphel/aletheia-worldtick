"""An MCAP leftover: every channel lands in one unsigned list."""

from __future__ import annotations

CHANNELS: dict[str, list] = {}


def register(topic: str | int, mcap_id: str | None = None) -> None:
    if not mcap_id:
        raise ValueError("mcap channel requires an mcap id")
    CHANNELS.setdefault(mcap_id, []).append({"topic": topic})
