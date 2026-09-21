#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from kslots import k_empty_slots
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_count":int(np.count_nonzero(np.array([])==1)),"n_bulbs":3}
def ours():
    n=k_empty_slots([1,3,2],1); empty="raised"
    try:
        k_empty_slots([],1); empty="accepted"
    except ValueError:
        pass
    return {"k_empty_slots": n, "empty": empty}
def main():
    rec={"schema":"gaplock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"three blooms, one empty slot, day 2; empty tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["k_empty_slots"]!=2 or rec["ours"]["empty"]!="raised":
        raise SystemExit("gaplock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
