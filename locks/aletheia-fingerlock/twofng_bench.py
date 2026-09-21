#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from twofng import minimum_distance
SEED, N, N_TRIALS, WARMUP = 20260919, 8, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return "".join(chr(65 + rng.randrange(26)) for _ in range(n))

def naive(word):
    return minimum_distance(word)

def main():
    word = tape(N, SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=minimum_distance(word); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(word); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("finger disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if minimum_distance("CAKE")!=3: raise SystemExit("identity")
    try:
        minimum_distance("")
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"fingerlock.twofng_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"finger_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"finger_seconds":a,"repeat_seconds":b,"dist_first":first,"dist_second":second,"dist_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
