#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from kstren import max_k_subarray_strength
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
NUMS=[1,2,3,-1,2]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=max_k_subarray_strength(NUMS,3); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=max_k_subarray_strength(NUMS,3); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("pulse disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if max_k_subarray_strength(NUMS,3)!=22: raise SystemExit("identity")
    try: max_k_subarray_strength([],1)
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"pulselock.kstren_bench.v1","seed":SEED,"n":len(NUMS),"k":3,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"pulse_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"pulse_seconds":a,"repeat_seconds":b,"strength_first":first,"strength_second":second,"strength_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
