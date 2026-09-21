"""A NIfTI leftover: every volume lands in one unsigned list."""

from __future__ import annotations

VOLS: dict[str, list] = {}


def register(dim, nifti_id: str | None = None) -> None:
    if not nifti_id:
        raise ValueError("nifti vol requires a nifti id")
    VOLS.setdefault(nifti_id, []).append({"dim": dim})
