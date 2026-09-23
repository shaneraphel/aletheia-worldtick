#!/usr/bin/env python3.12
"""Show: MNE on a Neuroscan CNT tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from cntocc import cnt_occupancy, read_cnt, read_cnt_events, write_cnt
from kslots import k_empty_slots

CNT = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.cnt"


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
    raw = mne.io.read_raw_cnt(str(CNT), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap.cnt")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_cnt(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_cnt": empty,
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
    }


def main():
    bulbs = read_cnt(CNT)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-gap.cnt")
    p.write_bytes(b"")
    try:
        read_cnt(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_events = "raised"
    try:
        write_cnt(Path("/tmp/aletheia-empty-cnt-events-gap.cnt"), [1], events=[])
        empty_events = "accepted"
    except ValueError:
        empty_events = "raised"
    rec = {
        "schema": "gaplock.show_cnt.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads CNT onsets [1,3,2] and stim 1/2; empty-slot day 2; empty CNT is absence",
        "theirs": theirs(),
        "ours": {
            "n": cnt_occupancy(CNT),
            "samples": bulbs,
            "day": k_empty_slots(bulbs, 1),
            "empty": empty,
            "empty_events": empty_events,
            "annot": read_cnt_events(CNT),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gaplock cnt show identity failed")
    if rec["ours"]["empty_events"] != "raised" or rec["ours"]["annot"] != ["1", "2"]:
        raise SystemExit("gaplock cnt event identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_cnt"] != "raised":
        raise SystemExit("mne cnt identity failed")
    if rec["theirs"]["annot"] != ["1", "2"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne cnt annot identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
