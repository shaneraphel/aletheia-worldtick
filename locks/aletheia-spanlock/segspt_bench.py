#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from segspt import segspt_sum
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [rng.randrange(0, 8) for _ in range(n)]

def naive(a, left, right):
    return sum(a[left:right + 1])

def main():
    vals = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = segspt_sum(vals, 16, N - 16); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(vals, 16, N - 16); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("segspt and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if segspt_sum([1,3,5,7,9],1,3) != 15:
        raise SystemExit("identity")
    try:
        segspt_sum([],0,0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "spanlock.segspt_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "segspt_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "segspt_seconds": a, "naive_seconds": b,
        "sum_first": first, "sum_second": second,
        "sum_identical": first == second, "sum_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
