"""The sound can change while the picture stays.

The frame is the seen map plus the hand cell. It does not contain the
left-right rate. So a complete window may retune the sound and leave
every pixel where it was, once no seen cell remains in front of the hand.

A dropped window changes neither. Seed 20260919, sixteen windows on
each of the 2,000 maps, the same streams as clock.py.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from clock import WINDOWS
from decisive import optimistic
from fleet import cuts
from grid2d import N, SEED, make_grid
from pace import hz_of, label, packet
from room import split_path

ROOT = Path(__file__).resolve().parent


def reel_for(true, seen, windows: random.Random) -> dict:
    path = optimistic(seen) or []
    admitted, _tail = split_path(path, true, seen)
    pos = 0
    held = 2
    pixel_changes = 0
    rate_only = 0
    drop_pixel = 0
    for _ in range(WINDOWS):
        samples = packet(windows)
        missing = windows.random() < 0.30
        before = pos
        if missing:
            if pos != before:
                drop_pixel += 1
            continue
        target = hz_of(label(samples))
        rate_changed = target != held
        if rate_changed:
            held = target
        stepped = False
        if label(samples) == "movement" and pos + 1 < len(admitted):
            pos += 1
            stepped = True
        if pos != before:
            pixel_changes += 1
        if rate_changed and not stepped:
            rate_only += 1
    return {"pixel_changes": pixel_changes, "rate_only": rate_only, "drop_pixel": drop_pixel}


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    maps = random.Random(seed)
    for _ in range(start):
        make_grid(maps)
    acc = {"pixel_changes": 0, "rate_only": 0, "drop_pixel": 0, "maps": 0}
    for i in range(start, stop):
        true, seen = make_grid(maps)
        windows = random.Random(seed + 10007 * (i + 1))
        row = reel_for(true, seen, windows)
        for key, value in row.items():
            acc[key] += value
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
        "schema": "worldtick.reel.v1",
        "seed": seed,
        "n": n,
        "windows": WINDOWS,
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
    image = Image.new("RGB", (1680, 720), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "Sound without a new frame  ·  声音变了，画面没变", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "左右声可以改。手没有新的可见格子时，像素不动。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The left-right rate may change. If the hand has no new seen cell, the pixels stay.", font=small, fill=(139, 148, 158))
    cards = [
        ("像素变了", "Pixels changed", s["pixel_changes"], (210, 153, 34)),
        ("只改了声音", "Sound changed, picture stayed", s["rate_only"], (121, 192, 255)),
        ("丢包时像素变了", "Pixels changed on a drop", s["drop_pixel"], (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 214), name, font=body, fill=color)
        draw.text((x + 24, 264), en, font=small, fill=color)
        draw.text((x + 24, 370), f"{value:,}", font=number, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"] or rec["serial"]["drop_pixel"] != 0:
        raise SystemExit(f"reel failed: {rec}")
    s = rec["serial"]
    if (s["pixel_changes"], s["rate_only"]) != (3665, 8377):
        raise SystemExit(f"reel counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "reel.png")
    out = ROOT / "results" / "REEL.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
