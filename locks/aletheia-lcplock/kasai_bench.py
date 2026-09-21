#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from kasai import kasai_lcp_at
SEED, N, N_TRIALS, WARMUP = 20260919, 1024, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return "".join(rng.choice("acgt") for _ in range(n))

def sa_of(text):
    return sorted(range(len(text)), key=lambda i: text[i:])

def naive(text, sa, i):
    a, b = sa[i], sa[i - 1]
    h = 0
    n = len(text)
    while a + h < n and b + h < n and text[a + h] == text[b + h]:
        h += 1
    return h

def main():
    text = tape(N, SEED)
    sa = sa_of(text)
    idx = N // 3
    if idx < 1:
        idx = 1
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = kasai_lcp_at(text, sa, idx); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(text, sa, idx); bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("kasai and naive disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if kasai_lcp_at("banana",[5,3,1,0,4,2],2) != 3:
        raise SystemExit("identity")
    try:
        kasai_lcp_at("",[5],0)
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "lcplock.kasai_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "kasai_seconds_median": statistics.median(a),
        "naive_seconds_median": statistics.median(b),
        "kasai_seconds": a, "naive_seconds": b,
        "lcp_first": first, "lcp_second": second,
        "lcp_identical": first == second, "lcp_equals_naive": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
