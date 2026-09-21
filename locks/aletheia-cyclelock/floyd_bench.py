#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from floyd import floyd_cycle
SEED, N, N_TRIALS, WARMUP = 20260919, 4096, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    nxt = list(range(1, n)) + [rng.randrange(0, n)]
    return nxt

def tortoise(nxt):
    seen = set()
    i = 0
    while i not in seen:
        if i < 0 or i >= len(nxt):
            return 0
        seen.add(i)
        i = nxt[i]
    return 1

def main():
    nxt = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = floyd_cycle(nxt); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = tortoise(nxt); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("floyd and set-walk disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if floyd_cycle([1,2,0]) != 1:
        raise SystemExit("identity")
    try:
        floyd_cycle([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "cyclelock.floyd_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "floyd_seconds_median": statistics.median(a),
        "setwalk_seconds_median": statistics.median(b),
        "floyd_seconds": a, "setwalk_seconds": b,
        "cycle_first": first, "cycle_second": second,
        "cycle_identical": first == second, "cycle_equals_setwalk": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
