"""Storing a finger reading is not showing it.

Vanjani, Li, Suliga, Reuss, Geraci, Jiang, and Lioutikov keep a buffer
per sensor and read it as the action is chosen. A picture that looks
only when it is copied still misses a reading that a later finger has
already replaced. The replaced reading can sit in a buffer and never
appear. A smaller set is still waiting when the session ends, so even
the latest reading was never shown. When nothing is missed, neither
case happens.

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
    "over",
    "strand",
    "over_close",
    "strand_close",
    "over_new_close",
    "strand_new_close",
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

    def discard(kind: str) -> None:
        acc[kind] += 1
        if pending_closed:
            acc[kind + "_close"] += 1
            if pending_changed:
                acc[kind + "_new_close"] += 1

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
                discard("over")
            pending = True
            pending_closed = local
            pending_changed = (not have_grip) or (local != prev_grip)
            have_grip = True
            prev_grip = local
            acc["arrivals"] += 1
        if rng.random() >= drop and pending:
            if arrived:
                acc["now"] += 1
            else:
                acc["later"] += 1
            pending = False
    if pending:
        discard("strand")
    return acc


def shard(start: int, stop: int, drop: float = DROP, seed: int = SEED) -> dict:
    acc = {key: 0 for key in KEYS}
    for i in range(start, stop):
        row = session(i, drop, seed)
        for key in KEYS:
            acc[key] += row[key]
    acc["sessions"] = stop - start
    acc["steps"] = (stop - start) * STEPS
    acc["dropped"] = acc["over"] + acc["strand"]
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
        "schema": "worldtick.store.v1",
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
    draw.text((36, 24), "Storing a reading is not showing it  ·  存下来，不等于画出来", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "下一次手指盖住的那一次，换画时已经看不到了。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A buffer can keep the reading. A picture that looks only when it updates still shows the later finger.", font=small, fill=(139, 148, 158))
    cards = [
        ("被下一次手指盖掉", "Readings replaced before the picture looked", f"{s['over']:,}", (218, 54, 51)),
        ("直到结束也没再看", "Readings still waiting when the session ended", f"{s['strand']:,}", (227, 179, 65)),
        ("盖掉的、还没画过的合上", "New closures replaced before they were shown", f"{s['over_new_close']:,}", (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 170, x + 500, 520), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 200), name, font=body, fill=color)
        draw.text((x + 24, 250), en, font=small, fill=color)
        draw.text((x + 24, 340), value, font=number, fill=(230, 237, 243))
    draw.text((48, 560), "被盖掉的次数先升后降。直到结束还在等的那一部分，一直在变多。", font=body, fill=(230, 237, 243))
    draw.text((48, 596), "Readings replaced before the picture looked. The ones still waiting at the end keep growing.", font=small, fill=(139, 148, 158))
    rows = rec["sweep"]
    peak = max(row["over"] for row in rows) or 1
    base, top = 900, 700
    for i, row in enumerate(rows):
        x = 80 + i * 250
        height = int((base - top) * row["over"] / peak)
        color = (218, 54, 51) if row["over"] else (48, 54, 61)
        draw.rounded_rectangle((x, base - max(height, 2), x + 120, base), radius=8, fill=color)
        draw.text((x + 28, 640), f"{int(row['drop'] * 100)}%", font=body, fill=(230, 237, 243))
        draw.text((x, 910), f"{row['over']:,}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    rec["sweep"] = sweep()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"store cores disagree: {s}")
    if s["over"] + s["strand"] != 26292 or s["now"] + s["later"] + s["dropped"] != s["arrivals"]:
        raise SystemExit(f"store does not match the unread count: {s}")
    pinned = (23912, 2380, 2692, 3060, 112098, 78634, 7172)
    got = (s["over"], s["strand"], s["over_new_close"], s["over_close"], s["arrivals"], s["now"], s["later"])
    if got != pinned:
        raise SystemExit(f"store counts moved: {got}")
    if s["over_new_close"] + s["strand_new_close"] != 2966:
        raise SystemExit(f"store closures moved: {s}")
    if [row["over"] for row in rec["sweep"]] != [0, 12089, 19926, 23912, 25568, 24494]:
        raise SystemExit(f"store curve moved: {rec['sweep']}")
    if rec["sweep"][0]["strand"] != 0 or rec["sweep"][5]["strand"] != 3347 or rec["sweep"][1]["strand"] != 910:
        raise SystemExit(f"store waiting curve moved: {rec['sweep']}")
    figure(rec, ROOT / "docs" / "figures" / "store.png")
    out = ROOT / "results" / "STORE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("over", "strand", "over_new_close", "over_close", "dropped")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
