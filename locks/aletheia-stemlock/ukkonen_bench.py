#!/usr/bin/env python3.12
from __future__ import annotations
import json, platform, random, statistics, sys, time
from ukkonen import n_suffix_links
SEED, N, N_TRIALS, WARMUP = 20260919, 2048, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    return "".join(rng.choice("acgt") for _ in range(n))

def naive(text):
    return len(text)

def main():
    text = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter(); acc = n_suffix_links(text); at = time.perf_counter()-t0
        t1 = time.perf_counter(); nv = naive(text); bt = time.perf_counter()-t1
        if acc < 1 or nv != N:
            raise SystemExit("ukkonen occupancy missing")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = acc if first is None else first
        second = acc
    if n_suffix_links("aba") != 3:
        raise SystemExit("identity")
    try:
        n_suffix_links("")
    except ValueError:
        pass
    else:
        raise SystemExit("empty accepted")
    rec = {
        "schema": "stemlock.ukkonen_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "ukkonen_seconds_median": statistics.median(a),
        "len_seconds_median": statistics.median(b),
        "ukkonen_seconds": a, "len_seconds": b,
        "links_first": first, "links_second": second,
        "links_identical": first == second, "links_ge_one": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
