"""Zero-fill is not the identity of the decision.

Class is 1 when the sum is positive. Replacing a subset of samples by
zero changes the sum by the negative of what was erased.

If every sample is non-negative, the filled sum cannot rise, so a rest
packet cannot become a go. The only error is a go read as rest.

If a sample is negative, erasing it can raise the sum. A rest packet
can become a go. A brain-computer product that writes zeros into a
dropout is not being conservative: the direction of the error is the
sign of the samples it deleted.

The non-negative packets are the same generator as bcisweep.py.
The signed packets use entries in {-2,-1,0,1,2}. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from bcisweep import WIDTH, packet
from decode import neural_class

ROOT = Path(__file__).resolve().parent
SEED = 20260919
N = 10_000
SIGNED = (-2, -1, 0, 1, 2)


def flips(samples: list[int], k: int) -> tuple[int, int]:
    full = neural_class(samples)
    filled = neural_class(samples[: WIDTH - k] + [0] * k)
    false_rest = int(full == 1 and filled == 0)
    false_go = int(full == 0 and filled == 1)
    return false_rest, false_go


def signed_packet(rng: random.Random) -> list[int]:
    return [rng.choice(SIGNED) for _ in range(WIDTH)]


def sweep(packets: list[list[int]]) -> list[dict]:
    points = []
    for k in range(WIDTH + 1):
        rest = go = 0
        for samples in packets:
            false_rest, false_go = flips(samples, k)
            rest += false_rest
            go += false_go
        points.append({"dropped": k, "false_rest": rest, "false_go": go})
    return points


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    nonneg = sweep([packet(rng) for _ in range(n)])
    signed = sweep([signed_packet(rng) for _ in range(n)])
    return {
        "schema": "worldtick.signfill.v1",
        "seed": seed,
        "n": n,
        "width": WIDTH,
        "nonnegative": nonneg,
        "signed": signed,
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
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 42)
    draw.text((36, 24), "Zero-fill  ·  补零不是“什么都没发生”  ·  10,000 packets", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "非负信号只能把动作读成静息。有符号电压还能把静息读成动作。", font=title, fill=(230, 237, 243))
    draw.text((36, 100), "Non-negative codes can only turn a go into rest. Signed voltages can also turn rest into a go.", font=small, fill=(139, 148, 158))
    # Dropped suffix of 4, the middle of the dose curve, where both errors are visible.
    k = 4
    nn = rec["nonnegative"][k]
    sg = rec["signed"][k]
    cards = [
        ("非负，假静息", "Non-negative, false rest", nn["false_rest"], (210, 153, 34)),
        ("非负，假动作", "Non-negative, false go", nn["false_go"], (63, 185, 80)),
        ("有符号，假静息", "Signed, false rest", sg["false_rest"], (210, 153, 34)),
        ("有符号，假动作", "Signed, false go", sg["false_go"], (248, 81, 73)),
    ]
    max_v = rec["n"]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + i * 411
        draw.rounded_rectangle((x, 170, x + 387, 720), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 198), name, font=body, fill=color)
        draw.text((x + 24, 236), en, font=small, fill=color)
        draw.text((x + 24, 310), f"{value:,}", font=number, fill=(230, 237, 243))
        bar_top = 660 - (value / max_v) * 200
        draw.rectangle((x + 24, bar_top, x + 363, 660), fill=color)
    draw.text(
        (36, 770),
        "丢掉最后 4 个采样再补零。假动作 = 静息被读成 go。  Drop the last 4 samples, write zeros. False go = rest read as a movement.",
        font=small,
        fill=(139, 148, 158),
    )
    draw.text(
        (36, 820),
        "类别是和是否为正。补零减去被删掉的和。被删的是负数时，和会上升。  Class is the sign of the sum. Zero-fill subtracts what was erased.",
        font=small,
        fill=(139, 148, 158),
    )
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    nn = [p["false_rest"] for p in rec["nonnegative"]]
    ng = [p["false_go"] for p in rec["nonnegative"]]
    if nn != [0, 0, 1, 9, 43, 161, 642, 2494, 10000]:
        raise SystemExit(f"non-negative false rest moved: {nn}")
    if any(g != 0 for g in ng):
        raise SystemExit(f"non-negative false go is not identically zero: {ng}")
    signed_go = [p["false_go"] for p in rec["signed"]]
    signed_rest = [p["false_rest"] for p in rec["signed"]]
    if signed_go[0] != 0 or signed_rest[0] != 0:
        raise SystemExit("dropping nothing flipped a class")
    if signed_go[-1] != 0:
        raise SystemExit("zeroing every sample produced a go")
    if signed_rest != [0, 587, 834, 1060, 1280, 1498, 1798, 2045, 4360]:
        raise SystemExit(f"signed false rest moved: {signed_rest}")
    if signed_go != [0, 630, 790, 1021, 1141, 1277, 1414, 1620, 0]:
        raise SystemExit(f"signed false go moved: {signed_go}")
    figure(rec, ROOT / "docs" / "figures" / "signfill.png")
    out = ROOT / "results" / "SIGNFILL.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump({"nonnegative_false_go": ng, "signed_false_rest": signed_rest, "signed_false_go": signed_go}, sys.stdout)
    sys.stdout.write("\n")
    print("python", rec["python"], "platform", rec["platform"], file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
