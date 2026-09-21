"""Graham-scan hull occupancy. Empty points is absence, not 0."""
from __future__ import annotations


def _cross(o: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def graham_hull(points: list[tuple[int, int]]) -> int:
    if not points:
        raise ValueError("empty graham scan is absence")
    pts = sorted(set(points))
    if len(pts) <= 2:
        return len(pts)
    lower: list[tuple[int, int]] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[int, int]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower[:-1] + upper[:-1])
