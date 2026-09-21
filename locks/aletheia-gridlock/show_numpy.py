#!/usr/bin/env python3.12
"""Use NumPy on a BEV quadtree. Record empty points. Refuse here."""
from __future__ import annotations
import json, platform, sys
from qdtree import qdtree_ne
PTS = [(1,1),(0,0)]

def theirs() -> dict:
    import numpy as np
    empty_norm = float(np.linalg.norm(np.array([])))
    pts = np.array(PTS)
    ne = int(np.sum((pts >= 1).all(axis=1)))
    return {"package":"numpy","version":np.__version__,"empty_norm":empty_norm,"ne":ne}

def ours() -> dict:
    n = qdtree_ne(PTS, 1, 1)
    empty = "raised"
    try:
        qdtree_ne([], 1, 1)
        empty = "accepted"
    except ValueError:
        pass
    return {"qdtree_ne": n, "empty": empty}

def main() -> int:
    rec = {"schema":"gridlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"two-point BEV NE 1; empty points are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["qdtree_ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("gridlock show identity failed")
    if rec["theirs"]["ne"] != 1:
        raise SystemExit("numpy bev identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
