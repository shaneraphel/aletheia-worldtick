#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from intervaltree import interval_tree_overlap
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    iv = []
    for _ in range(n):
        a = rng.randrange(0, 64)
        b = a + rng.randrange(1, 8)
        iv.append((a, b))
    return iv, 32

def naive(intervals, point):
    if not intervals:
        raise ValueError("empty")
    return sum(1 for a,b in intervals if a <= point < b)

def main():
    iv, pt = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = interval_tree_overlap(iv, pt); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(iv, pt); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("overlap and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if interval_tree_overlap([(0,4),(2,6)], 3) != 2:
        raise SystemExit("identity")
    try:
        interval_tree_overlap([], 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "slotlock.interval_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "overlap_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "overlap_seconds": a, "naive_seconds": b,
        "count_first": first, "count_second": second,
        "count_identical": first == second,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
