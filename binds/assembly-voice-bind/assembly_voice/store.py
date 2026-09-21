"""Open leftover: every assembly clip lands in one unsigned list."""

from __future__ import annotations

CLIPS: dict[str, list] = {}


def register(audio: str, voice_id: str | None = None) -> None:
    if not voice_id:
        raise ValueError("assembly clip requires a voice id")
    CLIPS.setdefault(voice_id, []).append({"audio": audio})
