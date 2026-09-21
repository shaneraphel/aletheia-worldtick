"""Nyquist occupancy. Empty tapes, a non-positive sample count, or a negative rate intern are absence.

This is not a sampling theorem solver. Rate 0 is the stored DC intern, not
absence of a Nyquist frequency.
"""
from __future__ import annotations


def nyquist(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty nyquist is absence")
    n = 0
    for n_samples, rate in steps:
        if n_samples < 1:
            raise ValueError("empty nyquist is absence")
        if rate < 0:
            raise ValueError("empty nyquist is absence")
        n += 1  # sampling occupancy, not a reconstruction engine
    return n
