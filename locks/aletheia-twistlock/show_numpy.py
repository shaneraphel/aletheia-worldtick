#!/usr/bin/env python3.12
"""Use NumPy hypot on a wrist frame. Record empty vector. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from givens import givens_hypot


def theirs() -> dict:
    import numpy as np

    return {
        "package": "numpy",
        "version": np.__version__,
        "empty_norm": float(np.linalg.norm(np.array([]))),
        "hypot_3_4": float(np.hypot(3, 4)),
    }


def ours() -> dict:
    h = givens_hypot([3, 4])
    empty = "raised"
    try:
        givens_hypot([])
        empty = "accepted"
    except ValueError:
        pass
    return {"givens_hypot": h, "empty": empty}


def main() -> int:
    rec = {
        "schema": "twistlock.show_numpy.v1",
        "used": "https://github.com/numpy/numpy",
        "built": "wrist hypot 5; empty frame is absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["givens_hypot"] != 5 or rec["ours"]["empty"] != "raised":
        raise SystemExit("twistlock show identity failed")
    if rec["theirs"]["hypot_3_4"] != 5.0:
        raise SystemExit("numpy hypot identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
