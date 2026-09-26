"""What they see of you is the last place that was delivered.

The other person stands at index 10. Two places are beside each other
when the index distance is at most two. One picture moves a hand one
index on every step, so after k steps it is at index k. It is beside
them on exactly five steps of every session, then stands at index 16.
The picture they are allowed to have copies the hand the sensors
moved, and only on a step when that copy is delivered. A miss leaves
the previous copy. The delivered index never exceeds the sensor index.

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
from scene import VISITOR

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
LAST = 16
BESIDE = 2


def beside(place: int) -> bool:
    return abs(place - VISITOR) <= BESIDE


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    delivered = 0
    walked = 0
    acc = {
        "only_walk": 0,
        "only_packet": 0,
        "both": 0,
        "neither": 0,
        "walk_beside": 0,
        "packet_beside": 0,
        "differ": 0,
        "ahead": 0,
        "overshoot": 0,
        "lag_sum": 0,
        "deliveries": 0,
        "walk_stump": 0,
        "packet_stump": 0,
    }
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if walked < LAST:
            walked += 1
        if rng.random() >= DROP:
            delivered = hand
            acc["deliveries"] += 1
        packet_near = beside(delivered)
        walk_near = beside(walked)
        acc["packet_beside"] += int(packet_near)
        acc["walk_beside"] += int(walk_near)
        if walk_near and not packet_near:
            acc["only_walk"] += 1
        elif packet_near and not walk_near:
            acc["only_packet"] += 1
        elif walk_near and packet_near:
            acc["both"] += 1
        else:
            acc["neither"] += 1
        if walked != delivered:
            acc["differ"] += 1
        if hand > delivered:
            acc["ahead"] += 1
        if delivered > hand:
            acc["overshoot"] += 1
        acc["lag_sum"] += hand - delivered
        acc["walk_stump"] += int(walked == LAST)
        acc["packet_stump"] += int(delivered == LAST)
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "only_walk": 0,
        "only_packet": 0,
        "both": 0,
        "neither": 0,
        "walk_beside": 0,
        "packet_beside": 0,
        "differ": 0,
        "ahead": 0,
        "overshoot": 0,
        "lag_sum": 0,
        "deliveries": 0,
        "walk_stump": 0,
        "packet_stump": 0,
        "sessions": 0,
    }
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
        "schema": "worldtick.relay.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "beside": BESIDE,
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
    disagree = s["only_walk"] + s["only_packet"]
    draw.text((36, 24), "What they see is the packet that arrived  ·  他看见的，是送到的那一包", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "每步都走的那只手，会先从他身边走过去。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The hand that moves every step walks past them. Their picture keeps the last place that was delivered.", font=small, fill=(139, 148, 158))
    cards = [
        ("每步都走，说在旁边", "Beside them, the hand that moves every step", f"{s['walk_beside']:,}", (218, 54, 51)),
        ("最后一包，说在旁边", "Beside them, the last delivered place", f"{s['packet_beside']:,}", (227, 179, 65)),
        ("两张说法不一样", "The two pictures disagree", f"{disagree:,}", (121, 192, 255)),
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
        raise SystemExit(f"relay cores disagree: {s}")
    if s["only_walk"] + s["only_packet"] + s["both"] + s["neither"] != rec["steps"]:
        raise SystemExit(f"relay steps do not add up: {s}")
    if s["overshoot"] != 0:
        raise SystemExit(f"a delivery got ahead of the sensors: {s}")
    if s["walk_beside"] != 5 * s["sessions"] or s["walk_stump"] != s["sessions"]:
        raise SystemExit(f"the every-step hand left its schedule: {s}")
    pinned = (47175, 15006, 2825, 94994, 17831, 62181, 153195, 27192, 112198, 32098, 0)
    got = (
        s["only_walk"],
        s["only_packet"],
        s["both"],
        s["neither"],
        s["packet_beside"],
        s["only_walk"] + s["only_packet"],
        s["differ"],
        s["ahead"],
        s["deliveries"],
        s["lag_sum"],
        s["packet_stump"],
    )
    if got != pinned:
        raise SystemExit(f"relay counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "relay.png")
    out = ROOT / "results" / "RELAY.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
