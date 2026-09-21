#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from infsq import infection_sequences
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_sum":float(np.sum(np.array([]))),"n":5}
def ours():
    n=infection_sequences(5,[0,4]); empty="raised"
    try:
        infection_sequences(5,[]); empty="accepted"
    except ValueError:
        pass
    return {"infection_sequences": n, "empty": empty}
def main():
    rec={"schema":"sicklock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"five children, sick ends 0 and 4, four orders; empty sick set is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["infection_sequences"]!=4 or rec["ours"]["empty"]!="raised":
        raise SystemExit("sicklock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
