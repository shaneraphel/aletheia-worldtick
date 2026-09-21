#!/usr/bin/env python3.12
"""Use FilterPy on an observation tape. Record empty update. Refuse here."""
from __future__ import annotations
import json, platform, sys
from kalman import kalman_filter

def theirs() -> dict:
    from filterpy.kalman import KalmanFilter
    kf = KalmanFilter(dim_x=1, dim_z=1)
    empty = "accepted"
    try:
        kf.update(None)
    except Exception as exc:
        empty = f"{type(exc).__name__}: {exc}"
    return {"package": "filterpy", "version": "1.4.5", "update_none": empty, "x0": float(kf.x.reshape(-1)[0])}

def ours() -> dict:
    n = kalman_filter([(2, 0), (3, 1), (1, 0)])
    empty = "raised"
    try:
        kalman_filter([])
        empty = "accepted"
    except ValueError:
        pass
    return {"kalman_filter": n, "empty": empty}

def main() -> int:
    rec = {"schema":"kalmanlock.show_filterpy.v1","used":"https://github.com/rlabbe/filterpy","built":"three-step observation occupancy 3; empty tape is absence","theirs":theirs(),"ours":ours(),"python":sys.version.split()[0],"platform":platform.platform(),"n_parameters":0,"gradient_descent_steps":0}
    if rec["ours"]["kalman_filter"] != 3 or rec["ours"]["empty"] != "raised":
        raise SystemExit("kalmanlock show identity failed")
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
