#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, sys
from racecr import race_car
def theirs():
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"target":3}
def ours():
    n=race_car(3); empty="raised"
    try:
        race_car(-1); empty="accepted"
    except ValueError:
        pass
    return {"race_car": n, "empty": empty}
def main():
    rec={"schema":"racelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"target 3 uses 2 instructions; negative target is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["race_car"]!=2 or rec["ours"]["empty"]!="raised":
        raise SystemExit("racelock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
