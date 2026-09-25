"""Horizon curve on the pinned 256-node world: reach grows 24 to 214.

Completion answers the closure in one call. One tick answers 24.
Walking h ticks converges to the closure at a finite horizon.
Seed 20260919, 256 nodes, 8 facts, 512 edges.
"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from datalog import datalog_fixpoint
from datalog_bench import N_EDGES, N_FACTS, N_NODES, SEED, world
from tick import reach_after, world_tick

HORIZONS = (0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128, 256)


def run() -> dict:
    facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
    closure = datalog_fixpoint(N_NODES, facts, edges)
    tick = world_tick(N_NODES, facts, edges)
    points = [{"horizon": h, "reach": reach_after(N_NODES, facts, edges, h)} for h in HORIZONS]
    steps_to_close = next(p["horizon"] for p in points if p["reach"] == closure)
    return {
        "schema": "worldtick.horizon.v1",
        "seed": SEED,
        "n_nodes": N_NODES,
        "n_facts": N_FACTS,
        "n_edges": N_EDGES,
        "one_tick": tick,
        "closure": closure,
        "steps_to_closure": steps_to_close,
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
    draw.text((36, 24), "Horizon  ·  步数曲线  ·  seed 20260919, 256 nodes, 8 facts, 512 edges", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "一步是 24。走下去收敛到 214。补全一次就到 214。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "One tick reaches 24. Walking on converges to 214. Completion answers 214 in one call.", font=small, fill=(139, 148, 158))
    left, top, right, bottom = 140, 170, 1600, 720
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    closure = rec["closure"]
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - frac * (bottom - top)
        draw.line((left, y, right, y), fill=(33, 38, 45), width=1)
        draw.text((60, y - 14), f"{int(frac * closure):,}", font=small, fill=(139, 148, 158))
    max_h = max(HORIZONS)
    xs = [left + (p["horizon"] / max_h) * (right - left) for p in rec["points"]]
    ys = [bottom - (p["reach"] / closure) * (bottom - top) for p in rec["points"]]
    draw.line([(left, bottom - (closure / closure) * (bottom - top),), (right, bottom - (closure / closure) * (bottom - top))], fill=(210, 153, 34), width=2)
    draw.line(list(zip(xs, ys)), fill=(63, 185, 80), width=5)
    for x, y, p in zip(xs, ys, rec["points"]):
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(63, 185, 80))
    marks = ((1, "tick 一步 24", -140), (rec["steps_to_closure"], f"close 收敛 {closure}", 12))
    for mark, label, dx in marks:
        x = left + (mark / max_h) * (right - left)
        draw.line([(x, top), (x, bottom)], fill=(48, 54, 61), width=1)
        draw.text((x + dx, bottom + 12), f"h={mark}", font=small, fill=(139, 148, 158))
        draw.text((x + dx, bottom + 40), label, font=body, fill=(63, 185, 80))
    draw.text((right - 420, top + 16), "completion 补全: 214, one call", font=body, fill=(210, 153, 34))
    draw.text((36, bottom + 72), "x: horizon 步数   y: reach 可达数", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    reaches = [p["reach"] for p in rec["points"]]
    if rec["one_tick"] != 24 or rec["closure"] != 214:
        raise SystemExit("horizon endpoints moved")
    if reaches[0] != 8:
        raise SystemExit("horizon-0 must equal the 8 measured facts")
    if not all(later >= first for first, later in zip(reaches, reaches[1:])):
        raise SystemExit("reach does not grow with horizon")
    if reaches[-1] != 214:
        raise SystemExit("horizon 256 did not meet the closure")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "horizon.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
