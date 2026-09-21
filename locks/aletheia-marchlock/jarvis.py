"""Jarvis-march hull occupancy. Empty points is absence, not 0."""
from __future__ import annotations


def jarvis_hull(points: list[tuple[int, int]]) -> int:
    if not points:
        raise ValueError("empty jarvis march is absence")
    pts = list(dict.fromkeys(points))
    if len(pts) <= 2:
        return len(pts)
    start = min(pts)
    hull: list[tuple[int, int]] = []
    p = start
    while True:
        hull.append(p)
        q = pts[0]
        for r in pts[1:]:
            cross = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
            farther = (r[0] - p[0]) ** 2 + (r[1] - p[1]) ** 2 > (q[0] - p[0]) ** 2 + (
                q[1] - p[1]
            ) ** 2
            if q == p or cross < 0 or (cross == 0 and farther):
                q = r
        p = q
        if p == start:
            break
    return len(hull)
