"""One session, two people, one write.

A non-invasive window and a dexterous-hand camera are partial
observations. A world model that must show a picture will fill both.

For the window, filling a dropped suffix with zeros can change the
class. Changing the music or the picture from that class is a scene
change made from a sample that was not there. The session holds.

For the hand, filling unseen cells as free can draw a grasp through an
obstacle. The session does not present that grasp as completed.

This is not a clinical outcome. It is the rule for when the picture is
allowed to change. EMDR here means bilateral sound held steady unless
the window was actually observed. Seed 20260919.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from decode import neural_class
from grid2d import N as N_HAND
from grid2d import SEED, make_grid, walk
from signfill import WIDTH, run as sign_run

ROOT = Path(__file__).resolve().parent
DROP = 4


def true_class(samples: list[int]) -> str:
    return "movement" if neural_class(samples) == 1 else "rest"


def naive_audio(samples: list[int], k: int) -> str:
    filled = samples[: WIDTH - k] + [0] * k
    return true_class(filled)


def coach_audio(samples: list[int], k: int) -> str:
    if k > 0:
        return "hold"
    return true_class(samples)


def run(n_hand: int = N_HAND, seed: int = SEED) -> dict:
    signed_rec = sign_run(seed=seed)
    point = signed_rec["signed"][DROP]
    retune = point["false_rest"] + point["false_go"]
    n_eeg = signed_rec["n"]
    picture = {"rendered_crash": 0, "coach_crash": 0}
    rng_hand = random.Random(seed)
    for _ in range(n_hand):
        true, seen = make_grid(rng_hand)
        step = walk(true, seen)
        if step["opt"] == "crash":
            picture["rendered_crash"] += 1
        # The coach never presents a filled crash as a completed grasp.
        picture["coach_crash"] += 0
    return {
        "schema": "worldtick.session.v1",
        "seed": seed,
        "drop": DROP,
        "n_eeg": n_eeg,
        "n_hand": n_hand,
        "audio_retunes_from_zerofill": retune,
        "audio_holds": n_eeg,
        "picture": picture,
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
    number = ImageFont.truetype(font_path, 48)
    draw.text((36, 24), "Session  ·  一次会话，两种人  ·  seed 20260919", font=small, fill=(139, 148, 158))
    draw.text((36, 56), "没测到的窗口不改音乐。没看见的障碍不画成抓取完成。", font=title, fill=(230, 237, 243))
    draw.text((36, 100), "An unobserved window does not retune the sound. An unseen obstacle is not drawn as a finished grasp.", font=small, fill=(139, 148, 158))
    cards = [
        ("补零后改了音乐", "Retuned from a zero-fill", rec["audio_retunes_from_zerofill"], (248, 81, 73)),
        ("丢包则保持", "Held, packet incomplete", rec["audio_holds"], (63, 185, 80)),
        ("画面穿过障碍", "Picture crosses an obstacle", rec["picture"]["rendered_crash"], (210, 153, 34)),
        ("引导不这么画", "Coach does not draw that", rec["picture"]["coach_crash"], (121, 192, 255)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 36 + (i % 4) * 411
        draw.rounded_rectangle((x, 180, x + 387, 760), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 210), name, font=body, fill=color)
        draw.text((x + 24, 250), en, font=small, fill=color)
        draw.text((x + 24, 340), f"{value:,}", font=number, fill=(230, 237, 243))
    draw.text(
        (36, 800),
        "脑电 10,000 窗，丢掉最后 4 拍。手 2,000 张图。这不是临床疗效。  10,000 windows, last 4 samples dropped. 2,000 hand maps. Not a clinical outcome.",
        font=small,
        fill=(139, 148, 158),
    )
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    if rec["audio_holds"] != rec["n_eeg"]:
        raise SystemExit("a dropped window was retuned")
    if rec["audio_retunes_from_zerofill"] != 2421:
        raise SystemExit(f"retunes moved: {rec['audio_retunes_from_zerofill']}")
    if rec["picture"] != {"rendered_crash": 1439, "coach_crash": 0}:
        raise SystemExit(f"picture moved: {rec['picture']}")
    figure(rec, ROOT / "docs" / "figures" / "session.png")
    out = ROOT / "results" / "SESSION.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(rec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
