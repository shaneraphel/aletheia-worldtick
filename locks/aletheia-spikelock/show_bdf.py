#!/usr/bin/env python3.12
"""Show: I used MNE and edfio on a BDF tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from edfocc import bdf_occupancy, read_bdf, read_bdf_annotations, write_bdf

BDF = Path(__file__).resolve().parent / "resources" / "synthetic" / "sub-01_task-spike_eeg.bdf"


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
    import edfio
    import mne

    mne.set_log_level("ERROR")
    raw = mne.io.read_raw_bdf(str(BDF), preload=True, verbose=False)
    ann = mne.read_annotations(str(BDF))
    rec = edfio.read_bdf(BDF)
    empty = "raised"
    p = Path("/tmp/aletheia-empty.bdf")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_bdf(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_bdf": empty,
        "annot": [str(x) for x in ann.description],
        "onset": [float(o) for o in ann.onset],
        "edfio": edfio.__version__,
        "edfio_n_signals": int(rec.num_signals),
        "edfio_n_samples": int(len(rec.signals[0].data)),
        "edfio_annot": [a.text for a in rec.annotations],
        "edfio_onset": [float(a.onset) for a in rec.annotations],
    }


def main():
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours.bdf")
    p.write_bytes(b"")
    try:
        read_bdf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_annot = "raised"
    try:
        write_bdf(Path("/tmp/aletheia-empty-bdf-annot.bdf"), [1], annotations=[])
        empty_annot = "accepted"
    except ValueError:
        empty_annot = "raised"
    rec = {
        "schema": "spikelock.show_bdf.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE and edfio read 8 BDF samples and BDF Annotations go/end; empty BDF is absence",
        "theirs": theirs(),
        "ours": {
            "n": bdf_occupancy(BDF),
            "samples": read_bdf(BDF)["samples"],
            "empty": empty,
            "empty_annot": empty_annot,
            "annot": read_bdf_annotations(BDF),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != 8 or rec["ours"]["empty"] != "raised":
        raise SystemExit("spikelock bdf show identity failed")
    if rec["ours"]["empty_annot"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("spikelock bdf annot identity failed")
    if rec["theirs"]["n_times"] != 8 or rec["theirs"]["empty_bdf"] != "raised":
        raise SystemExit("mne bdf identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne bdf annot identity failed")
    if rec["theirs"]["edfio_n_signals"] != 1 or rec["theirs"]["edfio_n_samples"] != 8:
        raise SystemExit("edfio bdf identity failed")
    if rec["theirs"]["edfio_annot"] != ["go", "end"] or rec["theirs"]["edfio_onset"] != [1.0, 2.0]:
        raise SystemExit("edfio bdf annot identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
