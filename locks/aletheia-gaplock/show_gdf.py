#!/usr/bin/env python3.12
"""Show: a BioSig GDF 1.25 tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from gdfocc import gdf_occupancy, read_gdf
from kslots import k_empty_slots

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"


def main():
    bulbs = read_gdf(GDF)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "gaplock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "GDF onsets [1,3,2] give empty-slot day 2; empty GDF is absence",
        "ours": {"n": gdf_occupancy(GDF), "day": k_empty_slots(bulbs, 1), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gaplock gdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
