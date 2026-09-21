#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from treap import treap_root
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    prios = list(range(n))
    rng.shuffle(prios)
    return keys, prios

def maxprio(keys, prios):
    return keys[prios.index(max(prios))]

def main():
    keys, prios = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = treap_root(keys, prios); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = maxprio(keys, prios); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("treap and max-priority disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if treap_root([5,3,8],[2,4,1]) != 3:
        raise SystemExit("identity")
    try:
        treap_root([], [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "treaplock.treap_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "treap_seconds_median": statistics.median(a),
        "maxprio_seconds_median": statistics.median(b),
        "treap_seconds": a, "maxprio_seconds": b,
        "root_first": first, "root_second": second,
        "root_identical": first == second, "root_equals_maxprio": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
