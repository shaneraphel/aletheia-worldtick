"""Two frames of the same map.

The held frame paints a cell only when it was seen. The hand sits on
the last seen free cell. Drawing that frame again, with no new
observation, yields the same pixels.

The filled frame paints missing cells as well. Those pixels are the
picture changing when nothing new was measured.

Seed 20260919, the same 2,000 maps. One example pair is saved.
Ten cores must count the same differing frames as one core.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from company import PEOPLE
from decisive import optimistic
from fleet import cuts
from grid2d import H, N, SEED, W, make_grid
from room import split_path

ROOT = Path(__file__).resolve().parent
BG = (14, 17, 22)
FREE = (31, 111, 74)
WALL = (33, 38, 45)
INVENTED = (210, 153, 34)
HIT = (218, 54, 51)
HAND = (230, 237, 243)
PERSON = (121, 192, 255)


def paint(true, seen, filled: bool) -> tuple:
    path = optimistic(seen) or []
    admitted, _tail = split_path(path, true, seen)
    hand = admitted[-1] if admitted else (0, 0)
    if filled and path:
        hand = path[-1]
    cells = []
    for y in range(H):
        for x in range(W):
            if seen[y][x] is None and not filled:
                color = BG
            elif seen[y][x] is None and true[y][x] == 1:
                color = HIT
            elif seen[y][x] is None:
                color = INVENTED
            elif true[y][x] == 1:
                color = WALL
            else:
                color = FREE
            if (x, y) == hand:
                color = HAND
            elif (x, y) in PEOPLE and seen[y][x] is not None:
                color = PERSON
            elif (x, y) in PEOPLE and filled:
                color = HIT
            cells.append(color)
    return tuple(cells)


def invented(frame, seen) -> int:
    n = 0
    i = 0
    for y in range(H):
        for x in range(W):
            if seen[y][x] is None and frame[i] != BG and frame[i] != HAND:
                n += 1
            i += 1
    return n


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    for _ in range(start):
        make_grid(rng)
    differ = 0
    invented_cells = 0
    held_repaint = 0
    maps = 0
    for _ in range(start, stop):
        true, seen = make_grid(rng)
        held = paint(true, seen, False)
        again = paint(true, seen, False)
        filled = paint(true, seen, True)
        maps += 1
        if held != again:
            held_repaint += 1
        if held != filled:
            differ += 1
        invented_cells += invented(filled, seen)
    return {"maps": maps, "differ": differ, "invented_cells": invented_cells, "held_repaint": held_repaint}


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
        "schema": "worldtick.frame.v1",
        "seed": seed,
        "n": n,
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def save_example() -> None:
    from PIL import Image

    rng = random.Random(SEED)
    true, seen = make_grid(rng)
    for name, filled in (("held", False), ("filled", True)):
        frame = paint(true, seen, filled)
        image = Image.new("RGB", (W, H))
        image.putdata(frame)
        image.resize((W * 24, H * 24), Image.Resampling.NEAREST).save(ROOT / "docs" / "figures" / f"frame-{name}.png")


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 720), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "The next frame  ·  下一帧", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "没有新的观测，再画一次，像素不变。补全会改像素。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Draw the held frame twice and the pixels match. The filled frame changes them.", font=small, fill=(139, 148, 158))
    cards = [
        ("再画一次，像素变了", "Held frame changed on repaint", s["held_repaint"], (63, 185, 80)),
        ("补全帧和保持帧不同", "Filled frame differs", s["differ"], (248, 81, 73)),
        ("补上的格子", "Cells painted though unseen", s["invented_cells"], (210, 153, 34)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 210), name, font=body, fill=color)
        draw.text((x + 24, 260), en, font=small, fill=color)
        draw.text((x + 24, 360), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 660), "左：保持帧。右：补全帧。见 frame-held.png 与 frame-filled.png。", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"] or s["held_repaint"] != 0:
        raise SystemExit(f"frame identity failed: {rec}")
    if (s["differ"], s["invented_cells"], s["held_repaint"]) != (2000, 127697, 0):
        raise SystemExit(f"frame counts moved: {s}")
    save_example()
    figure(rec, ROOT / "docs" / "figures" / "frames.png")
    out = ROOT / "results" / "FRAME.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
