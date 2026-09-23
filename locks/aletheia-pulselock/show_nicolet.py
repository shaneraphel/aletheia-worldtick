#!/usr/bin/env python3.12
"""Show: MNE on a Nicolet tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from nicoletocc import nicolet_occupancy, read_nicolet, write_nicolet
from kstren import max_k_subarray_strength

DATA = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse_nicolet.data"


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
    raw = mne.io.read_raw_nicolet(str(DATA), ch_type="eeg", preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse.data")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_nicolet(str(p), ch_type="eeg", preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_nicolet": empty,
        "ch_names": list(raw.ch_names),
        "n_annot": int(len(raw.annotations)),
    }


def main():
    nums = read_nicolet(DATA)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-pulse.data")
    p.write_bytes(b"")
    try:
        read_nicolet(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_samples = "raised"
    try:
        write_nicolet(Path("/tmp/aletheia-empty-nicolet-samples-pulse"), [])
        empty_samples = "accepted"
    except ValueError:
        empty_samples = "raised"
    rec = {
        "schema": "pulselock.show_nicolet.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads Nicolet [1,2,3,-1,2]; strength 22; empty Nicolet is absence",
        "theirs": theirs(),
        "ours": {
            "n": nicolet_occupancy(DATA),
            "samples": nums,
            "strength": max_k_subarray_strength(nums, 3),
            "empty": empty,
            "empty_samples": empty_samples,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock nicolet show identity failed")
    if rec["ours"]["empty_samples"] != "raised":
        raise SystemExit("pulselock nicolet empty identity failed")
    if rec["theirs"]["n_times"] != 5 or rec["theirs"]["empty_nicolet"] != "raised":
        raise SystemExit("mne nicolet identity failed")
    if rec["theirs"]["ch_names"] != ["Cz"] or rec["theirs"]["n_annot"] != 0:
        raise SystemExit("mne nicolet channel identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
