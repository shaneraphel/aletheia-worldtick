#!/usr/bin/env python3.12
"""Reproducible Aho–Corasick bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import string
import sys
import time

from acauto import aho_hits

SEED = 20260919
N = 65536
N_TRIALS = 7
WARMUP = 1
PATS = ("ab", "bc", "ca", "aa")


def tape(n: int, seed: int) -> str:
    rng = random.Random(seed)
    alphabet = "abc"
    return "".join(rng.choice(alphabet) for _ in range(n))


def count_hits(text: str, pats: tuple[str, ...]) -> int:
    hits = 0
    for i in range(len(text)):
        for p in pats:
            if text.startswith(p, i):
                hits += 1
    return hits


def main() -> int:
    text = tape(N, SEED)
    aho_times: list[float] = []
    count_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = aho_hits(text, list(PATS))
        at = time.perf_counter() - t0
        t1 = time.perf_counter()
        ct = count_hits(text, PATS)
        ctm = time.perf_counter() - t1
        if acc != ct:
            raise SystemExit("aho and count disagree")
        if trial < WARMUP:
            continue
        aho_times.append(at)
        count_times.append(ctm)
        if first is None:
            first = acc
        else:
            second = acc
    if aho_hits("abcabc", ["ab", "bc"]) != 4:
        raise SystemExit("aho identity failed")
    try:
        aho_hits("", ["ab"])
    except ValueError:
        pass
    else:
        raise SystemExit("empty text accepted")
    record = {
        "schema": "needlelock.acauto_bench.v1",
        "seed": SEED,
        "n": N,
        "pats": list(PATS),
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(aho_times),
        "aho_seconds_median": statistics.median(aho_times),
        "count_seconds_median": statistics.median(count_times),
        "aho_seconds": aho_times,
        "count_seconds": count_times,
        "hits_first": first,
        "hits_second": second,
        "hits_identical": first is not None and first == second,
        "hits_equals_count": True,
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
