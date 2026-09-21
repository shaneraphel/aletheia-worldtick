#!/usr/bin/env python3.12
"""Show: I used a MANO-shaped joint tape, and I refused an empty pose."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from manoocc import mano_occupancy, read_mano, read_mano_points
from hungar import hungar_cost

MANO = Path(__file__).resolve().parent / "resources" / "synthetic" / "hand.mano.json"


def main():
    pts = read_mano_points(MANO)
    # two fingertips vs two targets: first two joints make the 2x2 cost tape
    cost = [[abs(pts[0][0] - 0) + abs(pts[0][1] - 0), abs(pts[0][0] - 2) + abs(pts[0][1] - 1)],
            [abs(pts[1][0] - 0) + abs(pts[1][1] - 0), abs(pts[1][0] - 2) + abs(pts[1][1] - 1)]]
    empty = "raised"
    p = Path("/tmp/aletheia-empty.mano.json")
    p.write_text('{"mano_joints": []}\n')
    try:
        read_mano(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "handlock.show_mano.v1",
        "used": "https://mano.is.tue.mpg.de/",
        "built": "16 MANO-shaped joints, assignment cost 2; empty pose is absence",
        "ours": {"n": mano_occupancy(MANO), "cost": hungar_cost(cost), "empty": empty},
        "note": "MPI MANO model weights are not in this repo",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["cost"] != 2 or rec["ours"]["n"] != 16 or rec["ours"]["empty"] != "raised":
        raise SystemExit("handlock mano show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
