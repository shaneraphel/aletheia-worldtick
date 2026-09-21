#!/usr/bin/env python3.12
"""Reproducible Hungarian assignment bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import itertools
import json
import platform
import random
import statistics
import sys
import time

from hungar import hungar_cost

SEED = 20260919
N = 8
N_TRIALS = 7
WARMUP = 1


def cost_tape(n: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randrange(0, 9) for _ in range(n)] for _ in range(n)]


def brute(cost: list[list[int]]) -> int:
    n = len(cost)
    best = None
    for perm in itertools.permutations(range(n)):
        acc = sum(cost[i][perm[i]] for i in range(n))
        if best is None or acc < best:
            best = acc
    assert best is not None
    return best


def main() -> int:
    cost = cost_tape(N, SEED)
    hungar_times: list[float] = []
    brute_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = hungar_cost(cost)
        ht = time.perf_counter() - t0
        t1 = time.perf_counter()
        br = brute(cost)
        bt = time.perf_counter() - t1
        if acc != br:
            raise SystemExit("hungar and brute disagree")
        if trial < WARMUP:
            continue
        hungar_times.append(ht)
        brute_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if hungar_cost([[1, 2], [2, 1]]) != 2:
        raise SystemExit("hungar identity failed")
    try:
        hungar_cost([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty cost accepted")
    record = {
        "schema": "handlock.hungar_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(hungar_times),
        "hungar_seconds_median": statistics.median(hungar_times),
        "brute_seconds_median": statistics.median(brute_times),
        "hungar_seconds": hungar_times,
        "brute_seconds": brute_times,
        "cost_first": first,
        "cost_second": second,
        "cost_identical": first is not None and first == second,
        "cost_equals_brute": True,
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
