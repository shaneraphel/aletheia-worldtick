#!/usr/bin/env python3.12
"""Show: I used edfio on an EDF tape, and I refused an empty sick set."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from edfocc import read_edf, read_edf_annotations
from infsq import infection_sequences

EDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.edf"


def theirs() -> dict:
    import edfio

    rec = edfio.read_edf(EDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-sick-edfio.edf")
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
    samples = read_edf(EDF)["samples"]
    n = len(samples)
    sick = [i for i, v in enumerate(samples) if int(v) != 0]
    rec = {
        "schema": "sicklock.show_edfio.v1",
        "used": "https://github.com/the-siesta-group/edfio",
        "built": "edfio reads five EDF samples, sick 0 and 4; four orders; empty EDF is absence",
        "theirs": theirs(),
        "ours": {"n": n, "sick": sick, "sequences": infection_sequences(n, sick), "edf_annot": read_edf_annotations(EDF)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["sequences"] != 4:
        raise SystemExit("sicklock edfio show identity failed")
    if rec["theirs"]["n_samples"] != 5 or rec["theirs"]["empty"] != "raised":
        raise SystemExit("edfio sick identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["annot_onset"] != [1.0, 2.0]:
        raise SystemExit("edfio tal identity failed")
    if rec["ours"]["edf_annot"] != ["go", "end"]:
        raise SystemExit("ours edf tal identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
