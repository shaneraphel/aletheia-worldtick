#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from manh import min_manhattan_after_remove
PTS=[[3,10],[5,15],[10,2],[4,4]]
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([])))}
def ours():
    n=min_manhattan_after_remove(PTS); empty="raised"
    try:
        min_manhattan_after_remove([]); empty="accepted"
    except ValueError:
        pass
    return {"min_manhattan_after_remove": n, "empty": empty}
def main():
    rec={"schema":"farlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"four sites, span 12 after one delete; empty points are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["min_manhattan_after_remove"]!=12 or rec["ours"]["empty"]!="raised":
        raise SystemExit("farlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
