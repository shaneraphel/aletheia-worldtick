#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from hopcroft import hopcroft_karp
SEED, N, N_TRIALS, WARMUP = 20260919, 80, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    edges = []
    for u in range(n):
        for v in range(n):
            if rng.randrange(0, 4) == 0:
                edges.append((u, v))
    if not edges:
        edges.append((0, 0))
    return edges

def greedy(n, edges):
    used_l, used_r, m = set(), set(), 0
    for u, v in edges:
        if u not in used_l and v not in used_r:
            used_l.add(u); used_r.add(v); m += 1
    return m

def main():
    edges = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = hopcroft_karp(N, N, edges); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = greedy(N, edges); bt = time.perf_counter()-t1
        if acc < nv:
            raise SystemExit("hopcroft below greedy")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if hopcroft_karp(2, 2, [(0,0),(0,1),(1,1)]) != 2:
        raise SystemExit("identity")
    try:
        hopcroft_karp(2, 2, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "karplock.hopcroft_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "hopcroft_seconds_median": statistics.median(a),
        "greedy_seconds_median": statistics.median(b),
        "hopcroft_seconds": a, "greedy_seconds": b,
        "match_first": first, "match_second": second,
        "match_identical": first == second, "match_ge_greedy": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
