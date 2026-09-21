#!/usr/bin/env python3.12
"""Use NumPy on an infection tape. Record empty field. Refuse empty grid."""
from __future__ import annotations
import json, platform, sys
from virusw import contain_virus
GRID = [[0,1,0,0,0,0,0,1],[0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]]

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_cells":32}

def ours() -> dict:
    n = contain_virus([row[:] for row in GRID])
    empty = "raised"
    try:
        contain_virus([])
        empty = "accepted"
    except ValueError:
        pass
    return {"contain_virus": n, "empty": empty}

def main() -> int:
    rec={"schema":"cagelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"4x8 infection walls 10; empty grid is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["contain_virus"]!=10 or rec["ours"]["empty"]!="raised":
        raise SystemExit("cagelock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
