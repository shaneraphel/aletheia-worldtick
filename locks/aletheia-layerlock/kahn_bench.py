#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from kahn import kahn_layers
SEED, N, N_TRIALS, WARMUP = 20260919, 256, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    edges = [(i, i + 1) for i in range(n - 1)]
    extra = [(rng.randrange(0, n - 1), rng.randrange(i + 1, n)) for i in range(n // 8)]
    return edges + extra

def naive_layers(n, edges):
    indeg = [0] * n
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    layer = [i for i in range(n) if indeg[i] == 0]
    n_layers = 0
    seen = 0
    while layer:
        n_layers += 1
        seen += len(layer)
        nxt = []
        for u in layer:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        layer = nxt
    return 0 if seen != n else n_layers

def main():
    edges = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = kahn_layers(N, edges); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive_layers(N, edges); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("kahn and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if kahn_layers(3, [(0,1),(1,2)]) != 3:
        raise SystemExit("identity")
    try:
        kahn_layers(-1, [])
    except ValueError:
        pass
    else:
        raise SystemExit("negative accepted")
    rec = {
        "schema": "layerlock.kahn_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "kahn_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "kahn_seconds": a, "naive_seconds": b,
        "layers_first": first, "layers_second": second,
        "layers_identical": first == second, "layers_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
