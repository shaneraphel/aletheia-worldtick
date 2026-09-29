"""The stacked bars wear the later hand.

A catch-up that plays the missed steps inside the next picture plays
them with the grip and the place of that picture. A buried step is any
step inside that width except the step the picture arrives. It keeps
the grip and the place it had when it happened. Those often are not
the ones on the picture. A closed hand can be played open, and an open
hand played closed.

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
KEYS = (
    "sent",
    "tail",
    "buried",
    "agree",
    "closed_on_open",
    "open_on_closed",
    "place_differ",
    "both",
    "grip_only",
    "place_only",
    "neither",
    "overshoot",
)


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    theirs = False
    sent = 0
    last = 0
    prev = 0
    overshoot = 0
    grip_at: list[bool] = []
    hand_at: list[int] = []
    acc = {key: 0 for key in KEYS}
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
        grip_at.append(local)
        hand_at.append(hand)
        if rng.random() >= DROP:
            if hand < shown:
                overshoot += 1
            if not (hand == shown and local == theirs):
                for s in range(prev, t - 1):
                    acc["buried"] += 1
                    grip_differs = grip_at[s] != local
                    place_differs = hand_at[s] != hand
                    if grip_at[s] and not local:
                        acc["closed_on_open"] += 1
                    elif (not grip_at[s]) and local:
                        acc["open_on_closed"] += 1
                    else:
                        acc["agree"] += 1
                    if grip_differs and place_differs:
                        acc["both"] += 1
                    elif grip_differs:
                        acc["grip_only"] += 1
                    elif place_differs:
                        acc["place_only"] += 1
                    else:
                        acc["neither"] += 1
                    if place_differs:
                        acc["place_differ"] += 1
                sent += 1
                prev = t
                last = t
            shown = hand
            theirs = local
    acc["sent"] = sent
    acc["tail"] = STEPS - last
    acc["overshoot"] = overshoot
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {key: 0 for key in KEYS}
    for i in range(start, stop):
        row = session(i, seed)
        for key in KEYS:
            acc[key] += row[key]
    acc["sessions"] = stop - start
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
        "schema": "worldtick.paste.v1",
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
    reversed_grip = s["closed_on_open"] + s["open_on_closed"]
    draw.text((36, 24), "The stacked bars wear the later hand  ·  叠进去的步，穿的是后来的手", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "合着的会被听成张开。张开的会被听成合上。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The missed steps are played with the grip and the place of the picture that carries them.", font=small, fill=(139, 148, 158))
    cards = [
        ("握法被听反了", "Buried steps whose grip is reversed", f"{reversed_grip:,}", (218, 54, 51)),
        ("合上被听成张开", "Closed then, played open", f"{s['closed_on_open']:,}", (227, 179, 65)),
        ("已经不在那个位置", "Buried steps at a different place", f"{s['place_differ']:,}", (63, 185, 80)),
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
        raise SystemExit(f"paste cores disagree: {s}")
    if s["overshoot"] != 0 or s["sent"] != 68676 or s["tail"] != 11679 or s["buried"] != 79645:
        raise SystemExit(f"paste does not match the phrase: {s}")
    pinned = (63220, 6262, 10163, 65763, 12558, 3867, 53205, 10015)
    got = (
        s["agree"],
        s["closed_on_open"],
        s["open_on_closed"],
        s["place_differ"],
        s["both"],
        s["grip_only"],
        s["place_only"],
        s["neither"],
    )
    if got != pinned:
        raise SystemExit(f"paste counts moved: {got}")
    if s["agree"] + s["closed_on_open"] + s["open_on_closed"] != s["buried"]:
        raise SystemExit(f"paste grips do not add up: {s}")
    if s["both"] + s["grip_only"] + s["place_only"] + s["neither"] != s["buried"]:
        raise SystemExit(f"paste places do not add up: {s}")
    if s["both"] + s["grip_only"] != s["closed_on_open"] + s["open_on_closed"]:
        raise SystemExit(f"paste reversals do not add up: {s}")
    if s["both"] + s["place_only"] != s["place_differ"]:
        raise SystemExit(f"paste distances do not add up: {s}")
    figure(rec, ROOT / "docs" / "figures" / "paste.png")
    out = ROOT / "results" / "PASTE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("buried", "agree", "closed_on_open", "open_on_closed", "place_differ", "neither")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
