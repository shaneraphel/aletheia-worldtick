#!/usr/bin/env python3.12
"""Three completions, one smaller tick. Prints JSON."""
from __future__ import annotations

import json
import platform
import sys

from complete import completed_reach, measured_closure, measured_tick
from decode import GO, REST, neural_class, zero_fill
from policy import policy_iteration, row0_greedy

HOLE = [1, None, 0]
SEEN = [1, 0, 0]
TRAP = [[10, 1], [-100, -100]]


def main() -> int:
    hole = "raised"
    try:
        measured_tick(HOLE)
        hole = "accepted"
    except ValueError:
        pass
    drop = "raised"
    try:
        neural_class([])
        drop = "accepted"
    except ValueError:
        pass
    rec = {
        "schema": "worldtick.story.v1",
        "world_model": {
            "completed_reach": completed_reach(HOLE),
            "seen_closure": measured_closure(SEEN),
            "seen_tick": measured_tick(SEEN),
            "hole": hole,
        },
        "bci": {
            "go": neural_class(GO),
            "rest": neural_class(REST),
            "zerofill": neural_class(zero_fill(8)),
            "dropout": drop,
        },
        "action": {
            "row": row0_greedy(TRAP),
            "tick": policy_iteration(TRAP),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    same_completion = rec["world_model"]["completed_reach"] == rec["world_model"]["seen_closure"]
    smaller_tick = rec["world_model"]["seen_tick"] < rec["world_model"]["completed_reach"]
    rest_is_fill = rec["bci"]["rest"] == rec["bci"]["zerofill"]
    go_differs = rec["bci"]["go"] != rec["bci"]["zerofill"]
    action_differs = rec["action"]["row"] != rec["action"]["tick"]
    if not (same_completion and smaller_tick and rest_is_fill and go_differs and action_differs):
        raise SystemExit("story identity failed")
    if hole != "raised" or drop != "raised":
        raise SystemExit("story identity failed")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
