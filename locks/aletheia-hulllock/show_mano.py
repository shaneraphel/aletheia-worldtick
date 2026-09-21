#!/usr/bin/env python3.12
"""Show: I used a MANO-shaped joint tape, and I refused an empty pose."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from manoocc import mano_occupancy, read_mano, read_mano_points
from graham import graham_hull

MANO = Path(__file__).resolve().parent / "resources" / "synthetic" / "hand.mano.json"


def main():
    pts = read_mano_points(MANO)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.mano.json")
    p.write_text('{"mano_joints": []}\n')
    try:
        read_mano(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "hulllock.show_mano.v1",
        "used": "https://mano.is.tue.mpg.de/",
        "built": "16 MANO-shaped joints, hull 4; empty pose is absence",
        "ours": {"n": mano_occupancy(MANO), "hull": graham_hull(pts), "empty": empty},
        "note": "MPI MANO model weights are not in this repo",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["hull"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("hulllock mano show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
