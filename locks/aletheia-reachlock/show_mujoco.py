#!/usr/bin/env python3.12
"""Show: MuJoCo on an MJCF arm (an empty model)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from mjcfocc import mjcf_occupancy, read_mjcf_arm
from reach import two_link_ik

XML = Path(__file__).resolve().parent / "resources" / "synthetic" / "arm.xml"


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
        "ngeom": int(model.ngeom),
    }


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
        "schema": "reachlock.show_mujoco.v1",
        "used": "https://github.com/google-deepmind/mujoco",
        "built": "MJCF two capsules, reach (2,0); empty arm is absence",
        "theirs": theirs(),
        "ours": {"n_geoms": mjcf_occupancy(XML), "pose": list(pose), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n_geoms"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("reachlock mujoco show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
