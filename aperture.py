"""A missing joint sample is not a closed finger.

Code 0 means the finger is closed. A sample is missing with probability
0.30; otherwise the code is uniform on 0..7. The coach keeps the last
code that arrived, and draws nothing closed before the first arrival.
The zero buffer writes 0 on every miss, which closes a finger that was
last seen open, and also closes a finger that has never been seen.

Seed 20260919. Two thousand hands, sixteen packets, five fingers.
The same hand index uses the same stream on one core and on many.
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
HANDS = 2000
PACKETS = 16
FINGERS = 5
DROP = 0.30


def finger_step(last: int | None, sample: int | None) -> tuple[int | None, bool, bool]:
    """Return the coach state, whether the coach draws closed, whether the buffer does.

    The coach stores a received code and never invents 0. The buffer stores 0
    when the sample is missing. A present 0 closes both.
    """
    if sample is None:
        return last, last == 0, True
    return sample, sample == 0, sample == 0


def hand(rng: random.Random) -> dict:
    last = [None] * FINGERS
    invented = 0
    agreed = 0
    absent_closed = 0
    seen_open_closed = 0
    coach_closed = 0
    buffer_closed = 0
    dropped = 0
    unjustified = 0
    received_zero = [False] * FINGERS
    for _ in range(PACKETS):
        for finger in range(FINGERS):
            if rng.random() < DROP:
                sample = None
                dropped += 1
            else:
                sample = rng.randrange(8)
                if sample == 0:
                    received_zero[finger] = True
            state, coach, buffer = finger_step(last[finger], sample)
            last[finger] = state
            if coach and not received_zero[finger]:
                unjustified += 1
            if coach:
                coach_closed += 1
            if buffer:
                buffer_closed += 1
            if coach and buffer:
                agreed += 1
            if buffer and not coach:
                invented += 1
                if state is None:
                    absent_closed += 1
                else:
                    seen_open_closed += 1
    return {
        "invented": invented,
        "agreed": agreed,
        "absent_closed": absent_closed,
        "seen_open_closed": seen_open_closed,
        "coach_closed": coach_closed,
        "buffer_closed": buffer_closed,
        "dropped": dropped,
        "unjustified": unjustified,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "invented": 0,
        "agreed": 0,
        "absent_closed": 0,
        "seen_open_closed": 0,
        "coach_closed": 0,
        "buffer_closed": 0,
        "dropped": 0,
        "unjustified": 0,
        "hands": 0,
    }
    for i in range(start, stop):
        row = hand(random.Random(seed + 10007 * (i + 1)))
        for key, value in row.items():
            acc[key] += value
        acc["hands"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = HANDS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    steps = n * PACKETS * FINGERS
    return {
        "schema": "worldtick.aperture.v1",
        "seed": seed,
        "hands": n,
        "packets": PACKETS,
        "fingers": FINGERS,
        "steps": steps,
        "drop": DROP,
        "workers": len(parts),
        "zero_alloc": list(bytearray(FINGERS)),
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
    draw.text((36, 24), "A missing sample is not a closed finger  ·  没到的采样不是闭合", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "写成零，就把一根没看见的手指画成握上了。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Writing zero draws a finger closed when that closure was not observed.", font=small, fill=(139, 148, 158))
    cards = [
        ("画成闭合，但没测到闭合", "Drawn closed, closure not observed", s["invented"], (218, 54, 51)),
        ("上次张开，这次写成闭合", "Last seen open, then written closed", s["seen_open_closed"], (210, 153, 34)),
        ("从没到过，仍画成闭合", "Never arrived, still drawn closed", s["absent_closed"], (121, 192, 255)),
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
        raise SystemExit(f"aperture cores disagree: {rec}")
    pinned = (43014, 38623, 4391, 19335, 48423)
    got = (s["invented"], s["seen_open_closed"], s["absent_closed"], s["coach_closed"], s["dropped"])
    if got != pinned:
        raise SystemExit(f"aperture counts moved: {got}")
    if s["invented"] + s["agreed"] != s["buffer_closed"]:
        raise SystemExit(f"closure split failed: {s}")
    if s["coach_closed"] != s["agreed"] or s["unjustified"] != 0:
        raise SystemExit(f"coach closure was not an observed zero: {s}")
    if s["absent_closed"] + s["seen_open_closed"] != s["invented"]:
        raise SystemExit(f"invented split failed: {s}")
    if rec["zero_alloc"] != [0, 0, 0, 0, 0]:
        raise SystemExit(f"zero allocation was not closed: {rec['zero_alloc']}")
    figure(rec, ROOT / "docs" / "figures" / "aperture.png")
    out = ROOT / "results" / "APERTURE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
