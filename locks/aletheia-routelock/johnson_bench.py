#!/usr/bin/env python3.12
"""Reproducible Johnson routing bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import heapq
import json
import platform
import random
import statistics
import sys
import time

from johnson import johnson_dist

SEED = 20260919
N = 64
N_EDGES = 192
N_TRIALS = 7
WARMUP = 1


def tape(n: int, n_edges: int, seed: int) -> list[tuple[int, int, int]]:
    rng = random.Random(seed)
    edges: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    for i in range(n - 1):
        edges.append((i, i + 1, 1))
        seen.add((i, i + 1))
    while len(edges) < n_edges:
        u = rng.randrange(0, n)
        v = rng.randrange(0, n)
        if u == v or (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u, v, rng.randrange(1, 9)))
    return edges


def dijkstra(n: int, edges: list[tuple[int, int, int]], src: int, dst: int) -> int:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [None] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] is not None and d > dist[u]:
            continue
        for v, w in adj[u]:
            cand = d + w
            if dist[v] is None or cand < dist[v]:
                dist[v] = cand
                heapq.heappush(heap, (cand, v))
    if dist[dst] is None:
        raise SystemExit("dijkstra unreachable")
    return dist[dst]


def main() -> int:
    edges = tape(N, N_EDGES, SEED)
    src, dst = 0, N - 1
    johnson_times: list[float] = []
    dijkstra_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = johnson_dist(N, edges, src, dst)
        jt = time.perf_counter() - t0
        t1 = time.perf_counter()
        dj = dijkstra(N, edges, src, dst)
        dt = time.perf_counter() - t1
        if acc != dj:
            raise SystemExit("johnson and dijkstra disagree")
        if trial < WARMUP:
            continue
        johnson_times.append(jt)
        dijkstra_times.append(dt)
        if first is None:
            first = acc
        else:
            second = acc
    if johnson_dist(3, [(0, 1, 1), (1, 2, 1)], 0, 2) != 2:
        raise SystemExit("johnson identity failed")
    try:
        johnson_dist(3, [], 0, 2)
    except ValueError:
        pass
    else:
        raise SystemExit("empty edges accepted")
    record = {
        "schema": "routelock.johnson_bench.v1",
        "seed": SEED,
        "n": N,
        "n_edges": N_EDGES,
        "src": src,
        "dst": dst,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(johnson_times),
        "johnson_seconds_median": statistics.median(johnson_times),
        "dijkstra_seconds_median": statistics.median(dijkstra_times),
        "johnson_seconds": johnson_times,
        "dijkstra_seconds": dijkstra_times,
        "dist_first": first,
        "dist_second": second,
        "dist_identical": first is not None and first == second,
        "dist_equals_dijkstra": True,
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
