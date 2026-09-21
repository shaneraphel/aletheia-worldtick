"""Open leftover: every gdf header lands in one unsigned list."""

from __future__ import annotations

HEADERS: dict[str, list] = {}


def register(n_ch: int, gdf_id: str | None = None) -> None:
    if not gdf_id:
        raise ValueError("gdf header requires a gdf id")
    HEADERS.setdefault(gdf_id, []).append({"n_ch": n_ch})
