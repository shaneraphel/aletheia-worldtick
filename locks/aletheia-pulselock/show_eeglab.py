#!/usr/bin/env python3.12
"""Show: an EEGLAB set (an empty recording)."""
from __future__ import annotations
import json, platform, sys
from pathlib import Path
from eeglabocc import eeglab_occupancy, read_eeglab, read_eeglab_events, write_eeglab
from kstren import max_k_subarray_strength

SET = Path(__file__).resolve().parent / "resources" / "synthetic" / "pulse.set"


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
    from scipy.io import loadmat, savemat
    import numpy as np
    import scipy

    empty_path = Path("/tmp/aletheia-empty.set")
    savemat(empty_path, {"EEG": {"nbchan": 0, "pnts": 0, "data": np.zeros((0, 0))}})
    rec = loadmat(empty_path, squeeze_me=True, struct_as_record=False)
    pnts = int(getattr(rec["EEG"], "pnts", 0) or 0)
    shim = _shim_sph_harm()
    import mne

    mne.set_log_level("ERROR")
    ann = mne.read_annotations(str(SET))
    return {
        "package": "scipy",
        "version": scipy.__version__,
        "empty_pnts": pnts,
        "mne": mne.__version__,
        "import_shim": shim,
        "annot": [str(x) for x in ann.description],
        "onset": [float(o) for o in ann.onset],
    }


def main():
    nums = read_eeglab(SET)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-pulse.set")
    from scipy.io import savemat
    import numpy as np

    savemat(p, {"EEG": {"nbchan": 0, "pnts": 0, "data": np.zeros((0, 0))}})
    try:
        read_eeglab(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_events = "raised"
    try:
        write_eeglab(Path("/tmp/aletheia-empty-events-pulse.set"), [1], events=[])
        empty_events = "accepted"
    except ValueError:
        empty_events = "raised"
    rec = {
        "schema": "pulselock.show_eeglab.v1",
        "used": "https://eeglab.org/",
        "built": "five EEGLAB points, pulse strength 22; EEG.event go/end; empty set is absence",
        "theirs": theirs(),
        "ours": {
            "n": eeglab_occupancy(SET),
            "strength": max_k_subarray_strength(nums, 3),
            "empty": empty,
            "empty_events": empty_events,
            "annot": read_eeglab_events(SET),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["strength"] != 22 or rec["ours"]["empty"] != "raised":
        raise SystemExit("pulselock eeglab show identity failed")
    if rec["ours"]["empty_events"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("pulselock eeglab event identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne eeglab event identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
