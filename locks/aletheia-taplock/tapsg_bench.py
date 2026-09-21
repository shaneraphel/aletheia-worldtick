#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from tapsg import min_taps
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
R=[3,4,1,1,0,0]
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=min_taps(5,R); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=min_taps(5,R); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("tap disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if min_taps(5,R)!=1: raise SystemExit("identity")
    try: min_taps(0,[])
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"taplock.tapsg_bench.v1","seed":SEED,"n":5,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"tap_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"tap_seconds":a,"repeat_seconds":b,"taps_first":first,"taps_second":second,"taps_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
