"""An HDF5 leftover: every group lands in one unsigned list."""

from __future__ import annotations

GROUPS: dict[str, list] = {}


def register(path, hdf5_id: str | None = None) -> None:
    if not hdf5_id:
        raise ValueError("hdf5 group requires an hdf5 id")
    GROUPS.setdefault(hdf5_id, []).append({"path": path})
