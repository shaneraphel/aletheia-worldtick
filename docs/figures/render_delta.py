#!/usr/bin/env python3.12
"""Composite a product photo with the measured upstream return."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT = "/Library/Fonts/Arial Unicode.ttf"
BG = (14, 17, 22)
CARD = (22, 27, 34)
AMBER_BG = (42, 33, 20)
AMBER = (210, 153, 34)
GREEN_BG = (18, 38, 28)
GREEN = (63, 185, 80)
TEXT = (230, 237, 243)
MUTED = (139, 148, 158)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        buf = ""
        for ch in paragraph:
            trial = buf + ch
            if draw.textlength(trial, font=fnt) <= width:
                buf = trial
            else:
                if buf:
                    lines.append(buf)
                buf = ch
        if buf:
            lines.append(buf)
    return lines


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, stroke, title: str, body: str) -> None:
    draw.rounded_rectangle(box, radius=16, fill=fill, outline=stroke, width=2)
    x, y, r, _b = box
    draw.text((x + 24, y + 16), title, font=font(18), fill=stroke)
    fnt = font(26)
    yy = y + 52
    for line in wrap(draw, body, fnt, r - x - 48):
        color = TEXT
        if line.startswith("→"):
            color = stroke
        draw.text((x + 24, yy), line, font=fnt, fill=color)
        yy += 36


def compose(photo_name: str, out_name: str, kicker: str, title: str, kept: str, upstream: str, ours: str) -> None:
    W, H = 1680, 940
    canvas = Image.new("RGB", (W, H), BG)
    photo = Image.open(HERE / photo_name).convert("RGB")
    side = 860
    photo.thumbnail((side, 820), Image.Resampling.LANCZOS)
    px = 36 + (side - photo.width) // 2
    py = 90 + (820 - photo.height) // 2
    canvas.paste(photo, (px, py))
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 28), kicker, font=font(18), fill=MUTED)
    draw.text((36, 52), title, font=font(32), fill=TEXT)
    bar = (36, 860, 36 + side, 910)
    draw.rounded_rectangle(bar, radius=10, fill=(13, 17, 23))
    draw.text((52, 872), kept, font=font(20), fill=TEXT)
    panel(draw, (940, 100, 1644, 460), AMBER_BG, AMBER, "UPSTREAM  上游", upstream)
    panel(draw, (940, 480, 1644, 900), GREEN_BG, GREEN, "THIS REPO  这里", ours)
    canvas.save(HERE / out_name, quality=92)


def main() -> None:
    compose(
        "hand-product.png",
        "hand-delta.png",
        "DEXTEROUS HAND  ·  灵巧手",
        "空的抓取代价",
        "有内容的 2×2 抓取，分配代价仍是 2",
        "MuJoCo 3.13.0\n空的 <worldbody/>\n→ accepted\n\nmunkres 1.1.4  compute([[]])\n→ []",
        "没有数字的 MJCF\nread_mjcf_cost\n→ raise\n\nhungar_cost([])\n→ raise",
    )
    compose(
        "bci-product.png",
        "bci-delta.png",
        "BRAIN-COMPUTER INTERFACE  ·  脑机接口",
        "空的脑电磁带",
        "仓库里的磁带仍是 8 个采样，标记 go / end",
        "MNE-Python 1.9.0\n空的 RawArray\n→ n_times = 0，标注长度 0\n\nNumPy 2.4.6  mean([])\n→ nan",
        "空的 trial_type，空的 GDF\n→ raise\n\nnyquist([])\n→ raise",
    )
    compose(
        "robot-product.png",
        "robot-delta.png",
        "MOBILE ROBOT  ·  移动机器人",
        "一步，不是闭包",
        "1×3 地图：一步到 2，闭包到 3。256 节点：24，然后 214",
        "NetworkX 3.6.1\n空的 DiGraph\n→ nodes = []\n\n同一条链上的 descendants\n→ 一次调用到达 3",
        "边还在，事实是空的\ndatalog_fixpoint\n→ raise\n\nworld_tick → 2\n闭包 → 3",
    )
    compose(
        "vehicle-product.png",
        "vehicle-delta.png",
        "VEHICLE  ·  车",
        "空的雷达，空的观测",
        "两个雷达点仍占据东北子节点 1。三条观测仍占据 3",
        "NumPy 2.4.6  linalg.norm([])\n→ 0.0\n\nFilterPy 1.4.5  update(None)\n→ accepted，x0 = 0.0",
        "octpart_ne([])\n→ raise\n\nkalman_filter([])\n→ raise",
    )


if __name__ == "__main__":
    main()
