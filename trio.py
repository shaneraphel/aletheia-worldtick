"""Each stream multiplies the new-frame share.

Three streams: a brain stretch and two finger angles. Each misses with
probability 0.30, independently. A stretch that arrives is a movement
with probability 1/2. An angle that arrives is uniform on 0..7, and 0
means the finger is closed.

The frame is new only when all three arrive, with probability 0.7^3.
Adding the third stream multiplies the two-stream share by 0.7 again.
The held picture updates each part only on arrival. The guessed picture
reads a missing stretch as rest and draws a missing finger closed, no
matter how many streams there are.

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
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger1 = None if rng.random() < DROP else rng.randrange(8)
        finger2 = None if rng.random() < DROP else rng.randrange(8)
        out.append((brain, finger1, finger2))
    return out


def session(stream: list) -> dict:
    held = (False, False, False)
    acc = {"new": 0, "differ": 0, "none": 0}
    for brain, finger1, finger2 in stream:
        arrived = (brain is not None, finger1 is not None, finger2 is not None)
        guess = (
            False if brain is None else brain == 1,
            True if finger1 is None else finger1 == 0,
            True if finger2 is None else finger2 == 0,
        )
        held = (
            held[0] if brain is None else brain == 1,
            held[1] if finger1 is None else finger1 == 0,
            held[2] if finger2 is None else finger2 == 0,
        )
        if all(arrived):
            acc["new"] += 1
        if not any(arrived):
            acc["none"] += 1
        if guess != held:
            acc["differ"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"new": 0, "differ": 0, "none": 0, "sessions": 0}
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
        "schema": "worldtick.trio.v1",
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
    draw.text((36, 24), "Three streams, one new frame  ·  三路都到，才是全新的", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "脑电加两根手指。再加一路，再打七折。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The brain recording and two fingers. Each added stream multiplies by 0.7 again.", font=small, fill=(139, 148, 158))
    cards = [
        ("三路都到的步", "Steps where all three arrived", f"{s['new']:,}", (63, 185, 80)),
        ("一路都没到的步", "Steps where nothing arrived", f"{s['none']:,}", (210, 153, 34)),
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
        raise SystemExit(f"trio cores disagree: {s}")
    pinned = (55321, 85303, 4306)
    if (s["new"], s["differ"], s["none"]) != pinned:
        raise SystemExit(f"trio counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "trio.png")
    out = ROOT / "results" / "TRIO.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
