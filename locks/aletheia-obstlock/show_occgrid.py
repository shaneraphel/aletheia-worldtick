#!/usr/bin/env python3.12
"""Show: I used a ROS OccupancyGrid lane, and I refused an empty map."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from occgrid import read_occgrid
from gridk import shortest_path_obstacles

YML = Path(__file__).resolve().parent / "resources" / "synthetic" / "lane.yaml"


def main():
    grid = [[1 if v > 0 else 0 for v in row] for row in read_occgrid(YML)]
    empty = "raised"
    try:
        shortest_path_obstacles([], 1)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "obstlock.show_occgrid.v1",
        "used": "https://wiki.ros.org/map_server",
        "built": "5x3 OccupancyGrid, path 6 with one elim; empty grid is absence",
        "ours": {"path": shortest_path_obstacles(grid, 1), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["path"] != 6 or rec["ours"]["empty"] != "raised":
        raise SystemExit("obstlock occgrid show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
