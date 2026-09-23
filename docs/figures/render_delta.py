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
        "手指还没碰到任何东西",
        "表里真有数字时，分配代价仍是 2",
        "MuJoCo 会加载一个空的手部模型\n→ 当成加载成功\n\nmunkres 拿到一张空的分配表\n→ 返回一个空列表",
        "同一张空表\n→ 停下来报错\n\n不把“没碰到”写成代价 0",
    )
    compose(
        "bci-product.png",
        "bci-delta.png",
        "BRAIN-COMPUTER INTERFACE  ·  脑机接口",
        "这段脑电其实没录上",
        "录上的那一段仍是 8 个点，标记仍是 go / end",
        "MNE 遇到一段空录音\n→ 时长记成 0，标记个数记成 0\n\nNumPy 对空的采样求平均\n→ 得到 nan",
        "同一段空录音\n→ 停下来报错\n\n不把“没录上”写成电压 0",
    )
    compose(
        "robot-product.png",
        "robot-delta.png",
        "MOBILE ROBOT  ·  移动机器人",
        "地图这一步只亮了两格",
        "再往前走，第三格才会亮。大地图上是 24，然后 214",
        "NetworkX 拿到一张空地图\n→ 地点个数是 0\n\n路上有三格时，它一次就算到尽头\n→ 直接得到 3",
        "路上还有格子，但这一步什么都没看见\n→ 停下来报错\n\n看得到的时候：走一步是 2\n走到头是 3",
    )
    compose(
        "vehicle-product.png",
        "vehicle-delta.png",
        "VEHICLE  ·  车",
        "雷达这一帧是空的",
        "真有回波时，两个点仍算作 1。三次观测仍算作 3",
        "NumPy 对一帧空雷达求长度\n→ 得到 0.0\n\nFilterPy 收到一次空更新\n→ 照单接受，位置留在 0.0",
        "同一帧空雷达、同一次空观测\n→ 停下来报错\n\n不把“没扫到”写成四周是空的",
    )


if __name__ == "__main__":
    main()
