"""The same 2,000 maps, one core and many cores.

Each worker rebuilds the pinned random stream and plans only its slice.
The crash count has to match the serial walk. A faster schedule is not
allowed to be a different map.

Seed 20260919. Timings are not pinned.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from grid2d import N, SEED, make_grid, walk

ROOT = Path(__file__).resolve().parent


def shard(start: int, stop: int, seed: int = SEED) -> int:
    rng = random.Random(seed)
    for _ in range(start):
        make_grid(rng)
    crashes = 0
    for _ in range(start, stop):
        true, seen = make_grid(rng)
        if walk(true, seen)["opt"] == "crash":
            crashes += 1
    return crashes


def shard_pack(item: tuple[int, int, int]) -> int:
    start, stop, seed = item
    return shard(start, stop, seed)


def cuts(n: int, workers: int) -> list[tuple[int, int]]:
    workers = max(1, min(workers, n))
    size = (n + workers - 1) // workers
    edges = list(range(0, n, size)) + [n]
    return list(zip(edges, edges[1:]))


def run(n: int = N, seed: int = SEED, workers: int | None = None) -> dict:
    workers = os.cpu_count() or 1 if workers is None else workers
    serial = shard(0, n, seed)
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            parallel = sum(pool.map(shard_pack, [(a, b, seed) for a, b in parts]))
    return {
        "schema": "worldtick.fleet.v1",
        "seed": seed,
        "n": n,
        "workers": len(parts),
        "serial_crashes": serial,
        "parallel_crashes": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 720), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 56)
    draw.text((36, 24), "Fleet  ·  多核与单核同一个整数", font=small, fill=(139, 148, 158))
    draw.text((36, 64), "同一批地图，拆开算，撞上的次数必须一样。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Same maps, split across cores. The crash count has to match.", font=small, fill=(139, 148, 158))
    cards = [
        ("单核撞上", "Serial crashes", rec["serial_crashes"], (210, 153, 34)),
        ("多核撞上", "Parallel crashes", rec["parallel_crashes"], (121, 192, 255)),
        ("核数", "Workers", rec["workers"], (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 28, 210), name, font=body, fill=color)
        draw.text((x + 28, 248), en, font=small, fill=color)
        draw.text((x + 28, 340), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 660), f"equal = {rec['equal']}    n = {rec['n']:,}    seed {rec['seed']}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"] or rec["serial_crashes"] != 1439 or rec["parallel_crashes"] != 1439:
        raise SystemExit(f"fleet diverged: {rec}")
    figure(rec, ROOT / "docs" / "figures" / "fleet.png")
    out = ROOT / "results" / "FLEET.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
