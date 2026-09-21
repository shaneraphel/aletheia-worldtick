#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from aktous import aktous_discard
SEED, N, N_TRIALS, WARMUP = 20260919, 65536, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(0, 64), rng.randrange(0, 64)) for _ in range(n)]

def naive(points):
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    return sum(1 for x, y in points if xmin < x < xmax and ymin < y < ymax)

def main():
    pts = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = aktous_discard(pts); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(pts); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("akl and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if aktous_discard([(0,0),(2,0),(1,1),(0,2),(2,2)]) != 1:
        raise SystemExit("identity")
    try:
        aktous_discard([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "cliplock.aktous_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "aktous_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "aktous_seconds": a, "naive_seconds": b,
        "discard_first": first, "discard_second": second,
        "discard_identical": first == second, "discard_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
