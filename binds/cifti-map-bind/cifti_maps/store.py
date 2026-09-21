"""A CIFTI leftover: every map lands in one unsigned list."""

from __future__ import annotations

MAPS: dict[str, list] = {}


def register(dconn, cifti_id: str | None = None) -> None:
    if not cifti_id:
        raise ValueError("cifti map requires a cifti id")
    MAPS.setdefault(cifti_id, []).append({"dconn": dconn})
