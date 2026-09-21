#!/usr/bin/env python3.12
"""Use SciPy Voronoi on world-model sites. Record empty sites. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from voronoi import voronoi_unbounded

PTS = [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]


def theirs() -> dict:
    import numpy as np
    from scipy.spatial import Voronoi

    empty = "raised"
    try:
        Voronoi(np.zeros((0, 2)))
        empty = "accepted"
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}".split("\n", 1)[0]
    vor = Voronoi(np.array(PTS, dtype=float))
    return {
        "package": "scipy",
        "version": __import__("scipy").__version__,
        "empty": empty,
        "npoints": int(vor.npoints),
        "ridge_vertices": int(len(vor.ridge_vertices)),
    }


def ours() -> dict:
    n = voronoi_unbounded(PTS)
    empty = "raised"
    try:
        voronoi_unbounded([])
        empty = "accepted"
    except ValueError:
        pass
    return {"voronoi_unbounded": n, "empty": empty}


def main() -> int:
    rec = {
        "schema": "celllock.show_scipy.v1",
        "used": "https://github.com/scipy/scipy",
        "built": "five-site world cells 4; empty sites are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["voronoi_unbounded"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("celllock show identity failed")
    if rec["theirs"]["npoints"] != 5:
        raise SystemExit("scipy voronoi identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
