"""A GeoParquet leftover: every feature lands in one unsigned list."""

from __future__ import annotations

FEATURES: dict[str, list] = {}


def register(geom, geoparquet_id: str | None = None) -> None:
    if not geoparquet_id:
        raise ValueError("geoparquet feature requires a geoparquet id")
    FEATURES.setdefault(geoparquet_id, []).append({"geom": geom})
