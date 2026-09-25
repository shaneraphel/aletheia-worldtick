"""Dropped EEG suffixes, zero-filled, read as rest.

10,000 random go packets of 8 samples. Dropping the last k samples and
filling zeros classifies rest exactly when the kept sum is 0.
Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from decode import neural_class

SEED = 20260919
N = 10_000
WIDTH = 8
DROPS = tuple(range(0, WIDTH + 1))


def packet(rng: random.Random) -> list[int]:
    go = [rng.choice((0, 1, 2, 3)) for _ in range(WIDTH)]
    if sum(go) == 0:
        go[0] = 1
    return go


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    packets = [packet(rng) for _ in range(n)]
    points = []
    for k in DROPS:
        rest = sum(1 for go in packets if neural_class(go[: WIDTH - k] + [0] * k) == 0)
        points.append({"dropped": k, "n": n, "read_as_rest": rest})
    empty = "raised"
    try:
        neural_class([])
        empty = "accepted"
    except ValueError:
        pass
    return {
        "schema": "worldtick.bcisweep.v1",
        "seed": seed,
        "n": n,
        "width": WIDTH,
        "points": points,
        "empty_packet": empty,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    W, H = 1680, 900
    image = Image.new("RGB", (W, H), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    draw.text((36, 24), "EEG dropout  ·  脑电丢失曲线  ·  10,000 packets, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "丢掉的点越多，补零后被读成静息的越多。丢完 8 个点，全部是静息。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "The more samples dropped, the more zero-filled packets read as rest. All 8 dropped: all rest.", font=small, fill=(139, 148, 158))
    left, top, right, bottom = 140, 170, 1600, 720
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    n = rec["n"]
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - frac * (bottom - top)
        draw.line((left, y, right, y), fill=(33, 38, 45), width=1)
        draw.text((60, y - 14), f"{int(frac * n):,}", font=small, fill=(139, 148, 158))
    xs = [left + (p["dropped"] / WIDTH) * (right - left) for p in rec["points"]]
    ys = [bottom - (p["read_as_rest"] / n) * (bottom - top) for p in rec["points"]]
    draw.line(list(zip(xs, ys)), fill=(63, 185, 80), width=5)
    for x, y, p in zip(xs, ys, rec["points"]):
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(63, 185, 80))
        draw.text((x - 20, bottom + 12), f"{p['dropped']}", font=small, fill=(139, 148, 158))
        if p["dropped"] in (0, 4, 8):
            draw.text((x - 40, y - 44), f"{p['read_as_rest']:,}", font=body, fill=(63, 185, 80))
    draw.text((36, bottom + 44), "x: dropped 丢掉的点数   y: read as rest 被读成静息", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    by_drop = {p["dropped"]: p["read_as_rest"] for p in rec["points"]}
    if by_drop[0] != 0 or by_drop[WIDTH] != N:
        raise SystemExit("bcisweep endpoints moved")
    counts = [p["read_as_rest"] for p in rec["points"]]
    if not all(later >= first for first, later in zip(counts, counts[1:])):
        raise SystemExit("rest count does not grow with dropout")
    if rec["empty_packet"] != "raised":
        raise SystemExit("empty packet accepted")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "bcisweep.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
