"""What a session is allowed to keep.

Each map is one row. A dropped window stores no class. The picture
cell is the last cell that was observed free, never a cell the camera
did not see. An attempt that meets an unseen cell is stored as that
pair, not as a finished grasp.

The row is the data the two uses of the game can share: the hand
practice, and the sound that stayed. It is not a diagnosis, and it is
not a recording from a person. It is the shape of the record.

Maps use seed 20260919. Windows use seed 20260920, the same pairing
as attempt.py. Ten cores must write the same counts as one core.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from attempt import WINDOW_SEED, classify
from fleet import cuts
from grid2d import N, SEED, make_grid
from pace import label, packet
from room import split_path
from decisive import optimistic

ROOT = Path(__file__).resolve().parent


def row_for(true, seen, samples, missing: bool) -> dict:
    kind = classify(true, seen, samples, missing)
    path = optimistic(seen)
    admitted, tail = split_path(path, true, seen)
    cell = admitted[-1] if admitted else (0, 0)
    x, y = cell
    return {
        "window": "dropped" if missing else "complete",
        "cls": None if missing else label(samples),
        "cell": [x, y],
        "cell_was_seen_free": seen[y][x] == 0 and true[y][x] == 0,
        "picture_step": kind == "attempt_seen",
        "refused_step": kind == "attempt_unseen",
        "tail": len(tail) > 0,
    }


def shard(start: int, stop: int, map_seed: int = SEED, window_seed: int = WINDOW_SEED) -> dict:
    maps = random.Random(map_seed)
    windows = random.Random(window_seed)
    for _ in range(start):
        make_grid(maps)
        packet(windows)
        windows.random()
    acc = {
        "rows": 0,
        "class_on_drop": 0,
        "unseen_cell": 0,
        "picture_steps": 0,
        "refused_steps": 0,
        "classes_stored": 0,
    }
    for _ in range(start, stop):
        true, seen = make_grid(maps)
        samples = packet(windows)
        missing = windows.random() < 0.30
        row = row_for(true, seen, samples, missing)
        acc["rows"] += 1
        if row["window"] == "dropped" and row["cls"] is not None:
            acc["class_on_drop"] += 1
        if row["window"] == "dropped":
            pass
        else:
            acc["classes_stored"] += 1
        if not row["cell_was_seen_free"]:
            acc["unseen_cell"] += 1
        acc["picture_steps"] += int(row["picture_step"])
        acc["refused_steps"] += int(row["refused_step"])
    return acc


def _pack(item: tuple[int, int, int, int]) -> dict:
    return shard(*item)


def run(n: int = N, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed, WINDOW_SEED)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed, WINDOW_SEED) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    return {
        "schema": "worldtick.ledger.v1",
        "seed": seed,
        "window_seed": WINDOW_SEED,
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
    image = Image.new("RGB", (1680, 720), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "Ledger  ·  允许留下的记录", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "丢掉的窗口不记类别。手的位置不落在没看见的格子上。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "A dropped window stores no class. The hand's cell was seen, and it was free.", font=small, fill=(139, 148, 158))
    cards = [
        ("记下的类别", "Classes stored", s["classes_stored"], (121, 192, 255)),
        ("丢包却记下类别", "Class stored on a drop", s["class_on_drop"], (248, 81, 73)),
        ("手落在没看见的格子", "Hand on an unseen cell", s["unseen_cell"], (210, 153, 34)),
        ("拒绝画成抓取", "Refused as a grasp", s["refused_steps"], (63, 185, 80)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 170, x + 390, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 20, 200), name, font=body, fill=color)
        draw.text((x + 20, 246), en, font=small, fill=color)
        draw.text((x + 20, 340), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text((36, 660), "这不是从人身上采来的数据。这是记录允许长成的形状。  Not data from a person. The shape a record is allowed to have.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit("cores disagreed")
    if s["class_on_drop"] != 0 or s["unseen_cell"] != 0:
        raise SystemExit(f"ledger broke the rule: {s}")
    if s["refused_steps"] != 630 or s["classes_stored"] != 1428:
        raise SystemExit(f"ledger counts moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "ledger.png")
    out = ROOT / "results" / "LEDGER.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
