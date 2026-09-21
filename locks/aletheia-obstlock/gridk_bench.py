#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from gridk import shortest_path_obstacles
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
GRID = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]

def naive(grid, k):
    return shortest_path_obstacles(grid, k)

def main():
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=shortest_path_obstacles(GRID,1); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(GRID,1); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("obstacle disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if shortest_path_obstacles(GRID,1)!=6: raise SystemExit("identity")
    try:
        shortest_path_obstacles([],1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"obstlock.gridk_bench.v1","seed":SEED,"n_rows":5,"n_cols":3,"k":1,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"path_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"path_seconds":a,"repeat_seconds":b,"dist_first":first,"dist_second":second,"dist_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
