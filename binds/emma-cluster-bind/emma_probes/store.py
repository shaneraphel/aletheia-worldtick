"""emma leftover: every probe lands in one unsigned list."""

from __future__ import annotations

PROBES: dict[str, list] = {}


def ping(host: str, cluster_id: str | None = None) -> None:
    if not cluster_id:
        raise ValueError("emma probe requires a cluster id")
    PROBES.setdefault(cluster_id, []).append({"host": host})
