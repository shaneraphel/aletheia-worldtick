#!/usr/bin/env python3.12
"""Reproducible Runge–Kutta occupancy bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import statistics
import sys
import time

from rkutta import runge_kutta

SEED = 20260919
N_STEPS = 200000
N_TRIALS = 7
WARMUP = 1


def main() -> int:
    steps = [(1, 0)] * N_STEPS
    a_times: list[float] = []
    b_times: list[float] = []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = runge_kutta(steps)
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        ln = len(steps)
        bt = time.perf_counter() - t1
        if acc != ln:
            raise SystemExit("rk and len disagree")
        if trial < WARMUP:
            continue
        a_times.append(at)
        b_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if runge_kutta([(1, 0), (2, 1)]) != 2:
        raise SystemExit("rk identity failed")
    try:
        runge_kutta([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty runge-kutta accepted")
    record = {
        "schema": "steplock.rkutta_bench.v1",
        "seed": SEED,
        "n_steps": N_STEPS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(a_times),
        "rkutta_seconds_median": statistics.median(a_times),
        "len_seconds_median": statistics.median(b_times),
        "rkutta_seconds": a_times,
        "len_seconds": b_times,
        "occupancy_first": first,
        "occupancy_second": second,
        "occupancy_identical": first is not None and first == second,
        "occupancy_equals_len": True,
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
