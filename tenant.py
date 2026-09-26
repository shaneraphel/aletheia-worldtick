"""One tenant's late signal does not move another tenant's picture.

A compute service holds one picture per tenant: the last sound and the
last finger that tenant actually sent. Requests from different tenants
arrive interleaved. The update for a request reads and writes only the
held picture of the tenant that sent it.

So the sequence a tenant sees depends only on that tenant's own
requests. Serving tenants one after another, serving them round-robin,
and adding a tenant that never sends anything all show each tenant the
same sequence.

Each request carries a brain stretch and a finger angle, each missing
with probability 0.30, independently. When the stretch arrives it is a
movement with probability 1/2. When the angle arrives it is uniform on
0..7, and 0 means the finger is closed. Before a tenant's first arrival
the sound stays slow and the finger is not drawn closed.

Seed 20260919. Sixteen tenants, five hundred requests each. Tenants are
split across cores by index, so one core and many cores agree.
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
TENANTS = 16
REQUESTS = 500
DROP = 0.30


def tenant_requests(tenant: int, n: int = REQUESTS, seed: int = SEED) -> list:
    rng = random.Random(seed + 10007 * (tenant + 1))
    out = []
    for _ in range(n):
        brain_missing = rng.random() < DROP
        finger_missing = rng.random() < DROP
        brain = None if brain_missing else int(rng.random() < 0.5)
        finger = None if finger_missing else rng.randrange(8)
        out.append((brain, finger))
    return out


def serve_sequence(requests: list) -> tuple[list, dict]:
    held_fast = False
    held_closed = False
    shown: list[tuple[bool, bool]] = []
    counts = {"differ": 0, "held_requests": 0, "full_updates": 0}
    for brain, finger in requests:
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
        shown.append((show_fast, show_closed))
        if (guess_fast, guess_closed) != (show_fast, show_closed):
            counts["differ"] += 1
        if brain is None or finger is None:
            counts["held_requests"] += 1
        else:
            counts["full_updates"] += 1
    return shown, counts


def serve_interleaved(order: list[tuple[int, tuple]]) -> dict[int, list]:
    held: dict[int, tuple[bool, bool]] = {}
    shown: dict[int, list] = {}
    for tenant, (brain, finger) in order:
        fast, closed = held.get(tenant, (False, False))
        if brain is not None:
            fast = brain == 1
        if finger is not None:
            closed = finger == 0
        held[tenant] = (fast, closed)
        shown.setdefault(tenant, []).append((fast, closed))
    return shown


def shard(start: int, stop: int, seed: int = SEED) -> dict:
    acc = {"differ": 0, "held_requests": 0, "full_updates": 0, "requests": 0, "tenants": 0}
    for tenant in range(start, stop):
        _, counts = serve_sequence(tenant_requests(tenant, REQUESTS, seed))
        for key, value in counts.items():
            acc[key] += value
        acc["requests"] += REQUESTS
        acc["tenants"] += 1
    return acc


def _pack(item: tuple[int, int, int]) -> dict:
    return shard(*item)


def run(n_tenants: int = TENANTS, n_requests: int = REQUESTS, seed: int = SEED, workers: int | None = None) -> dict:
    serial = shard(0, n_tenants, seed) if n_requests == REQUESTS else _custom_shard(n_tenants, n_requests, seed)
    workers = os.cpu_count() or 1 if workers is None else workers
    parts = cuts(n_tenants, workers)
    if len(parts) == 1:
        parallel = serial
    else:
        if n_requests == REQUESTS:
            with ProcessPoolExecutor(max_workers=len(parts)) as pool:
                pieces = list(pool.map(_pack, [(a, b, seed) for a, b in parts]))
        else:
            with ProcessPoolExecutor(max_workers=len(parts)) as pool:
                pieces = list(pool.map(_custom_pack, [(a, b, n_requests, seed) for a, b in parts]))
        parallel = {key: sum(p[key] for p in pieces) for key in serial}
    streams = {t: tenant_requests(t, n_requests, seed) for t in range(n_tenants)}
    grouped = {t: serve_sequence(streams[t])[0] for t in range(n_tenants)}
    order = [(t, streams[t][k]) for k in range(n_requests) for t in range(n_tenants)]
    interleaved = serve_interleaved(order)
    isolated = sum(1 for t in range(n_tenants) if grouped[t] == interleaved[t])
    noisy_order = list(order)
    for k in range(n_requests):
        noisy_order.insert(2 * k + 1, (n_tenants, (None, None)))
    noisy = serve_interleaved(noisy_order)
    noisy_unchanged = sum(1 for t in range(n_tenants) if noisy[t] == grouped[t])
    return {
        "schema": "worldtick.tenant.v1",
        "seed": seed,
        "tenants": n_tenants,
        "requests_each": n_requests,
        "drop": DROP,
        "workers": len(parts),
        "serial": serial,
        "parallel": parallel,
        "equal": serial == parallel,
        "isolated": isolated,
        "noisy_unchanged": noisy_unchanged,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def _custom_shard(n_tenants: int, n_requests: int, seed: int) -> dict:
    acc = {"differ": 0, "held_requests": 0, "full_updates": 0, "requests": 0, "tenants": 0}
    for tenant in range(n_tenants):
        _, counts = serve_sequence(tenant_requests(tenant, n_requests, seed))
        for key, value in counts.items():
            acc[key] += value
        acc["requests"] += n_requests
        acc["tenants"] += 1
    return acc


def _custom_pack(item: tuple[int, int, int, int]) -> dict:
    start, stop, n_requests, seed = item
    acc = {"differ": 0, "held_requests": 0, "full_updates": 0, "requests": 0, "tenants": 0}
    for tenant in range(start, stop):
        _, counts = serve_sequence(tenant_requests(tenant, n_requests, seed))
        for key, value in counts.items():
            acc[key] += value
        acc["requests"] += n_requests
        acc["tenants"] += 1
    return acc


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
    draw.text((36, 24), "Tenants do not move each other  ·  谁晚到，也不改别人的画面", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "十六家排着来，和轮着来，每家看见的画面是一样的。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "Served one after another or round-robin, each tenant sees the same sequence.", font=small, fill=(139, 148, 158))
    cards = [
        ("前后顺序不改画面", "Tenants with identical sequences", f"{rec['isolated']}/{rec['tenants']}", (63, 185, 80)),
        ("猜测和留下的不一样", "The guess and the held picture differ", f"{s['differ']:,}", (218, 54, 51)),
        ("多一家从不发货的", "Tenants unchanged by a silent neighbor", f"{rec['noisy_unchanged']}/{rec['tenants']}", (121, 192, 255)),
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
        raise SystemExit(f"tenant cores disagree: {s}")
    pinned = (2981, 4078, 3922, 8000)
    got = (s["differ"], s["held_requests"], s["full_updates"], s["requests"])
    if got != pinned:
        raise SystemExit(f"tenant counts moved: {got}")
    if rec["isolated"] != rec["tenants"] or rec["noisy_unchanged"] != rec["tenants"]:
        raise SystemExit(f"tenant isolation failed: {rec['isolated']} {rec['noisy_unchanged']}")
    figure(rec, ROOT / "docs" / "figures" / "tenant.png")
    out = ROOT / "results" / "TENANT.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(
        {"serial": s, "equal": rec["equal"], "isolated": rec["isolated"], "noisy_unchanged": rec["noisy_unchanged"]},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
