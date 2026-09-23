#!/usr/bin/env python3.12
"""Show: PhysioNet wfdb on a format-16 tape (an empty header)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from wfdbocc import read_wfdb, read_wfdb_atr, wfdb_occupancy, write_wfdb_atr

STEM = Path(__file__).resolve().parent / "resources" / "synthetic" / "sub-01_task-spike"
HEA = STEM.with_suffix(".hea")


def theirs() -> dict:
    import wfdb

    rec = wfdb.rdrecord(str(STEM))
    ann = wfdb.rdann(str(STEM), "atr")
    empty = "raised"
    Path("/tmp/aletheia-empty.hea").write_text("")
    try:
        wfdb.rdrecord("/tmp/aletheia-empty")
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "wfdb",
        "version": wfdb.__version__,
        "n_samples": int(rec.p_signal.shape[0]),
        "n_signals": int(rec.p_signal.shape[1]),
        "empty": empty,
        "atr": [str(x) for x in ann.aux_note],
        "atr_onset": [float(s) / 8.0 for s in ann.sample],
    }


def main():
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours.hea")
    p.write_text("")
    try:
        read_wfdb(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_atr = "raised"
    try:
        write_wfdb_atr(Path("/tmp/aletheia-empty-atr"), [])
        empty_atr = "accepted"
    except ValueError:
        empty_atr = "raised"
    out = {
        "schema": "spikelock.show_wfdb_official.v1",
        "used": "https://github.com/MIT-LCP/wfdb-python",
        "built": "official wfdb reads 8 format-16 samples and .atr go/end; empty header is absence",
        "theirs": theirs(),
        "ours": {
            "n": wfdb_occupancy(HEA),
            "samples": read_wfdb(HEA)["samples"],
            "empty": empty,
            "empty_atr": empty_atr,
            "annot": read_wfdb_atr(STEM),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if out["ours"]["n"] != 8 or out["ours"]["empty"] != "raised":
        raise SystemExit("spikelock wfdb show identity failed")
    if out["ours"]["empty_atr"] != "raised" or out["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("spikelock wfdb atr identity failed")
    if out["theirs"]["n_samples"] != 8 or out["theirs"]["empty"] != "raised":
        raise SystemExit("official wfdb identity failed")
    if out["theirs"]["atr"] != ["go", "end"] or out["theirs"]["atr_onset"] != [1.0, 2.0]:
        raise SystemExit("official wfdb rdann identity failed")
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
