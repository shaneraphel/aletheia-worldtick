#!/usr/bin/env python3.12
"""Reproducible policy-occupancy bench. Prints JSON. Seed and N are pinned."""

from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from policy import policy_iteration

SEED = 20260919
N_STATES = 256
N_ACTIONS = 8
N_TRIALS = 7
WARMUP = 1


def rewards(n_states: int, n_actions: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randrange(0, 64) for _ in range(n_actions)] for _ in range(n_states)]


def greedy0(table: list[list[int]]) -> int:
    row = table[0]
    return max(range(len(row)), key=lambda a: row[a])


def main() -> int:
    table = rewards(N_STATES, N_ACTIONS, SEED)
    pol_times: list[float] = []
    g0_times: list[float] = []
    first: int | None = None
    second: int | None = None
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        acc = policy_iteration(table)
        pt = time.perf_counter() - t0
        t1 = time.perf_counter()
        g0 = greedy0(table)
        gt = time.perf_counter() - t1
        if acc != g0:
            raise SystemExit("policy_iteration and row-0 greedy disagree")
        if trial < WARMUP:
            continue
        pol_times.append(pt)
        g0_times.append(gt)
        if first is None:
            first = acc
        else:
            second = acc
    if policy_iteration([[1, 3], [0, 2]]) != 1:
        raise SystemExit("policy identity failed")
    try:
        policy_iteration([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty rewards accepted")
    record = {
        "schema": "worldtick.policy_bench.v1",
        "seed": SEED,
        "n_states": N_STATES,
        "n_actions": N_ACTIONS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(pol_times),
        "policy_seconds_median": statistics.median(pol_times),
        "greedy0_seconds_median": statistics.median(g0_times),
        "policy_seconds": pol_times,
        "greedy0_seconds": g0_times,
        "action_first": first,
        "action_second": second,
        "action_identical": first is not None and first == second,
        "action_equals_greedy0": True,
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
