#!/usr/bin/env python3.12
"""Show: I used MNE on a BOXY tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from boxyocc import boxy_occupancy, read_boxy, read_boxy_digaux, write_boxy

BOXY = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.boxy"
LOCK = "bloomlock"
N = 3


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
    raw = mne.io.read_raw_boxy(str(BOXY), preload=True, verbose=False)
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-{LOCK}.boxy")
    p.write_text("")
    try:
        mne.io.read_raw_boxy(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nostim = Path(f"/tmp/aletheia-boxy-nostim-{LOCK}.boxy")
    write_boxy(nostim, [1, 2, 3], events=[(1.0, 1)])
    out = []
    for ln in nostim.read_text().splitlines():
        cols = ln.split("\t")
        if len(cols) == 5 and cols[0].isdigit():
            cols[4] = "0"
            ln = "\t".join(cols)
        out.append(ln)
    nostim.write_text("\n".join(out) + "\n")
    raw_ns = mne.io.read_raw_boxy(str(nostim), preload=True, verbose=False)
    empty_stim = int(len(raw_ns.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_boxy": empty,
        "empty_stim": empty_stim,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "dc": [float(x) for x in raw.get_data(picks=[0])[0]],
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-boxy-{LOCK}.boxy")
    p.write_text("")
    try:
        read_boxy(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_stim = "raised"
    try:
        write_boxy(Path(f"/tmp/aletheia-empty-boxy-stim-{LOCK}.boxy"), [1], events=[])
        empty_stim = "accepted"
    except ValueError:
        empty_stim = "raised"
    rec = {
        "schema": f"{LOCK}.show_boxy.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads BOXY onsets [1,2,3] on S1_D1 DC and stim 1.0/2.0 at 1.0/2.0 s; empty BOXY is absence",
        "theirs": theirs(),
        "ours": {
            "n": boxy_occupancy(BOXY),
            "samples": read_boxy(BOXY)["samples"],
            "empty": empty,
            "empty_stim": empty_stim,
            "annot": read_boxy_digaux(BOXY),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit(f"{LOCK} boxy show identity failed")
    if rec["ours"]["empty_stim"] != "raised" or rec["ours"]["annot"] != ["1.0", "2.0"]:
        raise SystemExit(f"{LOCK} boxy stim identity failed")
    if rec["theirs"]["n_times"] != N + 1 or rec["theirs"]["empty_boxy"] != "raised":
        raise SystemExit("mne boxy identity failed")
    if rec["theirs"]["annot"] != ["1.0", "2.0"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne boxy annot identity failed")
    if rec["theirs"]["dc"][:N] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne boxy samples identity failed")
    if rec["theirs"]["empty_stim"] != 0:
        raise SystemExit("mne boxy empty stim identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
