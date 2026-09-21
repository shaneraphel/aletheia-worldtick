#!/usr/bin/env python3.12
"""Use SciPy ConvexHull on grasp contacts. Record empty points. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from graham import graham_hull

PTS = [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]


def theirs() -> dict:
    import numpy as np
    from scipy.spatial import ConvexHull

    empty = "raised"
    try:
        ConvexHull(np.zeros((0, 2)))
        empty = "accepted"
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}".split("\n", 1)[0]
    hull = ConvexHull(np.array(PTS, dtype=float))
    return {
        "package": "scipy",
        "version": __import__("scipy").__version__,
        "empty": empty,
        "hull_vertices": int(hull.vertices.size),
    }


def ours() -> dict:
    n = graham_hull(PTS)
    empty = "raised"
    try:
        graham_hull([])
        empty = "accepted"
    except ValueError:
        pass
    return {"graham_hull": n, "empty": empty}


def main() -> int:
    rec = {
        "schema": "hulllock.show_scipy.v1",
        "used": "https://github.com/scipy/scipy",
        "built": "five-contact grasp hull 4; empty points are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["graham_hull"] != 4 or rec["ours"]["empty"] != "raised":
        raise SystemExit("hulllock show identity failed")
    if rec["theirs"]["hull_vertices"] != 4:
        raise SystemExit("scipy hull identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
