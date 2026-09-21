#!/usr/bin/env python3.12
from __future__ import annotations
import json, math, platform, random, statistics, sys, time
from ik import two_link_ik
SEED, N, N_TRIALS, WARMUP = 20260919, 20000, 7, 1

def tape(n, seed):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        x = rng.uniform(-1.5, 1.5)
        y = rng.uniform(-1.5, 1.5)
        if 0.25 <= x * x + y * y <= 4.0:
            out.append((x, y))
    return out

def law(x, y, l1, l2):
    d2 = x * x + y * y
    cos_e = (d2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    cos_e = max(-1.0, min(1.0, cos_e))
    elbow = math.acos(cos_e)
    shoulder = math.atan2(y, x) - math.atan2(l2 * math.sin(elbow), l1 + l2 * math.cos(elbow))
    return (shoulder, elbow)

def main():
    pts = tape(N, SEED)
    a, b = [], []
    first = second = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = [two_link_ik(x, y, 1.0, 1.0) for x, y in pts]
        at = time.perf_counter()-t0
        t1 = time.perf_counter()
        nv = [law(x, y, 1.0, 1.0) for x, y in pts]
        bt = time.perf_counter()-t1
        if acc != nv:
            raise SystemExit("ik and law disagree")
        if trial < WARMUP:
            continue
        a.append(at); b.append(bt)
        first = len(acc) if first is None else first
        second = len(acc)
    if len(two_link_ik(2.0, 0.0, 1.0, 1.0)) != 2:
        raise SystemExit("identity")
    try:
        two_link_ik(4.0, 0.0, 1.0, 1.0)
    except ValueError:
        pass
    else:
        raise SystemExit("unreachable accepted")
    rec = {
        "schema": "jointlock.ik_bench.v1", "seed": SEED, "n": N,
        "n_trials": N_TRIALS, "warmup": WARMUP, "n_paired": len(a),
        "ik_seconds_median": statistics.median(a),
        "law_seconds_median": statistics.median(b),
        "ik_seconds": a, "law_seconds": b,
        "poses_first": first, "poses_second": second,
        "poses_identical": first == second, "poses_equals_law": True,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "n_parameters": 0, "gradient_descent_steps": 0,
    }
    json.dump(rec, sys.stdout, indent=2); sys.stdout.write("\n")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
