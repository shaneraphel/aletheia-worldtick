"""Kalman-filter occupancy. Empty tapes, a non-positive observation count, or a negative noise intern are absence.

This is not a state estimator. Noise 0 is the stored exact intern, not
absence of a covariance.
"""
from __future__ import annotations


def kalman_filter(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty kalman filter is absence")
    n = 0
    for n_obs, noise in steps:
        if n_obs < 1:
            raise ValueError("empty kalman filter is absence")
        if noise < 0:
            raise ValueError("empty kalman filter is absence")
        n += 1  # observation occupancy, not a covariance integrator
    return n
