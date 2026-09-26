"""Another person stands in the camp and does not move.

The path has seventeen places. The other person stands at place 10.
The guessed hand advances on every step, so after sixteen steps it has
passed that place. The hand the user sees advances only when both the
brain stretch and the finger angle arrived. It reaches the person only
when at least ten of the sixteen steps brought both.

Seed 20260919. Ten thousand sessions. The same session index uses the
same stream on one core and on many.
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


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    arrived = 0
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None:
            arrived += 1
    held = min(arrived, STEPS)
    guess = STEPS
    return {
        "held_reaches": int(held >= VISITOR),
        "guess_reaches": int(guess >= VISITOR),
        "only_guess": int(guess >= VISITOR and held < VISITOR),
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"held_reaches": 0, "guess_reaches": 0, "only_guess": 0, "sessions": 0}
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
        "schema": "worldtick.visitor.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "visitor_at": VISITOR,
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
    draw.text((36, 24), "Someone else stands in the camp  ·  营地里还站着一个人", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "他不走。猜的那只手会走到他面前。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "They do not move. The guessed hand walks up to where they stand.", font=small, fill=(139, 148, 158))
    cards = [
        ("猜的手走到了", "The guessed hand reaches them", f"{s['guess_reaches']:,}", (110, 118, 129)),
        ("给用户看的手走到了", "The hand the user sees reaches them", f"{s['held_reaches']:,}", (230, 237, 243)),
        ("只有猜的手走到了", "Only the guessed hand reaches them", f"{s['only_guess']:,}", (121, 192, 255)),
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
        raise SystemExit(f"visitor cores disagree: {s}")
    if (s["held_reaches"], s["guess_reaches"], s["only_guess"]) != (2138, 10000, 7862):
        raise SystemExit(f"visitor counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "visitor.png")
    out = ROOT / "results" / "VISITOR.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
