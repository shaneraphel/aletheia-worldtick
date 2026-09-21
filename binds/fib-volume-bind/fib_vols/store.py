"""A FIB leftover: every fibre volume lands in one unsigned list."""

from __future__ import annotations

FIBS: dict[str, list] = {}


def register(nfd, fib_id: str | None = None) -> None:
    if not fib_id:
        raise ValueError("fib volume requires a fib id")
    FIBS.setdefault(fib_id, []).append({"nfd": nfd})
