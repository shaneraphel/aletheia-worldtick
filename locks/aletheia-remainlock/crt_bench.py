#!/usr/bin/env python3.12
"""Reproducible CRT-pair bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from crt import crt_pair

SEED = 20260919
N_PAIRS = 2000
N_TRIALS = 7
WARMUP = 1
PAIRS = ((3, 5), (3, 7), (5, 7), (4, 9), (8, 9))


def tape(n: int, seed: int) -> list[tuple[int, int, int, int]]:
    rng = random.Random(seed)
    out: list[tuple[int, int, int, int]] = []
    for _ in range(n):
        m, nmod = rng.choice(PAIRS)
        a = rng.randrange(0, m)
        b = rng.randrange(0, nmod)
        out.append((a, m, b, nmod))
    return out


def brute(a: int, m: int, b: int, n: int) -> int:
    for x in range(m * n):
        if x % m == a % m and x % n == b % n:
            return x
    raise SystemExit("brute miss")


def main() -> int:
    rows = tape(N_PAIRS, SEED)
    crt_times: list[float] = []
    brute_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = 0
        for a, m, b, n in rows:
            acc ^= crt_pair(a, m, b, n)
        ct = time.perf_counter() - t0
        t1 = time.perf_counter()
        br = 0
        for a, m, b, n in rows:
            br ^= brute(a, m, b, n)
        bt = time.perf_counter() - t1
        if acc != br:
            raise SystemExit("crt and brute disagree")
        if trial < WARMUP:
            continue
        crt_times.append(ct)
        brute_times.append(bt)
        if first is None:
            first = acc
        else:
            second = acc
    if crt_pair(2, 3, 3, 5) != 8:
        raise SystemExit("crt identity failed")
    try:
        crt_pair(2, 0, 3, 5)
    except ValueError:
        pass
    else:
        raise SystemExit("non-positive modulus accepted")
    try:
        crt_pair(2, 4, 3, 6)
    except ValueError:
        pass
    else:
        raise SystemExit("non-coprime moduli accepted")
    record = {
        "schema": "remainlock.crt_bench.v1",
        "seed": SEED,
        "n_pairs": N_PAIRS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(crt_times),
        "crt_seconds_median": statistics.median(crt_times),
        "brute_seconds_median": statistics.median(brute_times),
        "crt_seconds": crt_times,
        "brute_seconds": brute_times,
        "xor_first": first,
        "xor_second": second,
        "xor_identical": first is not None and first == second,
        "xor_equals_brute": True,
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
