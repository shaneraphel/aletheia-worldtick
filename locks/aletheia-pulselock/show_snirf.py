#!/usr/bin/env python3.12
"""Show: I used MNE on a SNIRF tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import h5py

from snirfocc import read_snirf, read_snirf_stim, snirf_occupancy, write_snirf

SNIRF = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse.snirf"
LOCK = "pulselock"
N = 5


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
    raw = mne.io.read_raw_snirf(str(SNIRF), preload=True, verbose=False)
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-{LOCK}.snirf")
    with h5py.File(p, "w") as f:
        f.create_group("empty")
    try:
        mne.io.read_raw_snirf(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nostim = Path(f"/tmp/aletheia-snirf-nostim-{LOCK}.snirf")
    write_snirf(nostim, [1], events=[(1.0, "1.0")])
    with h5py.File(nostim, "a") as f:
        del f["nirs/stim1"]
    raw_ns = mne.io.read_raw_snirf(str(nostim), preload=True, verbose=False)
    empty_stim = int(len(raw_ns.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_snirf": empty,
        "empty_stim": empty_stim,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "ch0": [float(x) for x in raw.get_data(picks=[0])[0]],
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-snirf-{LOCK}.snirf")
    p.write_bytes(b"")
    try:
        read_snirf(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_stim = "raised"
    try:
        write_snirf(Path(f"/tmp/aletheia-empty-snirf-stim-{LOCK}.snirf"), [1], events=[])
        empty_stim = "accepted"
    except ValueError:
        empty_stim = "raised"
    rec = {
        "schema": f"{LOCK}.show_snirf.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads SNIRF [1,2,3,-1,2] on S1_D1 and stim 1.0/2.0 at 1.0/2.0 s; empty SNIRF is absence",
        "theirs": theirs(),
        "ours": {
            "n": snirf_occupancy(SNIRF),
            "samples": read_snirf(SNIRF)["samples"],
            "empty": empty,
            "empty_stim": empty_stim,
            "annot": read_snirf_stim(SNIRF),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit(f"{LOCK} snirf show identity failed")
    if rec["ours"]["empty_stim"] != "raised" or rec["ours"]["annot"] != ["1.0", "2.0"]:
        raise SystemExit(f"{LOCK} snirf stim identity failed")
    if rec["theirs"]["n_times"] != N or rec["theirs"]["empty_snirf"] != "raised":
        raise SystemExit("mne snirf identity failed")
    if rec["theirs"]["annot"] != ["1.0", "2.0"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne snirf annot identity failed")
    if rec["theirs"]["ch0"] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne snirf samples identity failed")
    if rec["theirs"]["empty_stim"] != 0:
        raise SystemExit("mne snirf empty stim identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
