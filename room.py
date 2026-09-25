"""The picture stops at the last cell the camera saw.

The filled path may continue through masked cells. Those cells are not
drawn. The hand in the scene sits on the last admitted cell, which was
observed free. A later dropout does not move it.

The other people in the room are fixed. They are not a path and they
are not a score. Their presence is the low-demand place. The picture
does not walk the hand through them, and it does not invent a grasp
beyond the camera.

Seed 20260919, the same 2,000 maps as grid2d.py.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from decisive import optimistic
from fleet import cuts
from grid2d import N, SEED, make_grid

ROOT = Path(__file__).resolve().parent


def split_path(path, true, seen):
    if path is None:
        return [], []
    for i, (x, y) in enumerate(path):
        if seen[y][x] is None:
            return path[:i], path[i:]
    return list(path), []


def one_map(true, seen) -> dict:
    path = optimistic(seen)
    admitted, tail = split_path(path, true, seen)
    tail_hits = sum(1 for x, y in tail if true[y][x] == 1)
    admitted_hits = sum(1 for x, y in admitted if true[y][x] == 1)
    return {
        "admitted": len(admitted),
        "tail": len(tail),
        "tail_hits": tail_hits,
        "admitted_hits": admitted_hits,
        "drew_past_camera": int(len(tail) > 0),
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    for _ in range(start):
        make_grid(rng)
    acc = {"admitted": 0, "tail": 0, "tail_hits": 0, "admitted_hits": 0, "drew_past_camera": 0, "maps": 0}
    for _ in range(start, stop):
        true, seen = make_grid(rng)
        row = one_map(true, seen)
        for key in acc:
            if key == "maps":
                continue
            acc[key] += row[key]
        acc["maps"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = N, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    return {
        "schema": "worldtick.room.v1",
        "seed": seed,
        "n": n,
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
    image = Image.new("RGB", (1680, 780), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "The picture stops  ·  画面停在摄像机看见的最后一格", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "补全路径多走的格子不画。手停在已经看见的空地上。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Cells past the camera are not drawn. The hand stays on ground that was seen.", font=small, fill=(139, 148, 158))
    cards = [
        ("画出了没看见的格子", "Drew past the camera", s["drew_past_camera"], (210, 153, 34)),
        ("那段里的真障碍", "Real obstacles in that tail", s["tail_hits"], (248, 81, 73)),
        ("看见的格子里的障碍", "Obstacles in the drawn part", s["admitted_hits"], (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 170, x + 500, 640), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 200), name, font=body, fill=color)
        draw.text((x + 24, 240), en, font=small, fill=color)
        draw.text((x + 24, 340), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 690), f"n = {rec['n']:,}    workers {rec['workers']}    equal = {rec['equal']}", font=small, fill=(139, 148, 158))
    draw.text((36, 724), "别人站在房间里，不移动。画面不把他们当成一条要走的路。  Other people stand in the room. The picture does not turn them into a path.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"]:
        raise SystemExit(f"cores disagreed: {rec['serial']} {rec['parallel']}")
    if rec["serial"]["admitted_hits"] != 0:
        raise SystemExit("the drawn picture entered an obstacle")
    s = rec["serial"]
    if (s["admitted"], s["tail"], s["tail_hits"], s["drew_past_camera"]) != (6657, 53456, 2474, 1938):
        raise SystemExit(f"room counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "room.png")
    out = ROOT / "results" / "ROOM.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
