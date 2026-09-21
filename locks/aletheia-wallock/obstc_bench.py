#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from obstc import min_obstacle_removal
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
GRID = [[0,1,1],[1,1,0],[1,1,0]]

def main():
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        g1=[row[:] for row in GRID]; g2=[row[:] for row in GRID]
        t0=time.perf_counter(); acc=min_obstacle_removal(g1); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=min_obstacle_removal(g2); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("wall disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if min_obstacle_removal([row[:] for row in GRID])!=2: raise SystemExit("identity")
    try:
        min_obstacle_removal([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"wallock.obstc_bench.v1","seed":SEED,"n_rows":3,"n_cols":3,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"removal_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"removal_seconds":a,"repeat_seconds":b,"removals_first":first,"removals_second":second,"removals_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
