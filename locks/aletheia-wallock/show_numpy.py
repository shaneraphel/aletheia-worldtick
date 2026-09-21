#!/usr/bin/env python3.12
"""Use NumPy on a 3x3 lane grid. Record empty field. Refuse empty grid."""
from __future__ import annotations
import json, platform, sys
from obstc import min_obstacle_removal
GRID = [[0,1,1],[1,1,0],[1,1,0]]

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_cells":9}

def ours() -> dict:
    n = min_obstacle_removal([row[:] for row in GRID])
    empty = "raised"
    try:
        min_obstacle_removal([])
        empty = "accepted"
    except ValueError:
        pass
    return {"min_obstacle_removal": n, "empty": empty}

def main() -> int:
    rec={"schema":"wallock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"3x3 lane removals 2; empty grid is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["min_obstacle_removal"]!=2 or rec["ours"]["empty"]!="raised":
        raise SystemExit("wallock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
