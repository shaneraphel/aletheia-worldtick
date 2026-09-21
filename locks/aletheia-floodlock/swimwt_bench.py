#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from swimwt import swim_rising
SEED, N, N_TRIALS, WARMUP = 20260919, 6, 7, 1

def tape(n, seed):
    rng=random.Random(seed)
    g=[[rng.randrange(20) for _ in range(n)] for _ in range(n)]
    g[0][0]=0
    return g

def naive(g):
    return swim_rising(g)

def main():
    g=tape(N,SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=swim_rising(g); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(g); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("flood disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first
        second=acc
    if swim_rising([[0,2],[1,3]])!=3: raise SystemExit("identity")
    try:
        swim_rising([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"floodlock.swimwt_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"swim_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"swim_seconds":a,"repeat_seconds":b,"t_first":first,"t_second":second,"t_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
