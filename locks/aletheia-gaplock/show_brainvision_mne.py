#!/usr/bin/env python3.12
"""Show: I used MNE on a BrainVision tape, and I refused an empty header."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from bvocc import read_brainvision, read_brainvision_annotations
from kslots import k_empty_slots

VHDR = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.vhdr"
VMRK = VHDR.with_suffix(".vmrk")


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
    raw = mne.io.read_raw_brainvision(str(VHDR), preload=True, verbose=False)
    ann = mne.read_annotations(str(VMRK))
    stim = [str(x) for x in ann.description if str(x).startswith("Stimulus/")]
    stim_onset = [float(o) for o, d in zip(ann.onset, ann.description) if str(d).startswith("Stimulus/")]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap.vhdr")
    p.write_text("")
    try:
        mne.io.read_raw_brainvision(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_vhdr": empty,
        "vmrk_stim": stim,
        "vmrk_onset": stim_onset,
    }


def main():
    bulbs = read_brainvision(VHDR)["samples"]
    rec = {
        "schema": "gaplock.show_brainvision_mne.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "MNE reads BrainVision [1,3,2]; empty-slot day 2; empty .vhdr is absence",
        "theirs": theirs(),
        "ours": {"annot": read_brainvision_annotations(VHDR), "samples": bulbs, "day": k_empty_slots(bulbs, 1)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2:
        raise SystemExit("gaplock brainvision show identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_vhdr"] != "raised":
        raise SystemExit("mne gap brainvision identity failed")
    if rec["theirs"]["vmrk_stim"] != ["Stimulus/go", "Stimulus/end"] or rec["theirs"]["vmrk_onset"] != [1.0, 2.0]:
        raise SystemExit("mne vmrk identity failed")
    if rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("ours vmrk identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
