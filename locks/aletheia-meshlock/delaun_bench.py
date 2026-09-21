#!/usr/bin/env python3.12
"""Reproducible Delaunay triangle-count bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from delaun import delaun_tris

SEED = 20260919
N = 256
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(rng.randrange(0, n * 4), rng.randrange(0, n * 4)) for _ in range(n)]


def hull_count(points: list[tuple[int, int]]) -> int:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return len(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return len(lower[:-1] + upper[:-1])


def formula(points: list[tuple[int, int]]) -> int:
    pts = sorted(set(points))
    n = len(pts)
    if n < 3:
        return 0
    h = hull_count(points)
    if h < 3:
        return 0
    return 2 * n - 2 - h


def main() -> int:
    pts = tape(N, SEED)
    a_times: list[float] = []
    b_times: list[float] = []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = delaun_tris(pts)
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = formula(pts)
        bt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("delaunay and formula disagree")
        if trial < WARMUP:
            continue
        a_times.append(at)
        b_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if delaun_tris([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("delaunay identity failed")
    try:
        delaun_tris([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty delaunay accepted")
    record = {
        "schema": "meshlock.delaun_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(a_times),
        "delaun_seconds_median": statistics.median(a_times),
        "formula_seconds_median": statistics.median(b_times),
        "delaun_seconds": a_times,
        "formula_seconds": b_times,
        "tris_first": first,
        "tris_second": second,
        "tris_identical": first is not None and first == second,
        "tris_equals_formula": True,
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
