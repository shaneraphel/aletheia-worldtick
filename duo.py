"""Two hands in one room move independently.

Two players share one frame. Each player sends a brain stretch and a
finger angle every step, each missing with probability 0.30,
independently. A stretch that arrives is a movement with probability
1/2. An angle that arrives is uniform on 0..7, and 0 means the finger
is closed. Each hand updates only on its own arrivals: a miss freezes
that hand and nothing else.

Serving A's request before B's, or B's before A's, shows both players
the same pair of hands, because the two updates touch disjoint states.
A player whose streams both miss leaves the other player's hand exactly
as that player's own arrivals dictate.

Seed 20260919. Ten thousand pairs, sixteen steps. The same pair index
uses the same stream on one core and on many.
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
PAIRS = 10000
STEPS = 16
DROP = 0.30


def pair_stream(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for _ in range(STEPS):
        step = []
        for _ in range(2):
            brain = None if rng.random() < DROP else int(rng.random() < 0.5)
            finger = None if rng.random() < DROP else rng.randrange(8)
            step.append((brain, finger))
        out.append(tuple(step))
    return out


def update(held: tuple[bool, bool], req: tuple) -> tuple[bool, bool]:
    fast, closed = held
    brain, finger = req
    if brain is not None:
        fast = brain == 1
    if finger is not None:
        closed = finger == 0
    return fast, closed


def pair(stream: list) -> dict:
    acc = {
        "bothmove": 0,
        "onlyA": 0,
        "onlyB": 0,
        "still": 0,
        "a_dark_b_moves": 0,
        "b_dark_a_moves": 0,
        "order_mismatch": 0,
    }
    held_ab = [(False, False), (False, False)]
    held_ba = [(False, False), (False, False)]
    for req_a, req_b in stream:
        held_ab[0] = update(held_ab[0], req_a)
        held_ab[1] = update(held_ab[1], req_b)
        held_ba[1] = update(held_ba[1], req_b)
        held_ba[0] = update(held_ba[0], req_a)
        if held_ab != held_ba:
            acc["order_mismatch"] += 1
        moved_a = req_a[0] is not None or req_a[1] is not None
        moved_b = req_b[0] is not None or req_b[1] is not None
        if moved_a and moved_b:
            acc["bothmove"] += 1
        elif moved_a:
            acc["onlyA"] += 1
        elif moved_b:
            acc["onlyB"] += 1
        else:
            acc["still"] += 1
        if not moved_a and moved_b:
            acc["a_dark_b_moves"] += 1
        if not moved_b and moved_a:
            acc["b_dark_a_moves"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    keys = ["bothmove", "onlyA", "onlyB", "still", "a_dark_b_moves", "b_dark_a_moves", "order_mismatch"]
    acc = {k: 0 for k in keys}
    acc["pairs"] = 0
    for i in range(start, stop):
        row = pair(pair_stream(i, seed))
        for key in keys:
            acc[key] += row[key]
        acc["pairs"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = PAIRS, seed: int = SEED, workers: int | None = None) -> dict:
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
        "schema": "worldtick.duo.v1",
        "seed": seed,
        "pairs": n,
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
    draw.text((36, 24), "Two hands move independently  ·  一间房里两只手，各动各的", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "谁没到冻谁。先算谁后算谁，两只手一样。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A miss freezes only that hand. Either order shows the same pair.", font=small, fill=(139, 148, 158))
    cards = [
        ("两只手都动了", "Steps where both hands moved", f"{s['bothmove']:,}", (63, 185, 80)),
        ("一只全黑，另一只照动", "One fully dark while the other moves", f"{s['a_dark_b_moves'] + s['b_dark_a_moves']:,}", (121, 192, 255)),
        ("换顺序后不一样", "Steps changed by serving order", f"{s['order_mismatch']:,}", (218, 54, 51)),
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
        raise SystemExit(f"duo cores disagree: {s}")
    pinned = (132416, 13146, 13117, 1321, 0)
    got = (s["bothmove"], s["onlyA"], s["onlyB"], s["still"], s["order_mismatch"])
    if got != pinned:
        raise SystemExit(f"duo counts moved: {got}")
    if (s["a_dark_b_moves"], s["b_dark_a_moves"]) != (s["onlyB"], s["onlyA"]):
        raise SystemExit(f"dark-move identity failed: {s}")
    figure(rec, ROOT / "docs" / "figures" / "duo.png")
    out = ROOT / "results" / "DUO.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
