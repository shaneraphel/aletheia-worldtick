#!/usr/bin/env python3.12
"""Show: I used MuJoCo on an MJCF cost tape, and I refused an empty table."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from mjcfocc import read_mjcf_cost
from hungar import hungar_cost

XML = Path(__file__).resolve().parent / "resources" / "synthetic" / "grasp.xml"


def theirs() -> dict:
    import mujoco

    empty = "raised"
    try:
        mujoco.MjModel.from_xml_string('<mujoco model="empty"><worldbody/></mujoco>')
        empty = "accepted"
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}".split("\n", 1)[0]
    model = mujoco.MjModel.from_xml_path(str(XML))
    return {
        "package": "mujoco",
        "version": mujoco.__version__,
        "empty_xml": empty,
        "nbody": int(model.nbody),
    }


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
        "schema": "handlock.show_mujoco.v1",
        "used": "https://github.com/google-deepmind/mujoco",
        "built": "MJCF 2x2 cost, assignment 2; empty numeric is absence",
        "theirs": theirs(),
        "ours": {"cost": hungar_cost(cost), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["cost"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("handlock mujoco show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
