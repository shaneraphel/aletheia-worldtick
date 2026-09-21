#!/usr/bin/env python3.12
"""Show: I used a ROS OccupancyGrid, and I refused an empty map."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from occgrid import occgrid_occupancy, occupied_points, read_occgrid
from qdtree import qdtree_ne

YML = Path(__file__).resolve().parent / "resources" / "synthetic" / "bev.yaml"


def main():
    pts = occupied_points(read_occgrid(YML))
    empty = "raised"
    p = Path("/tmp/aletheia-empty.yaml")
    p.write_text("image: missing.pgm\n")
    try:
        occgrid_occupancy(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "gridlock.show_occgrid.v1",
        "used": "https://wiki.ros.org/map_server",
        "built": "2x2 OccupancyGrid, NE 1; empty map is absence",
        "ours": {"n": occgrid_occupancy(YML), "ne": qdtree_ne(pts, 1, 1), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gridlock occgrid show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
