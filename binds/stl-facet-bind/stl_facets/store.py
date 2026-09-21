"""An STL leftover: every facet lands in one unsigned list."""

from __future__ import annotations

FACETS: dict[str, list] = {}


def register(ntri, stl_id: str | None = None) -> None:
    if not stl_id:
        raise ValueError("stl facet requires a stl id")
    FACETS.setdefault(stl_id, []).append({"ntri": ntri})
