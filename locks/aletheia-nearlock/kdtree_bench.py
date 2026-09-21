#!/usr/bin/env python3.12
"""Reproducible nearest-x bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from kdtree import kdtree_near

SEED = 20260919
N = 65536
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int):
    rng = random.Random(seed)
    pts = [(rng.randrange(0, n), rng.randrange(0, n)) for _ in range(n)]
    qx, qy = rng.randrange(0, n), rng.randrange(0, n)
    return pts, qx, qy


def naive(points, qx, qy):
    best = points[0]
    best_d = (best[0] - qx) ** 2 + (best[1] - qy) ** 2
    for p in points[1:]:
        d = (p[0] - qx) ** 2 + (p[1] - qy) ** 2
        if d < best_d:
            best = p
            best_d = d
    return best[0]


def main() -> int:
    pts, qx, qy = tape(N, SEED)
    a_times: list[float] = []
    b_times: list[float] = []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = kdtree_near(pts, qx, qy)
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = naive(pts, qx, qy)
        bt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("kd and naive disagree")
        if trial < WARMUP:
            continue
        a_times.append(at)
        b_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if kdtree_near([(0, 0), (3, 4)], 3, 4) != 3:
        raise SystemExit("kd identity failed")
    try:
        kdtree_near([], 0, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty kd-tree accepted")
    record = {
        "schema": "nearlock.kdtree_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(a_times),
        "kdtree_seconds_median": statistics.median(a_times),
        "naive_seconds_median": statistics.median(b_times),
        "kdtree_seconds": a_times,
        "naive_seconds": b_times,
        "x_first": first,
        "x_second": second,
        "x_identical": first is not None and first == second,
        "x_equals_naive": True,
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
