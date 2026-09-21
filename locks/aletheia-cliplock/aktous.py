"""Akl-Toussaint interior discard. Empty points is absence, not 0."""
from __future__ import annotations


def aktous_discard(points: list[tuple[int, int]]) -> int:
    if not points:
        raise ValueError("empty akl-toussaint is absence")
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    n = 0
    for x, y in points:
        if xmin < x < xmax and ymin < y < ymax:
            n += 1
    return n
