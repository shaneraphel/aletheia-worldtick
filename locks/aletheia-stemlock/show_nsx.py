#!/usr/bin/env python3.12
"""Show: MNE on a Blackrock NSX tape (an empty recording)."""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from nsxocc import nsx_occupancy, read_nsx, write_nsx
from ukkonen import n_suffix_links

NSX = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.ns3"


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
    raw = mne.io.read_raw_nsx(str(NSX), preload=True, verbose=False)
    empty = "raised"
    p = Path("/tmp/aletheia-empty-stem.ns3")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_nsx(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    return {
        "package": "mne",
        "version": mne.__version__,
        "import_shim": shim,
        "n_times": int(raw.n_times),
        "empty_nsx": empty,
        "ch_names": list(raw.ch_names),
        "n_annot": int(len(raw.annotations)),
    }


def main():
    nums = read_nsx(NSX)["samples"]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-ours-stem.ns3")
    p.write_bytes(b"")
    try:
        read_nsx(p)
        empty = "accepted"
    except ValueError:
        empty = "raised"
    empty_samples = "raised"
    try:
        write_nsx(Path("/tmp/aletheia-empty-nsx-samples-stem.ns3"), [])
        empty_samples = "accepted"
    except ValueError:
        empty_samples = "raised"
    rec = {
        "schema": "stemlock.show_nsx.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "official MNE reads NSX aba; suffix links 3; empty NSX is absence",
        "theirs": theirs(),
        "ours": {
            "n": nsx_occupancy(NSX),
            "samples": nums,
            "word": "".join(chr(int(v)) for v in nums),
            "links": n_suffix_links("".join(chr(int(v)) for v in nums)),
            "empty": empty,
            "empty_samples": empty_samples,
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["links"] != 3 or rec["ours"]["word"] != "aba" or rec["ours"]["empty"] != "raised":
        raise SystemExit("stemlock nsx show identity failed")
    if rec["ours"]["empty_samples"] != "raised":
        raise SystemExit("stemlock nsx empty identity failed")
    if rec["theirs"]["n_times"] != 3 or rec["theirs"]["empty_nsx"] != "raised":
        raise SystemExit("mne nsx identity failed")
    if rec["theirs"]["ch_names"] != ["Cz"] or rec["theirs"]["n_annot"] != 0:
        raise SystemExit("mne nsx channel identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
