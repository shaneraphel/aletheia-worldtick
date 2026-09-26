"""A missing finger angle is not a grip on the wood.

The hand walks the camp path. The guessed hand advances every step and,
when the finger angle is missing, is drawn closed. If that step stands
inside a model, the picture is a grip on that model. The hand the user
sees advances only when both streams arrived, and is drawn closed only
when a closed angle actually arrived.

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
from scene import PATH, footprints

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
BOXES = footprints()


def models_at(at: int) -> list[str]:
    x, z = PATH[at]
    return [name for name, x0, x1, z0, z1 in BOXES if x0 <= x <= x1 and z0 <= z <= z1]


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    held_at = 0
    guess_at = 0
    held_closed = False
    acc = {"guess_grip": 0, "held_grip": 0, "guess_stump": 0, "held_stump": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and held_at + 1 < len(PATH):
            held_at += 1
        if guess_at + 1 < len(PATH):
            guess_at += 1
        if finger is not None:
            held_closed = finger == 0
        guess_models = models_at(guess_at)
        held_models = models_at(held_at)
        if finger is None and guess_models:
            acc["guess_grip"] += 1
            if "stump_round.obj" in guess_models:
                acc["guess_stump"] += 1
        if held_closed and held_models:
            acc["held_grip"] += 1
            if "stump_round.obj" in held_models:
                acc["held_stump"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"guess_grip": 0, "held_grip": 0, "guess_stump": 0, "held_stump": 0, "sessions": 0}
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
        "schema": "worldtick.grip.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
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
    draw.text((36, 24), "A missing angle is not a grip  ·  角度没到，不是握住了木头", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "猜的手站在模型里，又被画成握紧。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The guessed hand stands inside a model and is drawn closed.", font=small, fill=(139, 148, 158))
    cards = [
        ("猜的手握住模型", "Guessed grips on a model", f"{s['guess_grip']:,}", (218, 54, 51)),
        ("其中握住树桩", "Of those, grips on the stump", f"{s['guess_stump']:,}", (210, 153, 34)),
        ("给用户看的手握住树桩", "The hand the user sees grips the stump", f"{s['held_stump']:,}", (63, 185, 80)),
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
        raise SystemExit(f"grip cores disagree: {s}")
    if (s["guess_grip"], s["held_grip"], s["guess_stump"], s["held_stump"]) != (2912, 0, 2912, 0):
        raise SystemExit(f"grip counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "grip.png")
    out = ROOT / "results" / "GRIP.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
