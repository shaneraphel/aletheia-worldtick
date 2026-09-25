"""Receding-horizon walking: re-observe every step, never commit to a fill.

On 10,000 roads, stand at each cell, draw a fresh observation of the
next cell, and advance only on an observed-free cell. A masked look
means waiting, not filling. Crashes are zero by construction: no step
is ever taken into an unobserved cell. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from hidden import DROP, OBSTACLE, WIDTH

SEED = 20260919
N = 10_000
MAX_WAITS = 2_000


def true_road(rng: random.Random) -> list[int]:
    true = [0] * WIDTH
    for i in range(1, WIDTH):
        if rng.random() < OBSTACLE:
            true[i] = 1
    return true


def walk(true: list[int], rng: random.Random) -> dict[str, int]:
    pos = 0
    waits = 0
    while pos < len(true) - 1:
        if rng.random() < DROP:
            waits += 1
            if waits > MAX_WAITS:
                return {"outcome": "timeout", "waits": waits}
            continue
        if true[pos + 1] == 1:
            return {"outcome": "correct_stop", "waits": waits}
        pos += 1
    return {"outcome": "reached", "waits": waits}


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    outcomes = {"crash": 0, "reached": 0, "correct_stop": 0, "timeout": 0}
    waits_total = 0
    for _ in range(n):
        true = true_road(rng)
        res = walk(true, rng)
        outcomes[res["outcome"]] += 1
        waits_total += res["waits"]
    return {
        "schema": "worldtick.closedloop.v1",
        "seed": seed,
        "n": n,
        "width": WIDTH,
        "drop": DROP,
        "obstacle": OBSTACLE,
        "outcomes": outcomes,
        "waits_total": waits_total,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    W, H = 1680, 900
    image = Image.new("RGB", (W, H), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 24)
    number = ImageFont.truetype(font_path, 44)
    draw.text((36, 24), "Closed loop  ·  闭环  ·  10,000 roads, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "每步重新看一眼再走。撞上归零，代价是等待。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Re-observe every step before moving. Crashes go to zero; the price is waiting.", font=small, fill=(139, 148, 158))
    o = rec["outcomes"]
    cards = [
        ("闭环撞上", "Closed-loop crashes", o["crash"], (63, 185, 80)),
        ("闭环走通", "Closed-loop reached", o["reached"], (210, 153, 34)),
        ("正确停下", "Correct stops", o["correct_stop"], (121, 192, 255)),
        ("等待总计", "Total waits", rec["waits_total"], (139, 148, 158)),
    ]
    max_v = max(c[2] for c in cards) or 1
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 160, x + 387, 760), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 190), name, font=body, fill=color)
        draw.text((x + 24, 228), en, font=small, fill=color)
        draw.text((x + 24, 300), f"{value:,}", font=number, fill=(230, 237, 243))
        bar_top = 700 - (value / max_v) * 220
        draw.rectangle((x + 24, bar_top, x + 363, 700), fill=color)
    draw.text((36, 786), f"n = {rec['n']:,}   vs open-loop optimistic 开环乐观: 2,995 crashes", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    o = rec["outcomes"]
    if o["crash"] != 0:
        raise SystemExit("closed loop crashed")
    if o["timeout"] != 0:
        raise SystemExit("closed loop timed out")
    if o["reached"] + o["correct_stop"] != N:
        raise SystemExit("outcomes do not sum to n")
    if o["reached"] != 9 or o["correct_stop"] != 9991:
        raise SystemExit("closed-loop outcomes moved")
    if rec["waits_total"] != 20975:
        raise SystemExit("waits total moved")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "closedloop.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
