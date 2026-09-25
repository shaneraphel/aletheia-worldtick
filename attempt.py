"""An attempt can be heard while the hand does not move.

A complete window whose sum is positive is an attempt: the left-right
rate may become 6 clicks a second. If the next cell on the filled path
was not seen, the picture does not step into it. The person hears that
the attempt arrived. The hand stays on the last seen free cell.

A fill would draw that step anyway. The two facts, attempt and unseen
cell, would become one picture of a finished grasp.

This is not a reading of confusion as an emotion, and it is not a
treatment. It is the pair the coach is allowed to show, because both
parts were observed: the window was complete, and the cell was not.

Maps use seed 20260919, the same stream as grid2d.py. Windows use a
second stream, seed 20260920, one window per map.
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
from grid2d import N, SEED, make_grid
from pace import label, packet
from room import split_path
from decisive import optimistic

ROOT = Path(__file__).resolve().parent
WINDOW_SEED = SEED + 1


def classify(true, seen, samples, missing: bool) -> str:
    path = optimistic(seen)
    _admitted, tail = split_path(path, true, seen)
    unseen_next = len(tail) > 0
    if missing:
        return "hold"
    heard = label(samples)
    if heard == "movement" and unseen_next:
        return "attempt_unseen"
    if heard == "movement":
        return "attempt_seen"
    return "rest"


def shard(start: int, stop: int, map_seed: int = SEED, window_seed: int = WINDOW_SEED) -> dict:
    maps = random.Random(map_seed)
    windows = random.Random(window_seed)
    for _ in range(start):
        make_grid(maps)
        packet(windows)
        windows.random()
    counts = {"hold": 0, "attempt_unseen": 0, "attempt_seen": 0, "rest": 0, "maps": 0}
    for _ in range(start, stop):
        true, seen = make_grid(maps)
        samples = packet(windows)
        missing = windows.random() < 0.30
        counts[classify(true, seen, samples, missing)] += 1
        counts["maps"] += 1
    return counts


def _pack(item: tuple[int, int, int, int]) -> dict:
    start, stop, map_seed, window_seed = item
    return shard(start, stop, map_seed, window_seed)


def run(n: int = N, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed, seed + 1)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed, seed + 1) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    return {
        "schema": "worldtick.attempt.v1",
        "seed": seed,
        "window_seed": seed + 1,
        "n": n,
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
    image = Image.new("RGB", (1680, 780), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "Attempt heard  ·  动作被听到，手没有前进", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "窗口完整而且是一次动作，但下一格没看见。画面不把这一下画成抓取。", font=title, fill=(230, 237, 243))
    draw.text((36, 112), "The window was complete and it was a movement, but the next cell was not seen. The picture does not draw a grasp.", font=small, fill=(139, 148, 158))
    cards = [
        ("听到动作，下一格没看见", "Attempt, cell unseen", s["attempt_unseen"], (248, 81, 73)),
        ("听到动作，下一格看得见", "Attempt, cell seen", s["attempt_seen"], (63, 185, 80)),
        ("窗口丢掉，全部保持", "Window dropped, hold", s["hold"], (121, 192, 255)),
        ("完整窗口，不是动作", "Complete, not a movement", s["rest"], (210, 153, 34)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + (i % 4) * 411
        draw.rounded_rectangle((x, 180, x + 390, 680), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 20, 210), name, font=body, fill=color)
        draw.text((x + 20, 260), en, font=small, fill=color)
        draw.text((x + 20, 360), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 720), "这不是情绪读取。两个事实都是观测到的：窗口完整，格子没有被看见。  Not an emotion. Both facts were observed.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"]:
        raise SystemExit("cores disagreed")
    if sum(rec["serial"][k] for k in ("hold", "attempt_unseen", "attempt_seen", "rest")) != rec["n"]:
        raise SystemExit("classes do not cover the maps")
    s = rec["serial"]
    if (s["hold"], s["attempt_unseen"], s["attempt_seen"], s["rest"]) != (572, 630, 22, 776):
        raise SystemExit(f"attempt counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "attempt.png")
    out = ROOT / "results" / "ATTEMPT.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
