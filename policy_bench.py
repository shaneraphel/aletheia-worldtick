#!/usr/bin/env python3.12
"""Reproducible policy-iteration bench. Prints JSON. Seed and shape are pinned."""
from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time

from policy import policy_iteration, row0_greedy

SEED = 20260919
N_STATES = 256
N_ACTIONS = 8
N_TRIALS = 7
WARMUP = 1


def table(n: int, a: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randrange(-5, 21) for _ in range(a)] for _ in range(n)]


def main() -> int:
    reward = table(N_STATES, N_ACTIONS, SEED)
    pi_times: list[float] = []
    greedy_times: list[float] = []
    first: int | None = None
    second: int | None = None
    greedy = row0_greedy(reward)
    for trial in range(WARMUP + N_TRIALS):
        t0 = time.perf_counter()
        action = policy_iteration(reward)
        dt = time.perf_counter() - t0
        t1 = time.perf_counter()
        g = row0_greedy(reward)
        bt = time.perf_counter() - t1
        if g != greedy:
            raise SystemExit("greedy action moved")
        if trial < WARMUP:
            continue
        pi_times.append(dt)
        greedy_times.append(bt)
        if first is None:
            first = action
        else:
            second = action
    if policy_iteration([[1, 3], [0, 2]]) != 1:
        raise SystemExit("policy identity failed")
    if first == greedy:
        raise SystemExit("pinned policy matches the greedy row")
    try:
        policy_iteration([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty reward accepted")
    record = {
        "schema": "worldtick.policy_bench.v1",
        "seed": SEED,
        "n_states": N_STATES,
        "n_actions": N_ACTIONS,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "n_paired": len(pi_times),
        "policy_seconds_median": statistics.median(pi_times),
        "greedy_seconds_median": statistics.median(greedy_times),
        "policy_seconds": pi_times,
        "greedy_seconds": greedy_times,
        "action_first": first,
        "action_second": second,
        "action_identical": first is not None and first == second,
        "greedy_action": greedy,
        "policy_differs_from_greedy": first is not None and first != greedy,
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
