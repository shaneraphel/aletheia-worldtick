"""A person is in the picture only if their cell was seen.

Two people stand on fixed cells of every map. They do not move, and
the hand is not asked to reach them. If the camera did not see their
cell, they are not drawn. The filled path may still walk through that
cell, because a missing cell was written free.

That is the unsafe social picture: more people, or a shorter way
across the room, produced by filling what was not seen.

Seed 20260919, the same 2,000 maps. The two cells are (4, 4) and (8, 8).
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from decisive import optimistic
from fleet import cuts
from grid2d import N, SEED, make_grid
from room import split_path

ROOT = Path(__file__).resolve().parent
PEOPLE = ((4, 4), (8, 8))


def one_map(true, seen) -> dict:
    path = optimistic(seen) or []
    admitted, _tail = split_path(path, true, seen)
    admitted_set = set(admitted)
    path_set = set(path)
    hidden = 0
    shown = 0
    filled_through_hidden = 0
    drawn_through = 0
    for x, y in PEOPLE:
        if seen[y][x] is None:
            hidden += 1
            if (x, y) in path_set:
                filled_through_hidden += 1
        else:
            shown += 1
            if (x, y) in admitted_set:
                drawn_through += 1
    return {
        "hidden": hidden,
        "shown": shown,
        "filled_through_hidden": filled_through_hidden,
        "drawn_through": drawn_through,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    for _ in range(start):
        make_grid(rng)
    acc = {"hidden": 0, "shown": 0, "filled_through_hidden": 0, "drawn_through": 0, "maps": 0}
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
        "schema": "worldtick.company.v1",
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
    draw.text((36, 24), "Who is in the room  ·  谁在房间里", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "没看见的人不画。补全后的路却会穿过他们。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A person is drawn only if their cell was seen. The filled path may still walk through that cell.", font=small, fill=(139, 148, 158))
    cards = [
        ("看见了，所以在场", "Seen, so present", s["shown"], (63, 185, 80)),
        ("没看见，所以不画", "Unseen, so not drawn", s["hidden"], (121, 192, 255)),
        ("补全的路穿过没看见的人", "Filled path through an unseen person", s["filled_through_hidden"], (248, 81, 73)),
        ("画出的路穿过在场的人", "Drawn path through a seen person", s["drawn_through"], (210, 153, 34)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 170, x + 390, 640), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 18, 198), name, font=body, fill=color)
        draw.text((x + 18, 250), en, font=small, fill=color)
        draw.text((x + 18, 360), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 680), "两个人站在 (4, 4) 和 (8, 8)，不移动，也不要求你走过去。  Two people stand at (4, 4) and (8, 8). They do not move, and you are not asked to reach them.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if not rec["equal"]:
        raise SystemExit("cores disagreed")
    s = rec["serial"]
    if s["shown"] + s["hidden"] != rec["n"] * len(PEOPLE):
        raise SystemExit("people were neither shown nor hidden")
    if (s["hidden"], s["shown"], s["filled_through_hidden"], s["drawn_through"]) != (997, 3003, 19, 2):
        raise SystemExit(f"company counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "company.png")
    out = ROOT / "results" / "COMPANY.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
