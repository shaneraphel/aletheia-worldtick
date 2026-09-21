#!/usr/bin/env python3.12
"""Reproducible Fortune vertex bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from fortun import fortun_verts

SEED = 20260919
N = 24
N_TRIALS = 7
WARMUP = 1


def tape(n, seed):
    rng = random.Random(seed)
    return [(rng.randrange(0, 64), rng.randrange(0, 64)) for _ in range(n)]


def main() -> int:
    pts = tape(N, SEED)
    times = []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = fortun_verts(pts)
        dt = time.perf_counter() - t0
        if trial < WARMUP:
            continue
        times.append(dt)
        if first is None:
            first = acc
        else:
            second = acc
            if second != first:
                raise SystemExit("fortune mismatch")
    if fortun_verts([(0, 0), (2, 0), (1, 2)]) != 1:
        raise SystemExit("fortune identity failed")
    try:
        fortun_verts([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty fortune accepted")
    # paired twice identity
    twice = fortun_verts(pts)
    record = {
        "schema": "sitelock.fortun_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(times),
        "fortun_seconds_median": statistics.median(times),
        "fortun_seconds": times,
        "verts_first": first,
        "verts_second": second,
        "verts_identical": first == second == twice,
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
