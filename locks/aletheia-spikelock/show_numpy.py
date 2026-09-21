#!/usr/bin/env python3.12
"""Use NumPy mean on a spike tape. Record empty samples. Refuse here."""
from __future__ import annotations
import json, platform, sys
from nyqst import nyquist

def theirs() -> dict:
    import numpy as np
    empty = np.mean(np.array([]))
    return {"package":"numpy","version":np.__version__,"empty_mean":None if np.isnan(empty) else float(empty),"n_bins":int(np.array([1,2,3]).size)}

def ours() -> dict:
    n = nyquist([(2,0),(3,1),(1,0)])
    empty = "raised"
    try:
        nyquist([])
        empty = "accepted"
    except ValueError:
        pass
    return {"nyquist": n, "empty": empty}

def main() -> int:
    rec = {"schema":"spikelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"three-bin spike occupancy 3; empty tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["nyquist"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("spikelock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
