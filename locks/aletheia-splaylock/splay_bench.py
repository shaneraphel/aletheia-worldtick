#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from splay import splay_root
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    return keys

def main():
    keys = tape(N, SEED)
    target = keys[N // 3]
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = splay_root(keys, target); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = keys.index(target); bt = time.perf_counter()-t1
        if acc != target or nv < 0:
            raise SystemExit("splay disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if splay_root([2,1,3], 1) != 1:
        raise SystemExit("identity")
    try:
        splay_root([], 1)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "splaylock.splay_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "splay_seconds_median": statistics.median(a),
        "index_seconds_median": statistics.median(b),
        "splay_seconds": a, "index_seconds": b,
        "root_first": first, "root_second": second,
        "root_identical": first == second, "root_equals_target": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
