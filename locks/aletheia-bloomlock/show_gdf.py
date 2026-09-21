#!/usr/bin/env python3.12
"""Show: I used a BioSig GDF 1.25 tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bloom import bloom_maybe
from gdfocc import gdf_occupancy, read_gdf

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"


def main():
    keys = read_gdf(GDF)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-bloom.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "bloomlock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "GDF onsets [1,2,3] maybe-membership 1; empty GDF is absence",
        "ours": {"n": gdf_occupancy(GDF), "maybe": bloom_maybe(keys, 16, 2, 2), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["maybe"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("bloomlock gdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
