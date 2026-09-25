"""Five seeds: completion-side counts move, tick-side zeros never do.

For seeds 20260919..20260923, rerun the dropout-0.30 sweep point and
the one-step decision at n=2,000 roads each. Pinned claims: every
tick-side column is 0 on every seed; every completion-side column is
positive and varies across seeds (the resampling actually happened).
"""
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

from decide import run as decide_run
from sweep import run_point

SEEDS = (20260919, 20260920, 20260921, 20260922, 20260923)
N = 2_000
DROP = 0.30


def run() -> dict:
    rows = []
    for seed in SEEDS:
        s = run_point(DROP, N, seed)
        d = decide_run(N, seed)
        rows.append(
            {
                "seed": seed,
                "sweep_completion_hits": s["completion_hits"],
                "sweep_tick_hits": s["tick_hits"],
                "decide_completion_crashes": d["completion_crashes"],
                "decide_tick_crashes": d["tick_crashes"],
            }
        )
    return {
        "schema": "worldtick.robust.v1",
        "n_per_seed": N,
        "drop": DROP,
        "rows": rows,
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
    draw.text((36, 24), "Robustness  ·  稳健性  ·  5 seeds, 2,000 roads each, drop 0.30", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "五个种子，补全侧的数都大于 0 且互不相同。实测侧全是 0。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Across five seeds every completion count is positive and varies. Every tick count is 0.", font=small, fill=(139, 148, 158))
    panels = [
        ("sweep 补全走进 completion hits", "sweep_completion_hits", (248, 81, 73), 180, 500),
        ("decision 补全撞上 completion crashes", "decide_completion_crashes", (210, 153, 34), 560, 840),
    ]
    for name, key, color, top, bottom in panels:
        left, right = 36, 1600
        draw.text((36, top - 40), name, font=body, fill=color)
        draw.text((right - 420, top - 40), "tick 实测侧 tick side: 0, 0, 0, 0, 0", font=body, fill=(63, 185, 80))
        draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
        vals = [r[key] for r in rec["rows"]]
        lo, hi = 0, max(vals)
        xs = [left + (i + 0.5) * (right - left) / len(vals) for i in range(len(vals))]
        for x, v, r in zip(xs, vals, rec["rows"]):
            y = bottom - 30 - (v / hi) * (bottom - top - 60)
            draw.rectangle((x - 60, y, x + 60, bottom - 30), fill=color)
            draw.text((x - 52, bottom - 22), str(r["seed"])[-2:], font=small, fill=(139, 148, 158))
            draw.text((x - 40, y - 34), f"{v:,}", font=body, fill=color)
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    for r in rec["rows"]:
        if r["sweep_tick_hits"] != 0 or r["decide_tick_crashes"] != 0:
            raise SystemExit(f"tick column nonzero on seed {r['seed']}")
        if r["sweep_completion_hits"] <= 0 or r["decide_completion_crashes"] <= 0:
            raise SystemExit(f"completion column empty on seed {r['seed']}")
    if len({r["sweep_completion_hits"] for r in rec["rows"]}) < 2:
        raise SystemExit("sweep counts identical across seeds")
    if len({r["decide_completion_crashes"] for r in rec["rows"]}) < 2:
        raise SystemExit("decide counts identical across seeds")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "robust.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
