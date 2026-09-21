"""A Parquet leftover: every column lands in one unsigned list."""

from __future__ import annotations

COLUMNS: dict[str, list] = {}


def register(col, parquet_id: str | None = None) -> None:
    if not parquet_id:
        raise ValueError("parquet column requires a parquet id")
    COLUMNS.setdefault(parquet_id, []).append({"col": col})
