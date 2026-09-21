#!/usr/bin/env python3.12
"""Reproducible skip-search bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from skiplist import skip_search

SEED = 20260919
N = 65536
N_TRIALS = 7
WARMUP = 1


def tape(n: int, seed: int) -> tuple[list[int], int]:
    rng = random.Random(seed)
    vals = sorted({rng.randrange(0, n * 4) for _ in range(n)})
    while len(vals) < n:
        vals.append(vals[-1] + 1)
    vals = vals[:n]
    target = vals[rng.randrange(0, n)]
    return vals, target


def main() -> int:
    vals, target = tape(N, SEED)
    skip_times: list[float] = []
    index_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = skip_search(vals, target)
        st = time.perf_counter() - t0
        t1 = time.perf_counter()
        ix = vals.index(target)
        it = time.perf_counter() - t1
        if acc != ix:
            raise SystemExit("skip_search and list.index disagree")
        if trial < WARMUP:
            continue
        skip_times.append(st)
        index_times.append(it)
        if first is None:
            first = acc
        else:
            second = acc
    if skip_search([1, 3, 5, 7], 5) != 2:
        raise SystemExit("skip identity failed")
    try:
        skip_search([], 5)
    except ValueError:
        pass
    else:
        raise SystemExit("empty list accepted")
    record = {
        "schema": "skiplock.skip_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(skip_times),
        "skip_seconds_median": statistics.median(skip_times),
        "index_seconds_median": statistics.median(index_times),
        "skip_seconds": skip_times,
        "index_seconds": index_times,
        "index_first": first,
        "index_second": second,
        "index_identical": first is not None and first == second,
        "index_equals_list_index": True,
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
