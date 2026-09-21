#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from tapsg import min_taps
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_sum":float(np.sum(np.array([]))),"n":5}
def ours():
    n=min_taps(5,[3,4,1,1,0,0]); empty="raised"
    try:
        min_taps(0,[]); empty="accepted"
    except ValueError:
        pass
    return {"min_taps": n, "empty": empty}
def main():
    rec={"schema":"taplock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"width-5 garden uses 1 tap; n=0 is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["min_taps"]!=1 or rec["ours"]["empty"]!="raised":
        raise SystemExit("taplock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
