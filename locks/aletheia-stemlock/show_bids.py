#!/usr/bin/env python3.12
"""Show: I used a BIDS-EEG events tape, and I refused an empty table."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bidseeg import bids_eeg_occupancy, read_bids_onsets, read_bids_trial_types, read_mne_annot_descriptions
from ukkonen import n_suffix_links

CH = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_channels.tsv"
EV = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_events.tsv"
MK = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_marker_events.tsv"
ANNOT = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_annotations.txt"


def main():
    word = "".join(chr(int(v)) for v in read_bids_onsets(EV))
    empty = "raised"
    p = Path("/tmp/aletheia-empty-stem-events.tsv")
    p.write_text("onset\tduration\ttrial_type\n")
    try:
        read_bids_onsets(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    rec = {
        "schema": "stemlock.show_bids.v1",
        "used": "https://bids.neuroimaging.io/",
        "built": "BIDS events aba have 3 suffix links; empty events are absence",
        "ours": {"n": bids_eeg_occupancy(CH, EV), "word": word, "links": n_suffix_links(word), "markers": read_bids_trial_types(MK), "annot": read_mne_annot_descriptions(ANNOT), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["links"] != 3 or rec["ours"]["word"] != "aba" or rec["ours"]["empty"] != "raised":
        raise SystemExit("stemlock bids show identity failed")
    if rec["ours"]["markers"] != ["go", "end"] or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("stemlock bids marker identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
