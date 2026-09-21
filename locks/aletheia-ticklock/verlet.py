"""Verlet-integration occupancy. Empty tapes, a non-positive step count, or a negative timestep intern are absence.

This is not an MD engine. Timestep 0 is the stored frozen intern, not
absence of a symplectic pair.
"""
from __future__ import annotations


def verlet_integration(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty verlet integration is absence")
    n = 0
    for n_steps, dt in steps:
        if n_steps < 1:
            raise ValueError("empty verlet integration is absence")
        if dt < 0:
            raise ValueError("empty verlet integration is absence")
        n += 1  # symplectic occupancy, not a trajectory engine
    return n
