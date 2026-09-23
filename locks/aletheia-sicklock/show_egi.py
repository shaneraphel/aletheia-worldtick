#!/usr/bin/env python3.12
"""Show: MNE on an EGI tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from egiocc import egi_occupancy, read_egi, read_egi_events, write_egi

RAW = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_egi.raw"
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
    raw = mne.io.read_raw_egi(str(RAW), preload=True, events_as_annotations=True, verbose=False)
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-{LOCK}.raw")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_egi(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    nostim = Path(f"/tmp/aletheia-egi-nostim-{LOCK}.raw")
    write_egi(nostim, [1, 2, 3], events=[(1.0, "DIN1")])
    # drop event pulses
    data = bytearray(nostim.read_bytes())
    n_events = 1
    off = 36 + n_events * 4
    row = 2 + n_events * 2
    for i in range(3):
        data[off + i * row + 2 : off + i * row + 4] = b"\x00\x00"
    nostim.write_bytes(bytes(data))
    raw_ns = mne.io.read_raw_egi(str(nostim), preload=True, events_as_annotations=True, verbose=False)
    empty_evt = int(len(raw_ns.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_egi": empty,
        "empty_evt": empty_evt,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "e1_uv": [round(float(x) / 1e-6) for x in raw.get_data(picks=[0])[0]],
    }


def main():
    empty = "raised"
    p = Path(f"/tmp/aletheia-empty-ours-egi-{LOCK}.raw")
    p.write_bytes(b"")
    try:
        read_egi(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_evt = "raised"
    try:
        write_egi(Path(f"/tmp/aletheia-empty-egi-evt-{LOCK}.raw"), [1], events=[])
        empty_evt = "accepted"
    except ValueError:
        empty_evt = "raised"
    rec = {
        "schema": f"{LOCK}.show_egi.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads five EGI samples on E1 and DIN1/DIN2 at 1.0/2.0 s; empty EGI is absence",
        "theirs": theirs(),
        "ours": {
            "n": egi_occupancy(RAW),
            "samples": read_egi(RAW)["samples"],
            "empty": empty,
            "empty_evt": empty_evt,
            "annot": read_egi_events(RAW),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["n"] != N or rec["ours"]["empty"] != "raised":
        raise SystemExit(f"{LOCK} egi show identity failed")
    if rec["ours"]["empty_evt"] != "raised" or rec["ours"]["annot"] != ["DIN1", "DIN2"]:
        raise SystemExit(f"{LOCK} egi evt identity failed")
    if rec["theirs"]["n_times"] != N or rec["theirs"]["empty_egi"] != "raised":
        raise SystemExit("mne egi identity failed")
    if rec["theirs"]["annot"] != ["DIN1", "DIN2"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne egi annot identity failed")
    if rec["theirs"]["e1_uv"] != rec["ours"]["samples"]:
        raise SystemExit("mne egi samples identity failed")
    if rec["theirs"]["empty_evt"] != 0:
        raise SystemExit("mne egi empty evt identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
