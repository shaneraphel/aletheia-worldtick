#!/usr/bin/env python3.12
"""Pinned reward table: row-0 greedy and policy iteration disagree."""
from __future__ import annotations

import json
import platform
import sys

from policy import policy_iteration, row0_greedy

# Action 0 pays 10 now and steps into -100.
# Action 1 pays 1 and stays. Greedy takes 0. Iteration takes 1.
TABLE = [[10, 1], [-100, -100]]


def main() -> int:
    greedy = row0_greedy(TABLE)
    planned = policy_iteration(TABLE)
    empty = "raised"
    try:
        policy_iteration([])
        empty = "accepted"
    except ValueError:
        pass
    rec = {
        "schema": "worldtick.show_policy.v1",
        "built": "2-state ring; greedy action 0; iterated action 1; empty table refuses",
        "ours": {"greedy": greedy, "policy": planned, "empty": empty},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "n_parameters": 0,
        "gradient_descent_steps": 0,
    }
    if greedy != 0 or planned != 1 or empty != "raised":
        raise SystemExit("worldtick policy show identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
