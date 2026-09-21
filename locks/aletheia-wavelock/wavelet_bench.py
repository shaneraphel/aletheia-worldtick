#!/usr/bin/env python3.12
"""Reproducible prefix-rank bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from wavelet import wavelet_rank

SEED = 20260919
N = 65536
SYMBOL = 1
N_TRIALS = 7
WARMUP = 1


def seq(n: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randrange(0, 4) for _ in range(n)]


def main() -> int:
    vals = seq(N, SEED)
    i = N
    wt_times: list[float] = []
    count_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = wavelet_rank(vals, SYMBOL, i)
        wt = time.perf_counter() - t0
        t1 = time.perf_counter()
        c = vals[:i].count(SYMBOL)
        ct = time.perf_counter() - t1
        if acc != c:
            raise SystemExit("wavelet_rank and count disagree")
        if trial < WARMUP:
            continue
        wt_times.append(wt)
        count_times.append(ct)
        if first is None:
            first = acc
        else:
            second = acc
    if wavelet_rank([1, 2, 1, 3, 1], 1, 5) != 3:
        raise SystemExit("wavelet identity failed")
    try:
        wavelet_rank([], 1, 0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty sequence accepted")
    record = {
        "schema": "wavelock.wavelet_bench.v1",
        "seed": SEED,
        "n": N,
        "symbol": SYMBOL,
        "index": i,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(wt_times),
        "wavelet_seconds_median": statistics.median(wt_times),
        "count_seconds_median": statistics.median(count_times),
        "wavelet_seconds": wt_times,
        "count_seconds": count_times,
        "rank_first": first,
        "rank_second": second,
        "rank_identical": first is not None and first == second,
        "rank_equals_count": True,
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
