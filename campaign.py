"""10_000 worlds, one seed. Completion versus one measured tick.

The completion operator is the one used by 2026 masked world models,
masked EEG models, and row-wise action completion: write a usable value
into the hole. The tick moves only a fact that was already measured.
"""
from __future__ import annotations

import json
import platform
import random
import sys

from complete import completed_reach, measured_tick
from decode import neural_class, zero_fill
from policy import policy_iteration, row0_greedy

SEED = 20260919
N = 10_000
WIDTH = 8


def world_trial(rng: random.Random) -> dict[str, int | str]:
    hole_at = rng.randrange(1, WIDTH - 1)
    cells: list[int | None] = [0] * WIDTH
    cells[0] = 1
    cells[hole_at] = None
    seen = [0 if c is None else c for c in cells]
    hole = "raised"
    try:
        measured_tick(cells)
        hole = "accepted"
    except ValueError:
        pass
    return {
        "completed": completed_reach(cells),
        "seen_tick": measured_tick(seen),
        "hole": hole,
    }


def bci_trial(rng: random.Random) -> dict[str, int | str]:
    go = [rng.choice((0, 1, 2, 3)) for _ in range(WIDTH)]
    if sum(go) == 0:
        go[0] = 1
    drop = "raised"
    try:
        neural_class([])
        drop = "accepted"
    except ValueError:
        pass
    return {
        "go": neural_class(go),
        "rest": neural_class([0] * WIDTH),
        "zerofill": neural_class(zero_fill(WIDTH)),
        "dropout": drop,
    }


def action_trial(rng: random.Random) -> dict[str, int]:
    # Action 0 pays more now and steps into a trap. Action 1 pays less and stays.
    reward = [
        [rng.randrange(8, 21), rng.randrange(1, 4)],
        [rng.randrange(-200, -40), rng.randrange(-200, -40)],
    ]
    return {"row": row0_greedy(reward), "tick": policy_iteration(reward)}


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    worlds = [world_trial(rng) for _ in range(n)]
    bcis = [bci_trial(rng) for _ in range(n)]
    actions = [action_trial(rng) for _ in range(n)]
    return {
        "schema": "worldtick.campaign.v1",
        "seed": seed,
        "n": n,
        "width": WIDTH,
        "world_model": {
            "completed_equals_8": sum(1 for w in worlds if w["completed"] == WIDTH),
            "tick_equals_2": sum(1 for w in worlds if w["seen_tick"] == 2),
            "hole_raised": sum(1 for w in worlds if w["hole"] == "raised"),
        },
        "bci": {
            "go_is_1": sum(1 for b in bcis if b["go"] == 1),
            "zerofill_equals_rest": sum(1 for b in bcis if b["zerofill"] == b["rest"] == 0),
            "dropout_raised": sum(1 for b in bcis if b["dropout"] == "raised"),
        },
        "action": {
            "row_is_0": sum(1 for a in actions if a["row"] == 0),
            "tick_is_1": sum(1 for a in actions if a["tick"] == 1),
            "differ": sum(1 for a in actions if a["row"] != a["tick"]),
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def main() -> int:
    rec = run()
    w, b, a = rec["world_model"], rec["bci"], rec["action"]
    if w["completed_equals_8"] != N or w["tick_equals_2"] != N or w["hole_raised"] != N:
        raise SystemExit("world campaign moved")
    if b["go_is_1"] != N or b["zerofill_equals_rest"] != N or b["dropout_raised"] != N:
        raise SystemExit("bci campaign moved")
    if a["differ"] != N or a["row_is_0"] != N or a["tick_is_1"] != N:
        raise SystemExit("action campaign moved")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
