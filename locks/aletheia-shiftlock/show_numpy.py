#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from jobsc import job_scheduling
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_sum":float(np.sum(np.array([]))),"n_jobs":4}
def ours():
    n=job_scheduling([1,2,3,3],[3,4,5,6],[50,10,40,70]); empty="raised"
    try:
        job_scheduling([],[],[]); empty="accepted"
    except ValueError:
        pass
    return {"job_scheduling": n, "empty": empty}
def main():
    rec={"schema":"shiftlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"four-job profit 120; empty job tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["job_scheduling"]!=120 or rec["ours"]["empty"]!="raised":
        raise SystemExit("shiftlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
