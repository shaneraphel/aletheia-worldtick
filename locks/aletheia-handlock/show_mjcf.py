#!/usr/bin/env python3.12
"""Show: I used an MJCF cost tape, and I refused an empty custom table."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from mjcfocc import read_mjcf_cost
from hungar import hungar_cost

XML = Path(__file__).resolve().parent / "resources" / "synthetic" / "grasp.xml"


def main():
    cost = read_mjcf_cost(XML)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-grasp.xml")
    p.write_text('<mujoco model="empty"><custom/></mujoco>\n')
    try:
        read_mjcf_cost(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "handlock.show_mjcf.v1",
        "used": "https://mujoco.readthedocs.io/en/stable/XMLreference.html",
        "built": "MJCF 2x2 cost, assignment 2; empty numeric is absence",
        "ours": {"cost": hungar_cost(cost), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["cost"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("handlock mjcf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
