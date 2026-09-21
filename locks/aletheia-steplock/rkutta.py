"""Runge–Kutta occupancy. Empty tapes, a non-positive stage count, or a negative step intern are absence.

This is not an ODE integrator. Step 0 is the stored stationary intern, not
absence of a Butcher tableau.
"""
from __future__ import annotations


def runge_kutta(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty runge-kutta is absence")
    n = 0
    for n_stages, step in steps:
        if n_stages < 1:
            raise ValueError("empty runge-kutta is absence")
        if step < 0:
            raise ValueError("empty runge-kutta is absence")
        n += 1  # tableau occupancy, not an RK4 stepper
    return n
