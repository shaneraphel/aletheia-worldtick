"""The picture knows how many steps old it is.

Each step a brain stretch and a finger angle arrive or not. A part that
arrived this step is 0 steps old. A part that did not arrive is one step
older than it was. The age of the frame is the older of the two parts:
both arrived means the frame is new, and anything late means the frame
shows something older.

Steps 6, 7, and 8 of every session are a burst: both streams miss all
three. Outside the burst each stream misses with probability 0.30,
independently. When the stretch arrives it is a movement with
probability 1/2. When the angle arrives it is uniform on 0..7, and 0
means the finger is closed. The held picture updates a part only when
that part arrived. The guessed picture reads a missing stretch as rest
and draws a missing finger closed.

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
BURST = (6, 7, 8)


def session_stream(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for step in range(STEPS):
        if step in BURST:
            out.append((None, None))
            continue
        brain_missing = rng.random() < DROP
        finger_missing = rng.random() < DROP
        brain = None if brain_missing else int(rng.random() < 0.5)
        finger = None if finger_missing else rng.randrange(8)
        out.append((brain, finger))
    return out


def session(stream: list) -> dict:
    held_fast = False
    held_closed = False
    brain_age = 0
    finger_age = 0
    acc = {
        "new_frames": 0,
        "age_sum": 0,
        "age_max": 0,
        "differ": 0,
        "burst_frozen": 0,
    }
    before_burst = None
    for step, (brain, finger) in enumerate(stream):
        if step == BURST[0]:
            before_burst = (held_fast, held_closed)
        if brain is None:
            guess_fast = False
            show_fast = held_fast
            brain_age += 1
        else:
            guess_fast = brain == 1
            show_fast = guess_fast
            held_fast = show_fast
            brain_age = 0
        if finger is None:
            guess_closed = True
            show_closed = held_closed
            finger_age += 1
        else:
            guess_closed = finger == 0
            show_closed = guess_closed
            held_closed = show_closed
            finger_age = 0
        frame_age = brain_age if brain_age > finger_age else finger_age
        if frame_age == 0:
            acc["new_frames"] += 1
        acc["age_sum"] += frame_age
        if frame_age > acc["age_max"]:
            acc["age_max"] = frame_age
        if (guess_fast, guess_closed) != (show_fast, show_closed):
            acc["differ"] += 1
        if step in BURST and (held_fast, held_closed) == before_burst:
            acc["burst_frozen"] += 1
    acc["old_session"] = int(acc["age_max"] >= 5)
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "new_frames": 0,
        "age_sum": 0,
        "age_max": 0,
        "differ": 0,
        "burst_frozen": 0,
        "old_session": 0,
        "sessions": 0,
    }
    for i in range(start, stop):
        row = session(session_stream(i, seed))
        for key in ("new_frames", "age_sum", "differ", "burst_frozen", "old_session"):
            acc[key] += row[key]
        if row["age_max"] > acc["age_max"]:
            acc["age_max"] = row["age_max"]
        acc["sessions"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    start, stop, seed = item
    return shard(start, stop, seed)


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial if key != "age_max"}
        parallel["age_max"] = max(p["age_max"] for p in pieces)
    return {
        "schema": "worldtick.stale.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": DROP,
        "burst": list(BURST),
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
    draw.text((36, 24), "The picture knows how old it is  ·  画面知道自己有几步没更新了", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "中间三步两边都没到。画面留着，年龄照涨。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Three steps in the middle bring nothing. The picture stays, and its age still grows.", font=small, fill=(139, 148, 158))
    cards = [
        ("两边都是刚到的", "Frames where both arrived this step", f"{s['new_frames']:,}", (63, 185, 80)),
        ("画面年龄合计", "Frame ages added over every step", f"{s['age_sum']:,}", (210, 153, 34)),
        ("三步全断时画面不动", "Burst steps where the held picture did not move", f"{s['burst_frozen']:,}", (121, 192, 255)),
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
        raise SystemExit(f"stale cores disagree: {s}")
    pinned = (63903, 199886, 12, 75353, 30000, 3939)
    got = (s["new_frames"], s["age_sum"], s["age_max"], s["differ"], s["burst_frozen"], s["old_session"])
    if got != pinned:
        raise SystemExit(f"stale counts moved: {got}")
    if s["burst_frozen"] != 3 * s["sessions"]:
        raise SystemExit(f"held picture moved during a burst: {s}")
    figure(rec, ROOT / "docs" / "figures" / "stale.png")
    out = ROOT / "results" / "STALE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
