#!/usr/bin/env python3.12
"""Show: I used MNE on an EyeLink tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from eyelinkocc import eyelink_occupancy, read_eyelink, read_eyelink_msg, write_eyelink
from ukkonen import n_suffix_links

ASC = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.asc"


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
    raw = mne.io.read_raw_eyelink(str(ASC), verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-stem.asc")
    p.write_text("")
    try:
        mne.io.read_raw_eyelink(str(p), verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_asc": empty,
        "ch_names": list(raw.ch_names),
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
        "pupil": [float(x) for x in raw.get_data(picks="pupil_left")[0]],
    }


def main():
    nums = read_eyelink(ASC)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-stem.asc")
    p.write_text("")
    try:
        read_eyelink(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_msg = "raised"
    try:
        write_eyelink(Path("/tmp/aletheia-empty-eyelink-msg-stem.asc"), [1], messages=[])
        empty_msg = "accepted"
    except ValueError:
        empty_msg = "raised"
    rec = {
        "schema": "stemlock.show_eyelink.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads EyeLink aba and go/end; suffix links 3; empty EyeLink is absence",
        "theirs": theirs(),
        "ours": {
            "n": eyelink_occupancy(ASC),
            "samples": nums,
            "word": "".join(chr(int(v)) for v in nums),
            "links": n_suffix_links("".join(chr(int(v)) for v in nums)),
            "empty": empty,
            "empty_msg": empty_msg,
            "annot": read_eyelink_msg(ASC),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["links"] != 3 or rec["ours"]["word"] != "aba" or rec["ours"]["empty"] != "raised":
        raise SystemExit("stemlock eyelink show identity failed")
    if rec["ours"]["empty_msg"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("stemlock eyelink msg identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_asc"] != "raised":
        raise SystemExit("mne eyelink identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne eyelink annot identity failed")
    if rec["theirs"]["pupil"] != [float(x) for x in rec["ours"]["samples"]]:
        raise SystemExit("mne eyelink pupil identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
