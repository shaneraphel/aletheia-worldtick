"""Streams that were never the same speed.

The brain stretch arrives every step unless it drops, with probability
0.30. The finger angle is scheduled every third step and never in
between: steps 0, 3, 6, 9, 12, and 15 of each sixteen-step session. When
the stretch arrives it is a movement with probability 1/2. When the
angle arrives it is uniform on 0..7, and 0 means the finger is closed.

The frame is new only on a scheduled step whose stretch also arrived:
at most 6 of 16 steps in a session, even if the brain never drops. The
finger age cycles 0, 1, 2 no matter what the brain does. The held
picture updates each part only on arrival. The guessed picture treats
all sixteen steps as new, reading a missing stretch as rest and drawing
a missing finger closed.

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

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
EVERY = 3


def session_stream(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for step in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        if step % EVERY == 0:
            finger = rng.randrange(8)
        else:
            finger = None
        out.append((brain, finger))
    return out


def session(stream: list) -> dict:
    held_fast = False
    held_closed = False
    acc = {
        "new_frames": 0,
        "finger_age_sum": 0,
        "brain_missing": 0,
        "differ": 0,
    }
    for step, (brain, finger) in enumerate(stream):
        if brain is None:
            guess_fast = False
            show_fast = held_fast
            acc["brain_missing"] += 1
        else:
            guess_fast = brain == 1
            show_fast = guess_fast
            held_fast = show_fast
        if finger is None:
            guess_closed = True
            show_closed = held_closed
        else:
            guess_closed = finger == 0
            show_closed = guess_closed
            held_closed = show_closed
        if brain is not None and finger is not None:
            acc["new_frames"] += 1
        acc["finger_age_sum"] += step % EVERY
        if (guess_fast, guess_closed) != (show_fast, show_closed):
            acc["differ"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"new_frames": 0, "finger_age_sum": 0, "brain_missing": 0, "differ": 0, "sessions": 0}
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
    scheduled = sum(1 for step in range(STEPS) if step % EVERY == 0)
    return {
        "schema": "worldtick.rate.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": DROP,
        "every": EVERY,
        "scheduled_each": scheduled,
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
    draw.text((36, 24), "Streams were never the same speed  ·  两路本来就不是一样快", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "手指三步来一次。画面全新的，一段最多六步。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The finger sends every third step. At most six steps of sixteen are fully new.", font=small, fill=(139, 148, 158))
    cards = [
        ("画面全新的步", "Steps where the frame is fully new", f"{s['new_frames']:,}", (63, 185, 80)),
        ("手指年龄合计", "Finger ages added over every step", f"{s['finger_age_sum']:,}", (210, 153, 34)),
        ("猜和留不一样", "Steps where the guess and the held picture differ", f"{s['differ']:,}", (218, 54, 51)),
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
        raise SystemExit(f"rate cores disagree: {s}")
    pinned = (42145, 150000, 47865, 96605)
    got = (s["new_frames"], s["finger_age_sum"], s["brain_missing"], s["differ"])
    if got != pinned:
        raise SystemExit(f"rate counts moved: {got}")
    if s["finger_age_sum"] != 15 * s["sessions"]:
        raise SystemExit(f"finger ages are not the fixed sawtooth: {s}")
    if s["new_frames"] > 6 * s["sessions"]:
        raise SystemExit(f"more new frames than scheduled steps: {s}")
    figure(rec, ROOT / "docs" / "figures" / "rate.png")
    out = ROOT / "results" / "RATE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
