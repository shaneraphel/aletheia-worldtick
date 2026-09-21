#!/usr/bin/env python3.12
"""Reproducible planning-layer bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time
from collections import deque

from kahn import kahn_layers

SEED = 20260919
N_NODES = 256
N_EDGES = 512
N_TRIALS = 7
WARMUP = 1


def dag(n: int, n_edges: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    while len(edges) < n_edges:
        u = rng.randrange(0, n - 1)
        v = rng.randrange(u + 1, n)
        if (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u, v))
    return edges


def bfs_layers(n: int, edges: list[tuple[int, int]]) -> int:
    indeg = [0] * n
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    n_layers = 0
    seen = 0
    while q:
        n_layers += 1
        nxt: deque[int] = deque()
        for _ in range(len(q)):
            u = q.popleft()
            seen += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        q = nxt
    if seen != n:
        return 0
    return n_layers


def main() -> int:
    edges = dag(N_NODES, N_EDGES, SEED)
    kahn_times: list[float] = []
    bfs_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = kahn_layers(N_NODES, edges)
        kt = time.perf_counter() - t0
        t1 = time.perf_counter()
        bf = bfs_layers(N_NODES, edges)
        bt = time.perf_counter() - t1
        if acc != bf:
            raise SystemExit("kahn and bfs layers disagree")
        if trial < WARMUP:
            continue
        kahn_times.append(kt)
        bfs_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if kahn_layers(3, [(0, 1), (1, 2)]) != 3:
        raise SystemExit("kahn identity failed")
    try:
        kahn_layers(-1, [])
    except ValueError:
        pass
    else:
        raise SystemExit("negative n accepted")
    record = {
        "schema": "lanelock.kahn_bench.v1",
        "seed": SEED,
        "n_nodes": N_NODES,
        "n_edges": N_EDGES,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(kahn_times),
        "kahn_seconds_median": statistics.median(kahn_times),
        "bfs_seconds_median": statistics.median(bfs_times),
        "kahn_seconds": kahn_times,
        "bfs_seconds": bfs_times,
        "layers_first": first,
        "layers_second": second,
        "layers_identical": first is not None and first == second,
        "layers_equals_bfs": True,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    json.dump(record, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
