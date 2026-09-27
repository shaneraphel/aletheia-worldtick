"""A closure belongs to the place the hand was at.

A finger value of zero that arrives on a step closes the sensor index
after that step. The hand advances on the step only when that value
arrived together with the brain stretch, so the angle and the place
are from the same step. The place shown to the other person is the
last delivered copy. Drawing the closure there, when the copy is
behind, closes a place the hand has already left. The picture that
advances on every step is somewhere else on most of these closures,
and on the last step it is inside the stump.

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
    acc = {
        "closed": 0,
        "same": 0,
        "behind": 0,
        "walk_differs": 0,
        "stump_walk": 0,
        "stump_sensor": 0,
        "stump_shown": 0,
        "behind_sum": 0,
        "open_arrived": 0,
        "no_finger": 0,
        "overshoot": 0,
    }
    for t in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        previous = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - previous > 1:
            raise RuntimeError("the sensor index moved by more than one")
        walked = t + 1
        if rng.random() >= DROP:
            shown = hand
        if shown > hand:
            acc["overshoot"] += 1
        if finger is None:
            acc["no_finger"] += 1
            continue
        if finger != 0:
            acc["open_arrived"] += 1
            continue
        acc["closed"] += 1
        if shown == hand:
            acc["same"] += 1
        else:
            acc["behind"] += 1
            acc["behind_sum"] += hand - shown
        if walked != hand:
            acc["walk_differs"] += 1
        if hand == LAST:
            acc["stump_sensor"] += 1
        if shown == LAST:
            acc["stump_shown"] += 1
        if walked == LAST:
            acc["stump_walk"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "closed": 0,
        "same": 0,
        "behind": 0,
        "walk_differs": 0,
        "stump_walk": 0,
        "stump_sensor": 0,
        "stump_shown": 0,
        "behind_sum": 0,
        "open_arrived": 0,
        "no_finger": 0,
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
        "schema": "worldtick.clasp.v1",
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
    draw.text((36, 24), "The hand closed where you were standing  ·  这一下合在你站的地方", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "合在旧位置上，就合错了地方。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A closure drawn on the place they still have, when that place is behind, closes somewhere you have left.", font=small, fill=(139, 148, 158))
    cards = [
        ("对方已经在这个位置", "Their picture already has the place", f"{s['same']:,}", (63, 185, 80)),
        ("合在他还停着的旧位置", "Drawn on the place they still have", f"{s['behind']:,}", (218, 54, 51)),
        ("每步都走的手握着树桩", "The every-step hand grips the stump", f"{s['stump_walk']:,}", (227, 179, 65)),
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
        raise SystemExit(f"clasp cores disagree: {s}")
    if s["same"] + s["behind"] != s["closed"]:
        raise SystemExit(f"clasp closures do not add up: {s}")
    if s["closed"] + s["open_arrived"] + s["no_finger"] != rec["steps"]:
        raise SystemExit(f"clasp steps do not add up: {s}")
    if s["overshoot"] != 0 or s["stump_sensor"] != 0 or s["stump_shown"] != 0:
        raise SystemExit(f"a closure landed ahead, or on the stump for real: {s}")
    if s["behind_sum"] < s["behind"]:
        raise SystemExit(f"a lagging closure was not behind: {s}")
    pinned = (14138, 10975, 3163, 12958, 915, 3738, 97960, 47902)
    got = (
        s["closed"],
        s["same"],
        s["behind"],
        s["walk_differs"],
        s["stump_walk"],
        s["behind_sum"],
        s["open_arrived"],
        s["no_finger"],
    )
    if got != pinned:
        raise SystemExit(f"clasp counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "clasp.png")
    out = ROOT / "results" / "CLASP.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
