#!/usr/bin/env python3.12
"""Show: I used an MJCF two-link arm, and I refused an empty model."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from mjcfocc import mjcf_occupancy, read_mjcf_arm
from reach import two_link_ik

XML = Path(__file__).resolve().parent / "resources" / "synthetic" / "arm.xml"


def main():
    arm = read_mjcf_arm(XML)
    pose = two_link_ik(2.0, 0.0, arm["l1"], arm["l2"])
    empty = "raised"
    p = Path("/tmp/aletheia-empty-arm.xml")
    p.write_text('<mujoco model="empty"><worldbody/></mujoco>\n')
    try:
        read_mjcf_arm(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "reachlock.show_mjcf.v1",
        "used": "https://mujoco.readthedocs.io/en/stable/XMLreference.html",
        "built": "MJCF two capsules, reach (2,0); empty arm is absence",
        "ours": {"n_geoms": mjcf_occupancy(XML), "pose": list(pose), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n_geoms"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("reachlock mjcf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
