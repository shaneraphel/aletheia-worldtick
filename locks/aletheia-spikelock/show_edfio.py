#!/usr/bin/env python3.12
"""Show: I used edfio on the MIT EDF tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from edfocc import edf_occupancy, read_edf, read_edf_annotations

EDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "sub-01_task-spike_eeg.edf"


def theirs() -> dict:
    import edfio

    rec = edfio.read_edf(EDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-edfio.edf")
    p.write_bytes(b"")
    try:
        edfio.read_edf(p)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "edfio",
        "version": edfio.__version__,
        "n_signals": int(rec.num_signals),
        "n_samples": int(len(rec.signals[0].data)),
        "empty": empty,
        "annot": [a.text for a in rec.annotations],
        "annot_onset": [float(a.onset) for a in rec.annotations],
    }


def main():
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-edf.edf")
    p.write_bytes(b"")
    try:
        read_edf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    out = {
        "schema": "spikelock.show_edfio.v1",
        "used": "https://github.com/the-siesta-group/edfio",
        "built": "edfio reads 8 EDF samples; empty EDF is absence",
        "theirs": theirs(),
        "ours": {"n": edf_occupancy(EDF), "samples": read_edf(EDF)["samples"], "empty": empty, "edf_annot": read_edf_annotations(EDF)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if out["ours"]["n"] != 8 or out["ours"]["empty"] != "raised":
        raise SystemExit("spikelock edfio show identity failed")
    if out["theirs"]["n_samples"] != 8 or out["theirs"]["empty"] != "raised":
        raise SystemExit("edfio identity failed")
    if out["theirs"]["annot"] != ["go", "end"] or out["theirs"]["annot_onset"] != [1.0, 2.0]:
        raise SystemExit("edfio tal identity failed")
    if out["ours"]["edf_annot"] != ["go", "end"]:
        raise SystemExit("ours edf tal identity failed")
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
