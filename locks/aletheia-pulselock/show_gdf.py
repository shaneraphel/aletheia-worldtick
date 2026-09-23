#!/usr/bin/env python3.12
"""Show: a BioSig GDF 1.25 pulse tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from gdfocc import read_gdf
from kstren import max_k_subarray_strength

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse.gdf"


def main():
    nums = read_gdf(GDF)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "pulselock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "GDF samples [1,2,3,-1,2] have strength 22; empty GDF is absence",
        "ours": {"samples": nums, "strength": max_k_subarray_strength(nums, 3), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock gdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
