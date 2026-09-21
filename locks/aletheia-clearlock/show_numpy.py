#!/usr/bin/env python3.12
"""Use NumPy on a disk rim. Record empty field. Refuse here."""
from __future__ import annotations
import json, platform, sys
from sdfocc import signed_distance_occupancy, disk_clearance2

def theirs() -> dict:
    import numpy as np
    empty=float(np.linalg.norm(np.array([])))
    rim=int(3*3+0*0-3*3)
    return {"package":"numpy","version":np.__version__,"empty_norm":empty,"rim_clearance2":rim}

def ours() -> dict:
    n=signed_distance_occupancy([(3,0),(4,1),(2,0)])
    c=disk_clearance2(3,0,0,0,3)
    empty="raised"
    try:
        signed_distance_occupancy([])
        empty="accepted"
    except ValueError:
        pass
    return {"signed_distance_occupancy": n, "disk_clearance2": c, "empty": empty}

def main() -> int:
    rec={"schema":"clearlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"three-step sdf occupancy 3 and rim clearance 0; empty field is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["signed_distance_occupancy"]!=3 or rec["ours"]["disk_clearance2"]!=0 or rec["ours"]["empty"]!="raised":
        raise SystemExit("clearlock show identity failed")
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
