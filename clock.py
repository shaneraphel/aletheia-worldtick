"""Sound and picture share one clock.

On each map, sixteen windows arrive. A dropped window changes neither
the left-right rate nor the frame. A complete window may change the
rate. The frame advances only when that window is a movement and a
seen free cell remains in front of the hand.

After those cells are used, further movements are still heard. The
picture stays on the last seen cell. A fill would keep walking.

Seed 20260919 for the maps. Each map has its own window stream, so
ten cores and one core see the same clocks.
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
from grid2d import N, SEED, make_grid
from pace import MOVE_HZ, REST_HZ, hz_of, label, packet
from room import split_path
from decisive import optimistic

ROOT = Path(__file__).resolve().parent
WINDOWS = 16


def clock_for(true, seen, windows: random.Random) -> dict:
    path = optimistic(seen) or []
    admitted, _tail = split_path(path, true, seen)
    pos = 0
    held = REST_HZ
    frame_moves = 0
    rate_moves = 0
    drop_frame = 0
    drop_rate = 0
    heard_after_end = 0
    for _ in range(WINDOWS):
        samples = packet(windows)
        missing = windows.random() < 0.30
        if missing:
            # Neither clock is allowed to move.
            continue
        target = hz_of(label(samples))
        if target != held:
            rate_moves += 1
            held = target
        if label(samples) == "movement" and pos + 1 < len(admitted):
            pos += 1
            frame_moves += 1
        elif label(samples) == "movement":
            heard_after_end += 1
    # The loops above cannot increment the drop counters. They stay zero
    # unless a later edit assigns during a missing window.
    return {
        "frame_moves": frame_moves,
        "rate_moves": rate_moves,
        "drop_frame": drop_frame,
        "drop_rate": drop_rate,
        "heard_after_end": heard_after_end,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    maps = random.Random(seed)
    for _ in range(start):
        make_grid(maps)
    acc = {key: 0 for key in ("frame_moves", "rate_moves", "drop_frame", "drop_rate", "heard_after_end", "maps")}
    for i in range(start, stop):
        true, seen = make_grid(maps)
        windows = random.Random(seed + 10007 * (i + 1))
        row = clock_for(true, seen, windows)
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
        "schema": "worldtick.clock.v1",
        "seed": seed,
        "n": n,
        "windows": WINDOWS,
        "rest_hz": REST_HZ,
        "movement_hz": MOVE_HZ,
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
    number = ImageFont.truetype(font_path, 44)
    s = rec["serial"]
    draw.text((36, 24), "One clock  ·  一个时钟", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "丢掉窗口时，声音和画面都不动。路走完后，声音还能跟上，画面停住。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A dropped window moves neither. After the seen cells run out, the sound can still follow and the picture stays.", font=small, fill=(139, 148, 158))
    cards = [
        ("丢包时画面移动", "Frame moved on a drop", s["drop_frame"], (63, 185, 80)),
        ("丢包时速度改变", "Rate changed on a drop", s["drop_rate"], (121, 192, 255)),
        ("画面向前的次数", "Picture steps", s["frame_moves"], (210, 153, 34)),
        ("路尽后仍听到的动作", "Heard after the seen path ended", s["heard_after_end"], (248, 81, 73)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 180, x + 390, 640), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 18, 210), name, font=body, fill=color)
        draw.text((x + 18, 268), en, font=small, fill=color)
        draw.text((x + 18, 370), f"{value:,}", font=number, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"]:
        raise SystemExit("cores disagreed")
    s = rec["serial"]
    if s["drop_frame"] != 0 or s["drop_rate"] != 0:
        raise SystemExit("a dropped window moved a clock")
    if (s["frame_moves"], s["rate_moves"], s["heard_after_end"]) != (3665, 10933, 6414):
        raise SystemExit(f"clock counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "clock.png")
    out = ROOT / "results" / "CLOCK.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
