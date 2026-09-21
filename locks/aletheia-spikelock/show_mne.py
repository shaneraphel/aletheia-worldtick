#!/usr/bin/env python3.12
"""Show: I used MNE on EDF and GDF tapes, and I refused empty recordings."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bidseeg import read_mne_annot_descriptions
from edfocc import read_edf_annotations

from edfocc import edf_occupancy, read_edf
from gdfocc import gdf_occupancy, read_gdf

ROOT = Path(__file__).resolve().parent / "resources" / "synthetic"
EDF = ROOT / "sub-01_task-spike_eeg.edf"
GDF = ROOT / "sub-01_task-spike.gdf"
ANNOT = ROOT / "sub-01_task-spike_annotations.txt"


def _shim_sph_harm() -> str:
    import scipy.special as sp

    if hasattr(sp, "sph_harm"):
        return "native"
    _y = sp.sph_harm_y

    def sph_harm(m, n, theta, phi, *args, **kwargs):
        return _y(n, m, phi, theta)

    sp.sph_harm = sph_harm
    return "scipy.special.sph_harm_y"


def theirs() -> dict:
    shim = _shim_sph_harm()
    import numpy as np
    import mne

    mne.set_log_level("ERROR")
    edf_tal = mne.read_annotations(str(EDF))
    annot = mne.read_annotations(str(ANNOT))
    empty_annot = Path("/tmp/aletheia-empty-spike-annot.txt")
    empty_annot.write_bytes(b"")
    empty_annot_n = int(len(mne.read_annotations(str(empty_annot))))
    edf = mne.io.read_raw_edf(str(EDF), preload=True, verbose=False)
    gdf = mne.io.read_raw_gdf(str(GDF), preload=True, verbose=False)
    empty_edf = "raised"
    p = Path("/tmp/aletheia-empty-mne.edf")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_edf(str(p), preload=True, verbose=False)
        empty_edf = "accepted"
    except Exception:
        empty_edf = "raised"
    empty_gdf = "raised"
    q = Path("/tmp/aletheia-empty-mne.gdf")
    q.write_bytes(b"")
    try:
        mne.io.read_raw_gdf(str(q), preload=True, verbose=False)
        empty_gdf = "accepted"
    except Exception:
        empty_gdf = "raised"
    info = mne.create_info(["EEG Cz"], sfreq=1.0, ch_types=["eeg"])
    raw0 = mne.io.RawArray(np.zeros((1, 0)), info, verbose=False)
    return {
        "package": "mne",
        "annot_description": [str(x) for x in annot.description],
        "edf_annot": [str(x) for x in edf_tal.description],
        "edf_annot_onset": [float(x) for x in edf_tal.onset],
        "annot_onset": [float(x) for x in annot.onset],
        "empty_annot_n": empty_annot_n,
        "version": mne.__version__,
        "import_shim": shim,
        "edf_n_times": int(edf.n_times),
        "gdf_n_times": int(gdf.n_times),
        "empty_edf": empty_edf,
        "empty_gdf": empty_gdf,
        "empty_rawarray_n_times": int(raw0.n_times),
    }


def main():
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours.gdf")
    p.write_bytes(b"")
    try:
        read_gdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_annot = "raised"
    qa = Path("/tmp/aletheia-empty-ours-spike-annot.txt")
    qa.write_bytes(b"")
    try:
        read_mne_annot_descriptions(qa)
        empty_annot = "accepted"
    except ValueError:
        empty_annot = "raised"
    rec = {
        "schema": "spikelock.show_mne.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE annotations copy BIDS trial_type go/end; empty trial_type is absence; MNE reads the MIT EDF and GDF 1.25 tapes; empty file is absence here",
        "theirs": theirs(),
        "ours": {"annot": read_mne_annot_descriptions(ANNOT), "empty_annot": empty_annot, "edf_annot": read_edf_annotations(EDF), 
            "edf": edf_occupancy(EDF),
            "gdf": gdf_occupancy(GDF),
            "edf_samples": read_edf(EDF)["samples"],
            "gdf_samples": read_gdf(GDF)["samples"],
            "empty": empty,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["edf"] != 8 or rec["ours"]["gdf"] != 8 or rec["ours"]["empty"] != "raised":
        raise SystemExit("spikelock mne show identity failed")
    if rec["theirs"]["edf_n_times"] != 8 or rec["theirs"]["gdf_n_times"] != 8:
        raise SystemExit("mne edf/gdf identity failed")
    if rec["theirs"]["empty_edf"] != "raised" or rec["theirs"]["empty_rawarray_n_times"] != 0:
        raise SystemExit("mne empty identity failed")
    if rec["theirs"]["annot_description"] != ["go", "end"] or rec["theirs"]["annot_onset"] != [1.0, 2.0]:
        raise SystemExit("mne annot identity failed")
    if rec["theirs"]["empty_annot_n"] != 0:
        raise SystemExit("mne empty annot identity failed")
    if rec["ours"]["annot"] != ["go", "end"] or rec["ours"]["empty_annot"] != "raised":
        raise SystemExit("ours annot identity failed")
    if rec["theirs"]["edf_annot"] != ["go", "end"] or rec["theirs"]["edf_annot_onset"] != [1.0, 2.0]:
        raise SystemExit("mne edf tal identity failed")
    if rec["ours"]["edf_annot"] != ["go", "end"]:
        raise SystemExit("ours edf tal identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
