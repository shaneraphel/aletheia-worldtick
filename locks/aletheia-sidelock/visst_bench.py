#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from visst import ways_rearrange_sticks
SEED, N, K, N_TRIALS, WARMUP = 20260919, 8, 4, 7, 1

def main():
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=ways_rearrange_sticks(N,K); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=ways_rearrange_sticks(N,K); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("side disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if ways_rearrange_sticks(3,2)!=3: raise SystemExit("identity")
    try:
        ways_rearrange_sticks(0,1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"sidelock.visst_bench.v1","seed":SEED,"n":N,"k":K,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"ways_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"ways_seconds":a,"repeat_seconds":b,"ways_first":first,"ways_second":second,"ways_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
