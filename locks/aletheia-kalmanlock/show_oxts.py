#!/usr/bin/env python3.12
"""Show: a KITTI OXTS tape (an empty IMU)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from oxtsocc import oxts_occupancy, read_oxts
from kalman import kalman_filter

OXTS = Path(__file__).resolve().parent / "resources" / "synthetic" / "imu.txt"


def main():
    steps = read_oxts(OXTS)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.oxts")
    p.write_text("")
    try:
        read_oxts(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "kalmanlock.show_oxts.v1",
        "used": "https://www.cvlibs.net/datasets/kitti/raw_data.php",
        "built": "three OXTS samples, occupancy 3; empty IMU is absence",
        "ours": {"n": oxts_occupancy(OXTS), "kalman": kalman_filter(steps), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["kalman"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("kalmanlock oxts show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
