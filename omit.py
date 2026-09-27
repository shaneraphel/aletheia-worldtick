"""A grip that ends before a delivery never appears on their picture.

Both pictures start open. A run of the same grip is on their picture
if it is that initial grip, or if a delivery happens during the run.
A delivery copies the grip that is current then. A later run with no
delivery is never copied. The next delivery, if any, copies a different
grip. Their picture never shows the omitted one.

Same seed and the same stream as the delivery count. One core and many.
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
LAST = 16


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    ep_grip = False
    ep_steps = 0
    ep_sent = True
    acc = {
        "episodes": 0,
        "seen": 0,
        "lost": 0,
        "closed_seen": 0,
        "closed_lost": 0,
        "open_seen": 0,
        "open_lost": 0,
        "lost_steps": 0,
        "closed_lost_steps": 0,
        "deliveries": 0,
        "overshoot": 0,
    }

    def close_ep(grip: bool, steps: int, sent: bool) -> None:
        if steps == 0:
            return
        acc["episodes"] += 1
        acc["seen" if sent else "lost"] += 1
        if not sent:
            acc["lost_steps"] += steps
        if grip:
            acc["closed_seen" if sent else "closed_lost"] += 1
            if not sent:
                acc["closed_lost_steps"] += steps
        else:
            acc["open_seen" if sent else "open_lost"] += 1

    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        new = (finger == 0) if finger is not None else local
        if ep_steps > 0 and new != ep_grip:
            close_ep(ep_grip, ep_steps, ep_sent)
            ep_steps = 0
            ep_sent = False
        ep_grip = new
        local = new
        ep_steps += 1
        if rng.random() >= DROP:
            if hand < shown:
                acc["overshoot"] += 1
            shown = hand
            acc["deliveries"] += 1
            ep_sent = True
    close_ep(ep_grip, ep_steps, ep_sent)
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "episodes": 0,
        "seen": 0,
        "lost": 0,
        "closed_seen": 0,
        "closed_lost": 0,
        "open_seen": 0,
        "open_lost": 0,
        "lost_steps": 0,
        "closed_lost_steps": 0,
        "deliveries": 0,
        "overshoot": 0,
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
        "schema": "worldtick.omit.v1",
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
    draw.text((36, 24), "A grip that ends before it is sent never appears  ·  没送到的那一下，画面上没有", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "合上又张开，中间没送到，他就没看见。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Their picture starts open. A later grip appears there only if a delivery happens while it still holds.", font=small, fill=(139, 148, 158))
    cards = [
        ("合上过，画面上没有", "Closed, and their picture never shows it", f"{s['closed_lost']:,}", (218, 54, 51)),
        ("张开过，画面上没有", "Opened, and their picture never shows it", f"{s['open_lost']:,}", (227, 179, 65)),
        ("这些握法维持的步数", "Steps those omitted grips lasted", f"{s['lost_steps']:,}", (121, 192, 255)),
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
        raise SystemExit(f"omit cores disagree: {s}")
    if s["seen"] + s["lost"] != s["episodes"]:
        raise SystemExit(f"omit episodes do not add up: {s}")
    if s["closed_seen"] + s["closed_lost"] + s["open_seen"] + s["open_lost"] != s["episodes"]:
        raise SystemExit(f"omit kinds do not add up: {s}")
    if s["closed_lost"] + s["open_lost"] != s["lost"] or s["overshoot"] != 0:
        raise SystemExit(f"omit losses do not add up: {s}")
    pinned = (32742, 29571, 3171, 2507, 664, 3751, 2830, 112198)
    got = (
        s["episodes"],
        s["seen"],
        s["lost"],
        s["closed_lost"],
        s["open_lost"],
        s["lost_steps"],
        s["closed_lost_steps"],
        s["deliveries"],
    )
    if got != pinned:
        raise SystemExit(f"omit counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "omit.png")
    out = ROOT / "results" / "OMIT.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
