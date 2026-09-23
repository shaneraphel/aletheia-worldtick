#!/usr/bin/env python3.12
"""Show: PhysioNet wfdb on a sick tape (an empty header)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from infsq import infection_sequences
from wfdbocc import read_wfdb, read_wfdb_atr, write_wfdb_atr

STEM = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape"
HEA = STEM.with_suffix(".hea")


def theirs() -> dict:
    import wfdb

    rec = wfdb.rdrecord(str(STEM))
    ann = wfdb.rdann(str(STEM), "atr")
    empty = "raised"
    Path("/tmp/aletheia-empty-sick.hea").write_text("")
    try:
        wfdb.rdrecord("/tmp/aletheia-empty-sick")
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
    samples = read_wfdb(HEA)["samples"]
    n = len(samples)
    sick = [i for i, v in enumerate(samples) if int(v) != 0]
    empty_atr = "raised"
    try:
        write_wfdb_atr(Path("/tmp/aletheia-empty-atr-sick"), [])
        empty_atr = "accepted"
    except ValueError:
        empty_atr = "raised"
    rec = {
        "schema": "sicklock.show_wfdb_official.v1",
        "used": "https://github.com/MIT-LCP/wfdb-python",
        "built": "official wfdb reads five samples, sick 0 and 4, and .atr go/end; four orders; empty header is absence",
        "theirs": theirs(),
        "ours": {
            "n": n,
            "sick": sick,
            "sequences": infection_sequences(n, sick),
            "empty_atr": empty_atr,
            "annot": read_wfdb_atr(STEM),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["sequences"] != 4:
        raise SystemExit("sicklock wfdb show identity failed")
    if rec["ours"]["empty_atr"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("sicklock wfdb atr identity failed")
    if rec["theirs"]["n_samples"] != 5 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("official wfdb sick identity failed")
    if rec["theirs"]["atr"] != ["go", "end"] or rec["theirs"]["atr_onset"] != [1.0, 2.0]:
        raise SystemExit("official wfdb rdann identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
