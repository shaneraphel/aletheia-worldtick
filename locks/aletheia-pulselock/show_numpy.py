#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from kstren import max_k_subarray_strength
NUMS=[1,2,3,-1,2]
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_sum":float(np.sum(np.array([])))}
def ours():
    n=max_k_subarray_strength(NUMS,3); empty="raised"
    try:
        max_k_subarray_strength([],1); empty="accepted"
    except ValueError:
        pass
    return {"max_k_subarray_strength": n, "empty": empty}
def main():
    rec={"schema":"pulselock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"five pulses, k=3, strength 22; empty tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["max_k_subarray_strength"]!=22 or rec["ours"]["empty"]!="raised":
        raise SystemExit("pulselock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
