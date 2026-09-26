"""The oldest a frame can get on a miss budget.

Sixteen steps, and each stream may miss k of them, for k from 0 to 8.
Missing the last k steps makes the frame the oldest it can be: ages 1
through k after the arrivals stop. No placement makes any frame older
than k, because an age counts misses and there are only k.

Values still vary by session: the brain is a movement with probability
1/2 and the finger is uniform on 0..7 with 0 closed. The held picture
updates only on arrival. The guessed picture reads a missing stretch as
rest and draws a missing finger closed. Ages are fixed by the schedule;
only the disagreement needs the seed.

Seed 20260919. Ten thousand sessions. The same session index uses the
same values on one core and on many.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from fleet import cuts
from grid2d import SEED

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
BUDGETS = tuple(range(9))


def session_values(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    return [(int(rng.random() < 0.5), rng.randrange(8)) for _ in range(STEPS)]


def run_budget(values: list, budget: int) -> dict:
    held_fast = False
    held_closed = False
    brain_age = 0
    finger_age = 0
    acc = {"new": 0, "age_sum": 0, "max_age": 0, "differ": 0}
    for step, (brain_val, finger_val) in enumerate(values):
        missing = step >= STEPS - budget
        if missing:
            guess_fast = False
            show_fast = held_fast
            guess_closed = True
            show_closed = held_closed
            brain_age += 1
            finger_age += 1
        else:
            guess_fast = brain_val == 1
            show_fast = guess_fast
            held_fast = show_fast
            guess_closed = finger_val == 0
            show_closed = guess_closed
            held_closed = show_closed
            brain_age = 0
            finger_age = 0
        frame_age = brain_age if brain_age > finger_age else finger_age
        if not missing:
            acc["new"] += 1
        acc["age_sum"] += frame_age
        if frame_age > acc["max_age"]:
            acc["max_age"] = frame_age
        if (guess_fast, guess_closed) != (show_fast, show_closed):
            acc["differ"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc: dict[str, int] = {}
    for k in BUDGETS:
        acc[f"new_{k}"] = 0
        acc[f"agesum_{k}"] = 0
        acc[f"maxage_{k}"] = 0
        acc[f"differ_{k}"] = 0
    acc["sessions"] = 0
    for i in range(start, stop):
        values = session_values(i, seed)
        for k in BUDGETS:
            row = run_budget(values, k)
            acc[f"new_{k}"] += row["new"]
            acc[f"agesum_{k}"] += row["age_sum"]
            if row["max_age"] > acc[f"maxage_{k}"]:
                acc[f"maxage_{k}"] = row["max_age"]
            acc[f"differ_{k}"] += row["differ"]
        acc["sessions"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        max_keys = {f"maxage_{k}" for k in BUDGETS}
        parallel = {}
        for key in serial:
            if key in max_keys:
                parallel[key] = max(p[key] for p in pieces)
            else:
                parallel[key] = sum(p[key] for p in pieces)
    return {
        "schema": "worldtick.worst.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "budgets": list(BUDGETS),
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 880), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    tiny = ImageFont.truetype(font_path, 15)
    s = rec["serial"]
    draw.text((36, 24), "How bad can it get  ·  最坏能坏到哪", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "预算晚几步，排在最后，画面最老。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Miss the last steps of the budget. No placement makes any frame older than the budget.", font=small, fill=(139, 148, 158))
    left, top, width, height = 90, 180, 1500, 560
    draw.rectangle((left, top, left + width, top + height), outline=(48, 54, 61), width=2)
    series = [
        ("agesum", [s[f"agesum_{k}"] for k in BUDGETS], (210, 153, 34), "年龄合计 age sum"),
        ("differ", [s[f"differ_{k}"] for k in BUDGETS], (218, 54, 51), "不一样 differ"),
    ]
    vmax = max(v for _, values, _, _ in series for v in values)
    for g in range(5):
        y = top + g * height // 4
        draw.line((left, y, left + width, y), fill=(33, 38, 45), width=1)
        draw.text((left - 76, y - 12), f"{vmax * (4 - g) // 4 // 1000}k", font=tiny, fill=(139, 148, 158))
    for j, (_, values, color, name) in enumerate(series):
        pts = []
        for i, v in enumerate(values):
            x = left + (i * width) // (len(BUDGETS) - 1)
            y = top + height - int(v / vmax * height)
            pts.append((x, y))
        draw.line(pts, fill=color, width=3)
        for x, y in pts:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color)
        lx = left + 1050 + j * 260
        draw.rectangle((lx, top + height + 44, lx + 120, top + height + 60), fill=color)
        draw.text((lx, top + height + 66), name, font=small, fill=color)
    for i, k in enumerate(BUDGETS):
        x = left + (i * width) // (len(BUDGETS) - 1)
        draw.text((x - 8, top + height + 8), f"{k}", font=small, fill=(139, 148, 158))
    draw.text((36, top + height + 66), "预算 budget →", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"worst cores disagree: {s}")
    n = s["sessions"]
    if tuple(s[f"maxage_{k}"] for k in BUDGETS) != tuple(BUDGETS):
        raise SystemExit(f"oldest frame is not the budget: {s}")
    if tuple(s[f"agesum_{k}"] for k in BUDGETS) != tuple(n * k * (k + 1) // 2 for k in BUDGETS):
        raise SystemExit(f"age sums are not triangular: {s}")
    if tuple(s[f"new_{k}"] for k in BUDGETS) != tuple((STEPS - k) * n for k in BUDGETS):
        raise SystemExit(f"new frames are not the schedule: {s}")
    pinned = (0, 9346, 18750, 27972, 37700, 46715, 56436, 65436, 75184)
    if tuple(s[f"differ_{k}"] for k in BUDGETS) != pinned:
        raise SystemExit("worst disagreement moved")
    figure(rec, ROOT / "docs" / "figures" / "worst.png")
    out = ROOT / "results" / "WORST.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    slim = {k: s[k] for k in sorted(s) if k != "sessions"}
    slim["sessions"] = s["sessions"]
    json.dump({"serial": slim, "equal": rec["equal"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
