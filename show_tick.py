#!/usr/bin/env python3.12
"""One tick on the checked-in occupancy map is not the closure."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from datalog import datalog_fixpoint
from occgrid import occupancy_graph, read_occgrid
from tick import reach_after, world_tick

YML = Path(__file__).resolve().parent / "resources" / "synthetic" / "world.yaml"
EDGES = [(0, 1), (1, 2)]


def main() -> int:
    n, grid_edges = occupancy_graph(read_occgrid(YML))
    one = world_tick(n, [0], grid_edges)
    closed = datalog_fixpoint(n, [0], grid_edges)
    after = reach_after(n, [0], grid_edges, n)
    empty = "raised"
    try:
        world_tick(3, [], EDGES)
        empty = "accepted"
    except ValueError:
        pass
    rec = {
        "schema": "worldtick.show_tick.v1",
        "built": "1x3 occupied map; one tick reaches 2; closure reaches 3",
        "ours": {
            "n": n,
            "one_tick": one,
            "closure": closed,
            "horizon_n": after,
            "empty": empty,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if one != 2 or closed != 3 or after != 3 or empty != "raised":
        raise SystemExit("worldtick tick show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
