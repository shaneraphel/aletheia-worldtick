#!/usr/bin/env python3.12
"""Use NumPy on an elevation grid. Record empty max. Refuse empty grid."""
from __future__ import annotations
import json, platform, sys
from swimwt import swim_rising

G=[[0,2],[1,3]]

def theirs() -> dict:
    import numpy as np
    empty="raised"
    try:
        float(np.max(np.array([])))
        empty="accepted"
    except ValueError:
        pass
    return {"package":"numpy","version":np.__version__,"empty_max":empty,"grid_max":int(np.max(np.array(G)))}

def ours() -> dict:
    n=swim_rising(G)
    empty="raised"
    try:
        swim_rising([])
        empty="accepted"
    except ValueError:
        pass
    return {"swim_rising":n,"empty":empty}

def main() -> int:
    rec={"schema":"floodlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"2x2 rising-water wait 3; empty grid is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["swim_rising"]!=3 or rec["ours"]["empty"]!="raised":
        raise SystemExit("floodlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
