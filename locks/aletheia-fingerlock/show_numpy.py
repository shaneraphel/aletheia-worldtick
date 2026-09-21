#!/usr/bin/env python3.12
"""Use NumPy on a two-finger word. Record empty field. Refuse empty word."""
from __future__ import annotations
import json, platform, sys
from twofng import minimum_distance

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_letters":4}

def ours() -> dict:
    n = minimum_distance("CAKE")
    empty = "raised"
    try:
        minimum_distance("")
        empty = "accepted"
    except ValueError:
        pass
    return {"minimum_distance": n, "empty": empty}

def main() -> int:
    rec={"schema":"fingerlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"two-finger distance 3 on CAKE; empty word is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["minimum_distance"]!=3 or rec["ours"]["empty"]!="raised":
        raise SystemExit("fingerlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
