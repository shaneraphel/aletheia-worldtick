#!/usr/bin/env python3.12
"""Use NumPy on a Verlet tape. Record empty steps. Refuse here."""
from __future__ import annotations
import json, platform, sys
from verlet import verlet_integration

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([])))}

def ours() -> dict:
    n = verlet_integration([(1,0),(2,1)])
    empty = "raised"
    try:
        verlet_integration([])
        empty = "accepted"
    except ValueError:
        pass
    return {"verlet_integration": n, "empty": empty}

def main() -> int:
    rec = {"schema":"ticklock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"two-row Verlet occupancy 2; empty steps are absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["verlet_integration"] != 2 or rec["ours"]["empty"] != "raised":
        raise SystemExit("ticklock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
