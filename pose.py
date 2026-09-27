"""A picture is new when the place changes or the grip changes.

A delivery copies both. It is the same picture only when the place and
the grip are both already what their screen shows. A delivery that
leaves the place and changes the grip is a new picture of the same
place. The earlier count of unchanged places still stands. It is not,
by itself, a count of unchanged pictures.

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
    local = False
    theirs = False
    acc = {"still": 0, "grip_only": 0, "place_only": 0, "both": 0, "deliveries": 0, "overshoot": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if finger is not None:
            local = finger == 0
        if rng.random() >= DROP:
            if hand < shown:
                acc["overshoot"] += 1
            acc["deliveries"] += 1
            place_same = hand == shown
            grip_same = local == theirs
            if place_same and grip_same:
                acc["still"] += 1
            elif place_same:
                acc["grip_only"] += 1
            elif grip_same:
                acc["place_only"] += 1
            else:
                acc["both"] += 1
            shown = hand
            theirs = local
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"still": 0, "grip_only": 0, "place_only": 0, "both": 0, "deliveries": 0, "overshoot": 0, "sessions": 0}
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
        "schema": "worldtick.pose.v1",
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
    draw.text((36, 24), "Same place, new grip, new picture  ·  人没动，握法变了，仍是新的一张", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "位置没变，不等于画面没变。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A delivery is the same picture only when both the place and the grip are already shown.", font=small, fill=(139, 148, 158))
    cards = [
        ("还是这一张", "Place and grip unchanged", f"{s['still']:,}", (63, 185, 80)),
        ("人没动，握法变了", "Same place, new grip", f"{s['grip_only']:,}", (218, 54, 51)),
        ("人走了，握法没变", "New place, same grip", f"{s['place_only']:,}", (121, 192, 255)),
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
        raise SystemExit(f"pose cores disagree: {s}")
    if s["still"] + s["grip_only"] + s["place_only"] + s["both"] != s["deliveries"]:
        raise SystemExit(f"pose deliveries do not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"a delivery ran ahead: {s}")
    pinned = (43522, 4442, 50877, 13357, 112198)
    got = (s["still"], s["grip_only"], s["place_only"], s["both"], s["deliveries"])
    if got != pinned:
        raise SystemExit(f"pose counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "pose.png")
    out = ROOT / "results" / "POSE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
