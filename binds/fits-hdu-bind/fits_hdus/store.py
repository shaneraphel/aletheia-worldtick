"""A FITS leftover: every HDU lands in one unsigned list."""

from __future__ import annotations

HDUS: dict[str, list] = {}


def register(ext, fits_id: str | None = None) -> None:
    if not fits_id:
        raise ValueError("fits hdu requires a fits id")
    HDUS.setdefault(fits_id, []).append({"ext": ext})
