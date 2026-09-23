"""ROS OccupancyGrid occupancy. An empty map is absence, not 0 cells.

nav_msgs/OccupancyGrid on disk is a YAML card plus a PGM. Zero width or
zero occupied cells refuse.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def write_occgrid(stem, grid):
    if grid is None or not grid or not grid[0]:
        raise ValueError("uncompiled occupancy grid is absence")
    h, w = len(grid), len(grid[0])
    if any(len(row) != w for row in grid):
        raise ValueError("uncompiled occupancy grid is absence")
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    pgm = stem.with_suffix(".pgm")
    yml = stem.with_suffix(".yaml")
    body = []
    for row in grid:
        body.append(" ".join(str(int(v)) for v in row))
    pgm.write_text(f"P2\n{w} {h}\n100\n" + "\n".join(body) + "\n")
    yml.write_text(
        f"image: {pgm.name}\n"
        "resolution: 1.0\n"
        "origin: [0.0, 0.0, 0.0]\n"
        "negate: 0\n"
        "occupied_thresh: 0.65\n"
        "free_thresh: 0.196\n"
    )
    return yml


def read_occgrid(yaml_path):
    p = Path(yaml_path)
    if not p.exists():
        raise ValueError("uncompiled occupancy grid is absence")
    image = None
    for ln in p.read_text().splitlines():
        if ln.startswith("image:"):
            image = ln.split(":", 1)[1].strip()
    if not image:
        raise ValueError("uncompiled occupancy grid is absence")
    img = p.parent / image
    if not img.exists():
        raise ValueError("uncompiled occupancy grid is absence")
    raw = img.read_text().split()
    if len(raw) < 4 or raw[0] != "P2":
        raise ValueError("uncompiled occupancy grid is absence")
    w, h = int(raw[1]), int(raw[2])
    if w < 1 or h < 1:
        raise ValueError("uncompiled occupancy grid is absence")
    vals = [int(x) for x in raw[4 : 4 + w * h]]
    if len(vals) < w * h:
        raise ValueError("uncompiled occupancy grid is absence")
    grid = [vals[i * w : (i + 1) * w] for i in range(h)]
    return grid


def occupied_points(grid):
    pts = []
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if v > 0:
                pts.append((x, y))
    if not pts:
        raise ValueError("uncompiled occupancy grid is absence")
    return pts


def occgrid_occupancy(yaml_path):
    return len(occupied_points(read_occgrid(yaml_path)))


def occupancy_graph(grid):
    """Occupied cells are nodes. Edges are 4-connected. A blank map refuses."""
    pts = occupied_points(grid)
    index = {p: i for i, p in enumerate(pts)}
    edges = []
    for (x, y), i in index.items():
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            j = index.get((x + dx, y + dy))
            if j is not None:
                edges.append((i, j))
    return len(pts), edges
