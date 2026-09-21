#!/usr/bin/env python3.12
"""Reproducible Givens hypot bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import math
import platform
import statistics
import sys
import time

from givens import givens_hypot

SEED = 20260919
N_CALLS = 200000
N_TRIALS = 7
WARMUP = 1


def main() -> int:
    v = [3, 4]
    givens_times: list[float] = []
    isqrt_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = 0
        for _ in range(N_CALLS):
            acc = givens_hypot(v)
        gt = time.perf_counter() - t0
        t1 = time.perf_counter()
        br = 0
        for _ in range(N_CALLS):
            br = math.isqrt(v[0] * v[0] + v[1] * v[1])
        it = time.perf_counter() - t1
        if acc != br:
            raise SystemExit("givens and isqrt disagree")
        if trial < WARMUP:
            continue
        givens_times.append(gt)
        isqrt_times.append(it)
        if first is None:
            first = acc
        else:
            second = acc
    if givens_hypot([3, 4]) != 5:
        raise SystemExit("givens identity failed")
    try:
        givens_hypot([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty vector accepted")
    record = {
        "schema": "twistlock.givens_bench.v1",
        "seed": SEED,
        "n_calls": N_CALLS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(givens_times),
        "givens_seconds_median": statistics.median(givens_times),
        "isqrt_seconds_median": statistics.median(isqrt_times),
        "givens_seconds": givens_times,
        "isqrt_seconds": isqrt_times,
        "hypot_first": first,
        "hypot_second": second,
        "hypot_identical": first is not None and first == second,
        "hypot_equals_isqrt": True,
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
