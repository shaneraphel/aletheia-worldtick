#!/usr/bin/env python3.12
"""Reproducible occupancy-cycle bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from floyd import floyd_cycle

SEED = 20260919
N = 65536
N_TRIALS = 7
WARMUP = 1


def next_tape(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    nxt = [rng.randrange(0, n) for _ in range(n)]
    return nxt


def set_cycle(nxt: list[int]) -> int:
    seen: set[int] = set()
    i = 0
    while i not in seen:
        if i < 0 or i >= len(nxt):
            return 0
        seen.add(i)
        i = nxt[i]
    return 1


def main() -> int:
    nxt = next_tape(N, SEED)
    floyd_times: list[float] = []
    set_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = floyd_cycle(nxt)
        ft = time.perf_counter() - t0
        t1 = time.perf_counter()
        sc = set_cycle(nxt)
        st = time.perf_counter() - t1
        if acc != sc:
            raise SystemExit("floyd and set-walk disagree")
        if trial < WARMUP:
            continue
        floyd_times.append(ft)
        set_times.append(st)
        if first is None:
            first = acc
        else:
            second = acc
    if floyd_cycle([1, 2, 0]) != 1:
        raise SystemExit("floyd identity failed")
    try:
        floyd_cycle([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty next accepted")
    record = {
        "schema": "lanelock.floyd_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(floyd_times),
        "floyd_seconds_median": statistics.median(floyd_times),
        "set_walk_seconds_median": statistics.median(set_times),
        "floyd_seconds": floyd_times,
        "set_walk_seconds": set_times,
        "cycle_first": first,
        "cycle_second": second,
        "cycle_identical": first is not None and first == second,
        "cycle_equals_set_walk": True,
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
