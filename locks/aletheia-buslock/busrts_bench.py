#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from busrts import num_buses
SEED, N, N_TRIALS, WARMUP = 20260919, 8, 7, 1

def tape(n, seed):
    rng=random.Random(seed)
    routes=[]
    for i in range(n):
        a=rng.randrange(n)
        b=rng.randrange(n)
        routes.append(sorted({a,b,i}))
    return routes

def naive(routes,s,t):
    return num_buses(routes,s,t)

def main():
    routes=tape(N,SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=num_buses(routes,0,N-1); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(routes,0,N-1); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("bus disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first
        second=acc
    if num_buses([[1,2,7],[3,6,7]],1,6)!=2: raise SystemExit("identity")
    try:
        num_buses(None,1,6)
    except ValueError:
        pass
    else:
        raise SystemExit("none accepted")
    rec={"schema":"buslock.busrts_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"bus_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"bus_seconds":a,"repeat_seconds":b,"hops_first":first,"hops_second":second,"hops_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
