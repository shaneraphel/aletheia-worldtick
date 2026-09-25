"""Nested plans on the same 16x16 grids.

Pessimistic search may enter only cells that were observed free.
Optimistic search may enter those cells and every masked cell.
The pessimistic feasible set is therefore a subset of the optimistic one.
Whenever both shortest paths exist, the optimistic path is no longer.

A selector that prefers the shorter existing path then returns the
optimistic plan on every trial. The oracle gap is exactly the trials
where only the pessimistic plan reaches: the optimistic plan exists,
is shorter, and crashes on a cell that was masked.

Seed 20260919, same generator as grid2d.py.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from grid2d import GOAL, N, SEED, START, bfs, make_grid
from selector import choose, outcome

ROOT = Path(__file__).resolve().parent


def plans(true, seen):
    filled = [[0 if c is None else c for c in row] for row in seen]
    opt = bfs(lambda p: filled[p[1]][p[0]] == 1)
    pes = bfs(lambda p: seen[p[1]][p[0]] != 0)
    return opt, pes


def audit(true, seen) -> dict:
    opt, pes = plans(true, seen)
    opt_out = outcome(opt, true)
    pes_out = outcome(pes, true)
    # Inclusion: a pessimistic path is feasible after optimistic fill.
    inclusion = True
    if pes is not None:
        for x, y in pes:
            if seen[y][x] != 0:
                inclusion = False
        if opt is None or len(opt) > len(pes):
            inclusion = False
    # A crash on the optimistic path can only be a masked true obstacle.
    crash_was_masked = True
    if opt is not None:
        for x, y in opt:
            if true[y][x] == 1 and seen[y][x] is not None:
                crash_was_masked = False
    uses_mask = bool(opt) and any(seen[y][x] is None for x, y in opt)
    visual = choose(true, seen)["visual"]
    return {
        "opt": opt_out,
        "pes": pes_out,
        "inclusion": inclusion,
        "crash_was_masked": crash_was_masked,
        "uses_mask": uses_mask,
        "visual_is_optimistic": visual == opt_out,
        "both_exist": opt is not None and pes is not None,
        "strictly_shorter": opt is not None and pes is not None and len(opt) < len(pes),
        "equal_length": opt is not None and pes is not None and len(opt) == len(pes),
    }


def cell(rec: dict) -> str:
    if rec["opt"] == "reached" and rec["pes"] == "reached":
        return "both"
    if rec["opt"] == "reached":
        return "only_optimistic"
    if rec["pes"] == "reached":
        return "only_pessimistic"
    return "neither"


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    cells = {"both": 0, "only_optimistic": 0, "only_pessimistic": 0, "neither": 0}
    inclusion_ok = 0
    crash_ok = 0
    visual_ok = 0
    strict = 0
    both_exist = 0
    only_opt_uses_free_mask = 0
    gap_shorter = 0
    gap_tie = 0
    for _ in range(n):
        true, seen = make_grid(rng)
        rec = audit(true, seen)
        cells[cell(rec)] += 1
        inclusion_ok += int(rec["inclusion"])
        crash_ok += int(rec["crash_was_masked"])
        visual_ok += int(rec["visual_is_optimistic"])
        strict += int(rec["strictly_shorter"])
        both_exist += int(rec["both_exist"])
        if cell(rec) == "only_optimistic" and rec["uses_mask"]:
            only_opt_uses_free_mask += 1
        if cell(rec) == "only_pessimistic":
            gap_shorter += int(rec["strictly_shorter"])
            gap_tie += int(rec["equal_length"])
    return {
        "schema": "worldtick.partition.v1",
        "seed": seed,
        "n": n,
        "cells": cells,
        "inclusion_holds": inclusion_ok,
        "crash_cell_was_masked": crash_ok,
        "visual_equals_optimistic": visual_ok,
        "both_paths_exist": both_exist,
        "optimistic_strictly_shorter": strict,
        "only_optimistic_uses_a_masked_free_cell": only_opt_uses_free_mask,
        "gap_strictly_shorter": gap_shorter,
        "gap_equal_length": gap_tie,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 900), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 44)
    cells = rec["cells"]
    draw.text((36, 24), "Nested plans  ·  路径包含  ·  2,000 grids, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "更短的路是乐观补全。悲观路径是它的子集。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "The shorter path is the optimistic one. Every pessimistic path is feasible after the fill.", font=small, fill=(139, 148, 158))
    cards = [
        ("两条都到达", "Both reach", cells["both"], (63, 185, 80)),
        ("只有乐观到达", "Only optimistic", cells["only_optimistic"], (210, 153, 34)),
        ("只有悲观到达", "Only pessimistic", cells["only_pessimistic"], (121, 192, 255)),
        ("都不到达", "Neither", cells["neither"], (139, 148, 158)),
    ]
    max_v = rec["n"]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 160, x + 387, 720), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 188), name, font=body, fill=color)
        draw.text((x + 24, 224), en, font=small, fill=color)
        draw.text((x + 24, 290), f"{value:,}", font=number, fill=(230, 237, 243))
        bar_top = 660 - (value / max_v) * 200
        draw.rectangle((x + 24, bar_top, x + 363, 660), fill=color)
    draw.text(
        (36, 760),
        f"inclusion {rec['inclusion_holds']:,}/{rec['n']:,}    "
        f"score picks the optimistic plan {rec['visual_equals_optimistic']:,}/{rec['n']:,}    "
        f"包含关系 {rec['inclusion_holds']:,} 次成立",
        font=small,
        fill=(139, 148, 158),
    )
    draw.text(
        (36, 800),
        f"gap {cells['only_pessimistic']:,} = strictly shorter {rec['gap_strictly_shorter']:,} + equal length {rec['gap_equal_length']:,}    "
        f"差距里 {rec['gap_equal_length']:,} 次两条路一样长，平局仍选了乐观方案",
        font=small,
        fill=(139, 148, 158),
    )
    image.save(path, quality=92)


def identities(rec: dict) -> None:
    cells = rec["cells"]
    n = rec["n"]
    if sum(cells.values()) != n:
        raise SystemExit("partition does not sum")
    if rec["inclusion_holds"] != n or rec["crash_cell_was_masked"] != n:
        raise SystemExit("inclusion or crash-cell claim failed")
    if rec["visual_equals_optimistic"] != n:
        raise SystemExit("shorter-path score left the optimistic plan")
    if cells["only_optimistic"] != rec["only_optimistic_uses_a_masked_free_cell"]:
        raise SystemExit("a pessimism miss did not use a masked free cell")
    # The four cells reconstruct the published grid and selector rows.
    if cells["only_pessimistic"] + cells["both"] + cells["only_optimistic"] + cells["neither"] != n:
        raise SystemExit("cells do not cover")


def main() -> int:
    rec = run()
    identities(rec)
    cells = rec["cells"]
    pinned = (cells["both"], cells["only_optimistic"], cells["only_pessimistic"], cells["neither"])
    if pinned != (122, 378, 297, 1203):
        raise SystemExit(f"partition counts moved: {pinned}")
    if (rec["gap_strictly_shorter"], rec["gap_equal_length"]) != (129, 168):
        raise SystemExit("gap length split moved")
    if rec["both_paths_exist"] != 419:
        raise SystemExit("pessimistic paths did not number 419")
    if rec["optimistic_strictly_shorter"] != 185:
        raise SystemExit("strict shortenings moved")
    figure(rec, ROOT / "docs" / "figures" / "partition.png")
    out = ROOT / "results" / "PARTITION.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
