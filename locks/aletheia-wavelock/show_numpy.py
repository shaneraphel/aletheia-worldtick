#!/usr/bin/env python3.12
"""Use NumPy count on a sample tape. Record empty count. Refuse empty tape."""
from __future__ import annotations
import json, platform, sys
from wavelet import wavelet_rank

def theirs() -> dict:
    import numpy as np
    empty = int(np.count_nonzero(np.array([]) == 1))
    seq = np.array([1,2,1,3,1])
    return {"package":"numpy","version":np.__version__,"empty_count":empty,"rank_1": int(np.count_nonzero(seq == 1))}

def ours() -> dict:
    n = wavelet_rank([1, 2, 1, 3, 1], 1, 5)
    empty = "raised"
    try:
        wavelet_rank([], 1, 0)
        empty = "accepted"
    except ValueError:
        pass
    return {"wavelet_rank": n, "empty": empty}

def main() -> int:
    rec = {"schema":"wavelock.show_numpy.v1","used":"https://github.com/numpy/numpy","built":"prefix rank 3; empty sample tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["wavelet_rank"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("wavelock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
