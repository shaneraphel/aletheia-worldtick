#!/usr/bin/env python3.12
"""Use NumPy on a lidar octant. Record empty points. Refuse here."""
from __future__ import annotations
import json, platform, sys
from octpart import octpart_ne
PTS = [(1,1,1),(0,0,0)]

def theirs() -> dict:
    import numpy as np
    empty_norm = float(np.linalg.norm(np.array([])))
    pts = np.array(PTS)
    ne = int(np.sum((pts >= 1).all(axis=1)))
    return {"package":"numpy","version":np.__version__,"empty_norm":empty_norm,"ne":ne}

def ours() -> dict:
    n = octpart_ne(PTS, 1, 1, 1)
    empty = "raised"
    try:
        octpart_ne([], 1, 1, 1)
        empty = "accepted"
    except ValueError:
        pass
    return {"octpart_ne": n, "empty": empty}

def main() -> int:
    rec = {"schema":"voxelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"two-point lidar NE 1; empty voxels are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["octpart_ne"] != 1 or rec["ours"]["empty"] != "raised":
        raise SystemExit("voxelock show identity failed")
    if rec["theirs"]["ne"] != 1:
        raise SystemExit("numpy octant identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
