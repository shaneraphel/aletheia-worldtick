"""Visual selector versus collision oracle, on the same 16x16 grids.

Two candidate plans per trial: optimistic (masked cells are free) and
pessimistic (masked cells are walls). The visual selector picks the
shorter imagined path, the score a pixel-complete map exposes. The
oracle picks a path that does not cross a true obstacle. Seed 20260919.
This is the selection gap in Yuan et al. (arXiv:2609.24745), measured
here as exact counts rather than as a robot success rate.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from grid2d import N, SEED, bfs, make_grid

ROOT = Path(__file__).resolve().parent


def outcome(path, true) -> str:
    if path is None:
        return "stopped"
    if any(true[y][x] == 1 for x, y in path):
        return "crash"
    return "reached"


def choose(true, seen) -> dict[str, str]:
    filled = [[0 if c is None else c for c in row] for row in seen]
    opt = bfs(lambda p: filled[p[1]][p[0]] == 1)
    pes = bfs(lambda p: seen[p[1]][p[0]] != 0)
    opt_out = outcome(opt, true)
    pes_out = outcome(pes, true)
    # Visual score: a rendered path that exists and is short. Walls hide the path.
    if opt is None and pes is None:
        visual = "stopped"
    elif pes is None or (opt is not None and len(opt) <= len(pes)):
        visual = opt_out
    else:
        visual = pes_out
    if opt_out == "reached" or pes_out == "reached":
        oracle = "reached"
    elif opt_out == "crash" or pes_out == "crash":
        oracle = "crash"
    else:
        oracle = "stopped"
    return {"visual": visual, "oracle": oracle}


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    visual = {"reached": 0, "crash": 0, "stopped": 0}
    oracle = {"reached": 0, "crash": 0, "stopped": 0}
    for _ in range(n):
        true, seen = make_grid(rng)
        picked = choose(true, seen)
        visual[picked["visual"]] += 1
        oracle[picked["oracle"]] += 1
    return {
        "schema": "worldtick.selector.v1",
        "seed": seed,
        "n": n,
        "visual": visual,
        "oracle": oracle,
        "gap_reached": oracle["reached"] - visual["reached"],
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 900), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 24)
    number = ImageFont.truetype(font_path, 44)
    draw.text((36, 24), "Selector gap  ·  选择差距  ·  2,000 grids, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "看起来更短的路，比碰撞先知少到达。差距是选择，不是生成。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "The shorter-looking path reaches less often than a collision oracle. The gap is selection.", font=small, fill=(139, 148, 158))
    cards = [
        ("画面选择到达", "Visual reached", rec["visual"]["reached"], (210, 153, 34)),
        ("先知到达", "Oracle reached", rec["oracle"]["reached"], (63, 185, 80)),
        ("画面选择撞上", "Visual crashes", rec["visual"]["crash"], (248, 81, 73)),
        ("到达差距", "Reached gap", rec["gap_reached"], (121, 192, 255)),
    ]
    max_v = rec["n"]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 160, x + 387, 760), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 190), name, font=body, fill=color)
        draw.text((x + 24, 228), en, font=small, fill=color)
        draw.text((x + 24, 300), f"{value:,}", font=number, fill=(230, 237, 243))
        bar_top = 700 - (value / max_v) * 220
        draw.rectangle((x + 24, bar_top, x + 363, 700), fill=color)
    draw.text((36, 786), f"n = {rec['n']:,}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if (rec["visual"]["reached"], rec["visual"]["crash"], rec["oracle"]["reached"], rec["gap_reached"]) != (500, 1439, 797, 297):
        raise SystemExit("selector counts moved")
    if rec["visual"]["reached"] + rec["visual"]["crash"] + rec["visual"]["stopped"] != rec["n"]:
        raise SystemExit("visual outcomes do not sum")
    figure(rec, ROOT / "docs" / "figures" / "selector.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
