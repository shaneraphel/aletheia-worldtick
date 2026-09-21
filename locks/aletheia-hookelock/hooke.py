"""Hooke's-law occupancy. Empty tapes, a non-positive spring count, or a negative stiffness intern are absence.

This is not a mechanics solver. Stiffness 0 is the stored slack intern, not
absence of a restoring force.
"""
from __future__ import annotations


def hooke_law(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty hooke's law is absence")
    n = 0
    for n_springs, stiffness in steps:
        if n_springs < 1:
            raise ValueError("empty hooke's law is absence")
        if stiffness < 0:
            raise ValueError("empty hooke's law is absence")
        n += 1  # spring occupancy, not a force integrator
    return n
