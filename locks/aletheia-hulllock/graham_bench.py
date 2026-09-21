#!/usr/bin/env python3.12
"""Reproducible Graham hull bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from graham import graham_hull

SEED = 20260919
N = 4096
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(rng.randrange(0, n), rng.randrange(0, n)) for _ in range(n)]


def jarvis(points: list[tuple[int, int]]) -> int:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return len(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    start = min(pts)
    hull = [start]
    while True:
        cand = pts[0] if pts[0] != hull[-1] else pts[1]
        for p in pts:
            if p == hull[-1]:
                continue
            cr = cross(hull[-1], cand, p)
            if cr < 0 or (cr == 0 and abs(p[0]-hull[-1][0])+abs(p[1]-hull[-1][1]) > abs(cand[0]-hull[-1][0])+abs(cand[1]-hull[-1][1])):
                cand = p
        if cand == start:
            break
        hull.append(cand)
        if len(hull) > len(pts):
            raise SystemExit("jarvis overflow")
    return len(hull)


def main() -> int:
    pts = tape(N, SEED)
    graham_times: list[float] = []
    jarvis_times: list[float] = []
    first = None
    second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = graham_hull(pts)
        gt = time.perf_counter() - t0
        t1 = time.perf_counter()
        jv = jarvis(pts)
        jt = time.perf_counter() - t1
        if acc != jv:
            raise SystemExit(f"graham and jarvis disagree {acc} {jv}")
        if trial < WARMUP:
            continue
        graham_times.append(gt)
        jarvis_times.append(jt)
        if first is None:
            first = acc
        else:
            second = acc
    if graham_hull([(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]) != 4:
        raise SystemExit("graham identity failed")
    try:
        graham_hull([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty points accepted")
    record = {
        "schema": "hulllock.graham_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(graham_times),
        "graham_seconds_median": statistics.median(graham_times),
        "jarvis_seconds_median": statistics.median(jarvis_times),
        "graham_seconds": graham_times,
        "jarvis_seconds": jarvis_times,
        "hull_first": first,
        "hull_second": second,
        "hull_identical": first is not None and first == second,
        "hull_equals_jarvis": True,
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
