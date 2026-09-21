#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from bloom import bloom_maybe
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    return keys

def main():
    keys = tape(N, SEED)
    q = keys[N // 3]
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = bloom_maybe(keys, 1 << 14, 3, q); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = 1 if q in set(keys) else 0; bt = time.perf_counter()-t1
        if acc != 1 or nv != 1:
            raise SystemExit("present key not maybe-1")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if bloom_maybe([1,2,3],16,2,2) != 1:
        raise SystemExit("identity")
    try:
        bloom_maybe([],16,2,2)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "bloomlock.bloom_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "bloom_seconds_median": statistics.median(a),
        "set_seconds_median": statistics.median(b),
        "bloom_seconds": a, "set_seconds": b,
        "maybe_first": first, "maybe_second": second,
        "maybe_identical": first == second, "present_is_one": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
