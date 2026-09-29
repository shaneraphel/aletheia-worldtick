"""A finger reading can arrive and never enter the picture.

Vanjani, Li, Suliga, Reuss, Geraci, Jiang, and Lioutikov say a shared
clock undersamples the fast sensor and misses a contact that does not
last. The picture here changes on its own schedule, not when the finger
arrives. A reading is current until the next finger arrives. If the
picture is not copied during that interval, the reading never enters.
When nothing is missed, every reading enters on its own step. Discarded
readings do not keep growing once the fingers themselves grow scarce.

Same session seeds as the phrase. The pinned row uses the same miss
rate. One core and many, on the pinned row.
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
KEYS = (
    "arrivals",
    "now",
    "later",
    "dropped",
    "dropped_closed",
    "dropped_changed",
    "dropped_new_close",
    "copied_closed",
)


def session(index: int, drop: float = DROP, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    local = False
    pending = False
    pending_closed = False
    pending_changed = False
    prev_grip = False
    have_grip = False
    acc = {key: 0 for key in KEYS}

    def discard() -> None:
        acc["dropped"] += 1
        if pending_closed:
            acc["dropped_closed"] += 1
            if pending_changed:
                acc["dropped_new_close"] += 1
        if pending_changed:
            acc["dropped_changed"] += 1

    for _ in range(STEPS):
        brain = None if rng.random() < drop else int(rng.random() < 0.5)
        finger = None if rng.random() < drop else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        arrived = finger is not None
        if arrived:
            local = finger == 0
            if pending:
                discard()
            pending = True
            pending_closed = local
            pending_changed = (not have_grip) or (local != prev_grip)
            have_grip = True
            prev_grip = local
            acc["arrivals"] += 1
        if rng.random() >= drop:
            if pending:
                if arrived:
                    acc["now"] += 1
                else:
                    acc["later"] += 1
                if pending_closed:
                    acc["copied_closed"] += 1
                pending = False
    if pending:
        discard()
    return acc


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
        "schema": "worldtick.unread.v1",
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
        "cited": "https://arxiv.org/abs/2606.12105",
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
    draw.text((36, 24), "A finger can arrive and never enter the picture  ·  手指到了，可以再也进不了画面", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "下一次手指来了，上一次还没画进去，这一次就丢了。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Discarded readings rise, then fall, because fewer fingers arrive. The share discarded keeps rising.", font=small, fill=(139, 148, 158))
    cards = [
        ("当步就进了画面", "Readings copied on the step they arrived", f"{s['now']:,}", (63, 185, 80)),
        ("晚一点才进去", "Readings copied before the next finger", f"{s['later']:,}", (227, 179, 65)),
        ("到了，却没进过画面", "Readings the picture never shows", f"{s['dropped']:,}", (218, 54, 51)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 170, x + 500, 520), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 200), name, font=body, fill=color)
        draw.text((x + 24, 250), en, font=small, fill=color)
        draw.text((x + 24, 340), value, font=number, fill=(230, 237, 243))
    draw.text((48, 560), "没进过画面的次数，先升后降。漏掉一半的时候，次数反而少了一点，因为手指自己也少了。", font=body, fill=(230, 237, 243))
    draw.text((48, 596), "Readings the picture never shows. At the highest miss rate the count falls, because fewer fingers arrive.", font=small, fill=(139, 148, 158))
    rows = rec["sweep"]
    peak = max(row["dropped"] for row in rows) or 1
    base, top = 900, 700
    for i, row in enumerate(rows):
        x = 80 + i * 250
        height = int((base - top) * row["dropped"] / peak)
        color = (218, 54, 51) if row["dropped"] else (48, 54, 61)
        draw.rounded_rectangle((x, base - max(height, 2), x + 120, base), radius=8, fill=color)
        draw.text((x + 28, 640), f"{int(row['drop'] * 100)}%", font=body, fill=(230, 237, 243))
        draw.text((x, 910), f"{row['dropped']:,}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    rec["sweep"] = sweep()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"unread cores disagree: {s}")
    if s["now"] + s["later"] + s["dropped"] != s["arrivals"]:
        raise SystemExit(f"unread fates do not add up: {s}")
    pinned = (112098, 78634, 7172, 26292, 3376, 7649, 2966, 410)
    got = (
        s["arrivals"],
        s["now"],
        s["later"],
        s["dropped"],
        s["dropped_closed"],
        s["dropped_changed"],
        s["dropped_new_close"],
        s["dropped_closed"] - s["dropped_new_close"],
    )
    if got != pinned:
        raise SystemExit(f"unread counts moved: {got}")
    curve = [row["dropped"] for row in rec["sweep"]]
    if curve != [0, 12999, 21603, 26292, 28388, 27841]:
        raise SystemExit(f"unread curve moved: {curve}")
    if rec["sweep"][0]["dropped"] != 0 or rec["sweep"][0]["now"] != 160000 or rec["sweep"][0]["later"] != 0:
        raise SystemExit(f"unread at no misses moved: {rec['sweep'][0]}")
    if rec["sweep"][5]["dropped"] != 27841 or rec["sweep"][5]["arrivals"] != 79829:
        raise SystemExit(f"unread half-miss moved: {rec['sweep'][5]}")
    if rec["sweep"][4]["dropped"] != 28388 or rec["sweep"][3]["dropped"] != s["dropped"]:
        raise SystemExit(f"unread peak moved: {rec['sweep']}")
    figure(rec, ROOT / "docs" / "figures" / "unread.png")
    out = ROOT / "results" / "UNREAD.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("arrivals", "now", "later", "dropped", "dropped_closed", "dropped_new_close")}
    json.dump({"serial": shown, "curve": curve, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
