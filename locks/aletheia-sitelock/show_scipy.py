#!/usr/bin/env python3.12
"""Use SciPy Voronoi on three sites. Record empty sites. Refuse here."""

from __future__ import annotations

import json
import platform
import sys

from fortun import fortun_verts

PTS = [(0, 0), (2, 0), (1, 2)]


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
        "vertices": int(vor.vertices.shape[0]),
    }


def ours() -> dict:
    n = fortun_verts(PTS)
    empty = "raised"
    try:
        fortun_verts([])
        empty = "accepted"
    except ValueError:
        pass
    return {"fortun_verts": n, "empty": empty}


def main() -> int:
    rec = {
        "schema": "sitelock.show_scipy.v1",
        "used": "https://github.com/scipy/scipy",
        "built": "three-site Fortune vertex 1; empty sites are absence",
        "theirs": theirs(),
        "ours": ours(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if rec["ours"]["fortun_verts"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("sitelock show identity failed")
    if rec["theirs"]["vertices"] != 1:
        raise SystemExit("scipy voronoi vertex identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
