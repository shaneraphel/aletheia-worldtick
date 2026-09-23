#!/usr/bin/env python3.12
"""Show: Open3D on a PCD tape (an empty scan)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from pcdocc import pcd_occupancy, read_pcd
from manh import min_manhattan_after_remove

PCD = Path(__file__).resolve().parent / "resources" / "synthetic" / "span.pcd"


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
    pts = [list(p) for p in read_pcd(PCD)]
    empty = "raised"
    p = Path("/tmp/aletheia-empty.pcd")
    p.write_text("VERSION 0.7\nPOINTS 0\nDATA ascii\n")
    try:
        read_pcd(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "farlock.show_open3d.v1",
        "used": "https://github.com/isl-org/Open3D",
        "built": "four PCD sites, Manhattan span 12; empty cloud is absence",
        "theirs": theirs(),
        "ours": {"n": pcd_occupancy(PCD), "span": min_manhattan_after_remove(pts), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["span"] != 12 or rec["ours"]["empty"] != "raised":
        raise SystemExit("farlock open3d show identity failed")
    if rec["theirs"]["empty_points"] != 0 or rec["theirs"]["pcd_points"] != 4:
        raise SystemExit("open3d pcd identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
