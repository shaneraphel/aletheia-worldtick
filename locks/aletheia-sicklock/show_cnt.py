#!/usr/bin/env python3.12
"""Show: I used MNE on a Neuroscan CNT tape, and I refused an empty sick set."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from cntocc import cnt_occupancy, read_cnt, read_cnt_events, write_cnt
from infsq import infection_sequences

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
    p = Path("/tmp/aletheia-empty-sick.cnt")
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
    samples = read_cnt(CNT)["samples"]
    n = len(samples)
    sick = [i for i, v in enumerate(samples) if int(v) != 0]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-sick.cnt")
    p.write_bytes(b"")
    try:
        read_cnt(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_events = "raised"
    try:
        write_cnt(Path("/tmp/aletheia-empty-cnt-events-sick.cnt"), [1], events=[])
        empty_events = "accepted"
    except ValueError:
        empty_events = "raised"
    rec = {
        "schema": "sicklock.show_cnt.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads five CNT samples, sick 0 and 4, and stim 1/2; four orders; empty CNT is absence",
        "theirs": theirs(),
        "ours": {
            "n": cnt_occupancy(CNT),
            "sick": sick,
            "sequences": infection_sequences(n, sick),
            "empty": empty,
            "empty_events": empty_events,
            "annot": read_cnt_events(CNT),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["sequences"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("sicklock cnt show identity failed")
    if rec["ours"]["empty_events"] != "raised" or rec["ours"]["annot"] != ["1", "2"]:
        raise SystemExit("sicklock cnt event identity failed")
    if rec["theirs"]["n_times"] != 5 or rec["theirs"]["empty_cnt"] != "raised":
        raise SystemExit("mne cnt identity failed")
    if rec["theirs"]["annot"] != ["1", "2"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne cnt annot identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
