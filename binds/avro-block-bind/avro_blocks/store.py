"""An Avro leftover: every block lands in one unsigned list."""

from __future__ import annotations

BLOCKS: dict[str, list] = {}


def register(nrec, avro_id: str | None = None) -> None:
    if not avro_id:
        raise ValueError("avro block requires an avro id")
    BLOCKS.setdefault(avro_id, []).append({"nrec": nrec})
