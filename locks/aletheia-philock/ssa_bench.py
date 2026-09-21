#!/usr/bin/env python3.12
"""Reproducible SSA-phi bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from ssa import ssa_phi_count

SEED = 20260919
N = 512
N_TRIALS = 7
WARMUP = 1


def cfg(n: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    preds: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        preds[v].append(v - 1)
        if rng.random() < 0.25:
            preds[v].append(rng.randrange(0, v))
    return preds


def naive_phi(preds: list[list[int]]) -> int:
    return sum(1 for incoming in preds if len(incoming) >= 2)


def main() -> int:
    preds = cfg(N, SEED)
    ssa_times: list[float] = []
    naive_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = ssa_phi_count(N, preds)
        st = time.perf_counter() - t0
        t1 = time.perf_counter()
        nv = naive_phi(preds)
        nt = time.perf_counter() - t1
        if acc != nv:
            raise SystemExit("ssa_phi_count and naive disagree")
        if trial < WARMUP:
            continue
        ssa_times.append(st)
        naive_times.append(nt)
        if first is None:
            first = acc
        else:
            second = acc
    if ssa_phi_count(3, [[], [], [0, 1]]) != 1:
        raise SystemExit("ssa identity failed")
    try:
        ssa_phi_count(0, [])
    except ValueError:
        pass
    else:
        raise SystemExit("empty cfg accepted")
    record = {
        "schema": "philock.ssa_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(ssa_times),
        "ssa_seconds_median": statistics.median(ssa_times),
        "naive_seconds_median": statistics.median(naive_times),
        "ssa_seconds": ssa_times,
        "naive_seconds": naive_times,
        "n_phi_first": first,
        "n_phi_second": second,
        "n_phi_identical": first is not None and first == second,
        "n_phi_equals_naive": True,
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
