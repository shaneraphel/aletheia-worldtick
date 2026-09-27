"""A skipped place keeps the grip it had, not the grip at the end of the jump.

A delivery that jumps copies only the place and the grip at the end.
The indices in between were sensor places on earlier steps. Each had
a grip while the hand was there. Painting those indices with the grip
from the end closes a place that was open, or opens a place that was
closed.

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
    grip_here = {0: False}
    acc = {
        "skipped": 0,
        "wrong": 0,
        "agree": 0,
        "leaps": 0,
        "closed_on_open": 0,
        "open_on_closed": 0,
        "deliveries": 0,
        "overshoot": 0,
    }
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
        if hand == old:
            grip_here[hand] = local
        else:
            grip_here[hand] = local
        if rng.random() >= DROP:
            if hand < shown:
                acc["overshoot"] += 1
            delta = hand - shown
            acc["deliveries"] += 1
            if delta >= 2:
                acc["leaps"] += 1
                for idx in range(shown + 1, hand):
                    acc["skipped"] += 1
                    past = grip_here[idx]
                    if past != local:
                        acc["wrong"] += 1
                        if local and not past:
                            acc["closed_on_open"] += 1
                        else:
                            acc["open_on_closed"] += 1
                    else:
                        acc["agree"] += 1
            shown = hand
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "skipped": 0,
        "wrong": 0,
        "agree": 0,
        "leaps": 0,
        "closed_on_open": 0,
        "open_on_closed": 0,
        "deliveries": 0,
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
        "schema": "worldtick.blend.v1",
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
    draw.text((36, 24), "Do not paint the jump with the last grip  ·  跳过的几步，不能涂成最后的握法", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "涂成最后的握法，会把当时的手涂反。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A smooth picture of the jump uses the grip from the end. That grip was not the grip at every skipped place.", font=small, fill=(139, 148, 158))
    cards = [
        ("涂成合上，当时张开", "Painted closed. It was open.", f"{s['closed_on_open']:,}", (218, 54, 51)),
        ("涂成张开，当时合上", "Painted open. It was closed.", f"{s['open_on_closed']:,}", (227, 179, 65)),
        ("涂反的位置", "Skipped places painted wrong", f"{s['wrong']:,}", (121, 192, 255)),
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
        raise SystemExit(f"blend cores disagree: {s}")
    if s["wrong"] + s["agree"] != s["skipped"]:
        raise SystemExit(f"blend skips do not add up: {s}")
    if s["closed_on_open"] + s["open_on_closed"] != s["wrong"]:
        raise SystemExit(f"blend errors do not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"a delivery ran ahead: {s}")
    pinned = (12190, 2645, 9545, 10354, 1307, 1338, 112198)
    got = (s["skipped"], s["wrong"], s["agree"], s["leaps"], s["closed_on_open"], s["open_on_closed"], s["deliveries"])
    if got != pinned:
        raise SystemExit(f"blend counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "blend.png")
    out = ROOT / "results" / "BLEND.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
