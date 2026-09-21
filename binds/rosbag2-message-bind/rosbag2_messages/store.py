"""A rosbag2 leftover: every message lands in one unsigned list."""

from __future__ import annotations

MESSAGES: dict[str, list] = {}


def register(typ, bag2_id: str | None = None) -> None:
    if not bag2_id:
        raise ValueError("rosbag2 message requires a bag2 id")
    MESSAGES.setdefault(bag2_id, []).append({"typ": typ})
