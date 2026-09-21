"""A Zarr leftover: every array lands in one unsigned list."""

from __future__ import annotations

ARRAYS: dict[str, list] = {}


def register(name, zarr_id: str | None = None) -> None:
    if not zarr_id:
        raise ValueError("zarr array requires a zarr id")
    ARRAYS.setdefault(zarr_id, []).append({"name": name})
