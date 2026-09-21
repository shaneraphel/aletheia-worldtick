#!/usr/bin/env python3.12
"""Show: I used a two-link URDF, and I refused an empty robot."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from urdfocc import read_urdf, urdf_occupancy
from ik import two_link_ik

URDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "two_link.urdf"


def main():
    recu = read_urdf(URDF)
    pose = two_link_ik(2.0, 0.0, recu["l1"], recu["l2"])
    empty = "raised"
    p = Path("/tmp/aletheia-empty.urdf")
    p.write_text("<robot name=\"empty\"></robot>\n")
    try:
        urdf_occupancy(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "jointlock.show_urdf.v1",
        "used": "https://wiki.ros.org/urdf",
        "built": "two-link URDF reach (2,0); empty robot is absence",
        "ours": {"n_links": recu["n_links"], "pose": list(pose), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n_links"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("jointlock urdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
