#!/usr/bin/env python3.12
"""Show: a ROS OccupancyGrid world (empty facts)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from occgrid import occupied_points, read_occgrid
from datalog import datalog_fixpoint

YML = Path(__file__).resolve().parent / "resources" / "synthetic" / "world.yaml"


def main():
    pts = occupied_points(read_occgrid(YML))
    n = len(pts)
    facts = [0]
    edges = [(i, i + 1) for i in range(n - 1)]
    empty = "raised"
    try:
        datalog_fixpoint(n, [], edges)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "worldtick.show_occgrid.v1",
        "used": "https://wiki.ros.org/map_server",
        "built": "1x3 OccupancyGrid chain, reach 3; empty facts are absence",
        "ours": {"reach": datalog_fixpoint(n, facts, edges), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["reach"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("worldtick occgrid show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
