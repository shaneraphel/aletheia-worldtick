"""A repeated place is not a new picture.

The place shown to the other person changes only when a delivery copies
a sensor index different from the one already shown. A miss leaves it.
A delivery of the same index leaves it. Asking for a new frame on those
steps has no new place to draw.

This is the same ten thousand sessions as the delivery count: the same
seed, the same stream, one core and many.
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
from grid2d import SEED

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
LAST = 16


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    acc = {"fresh": 0, "again": 0, "deliveries": 0, "repeat_delivery": 0, "ahead": 0, "overshoot": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        previous = shown
        if rng.random() >= DROP:
            shown = hand
            acc["deliveries"] += 1
            if shown == previous:
                acc["repeat_delivery"] += 1
        if shown != previous:
            acc["fresh"] += 1
        else:
            acc["again"] += 1
        if hand > shown:
            acc["ahead"] += 1
        if shown > hand:
            acc["overshoot"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"fresh": 0, "again": 0, "deliveries": 0, "repeat_delivery": 0, "ahead": 0, "overshoot": 0, "sessions": 0}
    for i in range(start, stop):
        row = session(i, seed)
        for key, value in row.items():
            acc[key] += value
        acc["sessions"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
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
        "schema": "worldtick.once.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": DROP,
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
    draw.text((36, 24), "A repeated place is not a new picture  ·  位置没变，就还是这一张", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "位置没变的那一步，不用再画一张。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A step whose place did not change has nothing new to draw.", font=small, fill=(139, 148, 158))
    cards = [
        ("位置变了", "The place changed", f"{s['fresh']:,}", (63, 185, 80)),
        ("位置没变", "The place stayed", f"{s['again']:,}", (227, 179, 65)),
        ("送到了，还是原处", "Delivered, and still the same place", f"{s['repeat_delivery']:,}", (121, 192, 255)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 214), name, font=body, fill=color)
        draw.text((x + 24, 264), en, font=small, fill=color)
        draw.text((x + 24, 370), value, font=number, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"once cores disagree: {s}")
    if s["fresh"] + s["again"] != rec["steps"]:
        raise SystemExit(f"once steps do not add up: {s}")
    if s["fresh"] + s["repeat_delivery"] != s["deliveries"]:
        raise SystemExit(f"once deliveries do not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"a shown place got ahead of the sensors: {s}")
    pinned = (64234, 95766, 47964, 112198, 27192)
    got = (s["fresh"], s["again"], s["repeat_delivery"], s["deliveries"], s["ahead"])
    if got != pinned:
        raise SystemExit(f"once counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "once.png")
    out = ROOT / "results" / "ONCE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
