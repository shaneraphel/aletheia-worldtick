#!/usr/bin/env python3.12
"""Use SciPy Delaunay on contact sites. Record empty sites. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from delaun import delaun_tris

PTS = [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]


def theirs() -> dict:
    import numpy as np
    from scipy.spatial import Delaunay

    empty = "raised"
    try:
        Delaunay(np.zeros((0, 2)))
        empty = "accepted"
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}".split("\n", 1)[0]
    tri = Delaunay(np.array(PTS, dtype=float))
    return {
        "package": "scipy",
        "version": __import__("scipy").__version__,
        "empty": empty,
        "triangles": int(tri.simplices.shape[0]),
    }


def ours() -> dict:
    n = delaun_tris(PTS)
    empty = "raised"
    try:
        delaun_tris([])
        empty = "accepted"
    except ValueError:
        pass
    return {"delaun_tris": n, "empty": empty}


def main() -> int:
    rec = {
        "schema": "meshlock.show_scipy.v1",
        "used": "https://github.com/scipy/scipy",
        "built": "five-site contact mesh 4 triangles; empty sites are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["delaun_tris"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("meshlock show identity failed")
    if rec["theirs"]["triangles"] != 4:
        raise SystemExit("scipy delaunay identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
