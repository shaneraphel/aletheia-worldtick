#!/usr/bin/env python3.12
"""Show: a nuScenes instance tape (an empty sample)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from nuscocc import nusc_occupancy, read_nusc
from octpart import octpart_ne

NUSC = Path(__file__).resolve().parent / "resources" / "synthetic" / "sample.json"


def main():
    pts = read_nusc(NUSC)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-nusc.json")
    p.write_text('{"instance": []}\n')
    try:
        read_nusc(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "voxelock.show_nusc.v1",
        "used": "https://www.nuscenes.org/nuscenes",
        "built": "two nuScenes translations, NE occupancy 1; empty sample is absence",
        "ours": {"n": nusc_occupancy(NUSC), "ne": octpart_ne(pts, 1, 1, 1), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("voxelock nusc show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
