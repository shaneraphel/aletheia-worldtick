"""Range-tree inclusive box occupancy. Empty points is absence, not 0."""
from __future__ import annotations


def rngtree_count(
    points: list[tuple[int, int]], x1: int, x2: int, y1: int, y2: int
) -> int:
    if not points:
        raise ValueError("empty range tree is absence")
    n = 0
    for x, y in points:
        if x1 <= x <= x2 and y1 <= y <= y2:
            n += 1
    return n
