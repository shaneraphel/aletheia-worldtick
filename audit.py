"""Post-imputation audit: the missingness signal is gone.

On 10,000 roads, count roads with masked cells, filled maps that still
carry a mask marker (zero by construction), filled maps that match the
true road cell for cell, and roads with an occluded obstacle.
A downstream checker that looks for mask markers catches none of the
wrong maps. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from hidden import road

SEED = 20260919
N = 10_000


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    with_hole = 0
    filled_markers = 0
    exact_match = 0
    occluded = 0
    for _ in range(n):
        true, seen = road(rng)
        if any(s is None for s in seen):
            with_hole += 1
        filled = [0 if s is None else s for s in seen]
        filled_markers += sum(1 for c in filled if c is None)
        if filled == true:
            exact_match += 1
        if any(s is None and t == 1 for s, t in zip(seen, true)):
            occluded += 1
    return {
        "schema": "worldtick.audit.v1",
        "seed": seed,
        "n": n,
        "roads_with_masked_cells": with_hole,
        "filled_maps_with_mask_markers": filled_markers,
        "filled_maps_matching_truth": exact_match,
        "roads_with_occluded_obstacle": occluded,
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
    body = ImageFont.truetype(font_path, 24)
    number = ImageFont.truetype(font_path, 44)
    draw.text((36, 24), "Audit  ·  审计  ·  10,000 roads, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "补完删掉了缺失标记。错图 downstream 看上去和真图一样。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Imputation deletes the mask. Wrong maps look exactly like true maps downstream.", font=small, fill=(139, 148, 158))
    cards = [
        ("有缺失的路", "Roads with masked cells", rec["roads_with_masked_cells"], (210, 153, 34)),
        ("补完后带标记", "Filled maps with markers", rec["filled_maps_with_mask_markers"], (63, 185, 80)),
        ("补完逐格全对", "Filled maps matching truth", rec["filled_maps_matching_truth"], (139, 148, 158)),
        ("藏着障碍的路", "Occluded-obstacle roads", rec["roads_with_occluded_obstacle"], (248, 81, 73)),
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
    if rec["filled_maps_with_mask_markers"] != 0:
        raise SystemExit("a mask marker survived imputation")
    if rec["roads_with_masked_cells"] != N:
        raise SystemExit("masked count moved")
    if rec["roads_with_occluded_obstacle"] != 8564:
        raise SystemExit("occluded count moved")
    if rec["filled_maps_matching_truth"] != 1436:
        raise SystemExit("exact-match count moved")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "audit.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
