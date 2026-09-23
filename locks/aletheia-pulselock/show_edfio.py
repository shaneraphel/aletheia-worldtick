#!/usr/bin/env python3.12
"""Show: edfio on the pulse EDF tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from edfocc import read_edf as _read_edf, read_edf_annotations
from kstren import max_k_subarray_strength

EDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_eeg.edf"


def read_edf(path):
    return _read_edf(path)["samples"]


def theirs() -> dict:
    import edfio

    rec = edfio.read_edf(EDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse-edfio.edf")
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
    nums = read_edf(EDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse-ours.edf")
    p.write_bytes(b"")
    try:
        read_edf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "pulselock.show_edfio.v1",
        "used": "https://github.com/the-siesta-group/edfio",
        "built": "edfio reads pulse EDF [1,2,3,-1,2]; strength 22; empty EDF is absence",
        "theirs": theirs(),
        "ours": {"samples": nums, "strength": max_k_subarray_strength(nums, 3), "empty": empty, "edf_annot": read_edf_annotations(EDF)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock edfio show identity failed")
    if rec["theirs"]["n_samples"] != 5 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("edfio pulse identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["annot_onset"] != [1.0, 2.0]:
        raise SystemExit("edfio tal identity failed")
    if rec["ours"]["edf_annot"] != ["go", "end"]:
        raise SystemExit("ours edf tal identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
