#!/usr/bin/env python3.12
"""Use NumPy on a spring tape. Record empty force. Refuse here."""
from __future__ import annotations
import json, platform, sys
from hooke import hooke_law

def theirs() -> dict:
    import numpy as np
    return {"package":"numpy","version":np.__version__,"empty_norm":float(np.linalg.norm(np.array([]))),"n_steps":3}

def ours() -> dict:
    n = hooke_law([(3, 0), (4, 1), (2, 0)])
    empty = "raised"
    try:
        hooke_law([])
        empty = "accepted"
    except ValueError:
        pass
    return {"hooke_law": n, "empty": empty}

def main() -> int:
    rec = {"schema":"hookelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"three-step spring occupancy 3; empty tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["hooke_law"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("hookelock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
