"""Airflow leftover: every task lands in one unsigned list."""

from __future__ import annotations

DAGS: dict[str, list] = {}


def queue(op: str, dag_id: str | None = None) -> None:
    if not dag_id:
        raise ValueError("airflow task requires a dag id")
    DAGS.setdefault(dag_id, []).append({"op": op})
