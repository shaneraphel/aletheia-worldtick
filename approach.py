"""A missing signal does not walk the other person toward you.

The other person starts at place 10. The hand starts at place 0 and
advances only when both of its streams arrived. When the other person's
signal arrives, they step one place toward the hand with probability
1/2, and otherwise stay. When it does not arrive, the guessed picture
still steps them toward the hand. The picture the user sees leaves them
where they are.

A meeting is a step on which that person and the hand share a place.
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


def toward(place: int, hand: int) -> int:
    if place > hand:
        return place - 1
    if place < hand:
        return place + 1
    return place


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    stay = VISITOR
    guess = VISITOR
    acc = {"invented": 0, "observed": 0, "stay_moved_on_miss": 0, "guess_moved_on_miss": 0}
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        missing = rng.random() < DROP
        before_stay = stay
        before_guess = guess
        if missing:
            guess = toward(guess, hand)
            if guess != before_guess:
                acc["guess_moved_on_miss"] += 1
            if stay != before_stay:
                acc["stay_moved_on_miss"] += 1
        elif rng.random() < 0.5:
            stay = toward(stay, hand)
            guess = toward(guess, hand)
        if guess == hand and stay != hand:
            acc["invented"] += 1
        if stay == hand:
            acc["observed"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"invented": 0, "observed": 0, "stay_moved_on_miss": 0, "guess_moved_on_miss": 0, "sessions": 0}
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
        "schema": "worldtick.approach.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "visitor_at": VISITOR,
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
    draw.text((36, 24), "They do not walk over because a signal was missing  ·  没传来，人不过来", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "猜的画面会把这个人带到你面前。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The guessed picture walks them to where you stand. The picture you see does not.", font=small, fill=(139, 148, 158))
    cards = [
        ("猜的画面里碰上了", "Meetings only the guessed picture shows", f"{s['invented']:,}", (218, 54, 51)),
        ("真的走到了同一处", "Meetings both pictures show", f"{s['observed']:,}", (63, 185, 80)),
        ("没传来时人动了", "The person moved while their signal was missing", f"{s['stay_moved_on_miss']:,}", (121, 192, 255)),
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
    if not rec["equal"] or s["stay_moved_on_miss"] != 0:
        raise SystemExit(f"approach failed: {s}")
    if (s["invented"], s["observed"], s["guess_moved_on_miss"]) != (34142, 27605, 38725):
        raise SystemExit(f"approach counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "approach.png")
    out = ROOT / "results" / "APPROACH.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
