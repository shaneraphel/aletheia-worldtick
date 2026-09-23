#!/usr/bin/env python3.12
"""Show: an OpenDRIVE junction (an empty map)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from xodrocc import opendrive_occupancy, read_opendrive_junction
from blossom import blossom_match

XODR = Path(__file__).resolve().parent / "resources" / "synthetic" / "pairs.xodr"


def main():
    graph = read_opendrive_junction(XODR)
    edges = [(i, j) for i, succs in enumerate(graph) for j in succs]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-j.xodr")
    p.write_text('<?xml version="1.0"?><OpenDRIVE><header name="empty"/></OpenDRIVE>\n')
    try:
        read_opendrive_junction(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "pairlock.show_opendrive.v1",
        "used": "https://www.asam.net/standards/detail/opendrive/",
        "built": "four-road OpenDRIVE pairing 2; empty network is absence",
        "ours": {"n_roads": opendrive_occupancy(XODR), "paired": blossom_match(len(graph), edges), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["paired"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pairlock opendrive show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
