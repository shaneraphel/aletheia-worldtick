"""Holding the last picture is not painting the gap with the next one.

Anand, Anand, and Vishe hold each sensor at its latest reading. Knowing
when the next sample will arrive does not say what that sample will be,
unless the arrival itself moves the machine. The brain recording and
the finger only report. The picture already shown and the picture that
arrives later are different pictures. A step between them cannot equal
both. On these sessions the picture already shown is the hand that was
there more often.

Same seed and the same stream as the phrase. One core and many.
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
from phrase import DROP, LAST, STEPS

ROOT = Path(__file__).resolve().parent
SESSIONS = 10000


def _bump(bucket: list[int], hold_ok: bool, paste_ok: bool) -> None:
    bucket[(int(hold_ok) << 1) | int(paste_ok)] += 1


def session(index: int, seed: int = SEED) -> dict:
    rng = random.Random(seed + 10007 * (index + 1))
    hand = 0
    shown = 0
    local = False
    theirs = False
    prev = 0
    overshoot = 0
    grip_at: list[bool] = []
    hand_at: list[int] = []
    grip = [0, 0, 0, 0]
    place = [0, 0, 0, 0]
    whole = [0, 0, 0, 0]
    buried = 0
    for t in range(1, STEPS + 1):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        old = hand
        if brain is not None and finger is not None and hand < LAST:
            hand += 1
        if hand - old > 1:
            raise RuntimeError("the sensor index moved by more than one")
        if finger is not None:
            local = finger == 0
        grip_at.append(local)
        hand_at.append(hand)
        if rng.random() >= DROP:
            if hand < shown:
                overshoot += 1
            if not (hand == shown and local == theirs):
                if prev == 0:
                    hold_g, hold_h = False, 0
                else:
                    hold_g, hold_h = grip_at[prev - 1], hand_at[prev - 1]
                for s in range(prev, t - 1):
                    buried += 1
                    grip_hold = hold_g == grip_at[s]
                    grip_paste = local == grip_at[s]
                    place_hold = hold_h == hand_at[s]
                    place_paste = hand == hand_at[s]
                    _bump(grip, grip_hold, grip_paste)
                    _bump(place, place_hold, place_paste)
                    _bump(whole, grip_hold and place_hold, grip_paste and place_paste)
                prev = t
            shown = hand
            theirs = local
    return {
        "buried": buried,
        "grip": grip,
        "place": place,
        "whole": whole,
        "overshoot": overshoot,
    }


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    buried = 0
    overshoot = 0
    grip = [0, 0, 0, 0]
    place = [0, 0, 0, 0]
    whole = [0, 0, 0, 0]
    for i in range(start, stop):
        row = session(i, seed)
        buried += row["buried"]
        overshoot += row["overshoot"]
        for k in range(4):
            grip[k] += row["grip"][k]
            place[k] += row["place"][k]
            whole[k] += row["whole"][k]
    return {
        "buried": buried,
        "grip": grip,
        "place": place,
        "whole": whole,
        "overshoot": overshoot,
        "sessions": stop - start,
    }


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def _right(bucket: list[int], side: str) -> int:
    if side == "hold":
        return bucket[2] + bucket[3]
    return bucket[1] + bucket[3]


def derive(raw: dict) -> dict:
    whole = raw["whole"]
    grip = raw["grip"]
    place = raw["place"]
    return {
        "buried": raw["buried"],
        "sessions": raw["sessions"],
        "overshoot": raw["overshoot"],
        "whole": whole,
        "grip": grip,
        "place": place,
        "hand_hold": _right(whole, "hold"),
        "hand_paste": _right(whole, "paste"),
        "hand_neither": whole[0],
        "hand_both": whole[3],
        "grip_hold": _right(grip, "hold"),
        "grip_paste": _right(grip, "paste"),
        "place_hold": _right(place, "hold"),
        "place_paste": _right(place, "paste"),
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
            "buried": sum(p["buried"] for p in pieces),
            "overshoot": sum(p["overshoot"] for p in pieces),
            "sessions": sum(p["sessions"] for p in pieces),
            "grip": [sum(p["grip"][k] for p in pieces) for k in range(4)],
            "place": [sum(p["place"][k] for p in pieces) for k in range(4)],
            "whole": [sum(p["whole"][k] for p in pieces) for k in range(4)],
        }
        parallel = derive(merged)
    return {
        "schema": "worldtick.hold.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "drop": DROP,
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cited": "https://arxiv.org/abs/2609.07299",
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
    draw.text((36, 24), "Hold the last picture, or paint the next one  ·  留着上一张，还是涂成下一张", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "这两张不是同一只手。上一张更常常就是当时的手。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Knowing when the next sample arrives does not say what the hand was doing in between.", font=small, fill=(139, 148, 158))
    cards = [
        ("留着上一张，手是对的", "Buried steps that match the picture already shown", f"{s['hand_hold']:,}", (63, 185, 80)),
        ("涂成下一张，手是对的", "Buried steps that match the picture that arrives later", f"{s['hand_paste']:,}", (227, 179, 65)),
        ("两张都不是当时的手", "Buried steps that match neither picture", f"{s['hand_neither']:,}", (218, 54, 51)),
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
        raise SystemExit(f"hold cores disagree: {s}")
    if s["overshoot"] != 0 or s["buried"] != 79645 or s["hand_both"] != 0:
        raise SystemExit(f"hold does not match the phrase: {s}")
    pinned = (53182, 10015, 16448, 72672, 63220, 54976, 13882)
    got = (
        s["hand_hold"],
        s["hand_paste"],
        s["hand_neither"],
        s["grip_hold"],
        s["grip_paste"],
        s["place_hold"],
        s["place_paste"],
    )
    if got != pinned:
        raise SystemExit(f"hold counts moved: {got}")
    if s["hand_hold"] + s["hand_paste"] + s["hand_neither"] + s["hand_both"] != s["buried"]:
        raise SystemExit(f"hold hands do not add up: {s}")
    if sum(s["grip"]) != s["buried"] or sum(s["place"]) != s["buried"] or sum(s["whole"]) != s["buried"]:
        raise SystemExit(f"hold buckets do not add up: {s}")
    figure(rec, ROOT / "docs" / "figures" / "hold.png")
    out = ROOT / "results" / "HOLD.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    shown = {key: s[key] for key in ("hand_hold", "hand_paste", "hand_neither", "grip_hold", "grip_paste", "place_hold", "place_paste")}
    json.dump({"serial": shown, "equal": rec["equal"], "steps": rec["steps"]}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
