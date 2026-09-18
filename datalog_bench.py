#!/usr/bin/env python3.12
"""Reproducible fact-reachability bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time
from collections import deque

from datalog import datalog_fixpoint

SEED = 20260919
N_NODES = 256
N_FACTS = 8
N_EDGES = 512
N_TRIALS = 7
WARMUP = 1


def world(n: int, n_facts: int, n_edges: int, seed: int) -> tuple[list[int], list[tuple[int, int]]]:
    rng = random.Random(seed)
    facts = sorted(rng.sample(range(n), n_facts))
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    while len(edges) < n_edges:
        u = rng.randrange(0, n)
        v = rng.randrange(0, n)
        if u == v or (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u, v))
    return facts, edges


def bfs_reach(n: int, facts: list[int], edges: list[tuple[int, int]]) -> int:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    q = deque(facts)
    seen = [False] * n
    for f in facts:
        seen[f] = True
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                q.append(v)
    return sum(1 for x in seen if x)


def main() -> int:
    facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
    dl_times: list[float] = []
    bfs_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = datalog_fixpoint(N_NODES, facts, edges)
        dt = time.perf_counter() - t0
        t1 = time.perf_counter()
        bf = bfs_reach(N_NODES, facts, edges)
        bt = time.perf_counter() - t1
        if acc != bf:
            raise SystemExit("datalog and bfs reach disagree")
        if trial < WARMUP:
            continue
        dl_times.append(dt)
        bfs_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if datalog_fixpoint(3, [0], [(0, 1), (1, 2)]) != 3:
        raise SystemExit("datalog identity failed")
    try:
        datalog_fixpoint(3, [], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("empty facts accepted")
    try:
        datalog_fixpoint(-1, [0], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("negative n accepted")
    record = {
        "schema": "worldtick.datalog_bench.v1",
        "seed": SEED,
        "n_nodes": N_NODES,
        "n_facts": N_FACTS,
        "n_edges": N_EDGES,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(dl_times),
        "datalog_seconds_median": statistics.median(dl_times),
        "bfs_seconds_median": statistics.median(bfs_times),
        "datalog_seconds": dl_times,
        "bfs_seconds": bfs_times,
        "reach_first": first,
        "reach_second": second,
        "reach_identical": first is not None and first == second,
        "reach_equals_bfs": True,
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
