"""Several bars stacked inside one picture are not the recording.

Catching up on the next new picture plays every bar since the previous
one inside that single step. A picture keeps the tempo of the recording
only when it carries one bar. Anything wider is several steps sounding
at once. On these sessions every session has at least one picture that
wide, and some pictures are asked to carry half the piece.

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
HALF = STEPS // 2


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    theirs = False
    sent = 0
    last = 0
    prev = 0
    hist = [0] * (STEPS + 1)
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
                width = t - prev
                if not 1 <= width <= STEPS:
                    raise RuntimeError("a picture carried a width outside the piece")
                hist[width] += 1
                sent += 1
                prev = t
                last = t
            shown = hand
            theirs = local
    return {
        "hist": hist,
        "sent": sent,
        "tail": STEPS - last,
        "stacked": int(any(hist[i] for i in range(2, STEPS + 1))),
        "half": int(any(hist[i] for i in range(HALF, STEPS + 1))),
        "overshoot": overshoot,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    hist = [0] * (STEPS + 1)
    sent = 0
    tail = 0
    stacked_sessions = 0
    half_sessions = 0
    overshoot = 0
    for i in range(start, stop):
        row = session(i, seed)
        for i_w, count in enumerate(row["hist"]):
            hist[i_w] += count
        sent += row["sent"]
        tail += row["tail"]
        stacked_sessions += row["stacked"]
        half_sessions += row["half"]
        overshoot += row["overshoot"]
    return {
        "hist": hist,
        "sent": sent,
        "tail": tail,
        "stacked_sessions": stacked_sessions,
        "half_sessions": half_sessions,
        "overshoot": overshoot,
        "sessions": stop - start,
    }


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def derive(raw: dict) -> dict:
    hist = raw["hist"]
    sessions = raw["sessions"]
    pictures = sum(hist)
    single = hist[1]
    stacked = sum(hist[2:])
    extra = sum((i - 1) * hist[i] for i in range(len(hist)))
    present = [i for i in range(len(hist)) if hist[i]]
    tick = sessions * STEPS
    return {
        "hist": hist,
        "sessions": sessions,
        "sent": raw["sent"],
        "pictures": pictures,
        "single": single,
        "stacked": stacked,
        "extra": extra,
        "tail": raw["tail"],
        "tick": tick,
        "heard": tick - raw["tail"],
        "stacked_sessions": raw["stacked_sessions"],
        "half_sessions": raw["half_sessions"],
        "widest": max(present) if present else 0,
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
            "tail": sum(p["tail"] for p in pieces),
            "stacked_sessions": sum(p["stacked_sessions"] for p in pieces),
            "half_sessions": sum(p["half_sessions"] for p in pieces),
            "overshoot": sum(p["overshoot"] for p in pieces),
            "sessions": sum(p["sessions"] for p in pieces),
        }
        parallel = derive(merged)
    return {
        "schema": "worldtick.stack.v1",
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
    draw.text((36, 24), "Several bars in one picture are not the recording  ·  一下里放了好几步，就不是这段录音", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "落下的几步叠进下一张画面。每一段里都有这样的一下。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A picture keeps the recording's tempo only when it carries a single step.", font=small, fill=(139, 148, 158))
    cards = [
        ("一次只放一步", "Pictures that keep the recording's tempo", f"{s['single']:,}", (63, 185, 80)),
        ("一下里放了好几步", "Pictures that stack more than one step", f"{s['stacked']:,}", (218, 54, 51)),
        ("一下里放了半首", "Sessions where one picture carries half the piece", f"{s['half_sessions']:,}", (227, 179, 65)),
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
        raise SystemExit(f"stack cores disagree: {s}")
    if s["overshoot"] != 0 or s["sent"] != 68676 or s["tail"] != 11679 or s["extra"] != 79645:
        raise SystemExit(f"stack does not match the phrase: {s}")
    pinned = (28049, 40627, 394, 10000, 15)
    got = (s["single"], s["stacked"], s["half_sessions"], s["stacked_sessions"], s["widest"])
    if got != pinned:
        raise SystemExit(f"stack counts moved: {got}")
    if s["single"] + s["stacked"] != s["pictures"] or s["pictures"] != s["sent"]:
        raise SystemExit(f"stack pictures do not add up: {s}")
    if s["pictures"] + s["extra"] != s["heard"] or s["heard"] + s["tail"] != s["tick"]:
        raise SystemExit(f"stack bars do not add up: {s}")
    if s["hist"] != [0, 28049, 19810, 10748, 5597, 2398, 1176, 504, 228, 97, 37, 15, 11, 3, 2, 1, 0]:
        raise SystemExit(f"stack widths moved: {s['hist']}")
    figure(rec, ROOT / "docs" / "figures" / "stack.png")
    out = ROOT / "results" / "STACK.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("single", "stacked", "extra", "half_sessions", "stacked_sessions", "widest")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
