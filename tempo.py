"""Speeding what is left so the phrase finishes on time is not the recording.

The playhead that waits for a new picture ends at the number of new
pictures in the session. On these sessions that number never reaches
the end of the piece, so every session is short. The speed that would
finish on time has to know, at the first step, how many new pictures
the rest of the session will bring. Doubling the advance on each new
picture does not need that number. It finishes only the sessions that
were not already in the first half, and in part of those it plays on
after the recording has ended.

Same sessions as the phrase. One core and many.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from fleet import cuts
from grid2d import SEED
from phrase import STEPS, session as phrase_session

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    hist = [0] * (STEPS + 1)
    overshoot = 0
    for i in range(start, stop):
        row = phrase_session(i, seed)
        sent = row["sent"]
        if not 0 <= sent <= STEPS:
            raise RuntimeError("the picture playhead left the piece")
        hist[sent] += 1
        overshoot += row["overshoot"]
    return {"hist": hist, "overshoot": overshoot, "sessions": stop - start}


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def derive(raw: dict) -> dict:
    hist = raw["hist"]
    sessions = raw["sessions"]
    sent = sum(i * hist[i] for i in range(len(hist)))
    present = [i for i in range(len(hist)) if hist[i]]
    floor = min(present)
    nearest = max(present)
    mode = max(range(len(hist)), key=lambda i: (hist[i], -i))
    double_exact = hist[STEPS // 2]
    double_past = sum(hist[STEPS // 2 + 1 :])
    double_short = sum(hist[: STEPS // 2])
    return {
        "hist": hist,
        "sessions": sessions,
        "sent": sent,
        "tick": sessions * STEPS,
        "shortfall": sessions * STEPS - sent,
        "floor": floor,
        "floor_sessions": hist[floor],
        "nearest": nearest,
        "at_nearest": hist[nearest],
        "left_at_nearest": STEPS - nearest,
        "mode": mode,
        "mode_n": hist[mode],
        "double_exact": double_exact,
        "double_past": double_past,
        "double_finish": double_exact + double_past,
        "double_short": double_short,
        "finished": hist[STEPS],
        "overshoot": raw["overshoot"],
    }


def run(n: int = SESSIONS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = derive(shard(0, n, seed))
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        with ProcessPoolExecutor(max_workers=len(parts)) as pool:
            pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        merged = {
            "hist": [sum(p["hist"][i] for p in pieces) for i in range(STEPS + 1)],
            "overshoot": sum(p["overshoot"] for p in pieces),
            "sessions": sum(p["sessions"] for p in pieces),
        }
        parallel = derive(merged)
    return {
        "schema": "worldtick.tempo.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
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
    draw.text((36, 24), "Speeding what is left is not this recording  ·  加快剩下的，就不是这段录音", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "要在段尾放完，就得先知道后面还有多少张新画面。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Doubling the tempo does not look ahead. Some sessions still fall short. Others play on after the piece has ended.", font=small, fill=(139, 148, 158))
    cards = [
        ("没放完的步数", "Steps the waiting phrase never plays", f"{s['shortfall']:,}", (218, 54, 51)),
        ("两倍速能放完", "Sessions a doubled tempo would finish", f"{s['double_finish']:,}", (63, 185, 80)),
        ("放到头以后还在走", "Of those, sessions that run past the end", f"{s['double_past']:,}", (227, 179, 65)),
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
        raise SystemExit(f"tempo cores disagree: {s}")
    if s["overshoot"] != 0 or s["finished"] != 0 or s["sent"] != 68676:
        raise SystemExit(f"tempo does not match the phrase: {s}")
    if s["shortfall"] + s["sent"] != s["tick"]:
        raise SystemExit(f"tempo shortfall does not add up: {s}")
    pinned = (91324, 3532, 1799, 1733, 2226, 2, 1, 3)
    got = (
        s["shortfall"],
        s["double_finish"],
        s["double_exact"],
        s["double_past"],
        s["mode_n"],
        s["left_at_nearest"],
        s["floor"],
        s["floor_sessions"],
    )
    if got != pinned:
        raise SystemExit(f"tempo counts moved: {got}")
    if s["hist"] != [0, 3, 42, 172, 630, 1353, 2042, 2226, 1799, 1046, 467, 172, 39, 8, 1, 0, 0]:
        raise SystemExit(f"tempo endings moved: {s['hist']}")
    if s["double_exact"] + s["double_past"] != s["double_finish"]:
        raise SystemExit(f"tempo double does not add up: {s}")
    if s["double_short"] != 6468 or s["mode"] != 7 or s["nearest"] != 14:
        raise SystemExit(f"tempo shape moved: {s}")
    figure(rec, ROOT / "docs" / "figures" / "tempo.png")
    out = ROOT / "results" / "TEMPO.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("shortfall", "double_finish", "double_exact", "double_past", "mode_n", "left_at_nearest", "floor_sessions")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
