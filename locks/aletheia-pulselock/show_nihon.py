#!/usr/bin/env python3.12
"""Show: MNE on a Nihon Kohden tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from nihonocc import nihon_occupancy, read_nihon, read_nihon_log, write_nihon
from kstren import max_k_subarray_strength

EEG = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse_nihon.EEG"


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
    raw = mne.io.read_raw_nihon(str(EEG), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse.EEG")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_nihon(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nolog = Path("/tmp/aletheia-nolog-nihon-pulse")
    write_nihon(nolog, [1], events=[(1.0, "go")])
    nolog.with_suffix(".LOG").unlink()
    raw_nolog = mne.io.read_raw_nihon(str(nolog.with_suffix(".EEG")), preload=True, verbose=False)
    empty_log = int(len(raw_nolog.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_eeg": empty,
        "empty_log": empty_log,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
    }


def main():
    nums = read_nihon(EEG)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-pulse.EEG")
    p.write_bytes(b"")
    try:
        read_nihon(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_log = "raised"
    try:
        write_nihon(Path("/tmp/aletheia-empty-nihon-log-pulse"), [1], events=[])
        empty_log = "accepted"
    except ValueError:
        empty_log = "raised"
    rec = {
        "schema": "pulselock.show_nihon.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads Nihon Kohden [1,2,3,-1,2] and go/end; strength 22; empty Nihon Kohden is absence",
        "theirs": theirs(),
        "ours": {
            "n": nihon_occupancy(EEG),
            "samples": nums,
            "strength": max_k_subarray_strength(nums, 3),
            "empty": empty,
            "empty_log": empty_log,
            "annot": read_nihon_log(EEG),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock nihon show identity failed")
    if rec["ours"]["empty_log"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("pulselock nihon log identity failed")
    if rec["theirs"]["n_times"] != 5 or rec["theirs"]["empty_eeg"] != "raised":
        raise SystemExit("mne nihon identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne nihon annot identity failed")
    if rec["theirs"]["ch_names"] != ["C3"] or rec["theirs"]["empty_log"] != 0:
        raise SystemExit("mne nihon channel identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
