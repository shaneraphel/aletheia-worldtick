"""Standing beside someone uses two places that arrived.

Two places on the camp path are beside each other when their index
distance is at most two. Each index step is 0.17 in the clearing, so
two steps is 0.34. The other person starts at index 10. The picture
the user sees moves that person only when their signal arrives, and
moves the hand only when both of its streams arrive. The other picture
moves the hand on every step, and on a missing signal steps the person
toward the hand.

On a missing signal the shown person does not move, so the shown
distance changes only when the hand itself advances. The other picture
can still pull the person into range. Seed 20260919. Ten thousand
sessions, sixteen steps. The same session index uses the same stream
on one core and on many.
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


def toward(place: int, hand: int) -> int:
    if place > hand:
        return place - 1
    if place < hand:
        return place + 1
    return place


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    guess_hand = 0
    person = VISITOR
    guess_person = VISITOR
    acc = {
        "only_guess": 0,
        "only_held": 0,
        "both": 0,
        "apart": 0,
        "you_closed": 0,
        "they_pulled": 0,
        "held_moved_on_miss": 0,
        "guess_shrunk_on_miss": 0,
    }
    for _ in range(STEPS):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        prev_hand, prev_person = hand, person
        prev_guess_hand, prev_guess_person = guess_hand, guess_person
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if guess_hand < LAST:
            guess_hand += 1
        missed = rng.random() < DROP
        if missed:
            guess_person = toward(guess_person, hand)
        elif rng.random() < 0.5:
            person = toward(person, hand)
            guess_person = toward(guess_person, hand)
        held_dist = abs(person - hand)
        guess_dist = abs(guess_person - guess_hand)
        held_near = held_dist <= BESIDE
        guess_near = guess_dist <= BESIDE
        if guess_near and not held_near:
            acc["only_guess"] += 1
        elif held_near and not guess_near:
            acc["only_held"] += 1
        elif held_near and guess_near:
            acc["both"] += 1
        else:
            acc["apart"] += 1
        prev_held = abs(prev_person - prev_hand)
        if prev_held > BESIDE and held_dist <= BESIDE and person == prev_person and hand != prev_hand:
            acc["you_closed"] += 1
        prev_guess = abs(prev_guess_person - prev_guess_hand)
        if missed and prev_guess > BESIDE and guess_dist <= BESIDE and guess_person != prev_guess_person:
            acc["they_pulled"] += 1
        if missed and person != prev_person:
            acc["held_moved_on_miss"] += 1
        if missed and guess_dist < prev_guess:
            acc["guess_shrunk_on_miss"] += 1
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {
        "only_guess": 0,
        "only_held": 0,
        "both": 0,
        "apart": 0,
        "you_closed": 0,
        "they_pulled": 0,
        "held_moved_on_miss": 0,
        "guess_shrunk_on_miss": 0,
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
        "schema": "worldtick.beside.v1",
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
    draw.text((36, 24), "Beside means two path steps  ·  隔两步以内，才算站在一起", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "每步都走的那只手，已经从人身边走过去了。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The hand that moves every step has walked past them. The picture that waits is still beside them.", font=small, fill=(139, 148, 158))
    cards = [
        ("只有猜的说在一起", "Beside only in the guessed picture", f"{s['only_guess']:,}", (218, 54, 51)),
        ("只有留下的说在一起", "Beside only in the picture you see", f"{s['only_held']:,}", (121, 192, 255)),
        ("两张都说在一起", "Beside in both pictures", f"{s['both']:,}", (63, 185, 80)),
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
    parts = ("only_guess", "only_held", "both", "apart")
    if not rec["equal"]:
        raise SystemExit(f"beside cores disagree: {s}")
    if sum(s[key] for key in parts) != rec["steps"]:
        raise SystemExit(f"beside steps do not add up: {s}")
    if s["held_moved_on_miss"] != 0:
        raise SystemExit(f"the person moved with no signal: {s}")
    pinned = (27971, 65303, 4712, 62014, 93274, 3691, 3657, 17000)
    got = (
        s["only_guess"],
        s["only_held"],
        s["both"],
        s["apart"],
        s["only_guess"] + s["only_held"],
        s["you_closed"],
        s["they_pulled"],
        s["guess_shrunk_on_miss"],
    )
    if got != pinned:
        raise SystemExit(f"beside counts moved: {got}")
    figure(rec, ROOT / "docs" / "figures" / "beside.png")
    out = ROOT / "results" / "BESIDE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"serial": s, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
