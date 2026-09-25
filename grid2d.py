"""Two-dimensional corridors: BFS on a filled grid versus observed cells.

On WxH occupancy grids with random obstacles and masked cells, plan a
BFS shortest path from the top-left to the bottom-right corner.
Optimistic fills masked cells as free and follows the filled path.
Pessimistic treats masked cells as walls. A pessimistic step never
enters an unobserved cell, so its crash count is zero by construction.
Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from collections import deque
from pathlib import Path

SEED = 20260919
N = 2_000
W = 16
H = 16
OBSTACLE = 0.15
DROP = 0.25
START = (0, 0)
GOAL = (W - 1, H - 1)
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def make_grid(rng: random.Random) -> tuple[list[list[int]], list[list[int | None]]]:
    true = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if (x, y) in (START, GOAL):
                continue
            if rng.random() < OBSTACLE:
                true[y][x] = 1
    seen: list[list[int | None]] = []
    for y in range(H):
        row = []
        for x in range(W):
            if (x, y) in (START, GOAL) or rng.random() >= DROP:
                row.append(true[y][x])
            else:
                row.append(None)
        seen.append(row)
    return true, seen


def bfs(blocked, w: int = W, h: int = H) -> list[tuple[int, int]] | None:
    prev: dict[tuple[int, int], tuple[int, int] | None] = {START: None}
    queue: deque[tuple[int, int]] = deque([START])
    while queue:
        here = queue.popleft()
        if here == GOAL:
            break
        for dx, dy in DIRS:
            nxt = (here[0] + dx, here[1] + dy)
            if 0 <= nxt[0] < w and 0 <= nxt[1] < h and nxt not in prev and not blocked(nxt):
                prev[nxt] = here
                queue.append(nxt)
    if GOAL not in prev:
        return None
    path = [GOAL]
    while path[-1] != START:
        parent = prev[path[-1]]
        assert parent is not None
        path.append(parent)
    return path[::-1]


def walk(true, seen) -> dict[str, int | float]:
    filled = [[0 if c is None else c for c in row] for row in seen]
    opt_path = bfs(lambda p: filled[p[1]][p[0]] == 1)
    pes_path = bfs(lambda p: seen[p[1]][p[0]] != 0)
    out: dict[str, int | float] = {"opt_len": 0, "pes_len": 0}
    if opt_path is None:
        out["opt"] = "stopped"
    elif any(true[y][x] == 1 for x, y in opt_path):
        out["opt"] = "crash"
    else:
        out["opt"] = "reached"
        out["opt_len"] = len(opt_path) - 1
    if pes_path is None:
        out["pes"] = "stopped"
    else:
        out["pes"] = "reached"
        out["pes_len"] = len(pes_path) - 1
    return out


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    opt = {"crash": 0, "stopped": 0, "reached": 0}
    pes = {"crash": 0, "stopped": 0, "reached": 0}
    opt_len = 0
    pes_len = 0
    for _ in range(n):
        true, seen = make_grid(rng)
        res = walk(true, seen)
        opt[res["opt"]] += 1  # type: ignore[index]
        pes[res["pes"]] += 1  # type: ignore[index]
        opt_len += res["opt_len"]  # type: ignore[operator]
        pes_len += res["pes_len"]  # type: ignore[operator]
    return {
        "schema": "worldtick.grid2d.v1",
        "seed": seed,
        "n": n,
        "width": W,
        "height": H,
        "obstacle": OBSTACLE,
        "drop": DROP,
        "optimistic": opt,
        "pessimistic": pes,
        "optimistic_mean_length": opt_len / max(1, opt["reached"]),
        "pessimistic_mean_length": pes_len / max(1, pes["reached"]),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def draw_example(path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    rng = random.Random(SEED)
    true, seen = make_grid(rng)
    filled = [[0 if c is None else c for c in row] for row in seen]
    opt_path = bfs(lambda p: filled[p[1]][p[0]] == 1) or []
    pes_path = bfs(lambda p: seen[p[1]][p[0]] != 0) or []
    opt_set = set(opt_path)
    pes_set = set(pes_path)
    crash = next(((x, y) for x, y in opt_path if true[y][x] == 1), None)
    S = 34
    image = Image.new("RGB", (W * S + 72, H * S + 120), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 18)
    draw.text((36, 16), "16x16 grid  ·  栅格  ·  black 真实障碍, gray 被遮 masked, red 乐观 optimistic", font=font, fill=(230, 237, 243))
    draw.text((36, 44), "seed 20260919, first trial — the red path crosses a masked obstacle", font=font, fill=(139, 148, 158))
    for y in range(H):
        for x in range(W):
            x0, y0 = 36 + x * S, 76 + y * S
            if true[y][x] == 1 and seen[y][x] is None:
                fill = (90, 90, 90)
            elif true[y][x] == 1:
                fill = (10, 10, 10)
            elif seen[y][x] is None:
                fill = (60, 63, 70)
            else:
                fill = (230, 237, 243)
            draw.rectangle((x0, y0, x0 + S - 2, y0 + S - 2), fill=fill, outline=(48, 54, 61))
            if (x, y) in opt_set and (x, y) not in (START, GOAL):
                draw.ellipse((x0 + 8, y0 + 8, x0 + S - 10, y0 + S - 10), fill=(248, 81, 73))
            if (x, y) in pes_set and (x, y) not in (START, GOAL) and (x, y) not in opt_set:
                draw.ellipse((x0 + 8, y0 + 8, x0 + S - 10, y0 + S - 10), fill=(63, 185, 80))
    for label, cell, color in (("S", START, (63, 185, 80)), ("G", GOAL, (63, 185, 80))):
        draw.text((36 + cell[0] * S + 10, 76 + cell[1] * S + 6), label, font=font, fill=color)
    if crash is not None:
        draw.text((36 + crash[0] * S - 6, 76 + crash[1] * S - 40), "撞 crash", font=font, fill=(248, 81, 73))
    image.save(path, quality=92)


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    W_, H_ = 1680, 900
    image = Image.new("RGB", (W_, H_), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 24)
    number = ImageFont.truetype(font_path, 44)
    draw.text((36, 24), "2-D grid  ·  二维栅格  ·  2,000 trials of 16x16, seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "乐观路径会穿过没看见的障碍。保守路径一次不撞，经常到不了。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "The optimistic path crosses unseen obstacles. The pessimistic path never crashes, often stops.", font=small, fill=(139, 148, 158))
    o, p = rec["optimistic"], rec["pessimistic"]
    cards = [
        ("乐观撞上", "Optimistic crashes", o["crash"], (248, 81, 73)),
        ("保守撞上", "Pessimistic crashes", p["crash"], (63, 185, 80)),
        ("乐观到达", "Optimistic reached", o["reached"], (210, 153, 34)),
        ("保守到达", "Pessimistic reached", p["reached"], (121, 192, 255)),
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
    draw.text((36, 786), f"n = {rec['n']:,}   mean length 乐观 {rec['optimistic_mean_length']:.1f} / 保守 {rec['pessimistic_mean_length']:.1f}", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["pessimistic"]["crash"] != 0:
        raise SystemExit("pessimistic path crashed")
    if (rec["optimistic"]["crash"], rec["optimistic"]["reached"], rec["optimistic"]["stopped"]) != (1439, 500, 61):
        raise SystemExit("optimistic crashes moved")
    if rec["optimistic"]["reached"] + rec["optimistic"]["stopped"] + rec["optimistic"]["crash"] != N:
        raise SystemExit("optimistic outcomes do not sum to n")
    if (rec["pessimistic"]["crash"], rec["pessimistic"]["reached"], rec["pessimistic"]["stopped"]) != (0, 419, 1581):
        raise SystemExit("pessimistic outcomes do not sum to n")
    root = Path(__file__).resolve().parent
    draw_example(root / "docs" / "figures" / "grid2d-map.png")
    figure(rec, root / "docs" / "figures" / "grid2d.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
