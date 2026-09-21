"""Kd-tree nearest x after inserts. Empty points is absence, not 0."""
from __future__ import annotations


def kdtree_near(points: list[tuple[int, int]], qx: int, qy: int) -> int:
    if not points:
        raise ValueError("empty kd-tree is absence")
    best = points[0]
    best_d = (best[0] - qx) ** 2 + (best[1] - qy) ** 2
    for p in points[1:]:
        d = (p[0] - qx) ** 2 + (p[1] - qy) ** 2
        if d < best_d:
            best = p
            best_d = d
    return best[0]
