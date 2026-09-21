#!/usr/bin/env python3.12
"""Reproducible Householder first-entry bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import math
import platform
import statistics
import sys
import time

from householder import householder_first

SEED = 20260919
N_CALLS = 200000
N_TRIALS = 7
WARMUP = 1


def naive(x: list[int]) -> int:
    n2 = sum(v * v for v in x)
    n = math.isqrt(n2)
    if n * n != n2:
        raise SystemExit("naive non-square")
    sign = 1 if x[0] >= 0 else -1
    return -sign * n


def main() -> int:
    x = [3, 4, 12]
    hh_times: list[float] = []
    naive_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = 0
        for _ in range(N_CALLS):
            acc = householder_first(x)
        ht = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = 0
        for _ in range(N_CALLS):
            nv = naive(x)
        nt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("householder and naive disagree")
        if trial < WARMUP:
            continue
        hh_times.append(ht)
        naive_times.append(nt)
        if first is None:
            first = acc
        else:
            second = acc
    if householder_first([3, 4, 12]) != -13:
        raise SystemExit("householder identity failed")
    try:
        householder_first([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty vector accepted")
    record = {
        "schema": "twistlock.householder_bench.v1",
        "seed": SEED,
        "n_calls": N_CALLS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(hh_times),
        "householder_seconds_median": statistics.median(hh_times),
        "naive_seconds_median": statistics.median(naive_times),
        "householder_seconds": hh_times,
        "naive_seconds": naive_times,
        "first_first": first,
        "first_second": second,
        "first_identical": first is not None and first == second,
        "first_equals_naive": True,
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
