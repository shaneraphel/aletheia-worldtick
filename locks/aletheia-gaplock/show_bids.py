#!/usr/bin/env python3.12
"""Show: a BIDS-EEG events tape (an empty table)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from bidseeg import read_bids_trial_types, read_mne_annot_descriptions
from kslots import k_empty_slots

EV = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_events.tsv"
MK = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_marker_events.tsv"
ANNOT = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_annotations.txt"


def bulbs_from_events(path):
    lines = [ln for ln in Path(path).read_text().splitlines() if ln.strip()]
    if len(lines) < 2:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    header = lines[0].split("\t")
    if "onset" not in header:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    i = header.index("onset")
    bulbs = [int(float(ln.split("\t")[i])) for ln in lines[1:]]
    if not bulbs:
        raise ValueError("uncompiled BIDS-EEG table is absence")
    return bulbs


def main():
    bulbs = bulbs_from_events(EV)
    empty = "raised"
    try:
        bulbs_from_events("/tmp/aletheia-empty-events.tsv")
        empty = "accepted"
    except (ValueError, FileNotFoundError):
        p = Path("/tmp/aletheia-empty-events.tsv")
        p.write_text("onset\tduration\ttrial_type\n")
        try:
            bulbs_from_events(p)
            empty = "accepted"
        except ValueError:
            empty = "raised"
    rec = {
        "schema": "gaplock.show_bids.v1",
        "used": "https://bids.neuroimaging.io/",
        "built": "BIDS events [1,3,2] give empty-slot day 2; empty events are absence",
        "ours": {"bulbs": bulbs, "day": k_empty_slots(bulbs, 1), "markers": read_bids_trial_types(MK), "annot": read_mne_annot_descriptions(ANNOT), "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gaplock bids show identity failed")
    if rec["ours"]["markers"] != ["go", "end"] or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("gaplock bids marker identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
