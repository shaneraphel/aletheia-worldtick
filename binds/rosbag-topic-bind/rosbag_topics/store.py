"""A rosbag leftover: every topic lands in one unsigned list."""

from __future__ import annotations

TOPICS: dict[str, list] = {}


def register(name: str, bag_id: str | None = None) -> None:
    if not bag_id:
        raise ValueError("rosbag topic requires a bag id")
    TOPICS.setdefault(bag_id, []).append({"name": name})
