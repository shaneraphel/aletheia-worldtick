"""A completed map can match a clear road and still cross a hidden obstacle.

The true road is a line of free cells and obstacles. The sensor drops cells.
Completion writes every drop as free, then walks. One tick stops at the first
drop. Seed 20260919, 10_000 roads.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

SEED = 20260919
N = 10_000
WIDTH = 32
DROP = 0.30
OBSTACLE = 0.20


def road(rng: random.Random) -> tuple[list[int], list[int | None]]:
    true = [0] * WIDTH
    true[0] = 0
    for i in range(1, WIDTH):
        if rng.random() < OBSTACLE:
            true[i] = 1
    seen: list[int | None] = []
    for i, cell in enumerate(true):
        if i > 0 and rng.random() < DROP:
            seen.append(None)
        else:
            seen.append(cell)
    return true, seen


def walk_completed(true: list[int], seen: list[int | None]) -> int:
    """Enter every cell the completion marks free. A hidden obstacle counts once."""
    for i in range(1, len(true)):
        filled = 0 if seen[i] is None else seen[i]
        if filled == 1:
            break
        if true[i] == 1:
            return 1
    return 0


def walk_tick(seen: list[int | None]) -> int:
    """Stop at the first unseen cell. Do not enter it."""
    for cell in seen[1:]:
        if cell is None or cell == 1:
            break
    return 0


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    completed_hits = 0
    tick_hits = 0
    hidden_obstacles = 0
    for _ in range(n):
        true, seen = road(rng)
        if any(s is None and t == 1 for s, t in zip(seen, true)):
            hidden_obstacles += 1
        completed_hits += walk_completed(true, seen)
        tick_hits += walk_tick(seen)
    return {
        "schema": "worldtick.hidden.v1",
        "seed": seed,
        "n": n,
        "width": WIDTH,
        "drop": DROP,
        "obstacle": OBSTACLE,
        "roads_with_a_hidden_obstacle": hidden_obstacles,
        "completion_enters_hidden_obstacle": completed_hits,
        "tick_enters_hidden_obstacle": tick_hits,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 520), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    title = ImageFont.truetype(font_path, 32)
    body = ImageFont.truetype(font_path, 26)
    small = ImageFont.truetype(font_path, 20)
    draw.text((36, 28), "HIDDEN OBSTACLE  ·  补全之后的路", font=small, fill=(139, 148, 158))
    draw.text((36, 64), "洞被写成空地之后，会走进没看见的障碍。一步停在看见的边界。", font=title, fill=(230, 237, 243))
    cards = [
        ("藏着障碍的路", f"{rec['roads_with_a_hidden_obstacle']:,} / {rec['n']:,}"),
        ("补全走了进去", f"{rec['completion_enters_hidden_obstacle']:,}"),
        ("一步走进去", f"{rec['tick_enters_hidden_obstacle']:,}"),
    ]
    colors = [(210, 153, 34), (248, 81, 73), (63, 185, 80)]
    for i, ((name, value), color) in enumerate(zip(cards, colors)):
        x = 36 + i * 540
        draw.rounded_rectangle((x, 160, x + 500, 440), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 28, 200), name, font=body, fill=color)
        draw.text((x + 28, 280), value, font=title, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["roads_with_a_hidden_obstacle"] != 8564:
        raise SystemExit("hidden-obstacle count moved")
    if rec["completion_enters_hidden_obstacle"] != 2995:
        raise SystemExit("completion-hit count moved")
    if rec["tick_enters_hidden_obstacle"] != 0:
        raise SystemExit("tick entered a hidden obstacle")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "hidden.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
