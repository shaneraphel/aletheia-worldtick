#!/usr/bin/env python3.12
"""Show: PhysioNet wfdb on a pulse tape (an empty header)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from kstren import max_k_subarray_strength
from wfdbocc import read_wfdb, read_wfdb_atr, write_wfdb_atr

STEM = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse"
HEA = STEM.with_suffix(".hea")


def theirs() -> dict:
    import wfdb

    rec = wfdb.rdrecord(str(STEM))
    ann = wfdb.rdann(str(STEM), "atr")
    empty = "raised"
    Path("/tmp/aletheia-empty-pulse.hea").write_text("")
    try:
        wfdb.rdrecord("/tmp/aletheia-empty-pulse")
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "wfdb",
        "version": wfdb.__version__,
        "n_samples": int(rec.p_signal.shape[0]),
        "empty": empty,
        "atr": [str(x) for x in ann.aux_note],
        "atr_onset": [float(s) / 8.0 for s in ann.sample],
    }


def main():
    nums = read_wfdb(HEA)["samples"]
    empty_atr = "raised"
    try:
        write_wfdb_atr(Path("/tmp/aletheia-empty-atr-pulse"), [])
        empty_atr = "accepted"
    except ValueError:
        empty_atr = "raised"
    rec = {
        "schema": "pulselock.show_wfdb_official.v1",
        "used": "https://github.com/MIT-LCP/wfdb-python",
        "built": "official wfdb reads [1,2,3,-1,2] and .atr go/end; strength 22; empty header is absence",
        "theirs": theirs(),
        "ours": {
            "samples": nums,
            "strength": max_k_subarray_strength(nums, 3),
            "empty_atr": empty_atr,
            "annot": read_wfdb_atr(STEM),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22:
        raise SystemExit("pulselock wfdb show identity failed")
    if rec["ours"]["empty_atr"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("pulselock wfdb atr identity failed")
    if rec["theirs"]["n_samples"] != 5 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("official wfdb pulse identity failed")
    if rec["theirs"]["atr"] != ["go", "end"] or rec["theirs"]["atr_onset"] != [1.0, 2.0]:
        raise SystemExit("official wfdb rdann identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
