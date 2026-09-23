#!/usr/bin/env python3.12
"""Show: a MANO-shaped joint tape (an empty pose)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from manoocc import mano_occupancy, read_mano, read_mano_word
from twofng import minimum_distance

MANO = Path(__file__).resolve().parent / "resources" / "synthetic" / "hand.mano.json"


def main():
    word = read_mano_word(MANO)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.mano.json")
    p.write_text('{"mano_joints": []}\n')
    try:
        read_mano(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "fingerlock.show_mano.v1",
        "used": "https://mano.is.tue.mpg.de/",
        "built": "16 MANO-shaped joints, two-finger 3; empty pose is absence",
        "ours": {"n": mano_occupancy(MANO), "word": word, "dist": minimum_distance(word), "empty": empty},
        "note": "MPI MANO model weights are not in this repo",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["dist"] != 3 or rec["ours"]["word"] != "CAKE" or rec["ours"]["empty"] != "raised":
        raise SystemExit("fingerlock mano show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
