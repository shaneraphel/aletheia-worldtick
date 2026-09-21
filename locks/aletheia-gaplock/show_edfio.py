#!/usr/bin/env python3.12
"""Show: I used edfio on an EDF tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from edfocc import read_edf, read_edf_annotations
from kslots import k_empty_slots

EDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.edf"


def theirs() -> dict:
    import edfio

    rec = edfio.read_edf(EDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap-edfio.edf")
    p.write_bytes(b"")
    try:
        edfio.read_edf(p)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "edfio",
        "version": edfio.__version__,
        "n_samples": int(len(rec.signals[0].data)),
        "empty": empty,
        "annot": [a.text for a in rec.annotations],
        "annot_onset": [float(a.onset) for a in rec.annotations],
    }


def main():
    bulbs = read_edf(EDF)["samples"]
    rec = {
        "schema": "gaplock.show_edfio.v1",
        "used": "https://github.com/the-siesta-group/edfio",
        "built": "edfio reads EDF onsets [1,3,2]; empty-slot day 2; empty EDF is absence",
        "theirs": theirs(),
        "ours": {"samples": bulbs, "day": k_empty_slots(bulbs, 1), "edf_annot": read_edf_annotations(EDF)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2:
        raise SystemExit("gaplock edfio show identity failed")
    if rec["theirs"]["n_samples"] != 3 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("edfio gap identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["annot_onset"] != [1.0, 2.0]:
        raise SystemExit("edfio tal identity failed")
    if rec["ours"]["edf_annot"] != ["go", "end"]:
        raise SystemExit("ours edf tal identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
