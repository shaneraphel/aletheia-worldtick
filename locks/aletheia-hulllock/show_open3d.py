#!/usr/bin/env python3.12
"""Show: Open3D on a PCD tape (an empty scan)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from pcdocc import pcd_occupancy, read_pcd
from graham import graham_hull

PCD = Path(__file__).resolve().parent / "resources" / "synthetic" / "contacts.pcd"


def theirs() -> dict:
    import open3d as o3d

    empty = o3d.geometry.PointCloud()
    cloud = o3d.io.read_point_cloud(str(PCD))
    return {
        "package": "open3d",
        "version": o3d.__version__,
        "empty_points": int(len(empty.points)),
        "pcd_points": int(len(cloud.points)),
    }


def main():
    pts = read_pcd(PCD)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.pcd")
    p.write_text("VERSION 0.7\nPOINTS 0\nDATA ascii\n")
    try:
        read_pcd(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "hulllock.show_open3d.v1",
        "used": "https://github.com/isl-org/Open3D",
        "built": "five PCD contacts, hull 4; empty cloud is absence",
        "theirs": theirs(),
        "ours": {"n": pcd_occupancy(PCD), "hull": graham_hull(pts), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["hull"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("hulllock open3d show identity failed")
    if rec["theirs"]["empty_points"] != 0 or rec["theirs"]["pcd_points"] != 5:
        raise SystemExit("open3d pcd identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
