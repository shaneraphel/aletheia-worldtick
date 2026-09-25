"""The bilateral rate stays when the window was not observed.

A complete window may set the left-right rate: 2 clicks a second for
rest, 6 for a movement. An incomplete window keeps the rate already
playing. Zero-filling the missing suffix and then setting the rate is
a change made from samples that were not there.

This is not a detector of fright, and it is not a treatment. It is the
rule for when the sound in the room is allowed to change.

Seed 20260919. Each step draws eight signed samples and then, with
probability 0.30, drops the last four.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from decode import neural_class
from signfill import SIGNED, WIDTH

ROOT = Path(__file__).resolve().parent
SEED = 20260919
N = 10_000
DROP_P = 0.30
DROP_K = 4
REST_HZ = 2
MOVE_HZ = 6


def packet(rng: random.Random) -> list[int]:
    return [rng.choice(SIGNED) for _ in range(WIDTH)]


def label(samples: list[int]) -> str:
    return "movement" if neural_class(samples) == 1 else "rest"


def hz_of(name: str) -> int:
    return MOVE_HZ if name == "movement" else REST_HZ


def naive_label(samples: list[int]) -> str:
    filled = samples[: WIDTH - DROP_K] + [0] * DROP_K
    return label(filled)


def run(n: int = N, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    held = REST_HZ
    dropped = 0
    naive_disagrees = 0
    hold_changes = 0
    allowed_changes = 0
    trace = []
    for i in range(n):
        samples = packet(rng)
        missing = rng.random() < DROP_P
        heard = label(samples)
        target = hz_of(heard)
        guessed = hz_of(naive_label(samples))
        if missing:
            dropped += 1
            if guessed != target:
                naive_disagrees += 1
            before = held
            # An incomplete window does not assign a new rate.
            if held != before:
                hold_changes += 1
        else:
            if target != held:
                allowed_changes += 1
                held = target
        if i < 40:
            trace.append({
                "missing": missing,
                "heard_hz": target,
                "guessed_hz": guessed,
                "played_hz": held,
            })
    return {
        "schema": "worldtick.pace.v1",
        "seed": seed,
        "n": n,
        "drop_p": DROP_P,
        "rest_hz": REST_HZ,
        "movement_hz": MOVE_HZ,
        "dropped": dropped,
        "naive_disagrees_while_dropped": naive_disagrees,
        "hold_changes_while_dropped": hold_changes,
        "allowed_changes": allowed_changes,
        "trace": trace,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 780), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    draw.text((36, 24), "Bilateral rate  ·  左右交替的速度  ·  first 40 steps", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "窗口不完整时，正在响的速度保持不变。", font=title, fill=(230, 237, 243))
    draw.text((36, 104), "When the window is incomplete, the rate already playing stays. Gray marks a dropped window.", font=small, fill=(139, 148, 158))
    left, top, right, bottom = 80, 180, 1600, 640
    draw.rectangle((left, top, right, bottom), outline=(48, 54, 61), width=2)
    trace = rec["trace"]
    span = right - left
    for i, step in enumerate(trace):
        x = left + (i + 0.5) * span / len(trace)
        if step["missing"]:
            draw.rectangle((x - 12, top, x + 12, bottom), fill=(33, 38, 45))
        y_play = bottom - (step["played_hz"] - 2) / 4 * (bottom - top - 40) - 20
        y_guess = bottom - (step["guessed_hz"] - 2) / 4 * (bottom - top - 40) - 20
        draw.ellipse((x - 5, y_guess - 5, x + 5, y_guess + 5), fill=(248, 81, 73))
        draw.ellipse((x - 7, y_play - 7, x + 7, y_play + 7), outline=(121, 192, 255), width=3)
    draw.text((left, 660), "红点：补零后会改成的速度    蓝圈：实际保持或根据完整窗口设定的速度", font=small, fill=(139, 148, 158))
    draw.text((left, 700), "Red: the rate a zero-fill would set. Blue: the rate the session plays. Gray column: the window was dropped.", font=small, fill=(139, 148, 158))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["hold_changes_while_dropped"] != 0:
        raise SystemExit("the held rate moved during a dropout")
    if (rec["dropped"], rec["naive_disagrees_while_dropped"], rec["allowed_changes"]) != (3057, 712, 3379):
        raise SystemExit(f"pace counts moved: {rec['dropped']} {rec['naive_disagrees_while_dropped']} {rec['allowed_changes']}")
    figure(rec, ROOT / "docs" / "figures" / "pace.png")
    out = ROOT / "results" / "PACE.json"
    # The trace is for the figure. The pinned file keeps the counts.
    stored = {k: v for k, v in rec.items() if k != "trace"}
    stored["trace_len"] = len(rec["trace"])
    out.write_text(json.dumps(stored, indent=2) + "\n")
    json.dump(stored, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
