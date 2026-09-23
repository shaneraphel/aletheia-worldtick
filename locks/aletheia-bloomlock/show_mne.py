#!/usr/bin/env python3.12
"""Show: MNE on a GDF 1.25 tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bidseeg import read_mne_annot_descriptions
from edfocc import read_edf_annotations

from bloom import bloom_maybe
from gdfocc import read_gdf

GDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.gdf"
ANNOT = GDF.parent / "tape_annotations.txt"
EDF = GDF.parent / "tape.edf"


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
    import mne

    mne.set_log_level("ERROR")
    edf_tal = mne.read_annotations(str(EDF))
    annot = mne.read_annotations(str(ANNOT))
    empty_annot = Path("/tmp/aletheia-empty-bloom-annot.txt")
    empty_annot.write_bytes(b"")
    empty_annot_n = int(len(mne.read_annotations(str(empty_annot))))
    gdf = mne.io.read_raw_gdf(str(GDF), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-bloom-mne.gdf")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_gdf(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "annot_description": [str(x) for x in annot.description],
        "edf_annot": [str(x) for x in edf_tal.description],
        "edf_annot_onset": [float(x) for x in edf_tal.onset],
        "annot_onset": [float(x) for x in annot.onset],
        "empty_annot_n": empty_annot_n,
        "version": mne.__version__,
        "import_shim": shim,
        "gdf_n_times": int(gdf.n_times),
        "empty_gdf": empty,
    }


def main():
    keys = read_gdf(GDF)["samples"]
    empty_annot = "raised"
    qa = Path("/tmp/aletheia-empty-ours-bloom-annot.txt")
    qa.write_bytes(b"")
    try:
        read_mne_annot_descriptions(qa)
        empty_annot = "accepted"
    except ValueError:
        empty_annot = "raised"
    rec = {
        "schema": "bloomlock.show_mne.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE annotations copy BIDS trial_type go/end; empty trial_type is absence; MNE reads GDF onsets [1,2,3]; maybe-membership 1; empty GDF is absence",
        "theirs": theirs(),
        "ours": {"annot": read_mne_annot_descriptions(ANNOT), "empty_annot": empty_annot, "edf_annot": read_edf_annotations(EDF), "samples": keys, "maybe": bloom_maybe(keys, 16, 2, 2)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["maybe"] != 1:
        raise SystemExit("bloomlock mne show identity failed")
    if rec["theirs"]["gdf_n_times"] != 3 or rec["theirs"]["empty_gdf"] != "raised":
        raise SystemExit("mne bloom identity failed")
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
