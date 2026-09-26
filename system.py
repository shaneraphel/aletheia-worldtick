"""Draw the system from a manifest: arrivals, the check, the model, the record.

NODES is the inventory. EDGES is who hands to whom. The figure is drawn
from these two lists, and they are saved as results/SYSTEM.json so the
diagram and the inventory cannot drift apart.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NODES = [
    {"id": "arrivals", "cn": "脑电和手指", "en": "brain and finger", "col": 0, "row": 1},
    {"id": "check", "cn": "检查", "en": "the check", "col": 1, "row": 1},
    {"id": "model", "cn": "世界模型", "en": "world model", "col": 2, "row": 1},
    {"id": "scene", "cn": "画面和声音", "en": "picture and sound", "col": 3, "row": 1},
    {"id": "record", "cn": "记录", "en": "record", "col": 1, "row": 2},
    {"id": "replay", "cn": "重算", "en": "replay", "col": 2, "row": 2},
]

EDGES = [
    ("arrivals", "check"),
    ("check", "model"),
    ("model", "scene"),
    ("check", "record"),
    ("record", "replay"),
    ("replay", "check"),
]


def figure(nodes: list, edges: list, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    image = Image.new("RGB", (1680, 880), (14, 17, 22))
    draw = ImageDraw.Draw(image)
    small = ImageFont.truetype(font_path, 18)
    title = ImageFont.truetype(font_path, 28)
    body = ImageFont.truetype(font_path, 22)
    draw.text((36, 24), "Where the check sits  ·  检查坐在什么位置", font=small, fill=(139, 148, 158))
    draw.text((36, 60), "检查坐在世界模型前面，记录坐在检查下面。", font=title, fill=(230, 237, 243))
    draw.text((36, 108), "The check sits in front of the world model. The record sits below the check.", font=small, fill=(139, 148, 158))

    def box(col: int, row: int) -> tuple[int, int, int, int]:
        x = 90 + col * 390
        y = 220 + row * 220
        return x, y, x + 320, y + 140

    centers = {}
    for node in nodes:
        x0, y0, x1, y1 = box(node["col"], node["row"])
        centers[node["id"]] = ((x0 + x1) // 2, (y0 + y1) // 2)
        color = (121, 192, 255) if node["id"] == "check" else (139, 148, 158)
        draw.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=(22, 27, 34), outline=color, width=2)
        draw.text((x0 + 24, y0 + 22), node["cn"], font=body, fill=(230, 237, 243))
        draw.text((x0 + 24, y0 + 62), node["en"], font=small, fill=color)

    def arrow(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        draw.line((x0, y0, x1, y1), fill=color, width=3)
        if x1 > x0:
            draw.polygon([(x1 - 14, y1 - 9), (x1 - 14, y1 + 9), (x1, y1)], fill=color)
        elif x1 < x0:
            draw.polygon([(x1 + 14, y1 - 9), (x1 + 14, y1 + 9), (x1, y1)], fill=color)
        elif y1 > y0:
            draw.polygon([(x1 - 9, y1 - 14), (x1 + 9, y1 - 14), (x1, y1)], fill=color)
        else:
            draw.polygon([(x1 - 9, y1 + 14), (x1 + 9, y1 + 14), (x1, y1)], fill=color)

    def dashed(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        span = max(abs(x1 - x0), abs(y1 - y0), 1)
        steps = max(span // 14, 1)
        for t in range(0, steps, 2):
            fx = x0 + (x1 - x0) * t // steps
            fy = y0 + (y1 - y0) * t // steps
            tx = x0 + (x1 - x0) * (t + 1) // steps
            ty = y0 + (y1 - y0) * (t + 1) // steps
            draw.line((fx, fy, tx, ty), fill=color, width=3)

    for a, b in edges:
        x0, y0 = centers[a]
        x1, y1 = centers[b]
        if (a, b) == ("replay", "check"):
            sx, sy = x0, y0 - 78
            ex, ey = x1, y1 + 78
            dashed(sx, sy, ex, ey, (99, 109, 119))
            import math

            dx, dy = ex - sx, ey - sy
            leng = math.hypot(dx, dy)
            ux, uy = dx / leng, dy / leng
            px, py = -uy, ux
            draw.polygon(
                [(ex - 16 * ux + 9 * px, ey - 16 * uy + 9 * py), (ex - 16 * ux - 9 * px, ey - 16 * uy - 9 * py), (ex, ey)],
                fill=(99, 109, 119),
            )
            draw.text(((sx + ex) // 2 - 110, (sy + ey) // 2 - 16), "对上 match", font=small, fill=(99, 109, 119))
        elif y0 == y1:
            gap = 168
            arrow(x0 + gap if x1 > x0 else x0 - gap, y0, x1 - gap if x1 > x0 else x1 + gap, y1, (230, 237, 243))
        else:
            gap = 78
            arrow(x0, y0 + gap if y1 > y0 else y0 - gap, x1, y1 - gap if y1 > y0 else y1 + gap, (230, 237, 243))
    image.save(path, quality=92)


def main() -> int:
    manifest = {"schema": "worldtick.system.v1", "nodes": NODES, "edges": [list(e) for e in EDGES]}
    ids = [n["id"] for n in NODES]
    if len(ids) != 6 or len(EDGES) != 6:
        raise SystemExit(f"system inventory moved: {len(ids)} nodes, {len(EDGES)} edges")
    for a, b in EDGES:
        if a not in ids or b not in ids:
            raise SystemExit(f"edge leaves the inventory: {(a, b)}")
    figure(NODES, EDGES, ROOT / "docs" / "figures" / "system.png")
    out = ROOT / "results" / "SYSTEM.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    json.dump({"nodes": len(ids), "edges": len(EDGES)}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
