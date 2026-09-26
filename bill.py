"""A frame is on the bill only when it happened.

Each step writes one line: where the hand is, whether it is drawn as a
grip on a model, and where the other person stands. The guessed line
advances the hand every step, draws a grip when the finger angle is
missing and the hand is inside a model, and walks the other person
toward the hand when their signal is missing. The line the user sees
does none of those unless the signal arrived.

A line that differs is a charge for something that did not happen.
Seed 20260919. Ten thousand sessions, sixteen steps. The same session
index uses the same stream on one core and on many.
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
from grip import models_at
from scene import VISITOR

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
LAST = 16


def toward(place: int, hand: int) -> int:
    if place > hand:
        return place - 1
    if place < hand:
        return place + 1
    return place


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    guess_hand = 0
    person = VISITOR
    guess_person = VISITOR
    acc = {"differ": 0, "hand": 0, "grip": 0, "person": 0, "same": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if guess_hand < LAST:
            guess_hand += 1
        hand_differs = guess_hand != hand
        guess_closed = finger is None or finger == 0
        grip_differs = bool(finger is None and models_at(guess_hand) and guess_closed)
        if rng.random() < DROP:
            guess_person = toward(guess_person, hand)
        elif rng.random() < 0.5:
            person = toward(person, hand)
            guess_person = toward(guess_person, hand)
        person_differs = guess_person != person
        if hand_differs or grip_differs or person_differs:
            acc["differ"] += 1
            acc["hand"] += int(hand_differs)
            acc["grip"] += int(grip_differs)
            acc["person"] += int(person_differs)
        else:
            acc["same"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"differ": 0, "hand": 0, "grip": 0, "person": 0, "same": 0, "sessions": 0}
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
        "schema": "worldtick.bill.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "lines": n * STEPS,
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
    draw.text((36, 24), "Charge only for what happened  ·  没发生的，不开账", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "两张账单。不一样的那一行，是猜出来的。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Two bills. A line that differs is a charge for something that did not happen.", font=small, fill=(139, 148, 158))
    cards = [
        ("账单不一样", "Lines that differ", f"{s['differ']:,}", (218, 54, 51)),
        ("两张账单相同", "Lines that match", f"{s['same']:,}", (63, 185, 80)),
        ("人被写近了", "Lines that walk the other person", f"{s['person']:,}", (121, 192, 255)),
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
        raise SystemExit(f"bill cores disagree: {s}")
    if s["differ"] + s["same"] != rec["lines"]:
        raise SystemExit(f"bill lines do not add up: {s}")
    if (s["differ"], s["same"], s["hand"], s["grip"], s["person"]) != (154689, 5311, 150279, 2989, 107227):
        raise SystemExit(f"bill counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "bill.png")
    out = ROOT / "results" / "BILL.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "lines": rec["lines"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
