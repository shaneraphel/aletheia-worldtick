"""Some sessions close the hand, and their picture stays open the whole time.

Both pictures start open. A later closure appears on their picture only
when a delivery happens while the hand is still closed. If every closure
in a session ends before a delivery, their picture never leaves open.
The hand did close. They were not sent that fact.

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
    local = False
    ep_grip = False
    ep_steps = 0
    ep_sent = True
    closed = False
    saw_closed = False

    def close_ep(grip: bool, steps: int, sent: bool) -> None:
        nonlocal closed, saw_closed
        if steps == 0 or not grip:
            return
        closed = True
        if sent:
            saw_closed = True

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
            ep_sent = True
    close_ep(ep_grip, ep_steps, ep_sent)
    return {"closed": int(closed), "saw": int(saw_closed), "never": int(closed and not saw_closed), "quiet": int(not closed)}


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"closed": 0, "saw": 0, "never": 0, "quiet": 0, "sessions": 0}
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
        "schema": "worldtick.whole.v1",
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
    draw.text((36, 24), "A whole session can hide every closure  ·  一整段里，他可以没看见合上", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "你合上过。他从头到尾看见的是张开。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Every closure in these sessions ended before a delivery, so their picture stays open.", font=small, fill=(139, 148, 158))
    cards = [
        ("你合上过", "Sessions where you closed", f"{s['closed']:,}", (121, 192, 255)),
        ("他看见了合上", "They saw a closure", f"{s['saw']:,}", (63, 185, 80)),
        ("从头到尾没看见", "They never saw one", f"{s['never']:,}", (218, 54, 51)),
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
        raise SystemExit(f"whole cores disagree: {s}")
    if s["closed"] + s["quiet"] != s["sessions"]:
        raise SystemExit(f"whole sessions do not add up: {s}")
    if s["saw"] + s["never"] != s["closed"]:
        raise SystemExit(f"whole closures do not add up: {s}")
    pinned = (7727, 6878, 849, 2273)
    got = (s["closed"], s["saw"], s["never"], s["quiet"])
    if got != pinned:
        raise SystemExit(f"whole counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "whole.png")
    out = ROOT / "results" / "WHOLE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
