"""The picture catches up on the first full arrival.

Steps 6, 7, and 8 of every session miss both streams. Before and after
the burst each stream misses with probability 0.30, independently. The
world still draws true values on every step: the brain is a movement
with probability 1/2, and the finger is uniform on 0..7 with 0 closed.
An arrival adopts the true value, so the held picture equals the truth
from the first step after the burst on which both streams arrive. That
step is when the picture has caught up.

Between the burst and that step, the held picture shows pre-burst
values for whatever is still late, while the guessed picture shows
defaults. Both can match the truth by luck there, and both are counted.

Seed 20260919. Ten thousand sessions, sixteen steps. The same session
index uses the same stream on one core and on many.
"""
from __future__ import annotations

import json
import os
import platform
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from fleet import cuts
from grid2d import SEED

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000
STEPS = 16
DROP = 0.30
BURST = (6, 7, 8)
BURST_END = 8


def session_stream(index: int, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (index + 1))
    out = []
    for step in range(STEPS):
        true_brain = int(rng.random() < 0.5)
        true_finger = rng.randrange(8)
        if step in BURST:
            out.append((None, None, true_brain, true_finger))
            continue
        brain = None if rng.random() < DROP else true_brain
        finger = None if rng.random() < DROP else true_finger
        out.append((brain, finger, true_brain, true_finger))
    return out


def session(stream: list) -> dict:
    held_fast = False
    held_closed = False
    acc = {
        "delay_sum": 0,
        "never": 0,
        "held_before": 0,
        "guess_before": 0,
        "before_steps": 0,
        "resync_mismatch": 0,
    }
    hist = {d: 0 for d in range(1, 8)}
    caught = False
    delay = 0
    for step, (brain, finger, true_brain, true_finger) in enumerate(stream):
        truth = (true_brain == 1, true_finger == 0)
        if brain is None:
            guess_fast = False
            show_fast = held_fast
        else:
            guess_fast = brain == 1
            show_fast = guess_fast
            held_fast = show_fast
        if finger is None:
            guess_closed = True
            show_closed = held_closed
        else:
            guess_closed = finger == 0
            show_closed = guess_closed
            held_closed = show_closed
        if step > BURST_END and not caught:
            if brain is not None and finger is not None:
                caught = True
                delay = step - BURST_END
                hist[delay] += 1
                if (show_fast, show_closed) != truth:
                    acc["resync_mismatch"] += 1
            else:
                acc["before_steps"] += 1
                if (show_fast, show_closed) == truth:
                    acc["held_before"] += 1
                if (guess_fast, guess_closed) == truth:
                    acc["guess_before"] += 1
    if caught:
        acc["delay_sum"] += delay
    else:
        acc["never"] += 1
    for d in range(1, 8):
        acc[f"delay{d}"] = hist[d]
    return acc


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    keys = ["delay_sum", "never", "held_before", "guess_before", "before_steps", "resync_mismatch"]
    keys += [f"delay{d}" for d in range(1, 8)]
    acc = {k: 0 for k in keys}
    acc["sessions"] = 0
    for i in range(start, stop):
        row = session(session_stream(i, seed))
        for key in keys:
            acc[key] += row[key]
        acc["sessions"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    return {
        "schema": "worldtick.catchup.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": DROP,
        "burst": list(BURST),
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def figure(rec: dict, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 720), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    number = ImageFont.truetype(font_path, 48)
    s = rec["serial"]
    draw.text((36, 24), "Catch up on the first full arrival  ·  两边都到的第一步，画面就追上了", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "三步全断之后，数一数第几步追上。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "After a three-step burst, count the steps until the picture matches the truth.", font=small, fill=(139, 148, 158))
    cards = [
        ("断完第一步就追上", "Sessions caught up on the first step back", f"{s['delay1']:,}", (63, 185, 80)),
        ("七步还没追上", "Sessions still not caught up after seven steps", f"{s['never']:,}", (210, 153, 34)),
        ("追上之前留对的", "Held matches before the catch-up step", f"{s['held_before']:,}", (121, 192, 255)),
    ]
    for i, (name, en, value, color) in enumerate(cards):
        x = 48 + i * 540
        draw.rounded_rectangle((x, 180, x + 500, 620), radius=16, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x + 24, 214), name, font=body, fill=color)
        draw.text((x + 24, 264), en, font=small, fill=color)
        draw.text((x + 24, 370), value, font=number, fill=(230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    rec = run()
    s = rec["serial"]
    if not rec["equal"]:
        raise SystemExit(f"catchup cores disagree: {s}")
    pinned = (19448, 87, 6022, 2693, 10144, 0)
    got = (s["delay_sum"], s["never"], s["held_before"], s["guess_before"], s["before_steps"], s["resync_mismatch"])
    if got != pinned:
        raise SystemExit(f"catchup counts moved: {got}")
    hist_pinned = (4938, 2531, 1230, 646, 311, 180, 77)
    hist_got = tuple(s[f"delay{d}"] for d in range(1, 8))
    if hist_got != hist_pinned:
        raise SystemExit(f"catchup histogram moved: {hist_got}")
    figure(rec, ROOT / "docs" / "figures" / "catchup.png")
    out = ROOT / "results" / "CATCHUP.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    slim = {k: s[k] for k in ("delay_sum", "never", "held_before", "guess_before", "before_steps", "resync_mismatch", "sessions")}
    slim.update({f"delay{d}": s[f"delay{d}"] for d in range(1, 8)})
    json.dump({"serial": slim, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
