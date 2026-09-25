#!/usr/bin/env python3.12
"""Every number cited in paper.md, checked against results/*.json.

Usage: python3.12 paper/check_numbers.py
Exits nonzero on the first mismatch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
PAPER = ROOT / "paper" / "paper.md"


def load(name: str) -> dict:
    return json.loads((RES / name).read_text())


def check(cond: bool, label: str) -> None:
    if not cond:
        raise SystemExit(f"number check failed: {label}")
    print(f"ok: {label}")


def main() -> int:
    text = PAPER.read_text()
    story = json.loads((RES / "STORY.json").read_text())
    campaign = load("CAMPAIGN.json")
    hidden = load("HIDDEN.json")
    decide = load("DECIDE.json")
    fill = load("FILLCHOICE.json")
    sweep = {p["drop"]: p["completion_hits"] for p in load("SWEEP.json")["points"]}
    sweep_tick = {p["drop"]: p["tick_hits"] for p in load("SWEEP.json")["points"]}
    horizon = {p["horizon"]: p["reach"] for p in load("HORIZON.json")["points"]}
    fore = load("FORESIGHT.json")
    bci = {p["dropped"]: p["read_as_rest"] for p in load("BCISWEEP.json")["points"]}
    audit = load("AUDIT.json")
    robust = load("ROBUST.json")
    closed = load("CLOSEDLOOP.json")

    check(story["world_model"]["completed_reach"] == 3, "story completed reach 3")
    check(story["world_model"]["seen_tick"] == 2, "story measured tick 2")
    check(story["bci"]["go"] == 1 and story["bci"]["zerofill"] == 0, "story go 1, zerofill 0")
    check(story["action"] == {"row": 0, "tick": 1}, "story action 0 vs 1")
    check(campaign["world_model"] == {"completed_equals_8": 10000, "tick_equals_2": 10000, "hole_raised": 10000}, "campaign world 10k")
    check(campaign["action"]["differ"] == 10000, "campaign actions differ 10k")
    check((hidden["roads_with_a_hidden_obstacle"], hidden["completion_enters_hidden_obstacle"], hidden["tick_enters_hidden_obstacle"]) == (8564, 2995, 0), "hidden 8564/2995/0")
    check((decide["completion_crashes"], decide["tick_crashes"], decide["tick_extra_stops"], decide["completion_extra_stops"]) == (552, 0, 2353, 0), "decide 552/0/2353/0")
    check((fill["optimistic"]["crash"], fill["optimistic"]["stop"], fill["optimistic"]["reached"]) == (2995, 6993, 12), "optimistic 2995/6993/12")
    check((fill["pessimistic"]["crash"], fill["pessimistic"]["stop"], fill["pessimistic"]["reached"]) == (0, 10000, 0), "pessimistic 0/10000/0")
    check([sweep[d] for d in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)] == [0, 503, 934, 2002, 2914, 3970, 5084], "sweep curve")
    check(all(v == 0 for v in sweep_tick.values()), "sweep tick always 0")
    check([horizon[h] for h in (0, 1, 2, 3, 4, 6, 8, 12)] == [8, 24, 50, 92, 138, 205, 212, 214], "horizon curve")
    check(fore["first_flip_discount"] == 0.10 and abs(fore["threshold_value"] - 9 / 101) < 1e-12, "foresight 9/101 flips at 0.10")
    check(fore["random_flips"] == 1000, "foresight 1000 random flips")
    check([bci[k] for k in range(9)] == [0, 0, 1, 9, 43, 161, 642, 2494, 10000], "bci dose-response")
    check((audit["roads_with_masked_cells"], audit["filled_maps_with_mask_markers"], audit["filled_maps_matching_truth"], audit["roads_with_occluded_obstacle"]) == (10000, 0, 1436, 8564), "audit 10000/0/1436/8564")
    check([r["sweep_completion_hits"] for r in robust["rows"]] == [605, 641, 580, 606, 560], "robust sweep rows")
    check([r["decide_completion_crashes"] for r in robust["rows"]] == [120, 143, 127, 126, 105], "robust decide rows")
    check(all(r["sweep_tick_hits"] == 0 and r["decide_tick_crashes"] == 0 for r in robust["rows"]), "robust tick zeros")
    check((closed["outcomes"]["crash"], closed["outcomes"]["reached"], closed["outcomes"]["correct_stop"]) == (0, 9, 9991), "closed loop 0/9/9991")
    check(closed["waits_total"] == 20975, "closed-loop waits 20975")
    trade = load("TRADEOFF.json")
    check(trade["one_step"]["breakeven_exact"] == "2353/552", "breakeven one step 2353/552")
    check(trade["full_walk"]["breakeven_exact"] == "20975/2995", "breakeven full walk 20975/2995")
    stats = load("STATS.json")["rates"]
    check((round(stats["one-step collision"]["lo"], 4), round(stats["one-step collision"]["hi"], 4)) == (0.0509, 0.0598), "wilson collision interval")
    check((round(stats["occluded road"]["lo"], 4), round(stats["occluded road"]["hi"], 4)) == (0.8494, 0.8631), "wilson occluded interval")
    grid = load("GRID2D.json")
    check((grid["optimistic"]["crash"], grid["optimistic"]["reached"], grid["optimistic"]["stopped"]) == (1439, 500, 61), "grid optimistic 1439/500/61")
    check((grid["pessimistic"]["crash"], grid["pessimistic"]["reached"], grid["pessimistic"]["stopped"]) == (0, 419, 1581), "grid pessimistic 0/419/1581")
    plan = load("PLANDEPTH.json")
    check([c["action"] for c in plan["trap_curve"]] == [0, 1, 1, 1, 1, 1], "trap depth curve 0-1-1-1-1-1")
    check(all(p["flipped_vs_myopic"] == 1000 and p["match_infinite"] == 1000 for p in plan["points"][1:]), "depth 1 matches infinite everywhere")
    sel = load("SELECTOR.json")
    check((sel["visual"]["reached"], sel["visual"]["crash"], sel["oracle"]["reached"], sel["gap_reached"]) == (500, 1439, 797, 297), "selector 500/1439/797/297")

    for token in ["2,995", "8,564", "10,000", "9/101", "1,436", "2,353", "5,084", "214", "2494", "1,000"]:
        check(token in text, f"paper cites {token}")
    print(f"all {32} number checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
