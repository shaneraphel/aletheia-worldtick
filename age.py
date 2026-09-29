"""The age of the picture is not the age of the hand in it.

Anand, Anand, and Vishe date each sensor by how long its own reading
has been held. A picture is a copy of the place and the grip at one
moment. That copy can be new while the grip inside it is already old,
and a newer finger can arrive without being copied into the picture.
When nothing is missed the two ages agree. As more samples are missed,
a newer finger sits outside the picture more often.

Same session seeds as the phrase. The pinned row uses the same miss
rate. The other rows change only that rate. One core and many, on the
pinned row.
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
RATES = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)


def session(index: int, drop: float = DROP, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    theirs = False
    finger_seen = False
    finger_age = 0
    screen_age = 0
    grip_age = 0
    copied = False
    newer = 0
    fresh_old = 0
    older = 0
    same = 0
    hidden = 0
    grip_steps = 0
    screen_on_grip = 0
    grip_sum = 0
    deliveries = 0
    place_ahead = 0
    place_gap = 0
    for _ in range(STEPS):
        brain = None if rng.random() < drop else int(rng.random() < 0.5)
        finger = None if rng.random() < drop else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if finger is not None:
            local = finger == 0
            finger_age = 0
            finger_seen = True
        elif finger_seen:
            finger_age += 1
        if rng.random() >= drop:
            deliveries += 1
            screen_age = 0
            if finger_seen:
                grip_age = finger_age
                copied = True
            shown = hand
            theirs = local
        else:
            screen_age += 1
            if copied:
                grip_age += 1
        if hand > shown:
            place_ahead += 1
            place_gap += hand - shown
        if copied:
            grip_steps += 1
            screen_on_grip += screen_age
            grip_sum += grip_age
            hidden += grip_age - screen_age
            if grip_age > screen_age:
                older += 1
            else:
                same += 1
            if screen_age == 0 and grip_age > 0:
                fresh_old += 1
            if finger_age < grip_age:
                newer += 1
    return {
        "newer": newer,
        "fresh_old": fresh_old,
        "older": older,
        "same": same,
        "hidden": hidden,
        "grip_steps": grip_steps,
        "screen_on_grip": screen_on_grip,
        "grip_sum": grip_sum,
        "deliveries": deliveries,
        "place_ahead": place_ahead,
        "place_gap": place_gap,
    }


KEYS = (
    "newer",
    "fresh_old",
    "older",
    "same",
    "hidden",
    "grip_steps",
    "screen_on_grip",
    "grip_sum",
    "deliveries",
    "place_ahead",
    "place_gap",
)


def shard(start: int, stop: int, drop: float = DROP, seed: int = SEED) -> dict:
    acc = {key: 0 for key in KEYS}
    for i in range(start, stop):
        row = session(i, drop, seed)
        for key in KEYS:
            acc[key] += row[key]
    acc["sessions"] = stop - start
    acc["steps"] = (stop - start) * STEPS
    return acc


def _pack(item: tuple[int, int, float, int]) -> dict:
    start, stop, drop, seed = item
    return shard(start, stop, drop, seed)


def run(n: int = SESSIONS, drop: float = DROP, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, drop, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, drop, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    return {
        "schema": "worldtick.age.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": drop,
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cited": "https://arxiv.org/abs/2609.07299",
    }


def sweep(n: int = SESSIONS, seed: int = SEED) -> list[dict]:
    rows = []
    for drop in RATES:
        row = shard(0, n, drop, seed)
        row["drop"] = drop
        rows.append(row)
    return rows


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 980), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "The picture's age is not the hand's age  ·  画面的年纪，不是手里那个动作的年纪", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "画面刚写上，不代表这一下也是刚到的。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A newer finger can be here and still not be the hand in the picture. With nothing missed, the two ages agree.", font=small, fill=(139, 148, 158))
    cards = [
        ("手指到了，还没进画面", "Steps where a newer finger is not in the picture", f"{s['newer']:,}", (218, 54, 51)),
        ("画面刚写上，动作已经旧了", "Pictures just written around an older grip", f"{s['fresh_old']:,}", (227, 179, 65)),
        ("动作比画面多出来的步", "Extra steps of age inside the picture", f"{s['hidden']:,}", (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 170, x + 500, 520), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 200), name, font=body, fill=color)
        draw.text((x + 24, 250), en, font=small, fill=color)
        draw.text((x + 24, 340), value, font=number, fill=(230, 237, 243))
    draw.text((48, 560), "手指比画面新的步，随漏掉的比例升高。都不漏的时候，这个数是零。", font=body, fill=(230, 237, 243))
    draw.text((48, 596), "Steps where a newer finger is outside the picture, as more samples are missed. With nothing missed, the count is zero.", font=small, fill=(139, 148, 158))
    rows = rec["sweep"]
    peak = max(row["newer"] for row in rows) or 1
    base = 900
    top = 700
    for i, row in enumerate(rows):
        x = 80 + i * 250
        height = int((base - top) * row["newer"] / peak)
        y0 = base - max(height, 2)
        color = (218, 54, 51) if row["newer"] else (48, 54, 61)
        draw.rounded_rectangle((x, y0, x + 120, base), radius=8, fill=color)
        draw.text((x + 28, 640), f"{int(row['drop'] * 100)}%", font=body, fill=(230, 237, 243))
        draw.text((x, 910), f"{row['newer']:,}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    rec["sweep"] = sweep()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"age cores disagree: {s}")
    if s["deliveries"] != 112198 or s["place_ahead"] != 27192 or s["place_gap"] != 32098:
        raise SystemExit(f"age does not match the deliveries: {s}")
    if s["older"] + s["same"] != s["grip_steps"] or s["grip_sum"] != s["hidden"] + s["screen_on_grip"]:
        raise SystemExit(f"age does not add up: {s}")
    pinned = (32157, 30441, 42252, 109074, 58171, 151326)
    got = (s["newer"], s["fresh_old"], s["older"], s["same"], s["hidden"], s["grip_steps"])
    if got != pinned:
        raise SystemExit(f"age counts moved: {got}")
    if s["steps"] - s["grip_steps"] != 8674:
        raise SystemExit(f"age starting picture moved: {s}")
    curve = [row["newer"] for row in rec["sweep"]]
    if curve != [0, 13244, 24077, 32157, 38449, 42109]:
        raise SystemExit(f"age curve moved: {curve}")
    if rec["sweep"][0]["fresh_old"] != 0 or rec["sweep"][0]["hidden"] != 0 or rec["sweep"][0]["same"] != 160000:
        raise SystemExit(f"age at no misses moved: {rec['sweep'][0]}")
    if rec["sweep"][3]["newer"] != s["newer"] or rec["sweep"][5]["hidden"] != 121322:
        raise SystemExit(f"age sweep does not meet the pinned row: {rec['sweep']}")
    figure(rec, ROOT / "docs" / "figures" / "age.png")
    out = ROOT / "results" / "AGE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("newer", "fresh_old", "older", "same", "hidden", "grip_steps")}
    json.dump({"serial": shown, "curve": curve, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
