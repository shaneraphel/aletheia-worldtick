"""World-model completion versus one measured tick.

A hole written as free space reaches as far as a fully seen map.
One tick of the cells that were actually measured is a smaller number.
"""
from __future__ import annotations

from datalog import datalog_fixpoint
from tick import world_tick

HOLE = None


def _chain(n: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(n - 1)]


def fill_as_free(cells: list[int | None]) -> list[int]:
    if not cells:
        raise ValueError("empty world")
    return [0 if c is HOLE else int(c) for c in cells]


def _facts(cells: list[int]) -> list[int]:
    facts = [i for i, c in enumerate(cells) if c == 1]
    if not facts:
        raise ValueError("no occupied fact")
    return facts


def completed_reach(cells: list[int | None]) -> int:
    filled = fill_as_free(cells)
    return datalog_fixpoint(len(filled), _facts(filled), _chain(len(filled)))


def measured_tick(cells: list[int | None]) -> int:
    if any(c is HOLE for c in cells):
        raise ValueError("unobserved cell")
    if not cells:
        raise ValueError("empty world")
    seen = [int(c) for c in cells]
    return world_tick(len(seen), _facts(seen), _chain(len(seen)))


def measured_closure(cells: list[int | None]) -> int:
    if any(c is HOLE for c in cells):
        raise ValueError("unobserved cell")
    seen = [int(c) for c in cells]
    return datalog_fixpoint(len(seen), _facts(seen), _chain(len(seen)))
