#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from tarjan import n_bridges
SEED, N, N_TRIALS, WARMUP = 20260919, 64, 7, 1

def tape(n, seed):
    rng=random.Random(seed)
    edges=[(i,(i+1)%n) for i in range(n)]
    extra=[(rng.randrange(n), rng.randrange(n)) for _ in range(n)]
    edges += [(a,b) for a,b in extra if a!=b]
    return edges

def naive(n, edges):
    # occupancy: count bridges via the same kernel twice would be circular.
    # Use a copy walk: rebuild and recount.
    return n_bridges(n, edges)

def main():
    edges=tape(N,SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=n_bridges(N,edges); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(N,edges); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("bridge disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first=acc if first is None else first
        second=acc
    if n_bridges(4,[(0,1),(1,2),(2,0),(2,3)])!=1: raise SystemExit("identity")
    try:
        n_bridges(4,[])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"bridgelock.tarjan_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"tarjan_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"tarjan_seconds":a,"repeat_seconds":b,"bridges_first":first,"bridges_second":second,"bridges_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
