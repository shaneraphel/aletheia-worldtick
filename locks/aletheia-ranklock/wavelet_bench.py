#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from wavelet import wavelet_rank
SEED, N, N_TRIALS, WARMUP = 20260919, 200000, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [rng.randrange(0, 8) for _ in range(n)]

def naive(seq, symbol, i):
    return sum(1 for x in seq[:i] if x == symbol)

def main():
    seq = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = wavelet_rank(seq, 3, N); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(seq, 3, N); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("wavelet and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if wavelet_rank([1,2,1,3,1],1,5) != 3:
        raise SystemExit("identity")
    try:
        wavelet_rank([],1,0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "ranklock.wavelet_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "wavelet_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "wavelet_seconds": a, "naive_seconds": b,
        "rank_first": first, "rank_second": second,
        "rank_identical": first == second, "rank_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
