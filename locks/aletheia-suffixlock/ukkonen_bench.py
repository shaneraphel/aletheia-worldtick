#!/usr/bin/env python3.12
"""Reproducible suffix-link bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import string
import sys
import time

from ukkonen import n_suffix_links

SEED = 20260919
N = 4096
N_TRIALS = 7
WARMUP = 1
ALPHABET = string.ascii_lowercase[:8]


def text(n: int, seed: int) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice(ALPHABET) for _ in range(n))


def n_unique_suffixes(s: str) -> int:
    return len({s[i:] for i in range(len(s))})


def main() -> int:
    s = text(N, SEED)
    uk_times: list[float] = []
    suf_times: list[float] = []
    first: int | None = None
    second: int | None = None
    n_suf = 0
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = n_suffix_links(s)
        ut = time.perf_counter() - t0
        t1 = time.perf_counter()
        n_suf = n_unique_suffixes(s)
        st = time.perf_counter() - t1
        if trial < WARMUP:
            continue
        uk_times.append(ut)
        suf_times.append(st)
        if first is None:
            first = acc
        else:
            second = acc
    if n_suffix_links("aba") != 3:
        raise SystemExit("ukkonen identity failed")
    try:
        n_suffix_links("")
    except ValueError:
        pass
    else:
        raise SystemExit("empty text accepted")
    record = {
        "schema": "suffixlock.ukkonen_bench.v1",
        "seed": SEED,
        "n": N,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(uk_times),
        "ukkonen_seconds_median": statistics.median(uk_times),
        "unique_suffix_seconds_median": statistics.median(suf_times),
        "ukkonen_seconds": uk_times,
        "unique_suffix_seconds": suf_times,
        "n_links_first": first,
        "n_links_second": second,
        "n_links_identical": first is not None and first == second,
        "n_unique_suffixes": n_suf,
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
