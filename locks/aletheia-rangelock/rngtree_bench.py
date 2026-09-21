#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from rngtree import rngtree_count
SEED, N, N_TRIALS, WARMUP = 20260919, 200000, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(0, 64), rng.randrange(0, 64)) for _ in range(n)]

def naive(points, x1, x2, y1, y2):
    return sum(1 for x, y in points if x1 <= x <= x2 and y1 <= y <= y2)

def main():
    pts = tape(N, SEED)
    box = (16, 48, 16, 48)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = rngtree_count(pts, *box); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(pts, *box); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("range and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if rngtree_count([(0,0),(1,1),(3,3)], 0, 2, 0, 2) != 2:
        raise SystemExit("identity")
    try:
        rngtree_count([], 0, 1, 0, 1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "rangelock.rngtree_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "rngtree_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "rngtree_seconds": a, "naive_seconds": b,
        "count_first": first, "count_second": second,
        "count_identical": first == second, "count_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
