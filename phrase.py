"""The phrase does not run ahead of a picture that was sent.

The recording does not switch, and it does not change speed because a
brain stretch looked tense. What can run ahead is the playhead. One
playhead advances on every step. The other advances only when a
delivery changes the place or the grip, which is when their picture is
actually new. After sixteen steps the first playhead has finished in
every session. The second has finished in none of these sessions.

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
    theirs = False
    sent = 0
    still = 0
    overshoot = 0
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if finger is not None:
            local = finger == 0
        if rng.random() >= DROP:
            if hand < shown:
                overshoot += 1
            if hand == shown and local == theirs:
                still += 1
            else:
                sent += 1
            shown = hand
            theirs = local
    return {
        "tick": STEPS,
        "sent": sent,
        "still": still,
        "finished_tick": 1,
        "finished_sent": int(sent == STEPS),
        "behind": int(sent < STEPS // 2),
        "overshoot": overshoot,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "tick": 0,
        "sent": 0,
        "still": 0,
        "finished_tick": 0,
        "finished_sent": 0,
        "behind": 0,
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
        "schema": "worldtick.phrase.v1",
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
    draw.text((36, 24), "The phrase does not run ahead of the picture  ·  乐句不跑在画面前面", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "曲子不换。按每一帧往前拨，八秒会先放完。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The recording stays the same. One playhead advances every step. The other advances only when their picture is new.", font=small, fill=(139, 148, 158))
    cards = [
        ("按每一帧，乐句走完", "Sessions where every-step playhead finishes", f"{s['finished_tick']:,}", (218, 54, 51)),
        ("按新画面，乐句走完", "Sessions where the sent playhead finishes", f"{s['finished_sent']:,}", (63, 185, 80)),
        ("新画面的乐句还在前一半", "Sent playhead still in the first half", f"{s['behind']:,}", (227, 179, 65)),
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
        raise SystemExit(f"phrase cores disagree: {s}")
    if s["tick"] != rec["steps"] or s["overshoot"] != 0:
        raise SystemExit(f"phrase steps do not add up: {s}")
    if s["sent"] + s["still"] != 112198:
        raise SystemExit(f"phrase pictures do not add up: {s}")
    pinned = (68676, 43522, 10000, 0, 6468)
    got = (s["sent"], s["still"], s["finished_tick"], s["finished_sent"], s["behind"])
    if got != pinned:
        raise SystemExit(f"phrase counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "phrase.png")
    out = ROOT / "results" / "PHRASE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
