"""The grip they see is the one copied on the last delivery.

Your grip updates when a finger value arrives. Their grip updates
only when a delivery copies it, and that copy sets the two equal.
A step that was not delivered cannot change the grip they see. If
the two differ, you have closed and they still show an open hand,
or you have opened and they still show a closed hand.

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
    acc = {
        "differ": 0,
        "you_closed": 0,
        "you_open": 0,
        "same": 0,
        "unsent_differ": 0,
        "deliveries": 0,
        "delivery_mismatch": 0,
        "overshoot": 0,
    }
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        previous = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - previous > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if finger is not None:
            local = finger == 0
        if rng.random() >= DROP:
            if hand < shown:
                acc["overshoot"] += 1
            shown = hand
            theirs = local
            acc["deliveries"] += 1
            if local != theirs:
                acc["delivery_mismatch"] += 1
        if local != theirs:
            acc["differ"] += 1
            if local:
                acc["you_closed"] += 1
            else:
                acc["you_open"] += 1
            acc["unsent_differ"] += 1
        else:
            acc["same"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "differ": 0,
        "you_closed": 0,
        "you_open": 0,
        "same": 0,
        "unsent_differ": 0,
        "deliveries": 0,
        "delivery_mismatch": 0,
        "overshoot": 0,
        "sessions": 0,
    }
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
        "schema": "worldtick.latch.v1",
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
    draw.text((36, 24), "The grip they see is the last one that was sent  ·  他看见的，是上次送到的握法", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "你已经张开，他还可以看着合上。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Their picture keeps the grip from the last delivery, until the next one is sent.", font=small, fill=(139, 148, 158))
    cards = [
        ("你合上了，他还看着张开", "You have closed. They still show open.", f"{s['you_closed']:,}", (218, 54, 51)),
        ("你张开了，他还看着合上", "You have opened. They still show closed.", f"{s['you_open']:,}", (227, 179, 65)),
        ("两种握法不一样", "The two grips differ", f"{s['differ']:,}", (121, 192, 255)),
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
        raise SystemExit(f"latch cores disagree: {s}")
    if s["you_closed"] + s["you_open"] != s["differ"]:
        raise SystemExit(f"latch sides do not add up: {s}")
    if s["same"] + s["differ"] != rec["steps"]:
        raise SystemExit(f"latch steps do not add up: {s}")
    if s["unsent_differ"] != s["differ"] or s["delivery_mismatch"] != 0 or s["overshoot"] != 0:
        raise SystemExit(f"a delivery changed the grip wrong: {s}")
    pinned = (7739, 4180, 3559, 152261, 112198)
    got = (s["differ"], s["you_closed"], s["you_open"], s["same"], s["deliveries"])
    if got != pinned:
        raise SystemExit(f"latch counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "latch.png")
    out = ROOT / "results" / "LATCH.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
