#!/usr/bin/env python3.12
"""Use NumPy on a left-visible tape. Record empty count. Refuse n=0."""
from __future__ import annotations
import json, platform, sys
from visst import ways_rearrange_sticks

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_count":int(np.count_nonzero(np.array([])==1)),"n":3}

def ours() -> dict:
    n = ways_rearrange_sticks(3, 2)
    empty = "raised"
    try:
        ways_rearrange_sticks(0, 1)
        empty = "accepted"
    except ValueError:
        pass
    return {"ways_rearrange_sticks": n, "empty": empty}

def main() -> int:
    rec={"schema":"sidelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"3 sticks 2 left-visible occupy 3 ways; n=0 is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["ways_rearrange_sticks"]!=3 or rec["ours"]["empty"]!="raised":
        raise SystemExit("sidelock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
