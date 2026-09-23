#!/usr/bin/env python3.12
"""Show: a PCD tape (an empty scan)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from pcdocc import pcd_occupancy, read_pcd
from kdtree import kdtree_near

PCD = Path(__file__).resolve().parent / "resources" / "synthetic" / "near.pcd"


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
        "schema": "nearlock.show_pcd.v1",
        "used": "https://pointclouds.org/documentation/tutorials/pcd_file_format.html",
        "built": "two PCD sites, nearest-x 3; empty cloud is absence",
        "ours": {"n": pcd_occupancy(PCD), "near_x": kdtree_near(pts, 3, 4), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["near_x"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("nearlock pcd show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
