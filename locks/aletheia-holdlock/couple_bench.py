#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from couple import min_swaps_couples
SEED, N, N_TRIALS, WARMUP = 20260919, 64, 7, 1

def tape(n, seed):
    rng=random.Random(seed)
    row=list(range(n))
    rng.shuffle(row)
    return row

def naive(row):
    return min_swaps_couples(list(row))

def main():
    row=tape(N,SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=min_swaps_couples(list(row)); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(row); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("hold disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first
        second=acc
    if min_swaps_couples([0,2,1,3])!=1: raise SystemExit("identity")
    try:
        min_swaps_couples(None)
    except ValueError:
        pass
    else:
        raise SystemExit("none accepted")
    rec={"schema":"holdlock.couple_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"swap_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"swap_seconds":a,"repeat_seconds":b,"swaps_first":first,"swaps_second":second,"swaps_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
