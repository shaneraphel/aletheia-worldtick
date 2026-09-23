#!/usr/bin/env python3.12
"""Worldtick — fact-reachability check."""

from __future__ import annotations

import argparse
import sys

from datalog import datalog_fixpoint
from datalog_bench import N_EDGES, N_FACTS, N_NODES, SEED, world
from policy import policy_iteration, row0_greedy
from tick import reach_after, world_tick

CHAIN = [(0, 1), (1, 2)]
TRAP = [[10, 1], [-100, -100]]


def verify_precision() -> str:
    if datalog_fixpoint(3, [0], CHAIN) != 3:
        raise SystemExit("datalog identity failed")
    if world_tick(3, [0], CHAIN) != 2:
        raise SystemExit("tick identity failed")
    if reach_after(3, [0], CHAIN, 3) != 3:
        raise SystemExit("horizon identity failed")
    if datalog_fixpoint(3, [0], CHAIN) != datalog_fixpoint(3, [0], CHAIN):
        raise SystemExit("datalog mismatch")
    if row0_greedy(TRAP) != 0 or policy_iteration(TRAP) != 1:
        raise SystemExit("policy identity failed")
    if policy_iteration([[1, 3], [0, 2]]) != 1:
        raise SystemExit("policy identity failed")
    try:
        datalog_fixpoint(3, [], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("empty facts accepted")
    try:
        world_tick(3, [], CHAIN)
    except ValueError:
        pass
    else:
        raise SystemExit("empty tick accepted")
    try:
        policy_iteration([])
    except ValueError:
        pass
    else:
        raise SystemExit("empty reward accepted")
    try:
        datalog_fixpoint(-1, [0], [(0, 1)])
    except ValueError:
        pass
    else:
        raise SystemExit("negative n accepted")
    facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
    if datalog_fixpoint(N_NODES, facts, edges) != 214:
        raise SystemExit("pinned reach moved")
    if not world_tick(N_NODES, facts, edges) < 214:
        raise SystemExit("pinned tick is not shorter than closure")
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description="Worldtick precision check")
    parser.add_argument("--verify-precision", action="store_true")
    args = parser.parse_args()
    if args.verify_precision:
        print("precision_ok", verify_precision())
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
