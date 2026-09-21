"""A GeoTIFF leftover: every tile lands in one unsigned list."""

from __future__ import annotations

TILES: dict[str, list] = {}


def register(xy, geotiff_id: str | None = None) -> None:
    if not geotiff_id:
        raise ValueError("geotiff tile requires a geotiff id")
    TILES.setdefault(geotiff_id, []).append({"xy": xy})
