#!/usr/bin/env python3.12
"""Show: I used MNE on a Hitachi tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from hitachiocc import hitachi_occupancy, read_hitachi, write_hitachi

CSV = Path(__file__).resolve().parent / "resources" / "synthetic" / "sub-01_task-spike_hitachi.csv"
LOCK = "spikelock"
N = 8


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
    raw = mne.io.read_raw_hitachi(str(CSV), preload=True, verbose=False)
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-hitachi-{LOCK}.csv")
    p.write_text("")
    try:
        mne.io.read_raw_hitachi(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_hitachi": empty,
        "ch0": raw.ch_names[0],
        "ch0_data": [float(x) for x in raw.get_data(picks=[0])[0]],
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-hitachi-{LOCK}.csv")
    p.write_text("")
    try:
        read_hitachi(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_samples = "raised"
    try:
        write_hitachi(Path(f"/tmp/aletheia-empty-hitachi-samples-{LOCK}.csv"), [])
        empty_samples = "accepted"
    except ValueError:
        empty_samples = "raised"
    rec = {
        "schema": f"{LOCK}.show_hitachi.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads 8 Hitachi samples on S1_D1 695; empty Hitachi is absence",
        "theirs": theirs(),
        "ours": {
            "n": hitachi_occupancy(CSV),
            "samples": read_hitachi(CSV)["samples"],
            "empty": empty,
            "empty_samples": empty_samples,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit(f"{LOCK} hitachi show identity failed")
    if rec["ours"]["empty_samples"] != "raised":
        raise SystemExit(f"{LOCK} hitachi empty identity failed")
    if rec["theirs"]["n_times"] != N or rec["theirs"]["empty_hitachi"] != "raised":
        raise SystemExit("mne hitachi identity failed")
    if rec["theirs"]["ch0"] != "S1_D1 695":
        raise SystemExit("mne hitachi ch0 identity failed")
    if rec["theirs"]["ch0_data"] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne hitachi samples identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
