#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from kslots import k_empty_slots
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
B,K=[1,3,2],1
def main():
    a,b=[],[]; first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=k_empty_slots(B,K); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=k_empty_slots(B,K); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("gap disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first; second=acc
    if k_empty_slots(B,K)!=2: raise SystemExit("identity")
    try: k_empty_slots([],1)
    except ValueError: pass
    else: raise SystemExit("empty accepted")
    rec={"schema":"gaplock.kslots_bench.v1","seed":SEED,"n_bulbs":3,"k":K,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"gap_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"gap_seconds":a,"repeat_seconds":b,"day_first":first,"day_second":second,"day_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
