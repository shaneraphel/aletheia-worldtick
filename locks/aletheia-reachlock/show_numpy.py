#!/usr/bin/env python3.12
"""Use NumPy on a two-link reach. Record empty field. Refuse unreachable."""
from __future__ import annotations
import json, platform, sys
from reach import two_link_ik
from sdfocc import disk_clearance2

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"reach_2_0":float(np.hypot(2.0,0.0))}

def ours() -> dict:
    pose = two_link_ik(2.0, 0.0, 1.0, 1.0)
    empty = "raised"
    try:
        two_link_ik(3.0, 0.0, 1.0, 1.0)
        empty = "accepted"
    except ValueError:
        pass
    return {"two_link_ik": [pose[0], pose[1]], "disk_clearance2": disk_clearance2(3,0,0,0,3), "unreachable": empty}

def main() -> int:
    rec = {"schema":"reachlock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"two-link reach (2,0) and rim clearance 0; unreachable pose is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["unreachable"] != "raised" or rec["ours"]["disk_clearance2"] != 0:
        raise SystemExit("reachlock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
