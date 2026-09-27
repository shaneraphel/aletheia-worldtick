"""A delivery can jump farther than the person moved.

The sensor index advances by at most one step. The place shown to the
other person stays put until a delivery, then copies the sensor index.
If several advances happened since the last copy, their picture jumps
over the indices in between. Those indices were never delivered. A
smooth picture that draws them is not a place they were sent.

Same seed and the same stream as the delivery count. One core and many.
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
    acc = {"stay": 0, "step": 0, "leap": 0, "skipped": 0, "by2": 0, "by3": 0, "maxjump": 0, "deliveries": 0, "overshoot": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        previous = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - previous > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if rng.random() >= DROP:
            delta = hand - shown
            if delta < 0:
                acc["overshoot"] += 1
            acc["deliveries"] += 1
            if delta == 0:
                acc["stay"] += 1
            elif delta == 1:
                acc["step"] += 1
            else:
                acc["leap"] += 1
                acc["skipped"] += delta - 1
                if delta == 2:
                    acc["by2"] += 1
                elif delta == 3:
                    acc["by3"] += 1
            if delta > acc["maxjump"]:
                acc["maxjump"] = delta
            shown = hand
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"stay": 0, "step": 0, "leap": 0, "skipped": 0, "by2": 0, "by3": 0, "maxjump": 0, "deliveries": 0, "overshoot": 0, "sessions": 0}
    for i in range(start, stop):
        row = session(i, seed)
        for key, value in row.items():
            if key == "maxjump":
                acc[key] = max(acc[key], value)
            else:
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
        parallel = {key: (max(p[key] for p in pieces) if key == "maxjump" else sum(p[key] for p in pieces)) for key in serial}
    return {
        "schema": "worldtick.leap.v1",
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
    draw.text((36, 24), "A delivery can jump  ·  人一次只走一步，画面可以一下跳过去", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "跳过的那些位置，没有送到。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The person moves at most one step at a time. Their picture can jump over the steps in between.", font=small, fill=(139, 148, 158))
    cards = [
        ("正好走一步", "Delivered one step ahead", f"{s['step']:,}", (63, 185, 80)),
        ("一下跳过好几步", "Jumped over at least one step", f"{s['leap']:,}", (218, 54, 51)),
        ("被跳过的位置", "Steps that were never sent", f"{s['skipped']:,}", (227, 179, 65)),
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
        raise SystemExit(f"leap cores disagree: {s}")
    if s["stay"] + s["step"] + s["leap"] != s["deliveries"]:
        raise SystemExit(f"leap deliveries do not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"a delivery ran ahead of the sensors: {s}")
    if s["skipped"] < s["leap"]:
        raise SystemExit(f"a leap skipped nothing: {s}")
    pinned = (47964, 53880, 10354, 12190, 8796, 1325, 8, 112198)
    got = (s["stay"], s["step"], s["leap"], s["skipped"], s["by2"], s["by3"], s["maxjump"], s["deliveries"])
    if got != pinned:
        raise SystemExit(f"leap counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "leap.png")
    out = ROOT / "results" / "LEAP.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
