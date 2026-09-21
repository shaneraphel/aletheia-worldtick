#!/usr/bin/env python3.12
"""Show: I used MuJoCo on an MJCF hand, and I refused an empty site tape."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from mjcfocc import mjcf_occupancy, read_mjcf_word
from twofng import minimum_distance

XML = Path(__file__).resolve().parent / "resources" / "synthetic" / "hand.xml"


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
        "n_sites": int(model.nsite),
    }


def main():
    word = read_mjcf_word(XML)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.xml")
    p.write_text('<mujoco model="empty"><worldbody/></mujoco>\n')
    try:
        read_mjcf_word(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "fingerlock.show_mujoco.v1",
        "used": "https://github.com/google-deepmind/mujoco",
        "built": "MJCF sites CAKE, two-finger 3; empty hand is absence",
        "theirs": theirs(),
        "ours": {"word": word, "n_sites": mjcf_occupancy(XML), "dist": minimum_distance(word), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["dist"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("fingerlock mujoco show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
