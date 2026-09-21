#!/usr/bin/env python3.12
"""Reproducible blossom matching bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from blossom import blossom_match

SEED = 20260919
N = 10
N_EDGES = 12
N_TRIALS = 7
WARMUP = 1


def tape(n: int, n_edges: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    edges: set[tuple[int, int]] = set()
    while len(edges) < n_edges:
        a = rng.randrange(0, n)
        b = rng.randrange(0, n)
        if a == b:
            continue
        if a > b:
            a, b = b, a
        edges.add((a, b))
    return sorted(edges)


def greedy(n: int, edges: list[tuple[int, int]]) -> int:
    used = [False] * n
    acc = 0
    for a, b in edges:
        if not used[a] and not used[b]:
            used[a] = True
            used[b] = True
            acc += 1
    return acc


def main() -> int:
    edges = tape(N, N_EDGES, SEED)
    blossom_times: list[float] = []
    greedy_times: list[float] = []
    first: int | None = None
    second: int | None = None
    greedy_first: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = blossom_match(N, edges)
        bt = time.perf_counter() - t0
        t1 = time.perf_counter()
        gd = greedy(N, edges)
        gt = time.perf_counter() - t1
        if acc < gd:
            raise SystemExit("blossom below greedy")
        if trial < WARMUP:
            continue
        blossom_times.append(bt)
        greedy_times.append(gt)
        if first is None:
            first = acc
            greedy_first = gd
        else:
            second = acc
    if blossom_match(4, [(0, 1), (2, 3)]) != 2:
        raise SystemExit("blossom identity failed")
    try:
        blossom_match(0, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty vertex set accepted")
    record = {
        "schema": "pairlock.blossom_bench.v1",
        "seed": SEED,
        "n": N,
        "n_edges": N_EDGES,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(blossom_times),
        "blossom_seconds_median": statistics.median(blossom_times),
        "greedy_seconds_median": statistics.median(greedy_times),
        "blossom_seconds": blossom_times,
        "greedy_seconds": greedy_times,
        "match_first": first,
        "match_second": second,
        "match_identical": first is not None and first == second,
        "greedy_match": greedy_first,
        "match_ge_greedy": True,
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
