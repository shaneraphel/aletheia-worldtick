"""Sandbox leftover: every job lands in one unsigned list."""

from __future__ import annotations

JOBS: dict[str, list] = {}


def enqueue(cmd: str, isolate_id: str | None = None) -> None:
    if not isolate_id:
        raise ValueError("sandbox job requires an isolate id")
    JOBS.setdefault(isolate_id, []).append({"cmd": cmd})
