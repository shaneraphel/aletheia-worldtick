#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from edfocc import edf_occupancy
from bidseeg import bids_eeg_occupancy
from xdfocc import xdf_occupancy
from bvocc import brainvision_occupancy
from wfdbocc import wfdb_occupancy

ROOT = Path(__file__).resolve().parent / "resources" / "synthetic"
EDF = ROOT / "sub-01_task-spike_eeg.edf"
CH = ROOT / "sub-01_task-spike_channels.tsv"
EV = ROOT / "sub-01_task-spike_events.tsv"
XDF = ROOT / "sub-01_task-spike.xdf"
VHDR = ROOT / "sub-01_task-spike.vhdr"
HEA = ROOT / "sub-01_task-spike.hea"


def theirs():
    import numpy as np
    return {
        "package": "numpy",
        "version": np.__version__,
        "empty_mean": None if np.isnan(np.mean(np.array([]))) else float(np.mean(np.array([]))),
        "used_also": "https://github.com/mne-tools/mne-python",
    }


def ours():
    empty = "raised"
    try:
        edf_occupancy(Path("/tmp/empty.edf") if False else b"")
        empty = "accepted"
    except (ValueError, TypeError, OSError):
        try:
            from pathlib import Path as P
            p = P("/tmp/aletheia-empty.edf")
            p.write_bytes(b"")
            edf_occupancy(p)
            empty = "accepted"
        except ValueError:
            empty = "raised"
    return {
        "edf_occupancy": edf_occupancy(EDF),
        "bids_occupancy": bids_eeg_occupancy(CH, EV),
        "xdf_occupancy": xdf_occupancy(XDF),
        "brainvision_occupancy": brainvision_occupancy(VHDR),
        "wfdb_occupancy": wfdb_occupancy(HEA),
        "empty": empty,
    }


def main():
    rec = {
        "schema": "spikelock.show_edf.v1",
        "used": "https://physionet.org/content/eegmmidb/",
        "built": "one-channel EDF, 8 samples; empty EDF is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["edf_occupancy"] != 8 or rec["ours"]["empty"] != "raised":
        raise SystemExit("spikelock edf show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
