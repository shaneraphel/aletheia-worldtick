"""Planning depth: how many lookahead steps flip the answer.

Finite-horizon dynamic programming in exact rationals at discount
9/10, depths 0..5, on 1,000 random trap tables plus the fixed TRAP.
Depth 0 is myopic. The flip fraction grows with depth and the fixed
trap flips at depth 1. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from fractions import Fraction
from pathlib import Path

from foresight import _nxt, discounted_policy, random_trap

SEED = 20260919
N = 1_000
DEPTHS = (0, 1, 2, 3, 4, 5)
DISCOUNT = Fraction(9, 10)
TRAP = [[10, 1], [-100, -100]]


def finite_action(reward: list[list[int]], depth: int) -> int:
    n = len(reward)
    value = [Fraction(0)] * n
    for _ in range(depth):
        value = [
            max(
                (Fraction(reward[s][a]) + DISCOUNT * value[_nxt(n, s, a)], -a)
                for a in range(len(reward[s]))
            )[0]
            for s in range(n)
        ]
    row = reward[0]
    qs = [Fraction(row[a]) + DISCOUNT * value[_nxt(n, 0, a)] for a in range(len(row))]
    return max(range(len(qs)), key=lambda a: (qs[a], -a))


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    tables = [random_trap(rng) for _ in range(n)]
    trap_curve = [{"depth": d, "action": finite_action(TRAP, d)} for d in DEPTHS]
    points = []
    for d in DEPTHS:
        acts = [finite_action(t, d) for t in tables]
        myopic = [finite_action(t, 0) for t in tables]
        far = [discounted_policy(t, DISCOUNT) for t in tables]
        points.append(
            {
                "depth": d,
                "flipped_vs_myopic": sum(1 for a, m in zip(acts, myopic) if a != m),
                "match_infinite": sum(1 for a, f in zip(acts, far) if a == f),
            }
        )
    return {
        "schema": "worldtick.plandepth.v1",
        "seed": seed,
        "n": n,
        "discount": "9/10",
        "trap_curve": trap_curve,
        "points": points,
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
    body = ImageFont.truetype(font_path, 22)
    draw.text((36, 24), "Planning depth  ·  规划深度  ·  1,000 trap tables, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "深度 1 翻转全部 1000 张表，此后与无穷视野完全一致。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Depth 1 flips all 1,000 tables and matches the infinite horizon everywhere after.", font=small, fill=(139, 148, 158))
    left, top, right, bottom = 200, 170, 1600, 760
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    n = rec["n"]
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - 30 - frac * (bottom - top - 60)
        draw.line((left, y, right, y), fill=(33, 38, 45), width=1)
        draw.text((90, y - 14), f"{int(frac * n):,}", font=small, fill=(139, 148, 158))
    depths = [p["depth"] for p in rec["points"]]
    max_d = max(depths)
    xs = [left + (d / max_d) * (right - left) for d in depths]
    for key, color in (("flipped_vs_myopic", (248, 81, 73)), ("match_infinite", (63, 185, 80))):
        vals = [p[key] for p in rec["points"]]
        ys = [bottom - 30 - (v / n) * (bottom - top - 60) for v in vals]
        draw.line(list(zip(xs, ys)), fill=color, width=5)
        for x, y, v, d in zip(xs, ys, vals, depths):
            draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=color)
            draw.text((x - 30, bottom + 8), f"{d}", font=small, fill=(139, 148, 158))
    draw.text((36, 800), "red 翻转 flipped vs myopic   green 与无穷视野一致 matches infinite horizon", font=body, fill=(230, 237, 243))
    trap = "-".join(str(c["action"]) for c in rec["trap_curve"])
    draw.text((36, 840), f"fixed trap 固定陷阱按深度: {trap}", font=body, fill=(210, 153, 34))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if [c["action"] for c in rec["trap_curve"]] != [0, 1, 1, 1, 1, 1]:
        raise SystemExit("trap depth curve moved")
    flips = [p["flipped_vs_myopic"] for p in rec["points"]]
    if flips[0] != 0:
        raise SystemExit("depth 0 flips against itself")
    if any(p["flipped_vs_myopic"] != N or p["match_infinite"] != N for p in rec["points"][1:]):
        raise SystemExit("depth 1 does not match the infinite horizon everywhere")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "plandepth.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
