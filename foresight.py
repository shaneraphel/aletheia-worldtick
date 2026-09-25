"""Where foresight flips the answer: discount sweep on a trap table.

TRAP pays 10 now for action 0 and steps into -100. Action 1 pays 1 and
stays. Greedy (discount 0) picks 0. Planning picks 1 once the discount
d exceeds 9/101. Proof: under "always action 0", V0 = (10-100d)/(1-d^2);
Q0(a1) = 1+dV0 > V0 iff 1+d > 10-100d iff 101d > 9.

Policy evaluation solves (I-dP)V = r in exact rationals, so the
threshold is sharp. Also flips 1,000 random trap tables at d=0 vs d=0.9.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from fractions import Fraction
from pathlib import Path

TRAP = [[10, 1], [-100, -100]]
THRESHOLD = Fraction(9, 101)
GRID = [round(i / 100, 2) for i in range(0, 100, 5)]
N_RANDOM = 1_000
SEED = 20260919


def _nxt(n: int, state: int, action: int) -> int:
    return (state + action + 1) % n


def evaluate(policy: list[int], reward: list[list[int]], d: Fraction) -> list[Fraction]:
    n = len(reward)
    rows: list[list[Fraction]] = []
    for s in range(n):
        row = [Fraction(0)] * (n + 1)
        row[s] = Fraction(1)
        row[_nxt(n, s, policy[s])] -= d
        row[n] = Fraction(reward[s][policy[s]])
        rows.append(row)
    for col in range(n):
        piv = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        div = rows[col][col]
        rows[col] = [v / div for v in rows[col]]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                mul = rows[r][col]
                rows[r] = [a - mul * b for a, b in zip(rows[r], rows[col])]
    return [rows[s][n] for s in range(n)]


def discounted_policy(reward: list[list[int]], d: Fraction) -> int:
    n = len(reward)
    a = len(reward[0])
    policy = [0] * n
    for _epoch in range(n * a + 1):
        values = evaluate(policy, reward, d)
        improved = False
        for s in range(n):
            qs = [Fraction(reward[s][act]) + d * values[_nxt(n, s, act)] for act in range(a)]
            best = max(range(a), key=lambda act: (qs[act], -act))
            if best != policy[s]:
                policy[s] = best
                improved = True
        if not improved:
            break
    return policy[0]


def random_trap(rng: random.Random) -> list[list[int]]:
    return [
        [rng.randrange(8, 21), rng.randrange(1, 4)],
        [rng.randrange(-200, -40), rng.randrange(-200, -40)],
    ]


def run() -> dict:
    curve = [{"discount": g, "action": discounted_policy(TRAP, Fraction(int(g * 100), 100))} for g in GRID]
    flip_at = next(c["discount"] for c in curve if c["action"] == 1)
    rng = random.Random(SEED)
    tables = [random_trap(rng) for _ in range(N_RANDOM)]
    myopic = [discounted_policy(t, Fraction(0)) for t in tables]
    farsighted = [discounted_policy(t, Fraction(9, 10)) for t in tables]
    flips = sum(1 for m, f in zip(myopic, farsighted) if m != f)
    return {
        "schema": "worldtick.foresight.v1",
        "trap": TRAP,
        "threshold_exact": "9/101",
        "threshold_value": float(THRESHOLD),
        "curve": curve,
        "first_flip_discount": flip_at,
        "n_random": N_RANDOM,
        "random_myopic_action_0": sum(1 for m in myopic if m == 0),
        "random_farsighted_action_1": sum(1 for f in farsighted if f == 1),
        "random_flips": flips,
        "seed": SEED,
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
    draw.text((36, 24), "Foresight  ·  远见曲线  ·  trap [[10,1],[-100,-100]], threshold 9/101", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "折扣过了 9/101，答案从动作 0 翻到动作 1。一千张随机陷阱表全部翻转。", font=title, fill=(230, 237, 243))
    draw.text((36, 96), "Past discount 9/101 the answer flips from action 0 to action 1. All 1,000 random traps flip.", font=small, fill=(139, 148, 158))
    left, top, right, bottom = 140, 170, 1600, 700
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    y0 = bottom - 60
    y1 = top + 60
    draw.line([(left, y0), (right, y0)], fill=(48, 54, 61), width=1)
    draw.line([(left, y1), (right, y1)], fill=(48, 54, 61), width=1)
    draw.text((52, y0 - 16), "0", font=small, fill=(139, 148, 158))
    draw.text((52, y1 - 16), "1", font=small, fill=(139, 148, 158))
    th = 9 / 101
    for c in rec["curve"]:
        x = left + c["discount"] * (right - left)
        y = y1 if c["action"] == 1 else y0
        color = (63, 185, 80) if c["action"] == 1 else (210, 153, 34)
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=color)
        if c["discount"] in (0.0, 0.5, 0.95):
            draw.text((x - 20, bottom + 12), f"{c['discount']:.2f}", font=small, fill=(139, 148, 158))
    xth = left + th * (right - left)
    draw.line([(xth, top), (xth, bottom)], fill=(248, 81, 73), width=3)
    draw.text((xth + 12, top + 16), "9/101 ≈ 0.089", font=body, fill=(248, 81, 73))
    draw.text((xth + 12, top + 52), "定理阈值 theorem", font=small, fill=(248, 81, 73))
    draw.text((36, bottom + 44), "x: discount 折扣   y: action 动作", font=small, fill=(139, 148, 158))
    draw.text((36, bottom + 76), f"random traps 随机陷阱表: {rec['random_flips']:,} / {rec['n_random']:,} flip 翻转", font=body, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["first_flip_discount"] != 0.10:
        raise SystemExit("flip discount moved")
    if abs(rec["threshold_value"] - 9 / 101) > 1e-12:
        raise SystemExit("threshold moved")
    for i in range(0, 9):
        if discounted_policy(TRAP, Fraction(i, 100)) != 0:
            raise SystemExit("action below threshold moved")
    for i in (9, 10, 50, 90, 99):
        if discounted_policy(TRAP, Fraction(i, 100)) != 1:
            raise SystemExit("action above threshold moved")
    if rec["random_flips"] != N_RANDOM:
        raise SystemExit("random-trap flips moved")
    root = Path(__file__).resolve().parent
    figure(rec, root / "docs" / "figures" / "foresight.png")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
