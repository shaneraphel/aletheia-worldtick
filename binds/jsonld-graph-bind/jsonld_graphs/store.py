"""A JSON-LD leftover: every graph lands in one unsigned list."""

from __future__ import annotations

GRAPHS: dict[str, list] = {}


def register(iri: str, jsonld_id: str | None = None) -> None:
    if not jsonld_id:
        raise ValueError("jsonld graph requires a jsonld id")
    GRAPHS.setdefault(jsonld_id, []).append({"iri": iri})
