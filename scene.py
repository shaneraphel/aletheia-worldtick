"""A clearing drawn from the nature models, with the hand behind the check.

Four CC0 models from Kenney's Nature Kit stand in fixed places. The hand
walks a fixed path. The picture the user sees advances only when both the
brain stretch and the finger angle arrived. The guessed picture advances
on every step. Seed 20260919, sixteen steps.
"""
from __future__ import annotations

import json
import platform
import random
import sys
from pathlib import Path

from gate import Gate
from grid2d import SEED

ROOT = Path(__file__).resolve().parent
KIT = ROOT / "resources" / "kenney"
STEPS = 16
DROP = 0.30

PLACEMENTS = [
    ("tree_simple.obj", (-1.6, 0.4), 1.0),
    ("tree_simple.obj", (1.5, -0.2), 0.85),
    ("tree_simple.obj", (0.2, 1.6), 1.15),
    ("rock_smallA.obj", (-0.4, -0.8), 1.2),
    ("stump_round.obj", (1.1, 0.9), 1.0),
    ("tent_smallClosed.obj", (-1.3, -1.2), 0.9),
]
PATH = [(-1.35 + i * 0.15, -0.55 + i * 0.08) for i in range(17)]


def load_obj(path: Path) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    verts = []
    faces = []
    for line in path.read_text().splitlines():
        if line.startswith("v "):
            _, x, y, z = line.split()[:4]
            verts.append((float(x), float(y), float(z)))
        elif line.startswith("f "):
            idx = []
            for part in line.split()[1:]:
                idx.append(int(part.split("/")[0]) - 1)
            for i in range(1, len(idx) - 1):
                faces.append((idx[0], idx[i], idx[i + 1]))
    return verts, faces


def mesh() -> tuple[list, int]:
    tris = []
    verts = 0
    for name, (px, pz), scale in PLACEMENTS:
        vs, fs = load_obj(KIT / name)
        verts += len(vs)
        for a, b, c in fs:
            tri = []
            for i in (a, b, c):
                x, y, z = vs[i]
                tri.append((px + x * scale, y * scale, pz + z * scale))
            tris.append(tri)
    return tris, verts


def project(x: float, y: float, z: float) -> tuple[float, float, float]:
    sx = 520 + (x - z) * 150
    sy = 430 - y * 150 + (x + z) * 46
    return sx, sy, x + z


def footprints() -> list[tuple[str, float, float, float, float]]:
    boxes = []
    for name, (px, pz), scale in PLACEMENTS:
        vs, _ = load_obj(KIT / name)
        xs = [px + x * scale for x, _, _ in vs]
        zs = [pz + z * scale for _, _, z in vs]
        boxes.append((name, min(xs), max(xs), min(zs), max(zs)))
    return boxes


def inside(at: int) -> list[str]:
    x, z = PATH[at]
    return [name for name, x0, x1, z0, z1 in footprints() if x0 <= x <= x1 and z0 <= z <= z1]


def walk(seed: int = SEED, n: int = STEPS) -> dict:
    rng = random.Random(seed)
    held = Gate()
    guess_at = 0
    for _ in range(n):
        brain = None if rng.random() < DROP else int(rng.random() < 0.5)
        finger = None if rng.random() < DROP else rng.randrange(8)
        held.step(brain, finger)
        guess_at = min(guess_at + 1, len(PATH) - 1)
    held_at = 0
    for brain, finger in held.rows:
        if brain is not None and finger is not None and held_at + 1 < len(PATH):
            held_at += 1
    replay = held.replay()
    return {
        "held_at": held_at,
        "guess_at": len(PATH) - 1 if n >= len(PATH) else n,
        "new_steps": sum(1 for b, f in held.rows if b is not None and f is not None),
        "replay_mismatch": sum(1 for a, b in zip(held.shown, replay) if a != b),
        "held_inside": inside(held_at),
        "guess_inside": inside(guess_at),
        "steps": n,
    }


def draw(tris: list, hand_at: int | None, path: Path) -> None:
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (1040, 640), (18, 28, 22))
    draw = ImageDraw.Draw(image)
    painted = []
    for tri in tris:
        pts = [project(*p) for p in tri]
        depth = sum(p[2] for p in pts) / 3
        height = sum(p[1] for p in tri) / 3
        if height > 0.7:
            color = (46, 120, 62)
        elif height > 0.25:
            color = (90, 78, 48)
        else:
            color = (72, 86, 64)
        painted.append((depth, [(p[0], p[1]) for p in pts], color))
    for _, pts, color in sorted(painted, key=lambda item: -item[0]):
        draw.polygon(pts, fill=color)
    if hand_at is not None:
        hx, hy, _ = project(PATH[hand_at][0], 0.15, PATH[hand_at][1])
        draw.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), fill=(230, 237, 243))
    image.save(path, quality=92)


def run(seed: int = SEED) -> dict:
    tris, verts = mesh()
    walked = walk(seed)
    draw(tris, None, ROOT / "docs" / "figures" / "clearing-camp.png")
    draw(tris, None, ROOT / "site" / "clearing-camp.png")
    draw(tris, walked["held_at"], ROOT / "docs" / "figures" / "clearing-held.png")
    draw(tris, walked["guess_at"], ROOT / "docs" / "figures" / "clearing-guess.png")
    return {
        "schema": "worldtick.scene.v1",
        "seed": seed,
        "models": [name for name, _, _ in PLACEMENTS],
        "vertices": verts,
        "triangles": len(tris),
        **walked,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def main() -> int:
    rec = run()
    pinned = (205, 478, 6, 16, 6, 0)
    got = (rec["vertices"], rec["triangles"], rec["held_at"], rec["guess_at"], rec["new_steps"], rec["replay_mismatch"])
    if got != pinned:
        raise SystemExit(f"clearing counts moved: {got}")
    if rec["held_inside"] != [] or rec["guess_inside"] != ["stump_round.obj"]:
        raise SystemExit(f"clearing overlap moved: {rec['held_inside']} {rec['guess_inside']}")
    out = ROOT / "results" / "SCENE.json"
    out.write_text(json.dumps(rec, indent=2) + "\n")
    json.dump(
        {"vertices": rec["vertices"], "held_at": rec["held_at"], "guess_at": rec["guess_at"], "new_steps": rec["new_steps"]},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
