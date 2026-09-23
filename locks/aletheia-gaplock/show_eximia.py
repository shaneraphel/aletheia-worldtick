#!/usr/bin/env python3.12
"""Show: MNE on an Eximia tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from eximiaocc import eximia_occupancy, read_eximia, write_eximia
from kslots import k_empty_slots

NXE = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.nxe"


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
    raw = mne.io.read_raw_eximia(str(NXE), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap.nxe")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_eximia(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    cal = 0.07629510948348212
    cz = [int(round(float(v) / cal)) for v in raw.get_data(picks=[32])[0]]
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_nxe": empty,
        "ch32": str(raw.ch_names[32]),
        "cz": cz,
        "n_annot": int(len(raw.annotations)),
    }


def main():
    nums = read_eximia(NXE)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-gap.nxe")
    p.write_bytes(b"")
    try:
        read_eximia(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_samples = "raised"
    try:
        write_eximia(Path("/tmp/aletheia-empty-eximia-samples-gap.nxe"), [])
        empty_samples = "accepted"
    except ValueError:
        empty_samples = "raised"
    rec = {
        "schema": "gaplock.show_eximia.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads Eximia onsets [1,3,2] on Cz; empty-slot day 2; empty Eximia is absence",
        "theirs": theirs(),
        "ours": {
            "n": eximia_occupancy(NXE),
            "samples": nums,
            "day": k_empty_slots(nums, 1),
            "empty": empty,
            "empty_samples": empty_samples,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gaplock eximia show identity failed")
    if rec["ours"]["empty_samples"] != "raised":
        raise SystemExit("gaplock eximia empty identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_nxe"] != "raised":
        raise SystemExit("mne eximia identity failed")
    if rec["theirs"]["ch32"] != "Cz" or rec["theirs"]["cz"] != rec["ours"]["samples"]:
        raise SystemExit("mne eximia cz identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
