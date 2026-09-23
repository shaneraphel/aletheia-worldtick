#!/usr/bin/env python3.12
"""Show: a BIDS-EEG events tape (an empty table)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bidseeg import bids_eeg_occupancy, read_bids_onsets, read_bids_trial_types, read_mne_annot_descriptions
from kstren import max_k_subarray_strength

CH = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_channels.tsv"
EV = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_events.tsv"
MK = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_marker_events.tsv"
ANNOT = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_annotations.txt"


def main():
    nums = read_bids_onsets(EV)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse-events.tsv")
    p.write_text("onset\tduration\ttrial_type\n")
    try:
        read_bids_onsets(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "pulselock.show_bids.v1",
        "used": "https://bids.neuroimaging.io/",
        "built": "BIDS events [1,2,3,-1,2] have strength 22; XDF markers copy to trial_type go/end",
        "ours": {"n": bids_eeg_occupancy(CH, EV), "strength": max_k_subarray_strength(nums, 3), "markers": read_bids_trial_types(MK), "annot": read_mne_annot_descriptions(ANNOT), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock bids show identity failed")
    if rec["ours"]["markers"] != ["go", "end"] or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("pulselock bids marker identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
