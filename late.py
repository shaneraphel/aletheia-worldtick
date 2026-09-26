"""A late signal is not a guess you can show.

Each step a brain stretch and a finger angle arrive or not, independently.
A missing stretch has probability 0.30. When the stretch arrives it is a
movement with probability 1/2. When the angle arrives it is uniform on
0..7, and 0 means the finger is closed.

The picture has two parts: whether the sound is fast, and whether the
finger is drawn closed. The held picture updates a part only when that
part arrived. Before the first arrival the sound stays slow and the
finger is not drawn closed. The guessed picture reads a missing stretch
as rest, and draws a missing finger closed.

The two pictures match on every step where both signals arrived. They
differ only when a missing signal is replaced by a default the held
picture is not already showing.

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


def step(held_fast: bool, held_closed: bool, rng: random.Random) -> tuple[bool, bool, dict]:
    brain_missing = rng.random() < DROP
    finger_missing = rng.random() < DROP
    brain = None if brain_missing else int(rng.random() < 0.5)
    finger = None if finger_missing else rng.randrange(8)
    if brain is None:
        guess_fast = False
        show_fast = held_fast
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
    sound_differs = guess_fast != show_fast
    finger_differs = guess_closed != show_closed
    row = {
        "differ": int(sound_differs or finger_differs),
        "sound_differs": int(sound_differs),
        "finger_differs": int(finger_differs),
        "both_arrived_differ": int(brain is not None and finger is not None and (sound_differs or finger_differs)),
        "one_late": int((brain is None) ^ (finger is None)),
        "both_late": int(brain is None and finger is None),
        "both_arrived": int(brain is not None and finger is not None),
    }
    return held_fast, held_closed, row


def session(rng: random.Random) -> dict:
    held_fast = False
    held_closed = False
    acc = {
        "differ": 0,
        "sound_differs": 0,
        "finger_differs": 0,
        "both_arrived_differ": 0,
        "one_late": 0,
        "both_late": 0,
        "both_arrived": 0,
    }
    for _ in range(STEPS):
        held_fast, held_closed, row = step(held_fast, held_closed, rng)
        for key, value in row.items():
            acc[key] += value
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "differ": 0,
        "sound_differs": 0,
        "finger_differs": 0,
        "both_arrived_differ": 0,
        "one_late": 0,
        "both_late": 0,
        "both_arrived": 0,
        "sessions": 0,
    }
    for i in range(start, stop):
        row = session(random.Random(seed + 10007 * (i + 1)))
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
        "schema": "worldtick.late.v1",
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
    draw.text((36, 24), "A late signal is not a guess  ·  晚到的信号不是一个可以拿来显示的猜测", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "脑电和手指有一边还没到，就先留着上一次真正到过的画面。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "If either the brain stretch or the finger is late, keep the last picture that was actually received.", font=small, fill=(139, 148, 158))
    cards = [
        ("猜测和保留的画面不一样", "The guess and the held picture differ", s["differ"], (218, 54, 51)),
        ("只有一边到了", "Only one of the two arrived", s["one_late"], (210, 153, 34)),
        ("两边都到了却不一样", "Both arrived, and the pictures differ", s["both_arrived_differ"], (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 214), name, font=body, fill=color)
        draw.text((x + 24, 264), en, font=small, fill=color)
        draw.text((x + 24, 370), f"{value:,}", font=number, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"late cores disagree: {s}")
    if not rec["equal"]:
        raise SystemExit(f"late cores disagree: {s}")
    pinned = (58569, 21864, 42417, 0, 67130)
    got = (s["differ"], s["sound_differs"], s["finger_differs"], s["both_arrived_differ"], s["one_late"])
    if got != pinned:
        raise SystemExit(f"late counts moved: {got}")
    if s["one_late"] + s["both_late"] + s["both_arrived"] != rec["steps"]:
        raise SystemExit(f"steps do not add up: {s}")
    figure(rec, ROOT / "docs" / "figures" / "late.png")
    out = ROOT / "results" / "LATE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
