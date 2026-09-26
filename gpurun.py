"""One batch, two processors.

One hundred thousand sessions of sixteen steps. The CPU draws shared
integer uniforms and counts new frames and guess-held disagreement with
integer compares against the threshold T = floor(0.3 * 2^32). The Mac
GPU counts the same integers with the same compares, one thread per
session. The two per-session arrays must match elementwise.

This is macOS-only and is not in CI. results/GPU.json carries the
pinned Mac run so the number checker still verifies it anywhere.

Seed 20260919.
"""
from __future__ import annotations

import array
import json
import platform
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from grid2d import SEED

ROOT = Path(__file__).resolve().parent
N = 100000
STEPS = 16
T = int(0.3 * 2**32)
assert T == 1288490188

GPU_DIR = ROOT / "gpucount"


def gen_uniforms(n: int = N, seed: int = SEED) -> array.array:
    rng = random.Random(seed)
    return array.array("I", rng.randbytes(n * STEPS * 4 * 4))


def cpu_reference(uni: array.array, n: int) -> tuple[list, list]:
    news: list[int] = []
    differs: list[int] = []
    for i in range(n):
        held_fast = False
        held_closed = False
        nnew = 0
        ndiff = 0
        base = i * STEPS * 4
        for s in range(STEPS):
            u0 = uni[base + s * 4 + 0]
            u1 = uni[base + s * 4 + 1]
            u2 = uni[base + s * 4 + 2]
            u3 = uni[base + s * 4 + 3]
            bmiss = u0 < T
            fmiss = u1 < T
            bv = (u2 & 1) != 0
            fv = (u3 & 7) == 0
            gfast = False if bmiss else bv
            gclosed = True if fmiss else fv
            if bmiss:
                sfast = held_fast
            else:
                sfast = bv
                held_fast = bv
            if fmiss:
                sclosed = held_closed
            else:
                sclosed = fv
                held_closed = fv
            if not bmiss and not fmiss:
                nnew += 1
            if gfast != sfast or gclosed != sclosed:
                ndiff += 1
        news.append(nnew)
        differs.append(ndiff)
    return news, differs


def build_driver(work: Path) -> Path:
    binary = work / "gpudriver"
    sources = [GPU_DIR / "main.swift", GPU_DIR / "count.metal"]
    if binary.exists() and all(binary.stat().st_mtime >= s.stat().st_mtime for s in sources):
        return binary
    proc = subprocess.run(
        ["swiftc", "-O", "-o", str(binary), str(GPU_DIR / "main.swift")],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"swiftc failed:\n{proc.stderr}")
    return binary


def gpu_counts(uni: array.array, n: int) -> tuple[dict, list, list]:
    if sys.platform != "darwin" or shutil.which("swiftc") is None:
        raise SystemExit("gpu run needs macOS with swiftc and Metal")
    work = Path(tempfile.mkdtemp(prefix="worldtick-gpu"))
    uni_path = work / "uniforms.bin"
    new_path = work / "out_new.bin"
    differ_path = work / "out_differ.bin"
    with open(uni_path, "wb") as f:
        uni.tofile(f)
    binary = build_driver(work)
    proc = subprocess.run(
        [str(binary), str(uni_path), str(new_path), str(differ_path), str(n)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"gpu driver failed:\n{proc.stderr}")
    summary = json.loads(proc.stdout)
    news = array.array("I")
    differs = array.array("I")
    with open(new_path, "rb") as f:
        news.fromfile(f, n)
    with open(differ_path, "rb") as f:
        differs.fromfile(f, n)
    return summary, list(news), list(differs)


def run(n: int = N, seed: int = SEED) -> dict:
    uni = gen_uniforms(n, seed)
    cpu_new, cpu_differ = cpu_reference(uni, n)
    summary, gpu_new, gpu_differ = gpu_counts(uni, n)
    mismatch = sum(1 for a, b, c, d in zip(cpu_new, gpu_new, cpu_differ, gpu_differ) if a != b or c != d)
    return {
        "schema": "worldtick.gpu.v1",
        "seed": seed,
        "sessions": n,
        "steps_each": STEPS,
        "steps": n * STEPS,
        "threshold": T,
        "cpu": {"new": sum(cpu_new), "differ": sum(cpu_differ)},
        "gpu": {"new": sum(gpu_new), "differ": sum(gpu_differ), "device": summary["device"]},
        "mismatch": mismatch,
        "arrays_match": mismatch == 0,
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
    draw.text((36, 24), "One batch, two processors  ·  同一批随机数，两种芯片各数一遍", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "十万段，CPU 和 GPU 数出同一个数。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "One hundred thousand sessions. The CPU and the GPU count the same batch.", font=small, fill=(139, 148, 158))
    cards = [
        ("CPU 数出全新的", "New frames counted by the CPU", f"{rec['cpu']['new']:,}", (121, 192, 255)),
        ("GPU 数出全新的", "New frames counted by the GPU", f"{rec['gpu']['new']:,}", (63, 185, 80)),
        ("两边对不上", "Sessions where the two counts differ", f"{rec['mismatch']:,}", (218, 54, 51)),
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
    if not rec["arrays_match"]:
        raise SystemExit(f"cpu and gpu disagree on {rec['mismatch']} sessions")
    pinned = (783232, 586904)
    if (rec["cpu"]["new"], rec["cpu"]["differ"]) != pinned:
        raise SystemExit(f"cpu counts moved: {rec['cpu']}")
    if (rec["gpu"]["new"], rec["gpu"]["differ"]) != pinned:
        raise SystemExit(f"gpu counts moved: {rec['gpu']}")
    figure(rec, ROOT / "docs" / "figures" / "gpu.png")
    out = ROOT / "results" / "GPU.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(
        {"cpu": rec["cpu"], "gpu": rec["gpu"], "mismatch": rec["mismatch"], "device": rec["gpu"]["device"]},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
