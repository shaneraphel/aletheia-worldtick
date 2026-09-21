"""Open leftover: every airflow approval lands in one unsigned list."""

from __future__ import annotations

APPROVALS: dict[str, list] = {}


def register(op: str, hitl_id: str | None = None) -> None:
    if not hitl_id:
        raise ValueError("airflow hitl requires a hitl id")
    APPROVALS.setdefault(hitl_id, []).append({"op": op})
