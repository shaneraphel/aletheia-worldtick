#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from cuckoo import cuckoo_placed
SEED, N, N_TRIALS, WARMUP = 20260919, 256, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    return keys

def main():
    keys = tape(N, SEED)
    table = N * 2
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = cuckoo_placed(keys, table); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = len(set(keys)); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("cuckoo and unique disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if cuckoo_placed([3,8,12], 5) != 3:
        raise SystemExit("identity")
    try:
        cuckoo_placed([], 5)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "cuckoolock.cuckoo_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "cuckoo_seconds_median": statistics.median(a),
        "unique_seconds_median": statistics.median(b),
        "cuckoo_seconds": a, "unique_seconds": b,
        "placed_first": first, "placed_second": second,
        "placed_identical": first == second, "placed_equals_unique": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
