#!/usr/bin/env python3.12
"""Show: a BioSig GDF 1.25 tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from gdfocc import gdf_occupancy, read_gdf, read_gdf_word
from ukkonen import n_suffix_links

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"


def main():
    word = read_gdf_word(GDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-stem.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "stemlock.show_gdf.v1",
        "used": "https://biosig.sourceforge.net/",
        "built": "GDF samples aba have 3 suffix links; empty GDF is absence",
        "ours": {"n": gdf_occupancy(GDF), "word": word, "links": n_suffix_links(word), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["links"] != 3 or rec["ours"]["word"] != "aba" or rec["ours"]["empty"] != "raised":
        raise SystemExit("stemlock gdf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
