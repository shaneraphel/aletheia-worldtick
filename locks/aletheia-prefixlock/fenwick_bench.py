#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from fenwick import fenwick_prefix
SEED, N, N_TRIALS, WARMUP = 20260919, 65536, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [rng.randrange(0, 8) for _ in range(n)]

def naive(vals, i):
    return sum(vals[: i + 1])

def main():
    vals = tape(N, SEED)
    idx = N - 1
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = fenwick_prefix(vals, idx); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(vals, idx); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("fenwick and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if fenwick_prefix([1,2,3,4], 3) != 10:
        raise SystemExit("identity")
    try:
        fenwick_prefix([], 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "prefixlock.fenwick_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "fenwick_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "fenwick_seconds": a, "naive_seconds": b,
        "prefix_first": first, "prefix_second": second,
        "prefix_identical": first == second, "prefix_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
