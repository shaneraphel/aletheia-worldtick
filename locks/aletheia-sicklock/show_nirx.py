#!/usr/bin/env python3.12
"""Show: I used MNE on a NIRx tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path

from nirxocc import nirx_occupancy, read_nirx, read_nirx_evt, write_nirx

NIRX = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_nirx"
LOCK = "sicklock"
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
    raw = mne.io.read_raw_nirx(str(NIRX), preload=True, verbose=False)
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-nirx-{LOCK}")
    if p.exists():
        shutil.rmtree(p)
    p.mkdir()
    try:
        mne.io.read_raw_nirx(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nolog = Path(f"/tmp/aletheia-nirx-noevt-{LOCK}")
    if nolog.exists():
        shutil.rmtree(nolog)
    write_nirx(nolog, [1], events=[(1.0, 1)])
    (nolog / "tape.evt").unlink()
    raw_nolog = mne.io.read_raw_nirx(str(nolog), preload=True, verbose=False)
    empty_evt = int(len(raw_nolog.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_nirx": empty,
        "empty_evt": empty_evt,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "wl1": [float(x) for x in raw.get_data(picks=[0])[0]],
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-nirx-{LOCK}")
    if p.exists():
        shutil.rmtree(p)
    p.mkdir()
    try:
        read_nirx(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_evt = "raised"
    try:
        write_nirx(Path(f"/tmp/aletheia-empty-nirx-evt-{LOCK}"), [1], events=[])
        empty_evt = "accepted"
    except ValueError:
        empty_evt = "raised"
    rec = {
        "schema": "sicklock.show_nirx.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads five NIRx samples on S1_D1 and stim 1.0/2.0 at 1.0/2.0 s; empty NIRx is absence",
        "theirs": theirs(),
        "ours": {
            "n": nirx_occupancy(NIRX),
            "samples": read_nirx(NIRX)["samples"],
            "empty": empty,
            "empty_evt": empty_evt,
            "annot": read_nirx_evt(NIRX),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit("sicklock nirx show identity failed")
    if rec["ours"]["empty_evt"] != "raised" or rec["ours"]["annot"] != ["1.0", "2.0"]:
        raise SystemExit("sicklock nirx evt identity failed")
    if rec["theirs"]["n_times"] != N or rec["theirs"]["empty_nirx"] != "raised":
        raise SystemExit("mne nirx identity failed")
    if rec["theirs"]["annot"] != ["1.0", "2.0"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne nirx annot identity failed")
    if rec["theirs"]["wl1"] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne nirx wl1 identity failed")
    if rec["theirs"]["empty_evt"] != 0:
        raise SystemExit("mne nirx empty evt identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
