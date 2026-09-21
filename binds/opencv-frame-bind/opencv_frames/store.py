"""Open leftover: every frame lands in one unsigned list."""

from __future__ import annotations

FRAMES: dict[str, list] = {}


def register(frame: str, camera_id: str | None = None) -> None:
    if not camera_id:
        raise ValueError("opencv frame requires a camera id")
    FRAMES.setdefault(camera_id, []).append({"frame": frame})
