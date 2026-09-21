#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from voronoi import voronoi_unbounded
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(0, n), rng.randrange(0, n)) for _ in range(n)]

def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return len(pts)
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower[:-1] + upper[:-1])

def main():
    pts = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = voronoi_unbounded(pts); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = hull(pts); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("voronoi and hull disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if voronoi_unbounded([(0,0),(2,0),(1,1),(0,2),(2,2)]) != 4:
        raise SystemExit("identity")
    try:
        voronoi_unbounded([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "celllock.voronoi_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "voronoi_seconds_median": statistics.median(a),
        "hull_seconds_median": statistics.median(b),
        "voronoi_seconds": a, "hull_seconds": b,
        "cells_first": first, "cells_second": second,
        "cells_identical": first == second, "cells_equals_hull": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
