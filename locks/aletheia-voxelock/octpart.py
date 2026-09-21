"""Octree NE occupancy after one split. Empty points is absence, not 0."""
from __future__ import annotations


def octpart_ne(
    points: list[tuple[int, int, int]], cx: int, cy: int, cz: int
) -> int:
    if not points:
        raise ValueError("empty octree is absence")
    n = 0
    for x, y, z in points:
        if x >= cx and y >= cy and z >= cz:
            n += 1
    return n
