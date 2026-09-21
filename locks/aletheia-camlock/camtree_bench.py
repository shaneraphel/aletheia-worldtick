#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from camtree import min_camera_cover
SEED, N, N_TRIALS, WARMUP = 20260919, 64, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    # balanced-ish binary tree as nested lists
    def build(i):
        if i >= n:
            return False
        return [i, build(2*i+1), build(2*i+2)]
    return build(0)

def naive(root):
    return min_camera_cover(root)

def main():
    tree = tape(N, SEED)
    a,b=[],[]
    first=second=None
    for trial in range(WARMUP+N_TRIALS):
        t0=time.perf_counter(); acc=min_camera_cover(tree); at=time.perf_counter()-t0
        t1=time.perf_counter(); nv=naive(tree); bt=time.perf_counter()-t1
        if acc!=nv: raise SystemExit("camera disagree")
        if trial<WARMUP: continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if min_camera_cover([0])!=1: raise SystemExit("identity")
    try:
        min_camera_cover(None)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec={"schema":"camlock.camtree_bench.v1","seed":SEED,"n":N,"n_trials":N_TRIALS,"warmup":WARMUP,"n_paired":len(a),"camera_seconds_median":statistics.median(a),"repeat_seconds_median":statistics.median(b),"camera_seconds":a,"repeat_seconds":b,"cover_first":first,"cover_second":second,"cover_identical":first==second,"python":sys.version.split()[0],"platform":platform.platform(),"implementation":platform.python_implementation(),"n_parameters":0,"gradient_descent_steps":0}
    json.dump(rec,sys.stdout,indent=2); sys.stdout.write("\n"); return 0
if __name__=="__main__":
    raise SystemExit(main())
