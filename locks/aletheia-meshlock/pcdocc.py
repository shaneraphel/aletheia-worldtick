"""PCD occupancy. An empty point cloud is absence, not 0 sites.

PCL / Open3D ASCII PCD is the contact-site interchange. POINTS 0 refuses.
"""
from __future__ import annotations

from pathlib import Path

Z = -1


def write_pcd(path, points):
    if points is None or not points:
        raise ValueError("uncompiled PCD cloud is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    n = len(points)
    body = "\n".join(f"{float(x)} {float(y)} 0" for x, y in points)
    dest.write_text(
        "# .PCD v0.7 - Point Cloud Data file format\n"
        "VERSION 0.7\n"
        "FIELDS x y z\n"
        "SIZE 4 4 4\n"
        "TYPE F F F\n"
        "COUNT 1 1 1\n"
        f"WIDTH {n}\n"
        "HEIGHT 1\n"
        "VIEWPOINT 0 0 0 1 0 0 0\n"
        f"POINTS {n}\n"
        "DATA ascii\n"
        f"{body}\n"
    )
    return dest


def read_pcd(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "POINTS" not in text or "DATA ascii" not in text:
        raise ValueError("uncompiled PCD cloud is absence")
    n = 0
    for ln in text.splitlines():
        if ln.startswith("POINTS"):
            n = int(ln.split()[1])
    if n < 1:
        raise ValueError("uncompiled PCD cloud is absence")
    data = text.split("DATA ascii", 1)[1].split()
    pts = []
    for i in range(n):
        x = float(data[3 * i])
        y = float(data[3 * i + 1])
        pts.append((int(x), int(y)))
    if not pts:
        raise ValueError("uncompiled PCD cloud is absence")
    return pts


def pcd_occupancy(path):
    return len(read_pcd(path))
