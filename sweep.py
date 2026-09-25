"""Dropout sweep: completion hits grow with the hole rate, one tick stays 0.

Each point is 10_000 roads of width 32, seed 20260919 plus the point
index. Obstacle rate stays 0.20. Dropout runs 0.00 to 0.50.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from hidden import road, walk_completed, walk_tick

SEED = 20260919
N = 10_000
WIDTH = 32
OBSTACLE = 0.20
DROPS = (0.00, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50)


def run_point(drop: float, n: int, seed: int) -> dict:
    rng = random.Random(seed)
    hidden = 0
    completed = 0
    # walk_tick never enters by construction; count it anyway.
    tick = 0
    for _ in range(n):
        true, seen = road_with_drop(rng, drop)
        if any(s is None and t == 1 for s, t in zip(seen, true)):
            hidden += 1
        completed += walk_completed(true, seen)
        tick += walk_tick(seen)
    return {
        "drop": drop,
        "n": n,
        "hidden_obstacle": hidden,
        "completion_hits": completed,
        "tick_hits": tick,
    }


def road_with_drop(rng: random.Random, drop: float):
    true = [0] * WIDTH
    for i in range(1, WIDTH):
        if rng.random() < OBSTACLE:
            true[i] = 1
    seen: list[int | None] = []
    for i, cell in enumerate(true):
        if i > 0 and rng.random() < drop:
            seen.append(None)
        else:
            seen.append(cell)
    return true, seen


def figure(points: list[dict], path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    W, H = 1680, 900
    image = Image.new("RGB", (W, H), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    draw.text((36, 24), "Dropout sweep  ·  丢失率曲线  ·  10,000 roads per point, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "洞越多，补全走进去的次数越多。一步始终是 0。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "As the hole rate rises, completion walks in more often. One tick stays 0.", font=small, fill=(139, 148, 158))
    # Plot area.
    left, top, right, bottom = 140, 170, 1600, 720
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    max_y = max(p["completion_hits"] for p in points)
    max_y = max(max_y, 1000)
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - frac * (bottom - top)
        draw.line((left, y, right, y), fill=(33, 38, 45), width=1)
        draw.text((36, y - 14), f"{int(frac * max_y):,}", font=small, fill=(139, 148, 158))
    xs = [left + (p["drop"] / 0.50) * (right - left) for p in points]
    ys = [bottom - (p["completion_hits"] / max_y) * (bottom - top) for p in points]
    draw.line(list(zip(xs, ys)), fill=(248, 81, 73), width=5)
    for x, y, p in zip(xs, ys, points):
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(248, 81, 73))
        draw.text((x - 30, bottom + 12), f"{p['drop']:.2f}", font=small, fill=(139, 148, 158))
        draw.text((x - 40, y - 44), f"{p['completion_hits']:,}", font=body, fill=(248, 81, 73))
    # Tick line at zero.
    draw.line([(left, bottom), (right, bottom)], fill=(63, 185, 80), width=5)
    draw.text((right - 320, bottom - 44), "one tick 一步: 0", font=body, fill=(63, 185, 80))
    draw.text((36, bottom + 44), "x: dropout 丢失率   y: hits 走进去的次数", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def run(n: int = N, seed: int = SEED) -> dict:
    points = [run_point(drop, n, seed + i) for i, drop in enumerate(DROPS)]
    return {
        "schema": "worldtick.sweep.v1",
        "seed": seed,
        "n_per_point": n,
        "width": WIDTH,
        "obstacle": OBSTACLE,
        "points": points,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def main() -> int:
    rec = run()
    for p in rec["points"]:
        if p["tick_hits"] != 0:
            raise SystemExit("tick entered a hidden obstacle")
    hits = [p["completion_hits"] for p in rec["points"]]
    if not all(later >= first for first, later in zip(hits, hits[1:])):
        raise SystemExit("completion hits do not grow with dropout")
    if hits[0] != 0 or hits[-1] < 1000:
        raise SystemExit("sweep endpoints moved")
    root = Path(__file__).resolve().parent
    figure(rec["points"], root / "docs" / "figures" / "sweep.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
