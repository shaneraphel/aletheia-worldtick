#!/usr/bin/env python3.12
"""Show: I used MNE on a Persyst tape, and I refused an empty recording."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from persystocc import persyst_occupancy, read_persyst, read_persyst_comments, write_persyst
from kslots import k_empty_slots

LAY = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape_persyst.lay"


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
    raw = mne.io.read_raw_persyst(str(LAY), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-gap.lay")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_persyst(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    stem = Path("/tmp/aletheia-persyst-official-empty-gap")
    write_persyst(stem, [1], comments=[(1.0, "go")])
    lay = stem.with_suffix(".lay")
    lay.write_text(lay.read_text().split("[Comments]")[0])
    raw_empty = mne.io.read_raw_persyst(str(lay), preload=True, verbose=False)
    empty_comments = int(len(raw_empty.annotations))
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_lay": empty,
        "empty_comments": empty_comments,
        "annot": [str(x) for x in raw.annotations.description],
        "onset": [float(o) for o in raw.annotations.onset],
    }


def main():
    nums = read_persyst(LAY)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-gap.lay")
    p.write_bytes(b"")
    try:
        read_persyst(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_comments = "raised"
    try:
        write_persyst(Path("/tmp/aletheia-empty-persyst-comments-gap"), [1], comments=[])
        empty_comments = "accepted"
    except ValueError:
        empty_comments = "raised"
    rec = {
        "schema": "gaplock.show_persyst.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads Persyst onsets [1,3,2] and go/end; empty-slot day 2; empty Persyst is absence",
        "theirs": theirs(),
        "ours": {
            "n": persyst_occupancy(LAY),
            "samples": nums,
            "day": k_empty_slots(nums, 1),
            "empty": empty,
            "empty_comments": empty_comments,
            "annot": read_persyst_comments(LAY),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["day"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gaplock persyst show identity failed")
    if rec["ours"]["n"] != 3:
        raise SystemExit("gaplock persyst n identity failed")
    if rec["ours"]["empty_comments"] != "raised" or rec["ours"]["annot"] != ["go", "end"]:
        raise SystemExit("gaplock persyst comment identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_lay"] != "raised":
        raise SystemExit("mne persyst identity failed")
    if rec["theirs"]["annot"] != ["go", "end"] or rec["theirs"]["onset"] != [1.0, 2.0]:
        raise SystemExit("mne persyst annot identity failed")
    if rec["theirs"]["empty_comments"] != 0:
        raise SystemExit("mne persyst empty comments identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
