"""Wilson 95% intervals for the headline rates. No randomness.

Each interval is closed-form from a pinned count in results/*.json,
so the numbers below are as reproducible as the counts themselves.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
Z = 1.96


def load(name: str) -> dict:
    return json.loads((RES / name).read_text())


def wilson(k: int, n: int) -> dict[str, float]:
    p = k / n
    denom = 1 + Z * Z / n
    center = (p + Z * Z / (2 * n)) / denom
    half = Z * (p * (1 - p) / n + Z * Z / (4 * n * n)) ** 0.5 / denom
    return {"k": k, "n": n, "p": p, "lo": center - half, "hi": center + half}


def run() -> dict:
    hidden = load("HIDDEN.json")
    decide = load("DECIDE.json")
    audit = load("AUDIT.json")
    closed = load("CLOSEDLOOP.json")
    fill = load("FILLCHOICE.json")
    rates = {
        "occluded road": wilson(hidden["roads_with_a_hidden_obstacle"], hidden["n"]),
        "optimistic entry": wilson(hidden["completion_enters_hidden_obstacle"], hidden["n"]),
        "one-step collision": wilson(decide["completion_crashes"], decide["n"]),
        "exact map match": wilson(audit["filled_maps_matching_truth"], audit["n"]),
        "closed-loop traversal": wilson(closed["outcomes"]["reached"], closed["n"]),
        "optimistic traversal": wilson(fill["optimistic"]["reached"], fill["n"]),
    }
    return {
        "schema": "worldtick.stats.v1",
        "z": Z,
        "rates": rates,
        "python": sys.version.split()[0],
        "platform": sys.platform,
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    W, H = 1680, 980
    image = Image.new("RGB", (W, H), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    names = {
        "occluded road": "有遮挡的路 occluded",
        "optimistic entry": "乐观走进 optimistic entry",
        "one-step collision": "单步撞上 one-step crash",
        "exact map match": "逐格全对 exact match",
        "closed-loop traversal": "闭环走通 closed-loop",
        "optimistic traversal": "乐观走通 optimistic",
    }
    draw.text((36, 24), "Wilson 95% intervals  ·  区间  ·  closed-form from pinned counts", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "点估计是钉住的数。区间是闭式公式算的，没有新随机数。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Point estimates are pinned counts. Intervals are closed-form, no new randomness.", font=small, fill=(139, 148, 158))
    left, right, top = 480, 1600, 170
    rows = list(rec["rates"].items())
    step = (860 - top) // len(rows)
    colors = [(248, 81, 73), (248, 81, 73), (248, 81, 73), (139, 148, 158), (63, 185, 80), (210, 153, 34)]
    draw.line([(left, top), (left, 860)], fill=(48, 54, 61), width=1)
    for x in (0.0, 0.25, 0.5, 0.75, 1.0):
        px = left + x * (right - left)
        draw.line([(px, top), (px, 860)], fill=(33, 38, 45), width=1)
        draw.text((px - 20, 866), f"{x:.2f}", font=small, fill=(139, 148, 158))
    for i, ((key, r), color) in enumerate(zip(rows, colors)):
        y = top + 40 + i * step
        draw.text((36, y - 18), names[key], font=body, fill=color)
        x0 = left + r["lo"] * (right - left)
        x1 = left + r["hi"] * (right - left)
        xp = left + r["p"] * (right - left)
        draw.line([(x0, y), (x1, y)], fill=color, width=6)
        draw.line([(x0, y - 10), (x0, y + 10)], fill=color, width=3)
        draw.line([(x1, y - 10), (x1, y + 10)], fill=color, width=3)
        draw.ellipse((xp - 8, y - 8, xp + 8, y + 8), fill=color)
        draw.text((right - 330, y - 36), f"{r['p']:.4f} [{r['lo']:.4f}, {r['hi']:.4f}]", font=small, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    for key, r in rec["rates"].items():
        if not r["lo"] < r["p"] < r["hi"]:
            raise SystemExit(f"interval misses estimate: {key}")
        if not 0 <= r["lo"] and r["hi"] <= 1:
            raise SystemExit(f"interval out of range: {key}")
    narrow = rec["rates"]["one-step collision"]
    if not narrow["hi"] - narrow["lo"] < 0.02:
        raise SystemExit("collision interval too wide")
    wide = rec["rates"]["occluded road"]
    if not wide["hi"] - wide["lo"] < 0.03:
        raise SystemExit("occluded interval too wide")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "stats.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
