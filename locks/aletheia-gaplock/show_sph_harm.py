#!/usr/bin/env python3.12
"""Show: I fixed the MNE import on SciPy 1.17, then used MNE on an Eximia tape."""
from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

NXE = Path(__file__).resolve().parent / "resources" / "synthetic" / "tape.nxe"


def theirs() -> dict:
    import scipy.special as sp

    import_before = "raised"
    try:
        from scipy.special import sph_harm  # noqa: F401
        import_before = "accepted"
    except ImportError:
        import_before = "raised"
    t0 = time.perf_counter()
    if not hasattr(sp, "sph_harm"):
        _y = sp.sph_harm_y

        def sph_harm(m, n, theta, phi, *args, **kwargs):
            return _y(n, m, phi, theta)

        sp.sph_harm = sph_harm
        shim = "applied"
    else:
        shim = "native"
    t1 = time.perf_counter()
    import mne

    mne.set_log_level("ERROR")
    t2 = time.perf_counter()
    raw = mne.io.read_raw_eximia(str(NXE), preload=True, verbose=False)
    cal = 0.07629510948348212
    cz = [int(round(float(v) / cal)) for v in raw.get_data(picks=[32])[0]]
    empty = "raised"
    p = Path("/tmp/aletheia-empty-sph-gap.nxe")
    p.write_bytes(b"")
    try:
        mne.io.read_raw_eximia(str(p), preload=True, verbose=False)
        empty = "accepted"
    except Exception:
        empty = "raised"
    v = sp.sph_harm(0, 0, 0.5, 1.0)
    w = sp.sph_harm_y(0, 0, 1.0, 0.5)
    return {
        "scipy": __import__("scipy").__version__,
        "has_sph_harm_before": False,
        "import_before": import_before,
        "shim": shim,
        "shim_us": round((t1 - t0) * 1e6, 1),
        "mne_import_s": round(t2 - t1, 3),
        "mne": mne.__version__,
        "n_times": int(raw.n_times),
        "ch32": str(raw.ch_names[32]),
        "cz": cz,
        "empty_nxe": empty,
        "numeric_match": complex(v) == complex(w),
    }


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from eximiaocc import eximia_occupancy, read_eximia

    rec = {
        "schema": "gaplock.show_sph_harm.v1",
        "used": "https://github.com/mne-tools/mne-python",
        "built": "fixed MNE 1.9.0 import on SciPy 1.17.1 with a 6-line shim; official MNE reads 3 Eximia samples on Cz",
        "theirs": theirs(),
        "ours": {
            "n": eximia_occupancy(NXE),
            "samples": read_eximia(NXE)["samples"],
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    t = rec["theirs"]
    if t["import_before"] != "raised" or t["shim"] != "applied":
        raise SystemExit("sph_harm fix identity failed")
    if not t["numeric_match"] or t["mne"] != "1.9.0":
        raise SystemExit("sph_harm numeric identity failed")
    if t["n_times"] != 3 or t["ch32"] != "Cz" or t["cz"] != rec["ours"]["samples"]:
        raise SystemExit("mne eximia read identity failed")
    if t["empty_nxe"] != "raised" or t["shim_us"] > 1000.0:
        raise SystemExit("sph_harm efficiency identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
