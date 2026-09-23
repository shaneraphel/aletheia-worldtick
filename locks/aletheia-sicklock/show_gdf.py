#!/usr/bin/env python3.12
"""Show: a BioSig GDF 1.25 tape (an empty sick set)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from gdfocc import read_gdf, read_gdf_sick
from infsq import infection_sequences

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"


def main():
    n, sick = read_gdf_sick(GDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-sick.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "sicklock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "five GDF channels, sick 0 and 4, four orders; empty GDF is absence",
        "ours": {"n": n, "sick": sick, "sequences": infection_sequences(n, sick), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["sequences"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("sicklock gdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
