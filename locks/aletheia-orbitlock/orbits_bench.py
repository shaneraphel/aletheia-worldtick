#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from orbits import DisjointSet
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def naive(n, pairs):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a,b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    return len({find(i) for i in range(n)})

def main():
    rng = random.Random(SEED)
    pairs = [(rng.randrange(N), rng.randrange(N)) for _ in range(N)]
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); d=DisjointSet(N)
        for u,v in pairs: d.union(u,v)
        acc=d.n_orbits(); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(N,pairs); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("dsu disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    d=DisjointSet(4); d.union(0,1); d.union(2,3)
    if d.n_orbits()!=2: raise SystemExit("identity")
    try:
        DisjointSet(-1)
    except ValueError:
        pass
    else:
        raise SystemExit("neg accepted")
    rec={"schema":"orbitlock.orbits_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"dsu_seconds_median":statistics.median(a),"naive_seconds_median":statistics.median(b),"dsu_seconds":a,"naive_seconds":b,"orbits_first":first,"orbits_second":second,"orbits_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
