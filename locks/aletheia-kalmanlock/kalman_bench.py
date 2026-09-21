#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from kalman import kalman_filter
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(1, 8), rng.randrange(0, 3)) for _ in range(n)]

def naive(steps):
    if not steps:
        raise ValueError("empty")
    n = 0
    for n_obs, noise in steps:
        if n_obs < 1 or noise < 0:
            raise ValueError("empty")
        n += 1
    return n

def main():
    steps = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = kalman_filter(steps); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(steps); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("kalman and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if kalman_filter([(2,0),(3,1),(1,0)]) != 3:
        raise SystemExit("identity")
    try:
        kalman_filter([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "kalmanlock.kalman_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "kalman_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "kalman_seconds": a, "naive_seconds": b,
        "occ_first": first, "occ_second": second,
        "occ_identical": first == second,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n"); return 0
if __name__ == "__main__":
    raise SystemExit(main())
