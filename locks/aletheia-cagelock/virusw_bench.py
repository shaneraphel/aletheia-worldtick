#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, statistics, sys, time
from virusw import contain_virus
SEED, N_TRIALS, WARMUP = 20260919, 7, 1
GRID = [[0,1,0,0,0,0,0,1],[0,1,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]]

def main():
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        g1=[row[:] for row in GRID]; g2=[row[:] for row in GRID]
        t0=time.perf_counter(); acc=contain_virus(g1); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=contain_virus(g2); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("cage disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if contain_virus([row[:] for row in GRID])!=10: raise SystemExit("identity")
    try:
        contain_virus([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"cagelock.virusw_bench.v1","seed":SEED,"n_rows":4,"n_cols":8,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"walls_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"walls_seconds":a,"repeat_seconds":b,"walls_first":first,"walls_second":second,"walls_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
