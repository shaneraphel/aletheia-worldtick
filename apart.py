"""The distance on your screen and the distance on theirs are not the same number.

The other person stands at index 10. Your distance is how far your
sensor index is from them. Their distance is how far the last delivered
copy is from them. The copy never runs ahead. The two distances differ
exactly when the copy is behind, except when the two indices are the
same number of steps from them on opposite sides.

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
from scene import VISITOR

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
LAST = 16


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    acc = {"differ": 0, "you_closer": 0, "them_closer": 0, "mirror": 0, "same": 0, "ahead": 0, "overshoot": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if rng.random() >= DROP:
            shown = hand
        you_d = abs(hand - VISITOR)
        them_d = abs(shown - VISITOR)
        if shown > hand:
            acc["overshoot"] += 1
        if hand > shown:
            acc["ahead"] += 1
        if you_d != them_d:
            acc["differ"] += 1
            if you_d < them_d:
                acc["you_closer"] += 1
            else:
                acc["them_closer"] += 1
        else:
            acc["same"] += 1
            if hand != shown:
                if hand + shown != 2 * VISITOR:
                    raise RuntimeError(f"equal distance without a mirror: {hand}, {shown}")
                acc["mirror"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"differ": 0, "you_closer": 0, "them_closer": 0, "mirror": 0, "same": 0, "ahead": 0, "overshoot": 0, "sessions": 0}
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
        "schema": "worldtick.apart.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "visitor": VISITOR,
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
    draw.text((36, 24), "Two screens, two distances  ·  你量到的，和他量到的，不是同一个数", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "你往往比他所以为的更近。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "You are usually closer to them than the place they still have of you.", font=small, fill=(139, 148, 158))
    cards = [
        ("两边距离不一样", "The two distances differ", f"{s['differ']:,}", (218, 54, 51)),
        ("你比他所以为的更近", "You are closer than they think", f"{s['you_closer']:,}", (121, 192, 255)),
        ("他以为你更近", "They think you are closer", f"{s['them_closer']:,}", (227, 179, 65)),
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
        raise SystemExit(f"apart cores disagree: {s}")
    if s["same"] + s["differ"] != rec["steps"]:
        raise SystemExit(f"apart steps do not add up: {s}")
    if s["you_closer"] + s["them_closer"] != s["differ"]:
        raise SystemExit(f"apart sides do not add up: {s}")
    if s["differ"] + s["mirror"] != s["ahead"]:
        raise SystemExit(f"apart lag does not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"their copy got ahead: {s}")
    pinned = (27143, 26761, 382, 49, 132857, 27192)
    got = (s["differ"], s["you_closer"], s["them_closer"], s["mirror"], s["same"], s["ahead"])
    if got != pinned:
        raise SystemExit(f"apart counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "apart.png")
    out = ROOT / "results" / "APART.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
