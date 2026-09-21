#!/usr/bin/env python3.12
"""Use NumPy on a lane grid. Record empty field. Refuse empty grid."""
from __future__ import annotations
import json, platform, sys
from gridk import shortest_path_obstacles

GRID = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_cells":15}

def ours() -> dict:
    n = shortest_path_obstacles(GRID, 1)
    empty = "raised"
    try:
        shortest_path_obstacles([], 1)
        empty = "accepted"
    except ValueError:
        pass
    return {"shortest_path_obstacles": n, "empty": empty}

def main() -> int:
    rec={"schema":"obstlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"5x3 lane path 6 with one elim; empty grid is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["shortest_path_obstacles"]!=6 or rec["ours"]["empty"]!="raised":
        raise SystemExit("obstlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
