"""How many questions the filled plan still needs.

Start from the optimistic path. Each time it crashes, block the first
obstacle on it and plan again. Count the questions until the path
arrives or no path remains.

One question is the special case already measured. The count here is
the length of that process. A trial that never crashes takes zero
questions. The closed loop is what this process approximates, one
revealed obstacle at a time, still leaving every unasked cell filled.

Same 2,000 grids as grid2d.py. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from decisive import first_obstacle
from grid2d import N, SEED, bfs, make_grid
from selector import outcome

ROOT = Path(__file__).resolve().parent
CAP = 64


def optimistic(seen, blocked_cells: set[tuple[int, int]]):
    filled = [[0 if c is None else c for c in row] for row in seen]

    def blocked(p):
        return p in blocked_cells or filled[p[1]][p[0]] == 1

    return bfs(blocked)


def ask_until_clear(true, seen) -> tuple[int, str]:
    blocked: set[tuple[int, int]] = set()
    asked = 0
    while asked <= CAP:
        path = optimistic(seen, blocked)
        status = outcome(path, true)
        if status != "crash":
            return asked, status
        cell = first_obstacle(path, true)
        if cell is None or cell in blocked:
            return asked, "stuck"
        blocked.add(cell)
        asked += 1
    return asked, "cap"


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    hist: dict[int, int] = {}
    ends = {"reached": 0, "stopped": 0, "stuck": 0, "cap": 0}
    more_than_one = 0
    crashed = 0
    total_questions = 0
    for _ in range(n):
        true, seen = make_grid(rng)
        asked, status = ask_until_clear(true, seen)
        hist[asked] = hist.get(asked, 0) + 1
        ends[status] += 1
        total_questions += asked
        if asked > 0:
            crashed += 1
        if asked > 1:
            more_than_one += 1
    return {
        "schema": "worldtick.askdepth.v1",
        "seed": seed,
        "n": n,
        "cap": CAP,
        "histogram": {str(k): hist[k] for k in sorted(hist)},
        "ends": ends,
        "trials_that_crash_at_least_once": crashed,
        "trials_needing_more_than_one_question": more_than_one,
        "questions_total": total_questions,
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
    draw.text((36, 24), "Questions until clear  ·  追问到不再撞  ·  2,000 grids", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "一次不够。多数会撞的图，要连续追问多于一次。", font=title, fill=(230, 237, 243))
    draw.text((36, 100), "One question is not the typical repair. Most crashing grids need more than one.", font=small, fill=(139, 148, 158))
    hist = {int(k): v for k, v in rec["histogram"].items()}
    keys = sorted(hist)
    left, top, right, bottom = 120, 180, 1600, 760
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    max_v = max(hist.values())
    slot = (right - left) / max(len(keys), 1)
    for i, k in enumerate(keys):
        value = hist[k]
        x0 = left + i * slot + 8
        x1 = left + (i + 1) * slot - 8
        h = (value / max_v) * (bottom - top - 40)
        draw.rectangle((x0, bottom - h, x1, bottom), fill=(121, 192, 255))
        draw.text((x0, bottom + 8), str(k), font=small, fill=(139, 148, 158))
    draw.text((left, top + 12), "questions  追问次数", font=small, fill=(139, 148, 158))
    draw.text(
        (36, 820),
        f"more than one question: {rec['trials_needing_more_than_one_question']:,}    "
        f"questions in total: {rec['questions_total']:,}    "
        f"多于一次：{rec['trials_needing_more_than_one_question']:,}    追问合计：{rec['questions_total']:,}",
        font=small,
        fill=(139, 148, 158),
    )
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["trials_that_crash_at_least_once"] != 1439:
        raise SystemExit("crash count moved")
    if rec["trials_needing_more_than_one_question"] != 786 or rec["questions_total"] != 2814:
        raise SystemExit("question depth moved")
    if rec["histogram"] != {"0": 561, "1": 653, "2": 422, "3": 217, "4": 90, "5": 41, "6": 13, "7": 2, "9": 1}:
        raise SystemExit(f"histogram moved: {rec['histogram']}")
    if rec["ends"] != {"reached": 1854, "stopped": 146, "stuck": 0, "cap": 0}:
        raise SystemExit(f"process did not finish: {rec['ends']}")
    figure(rec, ROOT / "docs" / "figures" / "askdepth.png")
    out = ROOT / "results" / "ASKDEPTH.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(
        {
            "more_than_one": rec["trials_needing_more_than_one_question"],
            "questions_total": rec["questions_total"],
            "histogram": rec["histogram"],
            "ends": rec["ends"],
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
