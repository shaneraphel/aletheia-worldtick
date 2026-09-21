#!/usr/bin/env python3.12
"""Use NumPy cumsum on a spike prefix. Record empty values. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from fenwick import fenwick_prefix


def theirs() -> dict:
    import numpy as np

    return {
        "package": "numpy",
        "version": np.__version__,
        "empty_cumsum": np.cumsum(np.array([], dtype=int)).tolist(),
        "prefix_through_3": int(np.cumsum(np.array([1, 2, 3, 4], dtype=int))[3]),
    }


def ours() -> dict:
    pref = fenwick_prefix([1, 2, 3, 4], 3)
    empty = "raised"
    try:
        fenwick_prefix([], 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"fenwick_prefix_through_3": pref, "empty": empty}


def main() -> int:
    rec = {
        "schema": "prefixlock.show_numpy.v1",
        "used": "https://github.com/numpy/numpy",
        "built": "four-bin spike prefix 10; empty values are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["fenwick_prefix_through_3"] != 10 or rec["ours"]["empty"] != "raised":
        raise SystemExit("prefixlock show identity failed")
    if rec["theirs"]["prefix_through_3"] != 10:
        raise SystemExit("numpy prefix identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
