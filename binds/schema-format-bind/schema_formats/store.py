"""Open leftover: every format schema lands in one unsigned list."""

from __future__ import annotations

SCHEMAS: dict[str, list] = {}


def register(path: str, schema_id: str | None = None) -> None:
    if not schema_id:
        raise ValueError("format schema requires a schema id")
    SCHEMAS.setdefault(schema_id, []).append({"path": path})
