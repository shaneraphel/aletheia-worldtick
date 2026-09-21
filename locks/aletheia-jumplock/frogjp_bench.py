#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from frogjp import can_cross
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
STONES=[0,1,3,5,6,8,12,17]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=can_cross(STONES); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=can_cross(STONES); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("jump disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if can_cross(STONES) is not True: raise SystemExit("identity")
    try: can_cross([])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"jumplock.frogjp_bench.v1","seed":SEED,"n_stones":len(STONES),"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"jump_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"jump_seconds":a,"repeat_seconds":b,"cross_first":first,"cross_second":second,"cross_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
