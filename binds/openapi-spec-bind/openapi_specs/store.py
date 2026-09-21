"""An OpenAPI leftover: every spec lands in one unsigned list."""

from __future__ import annotations

SPECS: dict[str, list] = {}


def register(href: str, openapi_id: str | None = None) -> None:
    if not openapi_id:
        raise ValueError("openapi spec requires an openapi id")
    SPECS.setdefault(openapi_id, []).append({"href": href})
