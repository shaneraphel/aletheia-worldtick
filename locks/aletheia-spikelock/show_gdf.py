#!/usr/bin/env python3.12
"""Show: I used a BioSig GDF 1.25 tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from gdfocc import gdf_occupancy, read_gdf
from nyqst import nyquist

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"


def main():
    rec = read_gdf(GDF)
    steps = [(int(v), 0) for v in rec["samples"]]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gdf.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    out = {
        "schema": "spikelock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "three GDF 1.25 samples, occupancy 3; empty GDF is absence",
        "ours": {
            "n": gdf_occupancy(GDF),
            "version": rec["version"],
            "nyquist": nyquist(steps),
            "empty": empty,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if out["ours"]["nyquist"] != 3 or out["ours"]["empty"] != "raised":
        raise SystemExit("spikelock gdf show identity failed")
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
