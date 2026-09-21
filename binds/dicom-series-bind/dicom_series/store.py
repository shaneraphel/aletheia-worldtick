"""A DICOM leftover: every SOP instance lands in one unsigned list."""

from __future__ import annotations

SERIES: dict[str, list] = {}


def register(sop, dicom_id: str | None = None) -> None:
    if not dicom_id:
        raise ValueError("dicom series requires a dicom id")
    SERIES.setdefault(dicom_id, []).append({"sop": sop})
