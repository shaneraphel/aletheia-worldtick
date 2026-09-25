"""One question along the filled path.

When the optimistic path crashes, the first obstacle on that path was
masked. Asking about that one cell and blocking it is a second plan,
still on the filled map.

The question is whether one answer is the whole repair. It is not.
Some replans arrive. Some crash on a later masked obstacle. Some stop.
The closed loop, which re-observes before every step, is the repair
that does not depend on the crash being the only one.

Same 2,000 grids as grid2d.py. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from grid2d import N, SEED, bfs, make_grid
from selector import outcome

ROOT = Path(__file__).resolve().parent


def optimistic(seen, extra=None):
    filled = [[0 if c is None else c for c in row] for row in seen]

    def blocked(p):
        if extra is not None and p == extra:
            return True
        return filled[p[1]][p[0]] == 1

    return bfs(blocked)


def first_obstacle(path, true):
    if path is None:
        return None
    for x, y in path:
        if true[y][x] == 1:
            return (x, y)
    return None


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    crashes = 0
    asked_was_masked = 0
    after = {"reached": 0, "crash": 0, "stopped": 0}
    for _ in range(n):
        true, seen = make_grid(rng)
        path = optimistic(seen)
        if outcome(path, true) != "crash":
            continue
        crashes += 1
        cell = first_obstacle(path, true)
        if cell is None or seen[cell[1]][cell[0]] is not None:
            continue
        asked_was_masked += 1
        again = optimistic(seen, extra=cell)
        after[outcome(again, true)] += 1
    return {
        "schema": "worldtick.decisive.v1",
        "seed": seed,
        "n": n,
        "crashes": crashes,
        "asked_cell_was_masked": asked_was_masked,
        "after_one_question": after,
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
    number = ImageFont.truetype(font_path, 48)
    after = rec["after_one_question"]
    draw.text((36, 24), "One question  ·  只追问一个格子  ·  2,000 grids, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "撞上之后只封住那一格，有的能到，有的还会再撞。", font=title, fill=(230, 237, 243))
    draw.text((36, 100), "Blocking the first masked obstacle does not finish the repair. Some paths crash again.", font=small, fill=(139, 148, 158))
    cards = [
        ("问完后到达", "Reached after one question", after["reached"], (63, 185, 80)),
        ("问完后再次撞上", "Crashed again", after["crash"], (248, 81, 73)),
        ("问完后无路", "Stopped", after["stopped"], (210, 153, 34)),
    ]
    max_v = max(rec["crashes"], 1)
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 740), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 28, 210), name, font=body, fill=color)
        draw.text((x + 28, 248), en, font=small, fill=color)
        draw.text((x + 28, 330), f"{value:,}", font=number, fill=(230, 237, 243))
        bar_top = 680 - (value / max_v) * 220
        draw.rectangle((x + 28, bar_top, x + 472, 680), fill=color)
    draw.text(
        (36, 790),
        f"optimistic crashes {rec['crashes']:,}    the asked cell was masked {rec['asked_cell_was_masked']:,}/{rec['crashes']:,}",
        font=small,
        fill=(139, 148, 158),
    )
    draw.text(
        (36, 830),
        "一次追问修不完。闭环是每一步走之前再观测。  One question does not finish it. The closed loop observes again before every step.",
        font=small,
        fill=(139, 148, 158),
    )
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    after = rec["after_one_question"]
    if rec["crashes"] != 1439 or rec["asked_cell_was_masked"] != rec["crashes"]:
        raise SystemExit(f"crash accounting moved: {rec['crashes']} {rec['asked_cell_was_masked']}")
    if (after["reached"], after["crash"], after["stopped"]) != (614, 786, 39):
        raise SystemExit(f"one-question outcomes moved: {after}")
    if sum(after.values()) != rec["crashes"]:
        raise SystemExit("outcomes do not cover the crashes")
    figure(rec, ROOT / "docs" / "figures" / "decisive.png")
    out = ROOT / "results" / "DECISIVE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
