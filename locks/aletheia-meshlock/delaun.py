"""Delaunay-triangle occupancy. Empty sites is absence, not 0."""
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


def delaun_tris(sites: list[tuple[int, int]]) -> int:
    if not sites:
        raise ValueError("empty delaunay is absence")
    pts = sorted(set(sites))
    n = len(pts)
    if n < 3:
        return 0
    lower: list[tuple[int, int]] = []
    for point in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[int, int]] = []
    for point in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    hull_vertices = len(lower[:-1] + upper[:-1])
    if hull_vertices < 3:
        return 0
    # A canonical Delaunay triangulation has 2n - 2 - h triangles.  This
    # avoids counting every cocircular diagonal as a separate triangulation.
    return 2 * n - 2 - hull_vertices
