#!/usr/bin/env python3.12
"""Show: I used an OpenDRIVE junction, and I refused an empty map."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from xodrocc import opendrive_occupancy, read_opendrive_bipartite
from hopcroft import hopcroft_karp

XODR = Path(__file__).resolve().parent / "resources" / "synthetic" / "grasp.xodr"


def main():
    n_left, n_right, edges = read_opendrive_bipartite(XODR, 2)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-j.xodr")
    p.write_text('<?xml version="1.0"?><OpenDRIVE><header name="empty"/></OpenDRIVE>\n')
    try:
        read_opendrive_bipartite(p, 2)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "karplock.show_opendrive.v1",
        "used": "https://www.asam.net/standards/detail/opendrive/",
        "built": "2x2 OpenDRIVE grasp matching 2; empty network is absence",
        "ours": {
            "n_roads": opendrive_occupancy(XODR),
            "paired": hopcroft_karp(n_left, n_right, edges),
            "empty": empty,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["paired"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("karplock opendrive show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
