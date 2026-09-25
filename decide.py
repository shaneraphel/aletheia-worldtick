"""One-step driving decision on 10,000 roads: completed map versus one tick.

Truth: go iff the true next cell is free. Completion goes iff the
hole-filled next cell is free. One tick goes iff the next cell was
measured free, and stops on any hole. Seed 20260919.
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


def decide(true_next: int | None, filled_next: int, seen_next: int | None) -> dict[str, str]:
    _ = true_next
    completion = "go" if filled_next == 0 else "stop"
    tick = "go" if seen_next == 0 else "stop"
    return {"completion": completion, "tick": tick}


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    completion_crashes = 0
    tick_crashes = 0
    tick_extra_stops = 0
    completion_extra_stops = 0
    for _ in range(n):
        true, seen = road(rng)
        filled = 0 if seen[1] is None else seen[1]
        truth = "go" if true[1] == 0 else "stop"
        acts = decide(true[1], filled, seen[1])
        if acts["completion"] == "go" and truth == "stop":
            completion_crashes += 1
        if acts["tick"] == "go" and truth == "stop":
            tick_crashes += 1
        if acts["tick"] == "stop" and truth == "go":
            tick_extra_stops += 1
        if acts["completion"] == "stop" and truth == "go":
            completion_extra_stops += 1
    return {
        "schema": "worldtick.decide.v1",
        "seed": seed,
        "n": n,
        "completion_crashes": completion_crashes,
        "tick_crashes": tick_crashes,
        "tick_extra_stops": tick_extra_stops,
        "completion_extra_stops": completion_extra_stops,
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
    draw.text((36, 24), "One decision  ·  一次决策  ·  10,000 roads, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "补全的“走”会撞上没看见的障碍。一步的“停”一次不撞，多停是代价。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Completion says go and hits an unseen obstacle. One tick never hits; its price is extra stops.", font=small, fill=(139, 148, 158))
    cards = [
        ("补全撞上", "Completion crashes", rec["completion_crashes"], (248, 81, 73)),
        ("一步撞上", "One tick crashes", rec["tick_crashes"], (63, 185, 80)),
        ("一步多停", "One tick extra stops", rec["tick_extra_stops"], (210, 153, 34)),
        ("补全多停", "Completion extra stops", rec["completion_extra_stops"], (139, 148, 158)),
    ]
    max_v = max(c[2] for c in cards) or 1
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
    if rec["tick_crashes"] != 0:
        raise SystemExit("tick crashed")
    if rec["completion_crashes"] != 552:
        raise SystemExit("completion never crashed")
    if rec["completion_extra_stops"] != 0:
        raise SystemExit("completion stopped on a free road")
    if rec["tick_extra_stops"] != 2353:
        raise SystemExit("tick extra stops moved")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "decide.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
