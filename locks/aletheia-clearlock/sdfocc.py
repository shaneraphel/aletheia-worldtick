"""Signed-distance occupancy. Empty field is absence, not touching zero.

This is not a physics engine. Radius intern 0 is a stored point obstacle, not
absence of a disk. disk_clearance2 is exact integer: r^2 compared, no square root.
"""
from __future__ import annotations


def disk_clearance2(px: int, py: int, cx: int, cy: int, radius: int) -> int:
    if radius < 0:
        raise ValueError("radius is absence")
    dx = px - cx
    dy = py - cy
    return dx * dx + dy * dy - radius * radius


def signed_distance_occupancy(steps: list[tuple[int, int]]) -> int:
    if not steps:
        raise ValueError("empty signed distance occupancy is absence")
    n = 0
    for n_cells, radius in steps:
        if n_cells < 1:
            raise ValueError("empty signed distance occupancy is absence")
        if radius < 0:
            raise ValueError("empty signed distance occupancy is absence")
        n += 1  # sample occupancy, not a clearance integrator
    return n
