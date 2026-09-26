"""Being right by luck is not a measurement.

Every step the world draws a true brain value and a true finger value,
whether they arrive or not. The brain is a movement with probability
1/2. The finger is uniform on 0..7, and 0 means closed. Each stream
misses with probability 0.30, independently.

The guessed picture shows the default for whatever is late: rest for a
missing stretch, closed for a missing finger. The held picture shows the
last values that arrived. On a step where something is late, either one
can match the truth by luck. The difference is not how often. The held
picture never presents a default as an arrival.

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

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30


def session_stream(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for _ in range(STEPS):
        brain_missing = rng.random() < DROP
        finger_missing = rng.random() < DROP
        true_brain = int(rng.random() < 0.5)
        true_finger = rng.randrange(8)
        out.append((brain_missing, finger_missing, true_brain, true_finger))
    return out


def session(stream: list) -> dict:
    held_fast = False
    held_closed = False
    acc = {
        "late_steps": 0,
        "guess_right": 0,
        "held_right": 0,
        "brain_missing": 0,
        "brain_lucky": 0,
        "finger_missing": 0,
        "finger_lucky": 0,
        "both_missing": 0,
        "both_lucky": 0,
        "brain_only": 0,
        "finger_only": 0,
        "guess_brain_only": 0,
        "held_brain_only": 0,
        "guess_finger_only": 0,
        "held_finger_only": 0,
        "guess_both": 0,
        "held_both": 0,
    }
    for brain_missing, finger_missing, true_brain, true_finger in stream:
        truth = (true_brain == 1, true_finger == 0)
        if brain_missing:
            guess_fast = False
            show_fast = held_fast
            acc["brain_missing"] += 1
            if true_brain == 0:
                acc["brain_lucky"] += 1
        else:
            guess_fast = true_brain == 1
            show_fast = guess_fast
            held_fast = show_fast
        if finger_missing:
            guess_closed = True
            show_closed = held_closed
            acc["finger_missing"] += 1
            if true_finger == 0:
                acc["finger_lucky"] += 1
        else:
            guess_closed = true_finger == 0
            show_closed = guess_closed
            held_closed = show_closed
        if brain_missing and finger_missing:
            acc["both_missing"] += 1
            if true_brain == 0 and true_finger == 0:
                acc["both_lucky"] += 1
        if brain_missing or finger_missing:
            acc["late_steps"] += 1
            guess_hit = (guess_fast, guess_closed) == truth
            held_hit = (show_fast, show_closed) == truth
            if guess_hit:
                acc["guess_right"] += 1
            if held_hit:
                acc["held_right"] += 1
            if brain_missing and finger_missing:
                if guess_hit:
                    acc["guess_both"] += 1
                if held_hit:
                    acc["held_both"] += 1
            elif brain_missing:
                acc["brain_only"] += 1
                if guess_hit:
                    acc["guess_brain_only"] += 1
                if held_hit:
                    acc["held_brain_only"] += 1
            else:
                acc["finger_only"] += 1
                if guess_hit:
                    acc["guess_finger_only"] += 1
                if held_hit:
                    acc["held_finger_only"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "late_steps": 0,
        "guess_right": 0,
        "held_right": 0,
        "brain_missing": 0,
        "brain_lucky": 0,
        "finger_missing": 0,
        "finger_lucky": 0,
        "both_missing": 0,
        "both_lucky": 0,
        "brain_only": 0,
        "finger_only": 0,
        "guess_brain_only": 0,
        "held_brain_only": 0,
        "guess_finger_only": 0,
        "held_finger_only": 0,
        "guess_both": 0,
        "held_both": 0,
        "sessions": 0,
    }
    for i in range(start, stop):
        row = session(session_stream(i, seed))
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
        "schema": "worldtick.luck.v1",
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
    draw.text((36, 24), "Right by luck is not measured  ·  蒙对不是测到", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "有一边没到，留下的那一版蒙对更多。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "When something is late, the held picture matches the truth more often.", font=small, fill=(139, 148, 158))
    cards = [
        ("有一边没到", "Steps where something is late", f"{s['late_steps']:,}", (121, 192, 255)),
        ("猜全对", "The guess matches the truth", f"{s['guess_right']:,}", (210, 153, 34)),
        ("留全对", "The held picture matches the truth", f"{s['held_right']:,}", (63, 185, 80)),
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
        raise SystemExit(f"luck cores disagree: {s}")
    pinned = (81428, 21801, 48700, 23856, 5978, 875)
    got = (s["late_steps"], s["guess_right"], s["held_right"], s["brain_lucky"], s["finger_lucky"], s["both_lucky"])
    if got != pinned:
        raise SystemExit(f"luck counts moved: {got}")
    split_pinned = (33484, 33670, 16776, 16554, 4150, 26544, 875, 5602)
    split_got = (s["brain_only"], s["finger_only"], s["guess_brain_only"], s["held_brain_only"], s["guess_finger_only"], s["held_finger_only"], s["guess_both"], s["held_both"])
    if split_got != split_pinned:
        raise SystemExit(f"luck splits moved: {split_got}")
    figure(rec, ROOT / "docs" / "figures" / "luck.png")
    out = ROOT / "results" / "LUCK.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
