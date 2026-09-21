#!/usr/bin/env python3.12
"""Reproducible quadtree NE bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from qdtree import qdtree_ne

SEED = 20260919
N = 200000
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(rng.randrange(0, 64), rng.randrange(0, 64)) for _ in range(n)]


def naive(points, cx, cy):
    return sum(1 for x, y in points if x >= cx and y >= cy)


def main() -> int:
    pts = tape(N, SEED)
    cx = cy = 32
    a_times: list[float] = []
    b_times: list[float] = []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = qdtree_ne(pts, cx, cy)
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = naive(pts, cx, cy)
        bt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("quad and naive disagree")
        if trial < WARMUP:
            continue
        a_times.append(at)
        b_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if qdtree_ne([(1, 1), (0, 0)], 1, 1) != 1:
        raise SystemExit("quad identity failed")
    try:
        qdtree_ne([], 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty quadtree accepted")
    record = {
        "schema": "gridlock.qdtree_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(a_times),
        "qdtree_seconds_median": statistics.median(a_times),
        "naive_seconds_median": statistics.median(b_times),
        "qdtree_seconds": a_times,
        "naive_seconds": b_times,
        "ne_first": first,
        "ne_second": second,
        "ne_identical": first is not None and first == second,
        "ne_equals_naive": True,
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
