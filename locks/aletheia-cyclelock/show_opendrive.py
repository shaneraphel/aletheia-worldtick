#!/usr/bin/env python3.12
"""Show: an OpenDRIVE loop (an empty map)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from xodrocc import opendrive_occupancy, read_opendrive
from floyd import floyd_cycle

XODR = Path(__file__).resolve().parent / "resources" / "synthetic" / "loop.xodr"


def main():
    nxt = read_opendrive(XODR)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.xodr")
    p.write_text('<?xml version="1.0"?><OpenDRIVE><header name="empty"/></OpenDRIVE>\n')
    try:
        read_opendrive(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "cyclelock.show_opendrive.v1",
        "used": "https://www.asam.net/standards/detail/opendrive/",
        "built": "three-road OpenDRIVE loop, cycle 1; empty network is absence",
        "ours": {"n_roads": opendrive_occupancy(XODR), "cycle": floyd_cycle(nxt), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["cycle"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("cyclelock opendrive show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
