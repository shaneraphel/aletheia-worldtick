"""Academy share leftover: every post lands in one unsigned list."""

from __future__ import annotations

SHARES: dict[str, list] = {}


def share(url: str, note: str, module_id: str | None = None) -> None:
    if not module_id:
        raise ValueError("academy share requires a module id")
    SHARES.setdefault(module_id, []).append({"url": url, "note": note})
