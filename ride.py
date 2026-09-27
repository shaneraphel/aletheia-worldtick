"""The ending has to ride on a new picture.

Catching up when the next new picture arrives does not need the number
of pictures still to come. On each new picture it plays, in that one
step, every bar since the previous picture, up to now. It never runs
past the wall clock. It also never plays a bar that comes after the
last new picture, because nothing later arrives to carry it. The eight
seconds are heard through only when the last step is itself a new
picture.

Same seed and the same stream as the phrase. One core and many.
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
from phrase import DROP, LAST, STEPS

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    theirs = False
    sent = 0
    last = 0
    overshoot = 0
    for t in range(1, STEPS + 1):
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
                pass
            else:
                sent += 1
                last = t
            shown = hand
            theirs = local
    return {"sent": sent, "tail": STEPS - last, "overshoot": overshoot}


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    hist = [0] * (STEPS + 1)
    sent = 0
    overshoot = 0
    for i in range(start, stop):
        row = session(i, seed)
        if not 0 <= row["tail"] <= STEPS:
            raise RuntimeError("the unheard ending left the piece")
        hist[row["tail"]] += 1
        sent += row["sent"]
        overshoot += row["overshoot"]
    return {"hist": hist, "sent": sent, "overshoot": overshoot, "sessions": stop - start}


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def derive(raw: dict) -> dict:
    hist = raw["hist"]
    sessions = raw["sessions"]
    sent = raw["sent"]
    tick = sessions * STEPS
    shortfall = tick - sent
    tail = sum(i * hist[i] for i in range(len(hist)))
    present = [i for i in range(len(hist)) if hist[i]]
    return {
        "hist": hist,
        "sessions": sessions,
        "sent": sent,
        "tick": tick,
        "shortfall": shortfall,
        "tail": tail,
        "interior": shortfall - tail,
        "carried": hist[0],
        "quiet": sessions - hist[0],
        "longest": max(present),
        "overshoot": raw["overshoot"],
    }


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = derive(shard(0, n, seed))
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        merged = {
            "hist": [sum(p["hist"][i] for p in pieces) for i in range(STEPS + 1)],
            "sent": sum(p["sent"] for p in pieces),
            "overshoot": sum(p["overshoot"] for p in pieces),
            "sessions": sum(p["sessions"] for p in pieces),
        }
        parallel = derive(merged)
    return {
        "schema": "worldtick.ride.v1",
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
    draw.text((36, 24), "The ending has to ride on a new picture  ·  结尾要搭在一张新画面上", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "下一张新画面只能带到它自己。它后面的几步没有东西可搭。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Catching up on the next picture never plays the bars that come after the last one.", font=small, fill=(139, 148, 158))
    cards = [
        ("结尾没被听见", "Steps after the last new picture", f"{s['tail']:,}", (218, 54, 51)),
        ("挤进前面的画面", "Steps played inside an earlier picture", f"{s['interior']:,}", (227, 179, 65)),
        ("最后一步带上了结尾", "Sessions whose last step is a new picture", f"{s['carried']:,}", (63, 185, 80)),
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
        raise SystemExit(f"ride cores disagree: {s}")
    if s["overshoot"] != 0 or s["sent"] != 68676 or s["shortfall"] != 91324:
        raise SystemExit(f"ride does not match the phrase: {s}")
    pinned = (11679, 79645, 4291, 5709)
    got = (s["tail"], s["interior"], s["carried"], s["quiet"])
    if got != pinned:
        raise SystemExit(f"ride counts moved: {got}")
    if s["tail"] + s["interior"] != s["shortfall"] or s["carried"] + s["quiet"] != s["sessions"]:
        raise SystemExit(f"ride does not add up: {s}")
    if s["hist"] != [4291, 2756, 1444, 770, 358, 193, 86, 52, 25, 10, 11, 2, 0, 2, 0, 0, 0]:
        raise SystemExit(f"ride endings moved: {s['hist']}")
    if s["longest"] != 13 or s["hist"][0] != s["carried"]:
        raise SystemExit(f"ride shape moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "ride.png")
    out = ROOT / "results" / "RIDE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("tail", "interior", "carried", "quiet", "sent", "shortfall")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
