#!/usr/bin/env python3.12
"""Show: a PCD tape (an empty scan)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from pcdocc import pcd_occupancy, read_pcd
from fortun import fortun_verts

PCD = Path(__file__).resolve().parent / "resources" / "synthetic" / "sites.pcd"


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
        "schema": "sitelock.show_pcd.v1",
        "used": "https://pointclouds.org/documentation/tutorials/pcd_file_format.html",
        "built": "three PCD sites, Fortune vertex 1; empty cloud is absence",
        "ours": {"n": pcd_occupancy(PCD), "verts": fortun_verts(pts), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["verts"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("sitelock pcd show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
