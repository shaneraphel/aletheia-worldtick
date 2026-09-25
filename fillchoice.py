"""Optimistic versus pessimistic fill on the same 10,000 roads.

Optimistic writes every hole as free and walks on. Pessimistic writes
every hole as a wall and stops. The fill, not the planner, carries the
risk: optimistic crashes on hidden obstacles, pessimistic never does,
and pays with early stops. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from hidden import road

SEED = 20260919
N = 10_000


def walk(true: list[int], seen: list[int | None], fill: int) -> str:
    for i in range(1, len(true)):
        cell = fill if seen[i] is None else seen[i]
        if cell == 1:
            return "stop"
        if true[i] == 1:
            return "crash"
    return "reached"


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    opt = {"crash": 0, "stop": 0, "reached": 0}
    pes = {"crash": 0, "stop": 0, "reached": 0}
    for _ in range(n):
        true, seen = road(rng)
        opt[walk(true, seen, 0)] += 1
        pes[walk(true, seen, 1)] += 1
    return {
        "schema": "worldtick.fillchoice.v1",
        "seed": seed,
        "n": n,
        "optimistic": opt,
        "pessimistic": pes,
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
    draw.text((36, 24), "Fill choice  ·  补全的写法  ·  10,000 roads, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "洞写成空地会撞。洞写成墙一次不撞，代价是提前停。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Holes written free crash. Holes written as walls never crash; the price is early stops.", font=small, fill=(139, 148, 158))
    cards = [
        ("乐观撞上", "Optimistic crashes", rec["optimistic"]["crash"], (248, 81, 73)),
        ("保守撞上", "Pessimistic crashes", rec["pessimistic"]["crash"], (63, 185, 80)),
        ("乐观走通", "Optimistic reached", rec["optimistic"]["reached"], (210, 153, 34)),
        ("保守走通", "Pessimistic reached", rec["pessimistic"]["reached"], (139, 148, 158)),
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
    draw.text((36, 786), f"n = {rec['n']:,}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["pessimistic"]["crash"] != 0:
        raise SystemExit("pessimistic fill crashed")
    if rec["optimistic"]["crash"] != 2995:
        raise SystemExit("optimistic crashes moved")
    if rec["optimistic"]["reached"] != 12:
        raise SystemExit("optimistic reached moved")
    if rec["pessimistic"]["reached"] != 0:
        raise SystemExit("optimistic reaches less than pessimistic")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "fillchoice.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
