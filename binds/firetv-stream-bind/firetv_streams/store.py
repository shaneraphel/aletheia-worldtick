"""Fire TV leftover: every stream lands in one unsigned list."""

from __future__ import annotations

STREAMS: dict[str, list] = {}


def queue(title: str, device_id: str | None = None) -> None:
    if not device_id:
        raise ValueError("firetv stream requires a device id")
    STREAMS.setdefault(device_id, []).append({"title": title})
