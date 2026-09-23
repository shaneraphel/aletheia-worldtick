#!/usr/bin/env python3.12
"""Same pinned world as the Datalog bench. One tick, then the closure."""
from __future__ import annotations

import json
import platform
import sys

from datalog import datalog_fixpoint
from datalog_bench import N_EDGES, N_FACTS, N_NODES, SEED, world
from tick import reach_after, world_tick


def main() -> int:
    facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
    one = world_tick(N_NODES, facts, edges)
    closed = datalog_fixpoint(N_NODES, facts, edges)
    horizon = reach_after(N_NODES, facts, edges, N_NODES)
    if horizon != closed:
        raise SystemExit("horizon does not meet the closure")
    if world_tick(N_NODES, facts, edges) != one:
        raise SystemExit("tick mismatch")
    record = {
        "schema": "worldtick.tick_bench.v1",
        "seed": SEED,
        "n_nodes": N_NODES,
        "n_facts": N_FACTS,
        "n_edges": N_EDGES,
        "one_tick": one,
        "closure": closed,
        "horizon_n": horizon,
        "one_tick_lt_closure": one < closed,
        "horizon_equals_closure": True,
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
    raise SystemExit(main())
