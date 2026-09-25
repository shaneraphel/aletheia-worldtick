"""Breakeven crash cost: how many waits is one collision worth?

One-step setting: 552 imputation collisions versus 2,353 measured
extra stops, so the measured step wins iff one collision costs more
than 2353/552 stops. Full-walk setting: 2,995 optimistic collisions
versus 20,975 closed-loop waits, breakeven 20975/2995 waits per crash.
Both ratios are exact fractions of pinned counts. No randomness here:
every number is derived from results/*.json.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"


def load(name: str) -> dict:
    return json.loads((RES / name).read_text())


def line(crashes: int, waits: int, ratios: list[Fraction]) -> list[dict]:
    return [
        {"crash_cost_in_waits": str(r), "open": float(crashes * r), "measured": float(waits)}
        for r in ratios
    ]


def run() -> dict:
    decide = load("DECIDE.json")
    fill = load("FILLCHOICE.json")
    closed = load("CLOSEDLOOP.json")
    one = {"crashes": decide["completion_crashes"], "waits": decide["tick_extra_stops"]}
    full = {"crashes": fill["optimistic"]["crash"], "waits": closed["waits_total"]}
    ratios = [Fraction(x, 10) for x in range(1, 201, 5)]
    return {
        "schema": "worldtick.tradeoff.v1",
        "one_step": {
            **one,
            "breakeven_exact": f"{one['waits']}/{one['crashes']}",
            "breakeven_value": float(Fraction(one["waits"], one["crashes"])),
            "curve": line(one["crashes"], one["waits"], ratios),
        },
        "full_walk": {
            **full,
            "breakeven_exact": f"{full['waits']}/{full['crashes']}",
            "breakeven_value": float(Fraction(full["waits"], full["crashes"])),
            "curve": line(full["crashes"], full["waits"], ratios),
        },
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
    draw.text((36, 24), "Breakeven  ·  决策账  ·  exact fractions of pinned counts", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "一次撞 = 4.3 次等待（单步），= 7.0 次等待（整条路）。撞更贵就该停。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "One crash = 4.3 waits (one step), = 7.0 waits (full walk). If a crash costs more, stop.", font=small, fill=(139, 148, 158))
    panels = [
        ("单步 one step: 552 vs 2,353", rec["one_step"], (210, 153, 34), 170, 540),
        ("整条路 full walk: 2,995 vs 20,975", rec["full_walk"], (248, 81, 73), 590, 920),
    ]
    for name, sec, color, top, bottom in panels:
        left, right = 200, 1600
        draw.text((36, top + 120), name, font=body, fill=color)
        draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
        curve = sec["curve"]
        max_r = float(Fraction(curve[-1]["crash_cost_in_waits"]))
        max_c = max(c["open"] for c in curve)
        xs = [left + (float(Fraction(c["crash_cost_in_waits"])) / max_r) * (right - left) for c in curve]
        yo = [bottom - 30 - (c["open"] / max_c) * (bottom - top - 60) for c in curve]
        ym = bottom - 30 - (sec["waits"] / max_c) * (bottom - top - 60)
        draw.line(list(zip(xs, yo)), fill=color, width=5)
        draw.line([(left, ym), (right, ym)], fill=(63, 185, 80), width=3)
        be = float(Fraction(sec["waits"], sec["crashes"]))
        xb = left + (be / max_r) * (right - left)
        draw.line([(xb, top), (xb, bottom)], fill=(248, 81, 73), width=2)
        draw.text((xb + 10, top + 12), f"= {be:.1f} waits", font=body, fill=(248, 81, 73))
        for mark in (1, 5, 10, 20):
            xm = left + (mark / max_r) * (right - left)
            draw.text((xm - 12, bottom + 8), str(mark), font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if Fraction(rec["one_step"]["waits"], rec["one_step"]["crashes"]) != Fraction(2353, 552):
        raise SystemExit("one-step breakeven moved")
    if Fraction(rec["full_walk"]["waits"], rec["full_walk"]["crashes"]) != Fraction(20975, 2995):
        raise SystemExit("full-walk breakeven moved")
    if not 4.2 < rec["one_step"]["breakeven_value"] < 4.3:
        raise SystemExit("one-step value moved")
    if not 7.0 < rec["full_walk"]["breakeven_value"] < 7.1:
        raise SystemExit("full-walk value moved")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "tradeoff.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
