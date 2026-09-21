#!/usr/bin/env python3.12
"""Use NumPy on a height field. Record empty max. Refuse empty matrix."""
from __future__ import annotations
import json, platform, sys
from lipath import longest_increasing_path

M=[[9,9,4],[6,6,8],[2,1,1]]

def theirs() -> dict:
    import numpy as np
    empty="raised"
    try:
        float(np.max(np.array([])))
        empty="accepted"
    except ValueError:
        pass
    return {"package":"numpy","version":np.__version__,"empty_max":empty,"field_max":int(np.max(np.array(M)))}

def ours() -> dict:
    n=longest_increasing_path(M)
    empty="raised"
    try:
        longest_increasing_path([])
        empty="accepted"
    except ValueError:
        pass
    return {"longest_increasing_path":n,"empty":empty}

def main() -> int:
    rec={"schema":"climblock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"3x3 height path 4; empty field is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["longest_increasing_path"]!=4 or rec["ours"]["empty"]!="raised":
        raise SystemExit("climblock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
