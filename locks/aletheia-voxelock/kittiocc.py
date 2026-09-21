"""KITTI velodyne occupancy. An empty scan is absence, not 0 points.

Autonomous-driving lidar dumps are little-endian float32 x,y,z,intensity
records. This writer emits that bin. Zero points refuse.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def write_kitti_bin(path, points):
    if points is None or not points:
        raise ValueError("uncompiled KITTI scan is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    blob = b"".join(struct.pack("<ffff", float(x), float(y), float(z), float(i)) for x, y, z, i in points)
    dest.write_bytes(blob)
    return dest


def read_kitti_bin(path):
    raw = Path(path).read_bytes()
    if len(raw) < 16 or len(raw) % 16 != 0:
        raise ValueError("uncompiled KITTI scan is absence")
    n = len(raw) // 16
    out = []
    for i in range(n):
        x, y, z, inten = struct.unpack_from("<ffff", raw, 16 * i)
        out.append((x, y, z, inten))
    return out


def kitti_occupancy(path):
    return len(read_kitti_bin(path))
