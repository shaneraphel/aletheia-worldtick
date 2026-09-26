"""The record replays itself.

Every step logs one row: the brain arrival or nothing, the finger
arrival or nothing. The shown picture is a pure function of those rows.
Two independent replays read the same rows: one walks forward updating
held values, the other recomputes each step from scratch by scanning
all rows from the session start. Both show the online picture on every
step.

A service that bills per frame needs this. The bill is the record, and
the record has to add up when it is recomputed.

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
        finger = None if rng.random() < DROP else rng.randrange(8)
        out.append((brain, finger))
    return out


def apply(held: tuple[bool, bool], row: tuple) -> tuple[bool, bool]:
    fast, closed = held
    brain, finger = row
    if brain is not None:
        fast = brain == 1
    if finger is not None:
        closed = finger == 0
    return fast, closed


def online(stream: list) -> tuple[list, list, dict]:
    held = (False, False)
    shown = []
    record = []
    totals = {"updates": 0, "new": 0, "differ": 0}
    for brain, finger in stream:
        before = held
        held = apply(held, (brain, finger))
        shown.append(held)
        record.append((brain, finger))
        if held != before:
            totals["updates"] += 1
        if brain is not None and finger is not None:
            totals["new"] += 1
        guess = (False if brain is None else brain == 1, True if finger is None else finger == 0)
        if guess != held:
            totals["differ"] += 1
    return shown, record, totals


def replay_forward(record: list) -> list:
    held = (False, False)
    shown = []
    for row in record:
        held = apply(held, row)
        shown.append(held)
    return shown


def replay_rescan(record: list) -> list:
    shown = []
    for end in range(len(record)):
        held = (False, False)
        for row in record[: end + 1]:
            held = apply(held, row)
        shown.append(held)
    return shown


def session(stream: list) -> dict:
    shown, record, totals = online(stream)
    first = replay_forward(record)
    second = replay_rescan(record)
    mismatch = sum(1 for a, b, c in zip(shown, first, second) if not (a == b == c))
    return {
        "replayed": len(record),
        "mismatch": mismatch,
        "clean": int(mismatch == 0),
        "updates": totals["updates"],
        "new": totals["new"],
        "differ": totals["differ"],
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"replayed": 0, "mismatch": 0, "clean": 0, "updates": 0, "new": 0, "differ": 0, "sessions": 0}
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
        "schema": "worldtick.replay.v1",
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
    draw.text((36, 24), "The record replays itself  ·  记下来再算一遍", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "两套算法各算一遍，步步都是在线那一幅。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Two separate routines replay the same rows and show the online picture.", font=small, fill=(139, 148, 158))
    cards = [
        ("重算的步数", "Steps replayed from the record", f"{s['replayed']:,}", (121, 192, 255)),
        ("对不上的步数", "Steps where the three pictures differ", f"{s['mismatch']:,}", (63, 185, 80)),
        ("整段对上的", "Sessions matching on every step", f"{s['clean']:,}/{s['sessions']:,}", (210, 153, 34)),
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
        raise SystemExit(f"replay cores disagree: {s}")
    pinned = (160000, 0, 10000, 71442, 78861, 58450)
    got = (s["replayed"], s["mismatch"], s["clean"], s["updates"], s["new"], s["differ"])
    if got != pinned:
        raise SystemExit(f"replay counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "replay.png")
    out = ROOT / "results" / "REPLAY.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
