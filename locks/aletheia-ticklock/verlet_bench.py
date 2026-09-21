#!/usr/bin/env python3.12
"""Reproducible Verlet occupancy bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import statistics
import sys
import time

from verlet import verlet_integration

SEED = 20260919
N_STEPS = 200000
N_TRIALS = 7
WARMUP = 1


def main() -> int:
    steps = [(1, 0)] * N_STEPS
    verlet_times: list[float] = []
    len_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = verlet_integration(steps)
        vt = time.perf_counter() - t0
        t1 = time.perf_counter()
        ln = len(steps)
        lt = time.perf_counter() - t1
        if acc != ln:
            raise SystemExit("verlet and len disagree")
        if trial < WARMUP:
            continue
        verlet_times.append(vt)
        len_times.append(lt)
        if first is None:
            first = acc
        else:
            second = acc
    if verlet_integration([(1, 0), (2, 1)]) != 2:
        raise SystemExit("verlet identity failed")
    try:
        verlet_integration([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty steps accepted")
    record = {
        "schema": "ticklock.verlet_bench.v1",
        "seed": SEED,
        "n_steps": N_STEPS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(verlet_times),
        "verlet_seconds_median": statistics.median(verlet_times),
        "len_seconds_median": statistics.median(len_times),
        "verlet_seconds": verlet_times,
        "len_seconds": len_times,
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
