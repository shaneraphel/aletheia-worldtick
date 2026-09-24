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


def story() -> None:
    W, H = 1680, 720
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 28), "ONE SPLIT  ·  同一种分裂", font=font(18), fill=MUTED)
    draw.text((36, 58), "补全得到较大的数。一步是更小的数。空记录报错。", font=font(32), fill=TEXT)
    cols = [
        ("世界模型", "补上没看见的格子\n→ 可达 3\n和一张全看见的地图相同", "只走已经看见的一步\n→ 2\n中间那格是洞\n→ 报错"),
        ("脑机接口", "掉线补成 8 个 0\n→ 类别 0\n和静息相同", "录上的 8 个点\n→ 类别 1，标记 go\n空包\n→ 报错"),
        ("下一步动作", "只补全眼前这一行\n→ 动作 0", "按世界走一步\n→ 动作 1\n空的奖励表\n→ 报错"),
    ]
    for i, (name, big, small) in enumerate(cols):
        x = 36 + i * 548
        draw.rounded_rectangle((x, 130, x + 520, 680), radius=16, fill=CARD, outline=(48, 54, 61), width=2)
        draw.text((x + 24, 150), name, font=font(28), fill=TEXT)
        panel(draw, (x + 20, 210, x + 500, 420), AMBER_BG, AMBER, "补全", big)
        panel(draw, (x + 20, 440, x + 500, 660), GREEN_BG, GREEN, "一步", small)
    canvas.save(HERE / "story.png", quality=92)


def main() -> None:
    compose(
        "hand-product.png",
        "hand-delta.png",
        "DEXTEROUS HAND  ·  灵巧手",
        "手指还没碰到任何东西",
        "表里真有数字时，分配代价仍是 2",
        "MuJoCo 会加载一个空的手部模型\n→ 当成加载成功\n\nmunkres 拿到一张空的分配表\n→ 返回一个空列表",
        "空的分配表\n→ 报错\n\n2×2 有数字的表\n→ 代价 2",
    )
    compose(
        "bci-product.png",
        "bci-delta.png",
        "BRAIN-COMPUTER INTERFACE  ·  脑机接口",
        "这段脑电其实没录上",
        "录上的那一段仍是 8 个点，标记仍是 go / end",
        "MNE 遇到一段空录音\n→ 时长记成 0，标记个数记成 0\n\nNumPy 对空的采样求平均\n→ 得到 nan",
        "空录音\n→ 报错\n\n录上的一段\n→ 8 个点，标记 go / end",
    )
    compose(
        "robot-product.png",
        "robot-delta.png",
        "MOBILE ROBOT  ·  移动机器人",
        "地图这一步只亮了两格",
        "再往前走，第三格才会亮。大地图上是 24，然后 214",
        "NetworkX 拿到一张空地图\n→ 地点个数是 0\n\n路上有三格时，它一次就算到尽头\n→ 直接得到 3",
        "这一步是空的\n→ 报错\n\n走一步 → 2\n走到头 → 3",
    )
    compose(
        "vehicle-product.png",
        "vehicle-delta.png",
        "VEHICLE  ·  车",
        "雷达这一帧是空的",
        "真有回波时，两个点仍算作 1。三次观测仍算作 3",
        "NumPy 对一帧空雷达求长度\n→ 得到 0.0\n\nFilterPy 收到一次空更新\n→ 照单接受，位置留在 0.0",
        "空雷达、空观测\n→ 报错\n\n两个点 → 1\n三次观测 → 3",
    )
    story()


if __name__ == "__main__":
    main()
