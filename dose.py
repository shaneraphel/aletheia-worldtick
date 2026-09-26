"""Fewer arrivals, fewer new frames.

Six missing rates: 0.00, 0.10, 0.20, 0.30, 0.40, 0.50. Every session
draws one stream of uniforms; each rate thresholds the same uniforms,
so a higher rate misses a superset of what a lower rate misses. The
brain stretch arrives unless its uniform falls below the rate, and then
is a movement with probability 1/2. The finger angle arrives the same
way, and then is uniform on 0..7 with 0 closed.

The frame is new only when both arrive. With nothing late the two
pictures never part, because there is nothing to guess. Each rate reads
the same uniforms with its own threshold, so the columns compare directly.

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

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
RATES = (0.00, 0.10, 0.20, 0.30, 0.40, 0.50)


def session_uniforms(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for _ in range(STEPS):
        brain_miss = rng.random()
        finger_miss = rng.random()
        brain_val = int(rng.random() < 0.5)
        finger_val = rng.randrange(8)
        out.append((brain_miss, finger_miss, brain_val, finger_val))
    return out


def run_rate(uniforms: list, rate: float) -> dict:
    held_fast = False
    held_closed = False
    new = 0
    differ = 0
    for brain_miss, finger_miss, brain_val, finger_val in uniforms:
        brain_missing = brain_miss < rate
        finger_missing = finger_miss < rate
        if brain_missing:
            guess_fast = False
            show_fast = held_fast
        else:
            guess_fast = brain_val == 1
            show_fast = guess_fast
            held_fast = show_fast
        if finger_missing:
            guess_closed = True
            show_closed = held_closed
        else:
            guess_closed = finger_val == 0
            show_closed = guess_closed
            held_closed = show_closed
        if not brain_missing and not finger_missing:
            new += 1
        if (guess_fast, guess_closed) != (show_fast, show_closed):
            differ += 1
    return {"new": new, "differ": differ}


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {f"{r:.2f}": {"new": 0, "differ": 0} for r in RATES}
    for i in range(start, stop):
        uniforms = session_uniforms(i, seed)
        for r in RATES:
            row = run_rate(uniforms, r)
            acc[f"{r:.2f}"]["new"] += row["new"]
            acc[f"{r:.2f}"]["differ"] += row["differ"]
    flat = {}
    for r in RATES:
        flat[f"new_{r:.2f}"] = acc[f"{r:.2f}"]["new"]
        flat[f"differ_{r:.2f}"] = acc[f"{r:.2f}"]["differ"]
    flat["sessions"] = stop - start
    return flat


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
        "schema": "worldtick.dose.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "rates": list(RATES),
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
    image = Image.new("RGB", (1680, 880), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    tiny = ImageFont.truetype(font_path, 15)
    s = rec["serial"]
    draw.text((36, 24), "Fewer arrivals, fewer new frames  ·  越晚，全新的越少", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "同一批随机数，阈值越高，晚得越多。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The same uniforms under higher thresholds. Nothing late: the two pictures never part.", font=small, fill=(139, 148, 158))
    left, top, width, height = 90, 180, 1500, 560
    draw.rectangle((left, top, left + width, top + height), outline=(48, 54, 61), width=2)
    for g in range(5):
        y = top + g * height // 4
        draw.line((left, y, left + width, y), fill=(33, 38, 45), width=1)
        draw.text((left - 76, y - 12), f"{160 - g * 40}k", font=tiny, fill=(139, 148, 158))
    series = [
        ("new", [s[f"new_{r:.2f}"] for r in RATES], (63, 185, 80)),
        ("differ", [s[f"differ_{r:.2f}"] for r in RATES], (218, 54, 51)),
    ]
    names = {"new": "全新的 new", "differ": "不一样 differ"}
    for j, (key, values, color) in enumerate(series):
        pts = []
        for i, v in enumerate(values):
            x = left + (i * width) // (len(RATES) - 1)
            y = top + height - int(v / 160000 * height)
            pts.append((x, y))
        draw.line(pts, fill=color, width=3)
        for x, y in pts:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color)
        lx = left + 1050 + j * 260
        draw.rectangle((lx, top + height + 44, lx + 120, top + height + 60), fill=color)
        draw.text((lx, top + height + 66), names[key], font=small, fill=color)
    for i, r in enumerate(RATES):
        x = left + (i * width) // (len(RATES) - 1)
        draw.text((x - 18, top + height + 8), f"{r:.1f}", font=small, fill=(139, 148, 158))
    draw.text((36, top + height + 66), "晚点 missing rate →", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"dose cores disagree: {s}")
    pinned = (160000, 129652, 102479, 78572, 57683, 40037, 0, 20843, 40359, 58471, 75109, 90720)
    got = tuple(s[f"new_{r:.2f}"] for r in RATES) + tuple(s[f"differ_{r:.2f}"] for r in RATES)
    if got != pinned:
        raise SystemExit(f"dose counts moved: {got}")
    news = [s[f"new_{r:.2f}"] for r in RATES]
    differs = [s[f"differ_{r:.2f}"] for r in RATES]
    if not all(a >= b for a, b in zip(news, news[1:])):
        raise SystemExit(f"new frames are not nested: {news}")
    if not all(a <= b for a, b in zip(differs, differs[1:])):
        raise SystemExit(f"disagreement is not monotone: {differs}")
    figure(rec, ROOT / "docs" / "figures" / "dose.png")
    out = ROOT / "results" / "DOSE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    slim = {k: s[k] for k in sorted(s) if k != "sessions"}
    slim["sessions"] = s["sessions"]
    json.dump({"serial": slim, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
