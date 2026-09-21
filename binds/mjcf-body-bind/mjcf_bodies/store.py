"""An MJCF leftover: every body lands in one unsigned list."""

from __future__ import annotations

BODIES: dict[str, list] = {}


def register(link: str | int, mjcf_id: str | None = None) -> None:
    if not mjcf_id:
        raise ValueError("mjcf body requires an mjcf id")
    BODIES.setdefault(mjcf_id, []).append({"link": link})
