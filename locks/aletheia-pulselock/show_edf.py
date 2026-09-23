#!/usr/bin/env python3.12
"""Show: an EDF pulse tape (an empty recording)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from edfocc import read_edf as _read_edf
from kstren import max_k_subarray_strength

EDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_eeg.edf"


def read_edf(path):
    if isinstance(path, (bytes, bytearray)) and not path:
        raise ValueError("uncompiled EDF recording is absence")
    return _read_edf(path)["samples"]


def main():
    nums = read_edf(EDF)
    empty = "raised"
    try:
        read_edf(b"")
        empty = "accepted"
    except (ValueError, TypeError):
        try:
            p = Path("/tmp/aletheia-empty.edf")
            p.write_bytes(b"")
            read_edf(p)
            empty = "accepted"
        except ValueError:
            empty = "raised"
    rec = {
        "schema": "pulselock.show_edf.v1",
        "used": "https://physionet.org/",
        "built": "EDF samples [1,2,3,-1,2] have strength 22; empty EDF is absence",
        "ours": {"samples": nums, "strength": max_k_subarray_strength(nums, 3), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock edf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
