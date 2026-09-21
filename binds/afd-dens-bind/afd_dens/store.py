"""An AFD leftover: every row lands in one unsigned list."""

from __future__ import annotations

DENS: dict[str, list] = {}


def register(afd, afd_id: str | None = None) -> None:
    if not afd_id:
        raise ValueError("afd dens requires an afd id")
    DENS.setdefault(afd_id, []).append({"afd": afd})
