#!/usr/bin/env python3.12
"""Show: a KITTI velodyne bin (an empty scan)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from kittiocc import kitti_occupancy, read_kitti_bin
from octpart import octpart_ne

BIN = Path(__file__).resolve().parent / "resources" / "synthetic" / "scan.bin"


def main():
    pts = [(int(x), int(y), int(z)) for x, y, z, _ in read_kitti_bin(BIN)]
    empty = "raised"
    p = Path("/tmp/aletheia-empty.bin")
    p.write_bytes(b"")
    try:
        kitti_occupancy(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "voxelock.show_kitti.v1",
        "used": "https://www.cvlibs.net/datasets/kitti/",
        "built": "two KITTI points, NE occupancy 1; empty bin is absence",
        "ours": {"n_points": kitti_occupancy(BIN), "ne": octpart_ne(pts, 1, 1, 1), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("voxelock kitti show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
