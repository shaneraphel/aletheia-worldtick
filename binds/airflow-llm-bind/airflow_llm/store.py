"""Open leftover: every airflow llm branch lands in one unsigned list."""

from __future__ import annotations

BRANCHES: dict[str, list] = {}


def register(prompt: str, llm_id: str | None = None) -> None:
    if not llm_id:
        raise ValueError("airflow llm branch requires an llm id")
    BRANCHES.setdefault(llm_id, []).append({"prompt": prompt})
