#!/usr/bin/env python3.12
"""Reproducible sample-occupancy bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from nyqst import nyquist

SEED = 20260919
N_STEPS = 200000
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    return [(rng.randrange(1, 9), rng.randrange(0, 4)) for _ in range(n)]


def main() -> int:
    steps = tape(N_STEPS, SEED)
    nyq_times: list[float] = []
    len_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = nyquist(steps)
        nt = time.perf_counter() - t0
        t1 = time.perf_counter()
        ln = len(steps)
        lt = time.perf_counter() - t1
        if acc != ln:
            raise SystemExit("nyquist occupancy and len disagree")
        if trial < WARMUP:
            continue
        nyq_times.append(nt)
        len_times.append(lt)
        if first is None:
            first = acc
        else:
            second = acc
    if nyquist([(4, 0), (4, 1), (2, 0)]) != 3:
        raise SystemExit("nyquist identity failed")
    try:
        nyquist([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty tape accepted")
    try:
        nyquist([(0, 0)])
    except ValueError:
        pass
    else:
        raise SystemExit("nonpositive sample count accepted")
    try:
        nyquist([(1, -1)])
    except ValueError:
        pass
    else:
        raise SystemExit("negative rate accepted")
    record = {
        "schema": "spikelock.nyquist_bench.v1",
        "seed": SEED,
        "n_steps": N_STEPS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(nyq_times),
        "nyquist_seconds_median": statistics.median(nyq_times),
        "len_seconds_median": statistics.median(len_times),
        "nyquist_seconds": nyq_times,
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
