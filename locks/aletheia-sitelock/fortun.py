"""Fortune Voronoi-vertex occupancy. Empty sites is absence, not 0."""
from __future__ import annotations


def _cross(o: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _incircle(
    a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int]
) -> int:
    ax, ay = a[0] - d[0], a[1] - d[1]
    bx, by = b[0] - d[0], b[1] - d[1]
    cx, cy = c[0] - d[0], c[1] - d[1]
    return (
        (ax * ax + ay * ay) * (bx * cy - by * cx)
        - (bx * bx + by * by) * (ax * cy - ay * cx)
        + (cx * cx + cy * cy) * (ax * by - ay * bx)
    )


def fortun_verts(sites: list[tuple[int, int]]) -> int:
    if not sites:
        raise ValueError("empty fortune is absence")
    pts = list(sites)
    n = len(pts)
    verts = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = pts[i], pts[j], pts[k]
                cr = _cross(a, b, c)
                if cr == 0:
                    continue
                if cr < 0:
                    b, c = c, b
                empty = True
                for t, p in enumerate(pts):
                    if t in (i, j, k):
                        continue
                    if _incircle(a, b, c, p) > 0:
                        empty = False
                        break
                if empty:
                    verts += 1
    return verts
