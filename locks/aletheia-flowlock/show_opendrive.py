#!/usr/bin/env python3.12
"""Show: I used an OpenDRIVE junction, and I refused an empty map."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from xodrocc import opendrive_occupancy, read_opendrive_weighted, read_opendrive_junction
from dinic import dinic_max_flow

XODR = Path(__file__).resolve().parent / "resources" / "synthetic" / "diamond.xodr"


def main():
    graph = read_opendrive_junction(XODR)
    caps = read_opendrive_weighted(XODR)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-j.xodr")
    p.write_text('<?xml version="1.0"?><OpenDRIVE><header name="empty"/></OpenDRIVE>\n')
    try:
        read_opendrive_junction(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "flowlock.show_opendrive.v1",
        "used": "https://www.asam.net/standards/detail/opendrive/",
        "built": "OpenDRIVE diamond, max-flow 2; empty network is absence",
        "ours": {
            "n_roads": opendrive_occupancy(XODR),
            "flow": dinic_max_flow(len(graph), caps, 0, len(graph) - 1),
            "empty": empty,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["flow"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("flowlock opendrive show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
