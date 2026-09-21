#!/usr/bin/env python3.12
"""Use NumPy sum on a count window. Record empty array. Refuse here."""
from __future__ import annotations
import json, platform, sys
from segspt import segspt_sum

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_sum":float(np.sum(np.array([]))),"sum_1_3":int(np.sum(np.array([1,3,5,7,9])[1:4]))}

def ours() -> dict:
    n = segspt_sum([1,3,5,7,9], 1, 3)
    empty = "raised"
    try:
        segspt_sum([], 0, 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"segspt_sum": n, "empty": empty}

def main() -> int:
    rec = {"schema":"spanlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"five-bin window sum 15; empty counts are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["segspt_sum"] != 15 or rec["ours"]["empty"] != "raised":
        raise SystemExit("spanlock show identity failed")
    if rec["theirs"]["sum_1_3"] != 15:
        raise SystemExit("numpy window identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
