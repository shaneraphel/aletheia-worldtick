"""How far the hand is from someone, on seen ground and on the fill.

Two people stand at (4, 4) and (8, 8). The hand starts at the last
cell the camera saw to be free. Distance is a walk that stops on
their cell.

On seen ground the walk enters only cells observed free. On the
filled map a missing cell is free, so the walk can be shorter, and
it can arrive where the camera never arrived.

The people do not move. Nobody is asked to reach them. The shorter
number is what a filled picture would call "nearby."

Seed 20260919, the same 2,000 maps. Ten cores must match one core.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from company import PEOPLE
from fleet import cuts
from grid2d import DIRS, H, N, SEED, W, make_grid
from room import split_path
from decisive import optimistic

ROOT = Path(__file__).resolve().parent


def distances(origin: tuple[int, int], enter) -> dict[tuple[int, int], int]:
    dist = {origin: 0}
    queue: deque[tuple[int, int]] = deque([origin])
    while queue:
        here = queue.popleft()
        for dx, dy in DIRS:
            nxt = (here[0] + dx, here[1] + dy)
            if nxt in dist or not (0 <= nxt[0] < W and 0 <= nxt[1] < H):
                continue
            if nxt != origin and not enter(nxt):
                continue
            dist[nxt] = dist[here] + 1
            queue.append(nxt)
    return dist


def one_map(true, seen) -> dict:
    path = optimistic(seen) or []
    admitted, _tail = split_path(path, true, seen)
    origin = admitted[-1] if admitted else (0, 0)
    seen_dist = distances(origin, lambda p: seen[p[1]][p[0]] == 0)
    fill_dist = distances(origin, lambda p: seen[p[1]][p[0]] != 1)
    only_fill = 0
    shorter = 0
    both = 0
    for person in PEOPLE:
        s = seen_dist.get(person)
        f = fill_dist.get(person)
        if f is not None and s is None:
            only_fill += 1
        if f is not None and s is not None:
            both += 1
            if f < s:
                shorter += 1
    return {"only_fill": only_fill, "shorter": shorter, "both": both}


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    for _ in range(start):
        make_grid(rng)
    acc = {"only_fill": 0, "shorter": 0, "both": 0, "maps": 0}
    for _ in range(start, stop):
        true, seen = make_grid(rng)
        row = one_map(true, seen)
        for key, value in row.items():
            acc[key] += value
        acc["maps"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = N, seed: int = SEED, workers: int | None = None) -> dict:
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
        "schema": "worldtick.near.v1",
        "seed": seed,
        "n": n,
        "people": [list(p) for p in PEOPLE],
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
    draw.text((36, 24), "Nearby  ·  离别人有多近", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "补全后的路可以更近。那条更近的路穿过没看见的格子。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The filled walk can be shorter. That shorter walk crosses cells the camera did not see.", font=small, fill=(139, 148, 158))
    cards = [
        ("只有补全能走到", "Reachable only after the fill", s["only_fill"], (248, 81, 73)),
        ("两条路都到，补全更短", "Both arrive, fill is shorter", s["shorter"], (210, 153, 34)),
        ("两条路都到", "Both arrive", s["both"], (121, 192, 255)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 210), name, font=body, fill=color)
        draw.text((x + 24, 260), en, font=small, fill=color)
        draw.text((x + 24, 370), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 660), "人不移动，也不要求你走过去。更近不是更安全。  People do not move, and you are not asked to go to them. Nearer is not safer.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"]:
        raise SystemExit("cores disagreed")
    s = rec["serial"]
    if (s["only_fill"], s["shorter"], s["both"]) != (2301, 560, 1192):
        raise SystemExit(f"near counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "near.png")
    out = ROOT / "results" / "NEAR.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
