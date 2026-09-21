"""Quadtree NE occupancy after one split. Empty points is absence, not 0."""
from __future__ import annotations


def qdtree_ne(points: list[tuple[int, int]], cx: int, cy: int) -> int:
    if not points:
        raise ValueError("empty quadtree is absence")
    n = 0
    for x, y in points:
        if x >= cx and y >= cy:
            n += 1
    return n
