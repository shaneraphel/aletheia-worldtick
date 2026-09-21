#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from lipath import longest_increasing_path
SEED, N, N_TRIALS, WARMUP = 20260919, 8, 7, 1

def tape(n, seed):
    rng=random.Random(seed)
    return [[rng.randrange(20) for _ in range(n)] for _ in range(n)]

def naive(m):
    return longest_increasing_path(m)

def main():
    m=tape(N,SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=longest_increasing_path(m); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(m); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("climb disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first
        second=acc
    if longest_increasing_path([[9,9,4],[6,6,8],[2,1,1]])!=4: raise SystemExit("identity")
    try:
        longest_increasing_path([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"climblock.lipath_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"climb_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"climb_seconds":a,"repeat_seconds":b,"path_first":first,"path_second":second,"path_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
