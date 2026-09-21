#!/usr/bin/env python3.12
"""Show: I used MNE on a Curry tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

from curryocc import curry_occupancy, read_curry, read_curry_cef, write_curry

DAP = Path(__file__).resolve().parent / "resources" / "synthetic" / "sub-01_task-spike_curry.dap"
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
    t0 = time.perf_counter()
    raw = mne.io.read_raw_curry(str(DAP), preload=True, verbose=False)
    read_s = time.perf_counter() - t0
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-{LOCK}.dap")
    p.write_text("")
    try:
        mne.io.read_raw_curry(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nostim = Path(f"/tmp/aletheia-curry-nostim-{LOCK}.dap")
    write_curry(nostim, [1, 2, 3], events=[(1.0, 1)])
    Path(str(nostim)[:-4] + ".cef").unlink()
    raw_ns = mne.io.read_raw_curry(str(nostim), preload=True, verbose=False)
    empty_evt = int(len(raw_ns.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_curry": empty,
        "empty_evt": empty_evt,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "cz_uv": [round(float(x) / 1e-6) for x in raw.get_data(picks=[0])[0]],
        "read_s": read_s,
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-curry-{LOCK}.dap")
    p.write_text("")
    try:
        read_curry(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_evt = "raised"
    try:
        write_curry(Path(f"/tmp/aletheia-empty-curry-evt-{LOCK}.dap"), [1], events=[])
        empty_evt = "accepted"
    except ValueError:
        empty_evt = "raised"
    t0 = time.perf_counter()
    n = curry_occupancy(DAP)
    write_s = time.perf_counter() - t0
    rec = {
        "schema": f"{LOCK}.show_curry.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads 8 Curry samples on Cz and event 1/2 at 1.0/2.0 s; empty Curry is absence",
        "theirs": theirs(),
        "ours": {
            "n": n,
            "samples": read_curry(DAP)["samples"],
            "empty": empty,
            "empty_evt": empty_evt,
            "annot": read_curry_cef(DAP),
            "occupancy_s": write_s,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit(f"{LOCK} curry show identity failed")
    if rec["ours"]["empty_evt"] != "raised" or rec["ours"]["annot"] != ["1", "2"]:
        raise SystemExit(f"{LOCK} curry evt identity failed")
    if rec["theirs"]["n_times"] != N or rec["theirs"]["empty_curry"] != "raised":
        raise SystemExit("mne curry identity failed")
    if rec["theirs"]["annot"] != ["1", "2"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne curry annot identity failed")
    if rec["theirs"]["cz_uv"] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne curry samples identity failed")
    if rec["theirs"]["empty_evt"] != 0:
        raise SystemExit("mne curry empty evt identity failed")
    if rec["theirs"]["ch_names"] != ["Cz"]:
        raise SystemExit("mne curry channel identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
