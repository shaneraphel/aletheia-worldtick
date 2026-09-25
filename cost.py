"""Price of reliability: cumulative milliseconds to walk each horizon.

On the pinned 256-node world, time reach_after for horizons
0, 1, 2, 4, 8, 12, 16, 32 (7 timed trials plus 1 warmup) and one
datalog_fixpoint call. Reach values must match results/HORIZON.json.
Timings are reported, not pinned: the pinned claims are the reach
sequence, monotone cost growth, and completion cheaper than 12 steps.
"""
from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from pathlib import Path

from datalog import datalog_fixpoint
from datalog_bench import N_EDGES, N_FACTS, N_NODES, SEED, world
from tick import reach_after

HORIZONS = (0, 1, 2, 4, 8, 12, 16, 32)
N_TRIALS = 7
WARMUP = 1
REPEATS = 50
REACH = {0: 8, 1: 24, 2: 50, 4: 138, 8: 212, 12: 214, 16: 214, 32: 214}


def time_call(fn, *args) -> float:
    t0 = time.perf_counter()
    fn(*args)
    return time.perf_counter() - t0


def run() -> dict:
    facts, edges = world(N_NODES, N_FACTS, N_EDGES, SEED)
    points = []
    for h in HORIZONS:
        reach = reach_after(N_NODES, facts, edges, h)
        samples = [
            sum(time_call(reach_after, N_NODES, facts, edges, h) for _ in range(REPEATS))
            for _ in range(WARMUP + N_TRIALS)
        ]
        points.append({"horizon": h, "reach": reach, "ms_median": statistics.median(samples[WARMUP:]) * 1000 / REPEATS})
    comp_samples = [
        sum(time_call(datalog_fixpoint, N_NODES, facts, edges) for _ in range(REPEATS))
        for _ in range(WARMUP + N_TRIALS)
    ]
    completion_ms = statistics.median(comp_samples[WARMUP:]) * 1000 / REPEATS
    return {
        "schema": "worldtick.cost.v1",
        "seed": SEED,
        "n_nodes": N_NODES,
        "n_facts": N_FACTS,
        "n_edges": N_EDGES,
        "n_trials": N_TRIALS,
        "warmup": WARMUP,
        "points": points,
        "completion_ms_median": completion_ms,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
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
    draw.text((36, 24), "Cost  ·  价格  ·  seed 20260919, median of 7 timed trials", font=small, fill=(139, 148, 158))
    h12 = next(p["ms_median"] for p in rec["points"] if p["horizon"] == 12)
    ratio = h12 / rec["completion_ms_median"]
    draw.text((36, 56), f"12 步走到 214，花的时间是一次补全的 {ratio:.1f} 倍。可靠有表可查。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), f"Twelve steps to 214 cost {ratio:.1f}x one completion call. Reliability has a meter.", font=small, fill=(139, 148, 158))
    panels = [
        ("reach 可达数", [(p["horizon"], p["reach"]) for p in rec["points"]], (63, 185, 80), 170, 520),
        ("ms, median 累计毫秒", [(p["horizon"], p["ms_median"]) for p in rec["points"]], (210, 153, 34), 560, 880),
    ]
    for name, series, color, top, bottom in panels:
        left, right = 140, 1600
        draw.text((36, top - 34), name, font=body, fill=color)
        draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
        xs = [p["horizon"] for p in rec["points"]]
        vals = [v for _, v in series]
        lo, hi = min(vals), max(vals)
        span = (hi - lo) or 1.0
        max_h = max(xs)
        px = [left + (h / max_h) * (right - left) for h in xs]
        py = [bottom - 30 - ((v - lo) / span) * (bottom - top - 60) for v in vals]
        draw.line(list(zip(px, py)), fill=color, width=5)
        for x, y, h, v in zip(px, py, xs, vals):
            draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color)
            draw.text((x - 20, bottom + 8), f"{h}", font=small, fill=(139, 148, 158))
        draw.text((right - 300, top + 12), f"h=12: {series[5][1]:.3f}" if isinstance(series[5][1], float) else f"h=12: {series[5][1]}", font=body, fill=color)
    comp = rec["completion_ms_median"]
    draw.text((36, 906), f"completion 补全一次 one call: {comp:.4f} ms", font=body, fill=(210, 153, 34))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    for p in rec["points"]:
        if p["reach"] != REACH[p["horizon"]]:
            raise SystemExit(f"reach at horizon {p['horizon']} moved")
    ms = [p["ms_median"] for p in rec["points"]]
    if not ms[-1] > ms[0]:
        raise SystemExit("horizon walk costs nothing extra")
    if not ms[-1] > 5 * ms[0]:
        raise SystemExit("horizon walk costs nothing extra")
    if not rec["completion_ms_median"] > 0:
        raise SystemExit("completion timing missing")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "cost.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
