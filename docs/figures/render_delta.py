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
    W, H = 1680, 860
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 24), "The same split  ·  同一种分裂", font=font(18), fill=MUTED)
    draw.text((36, 52), "补全是较大的数。一步是较小的数。空记录报错。", font=font(28), fill=TEXT)
    draw.text((36, 90), "Completion is the larger number. One tick is the smaller one. An empty record is an error.", font=font(20), fill=MUTED)
    cols = [
        ("世界模型  World model", "补上没看见的格子\nFill the unseen cell\n→ 可达 reach 3\n与全看见的地图相同\nSame as a fully seen map", "只走看见的一步\nOne tick of what was seen\n→ 2\n中间是洞 The middle is a hole\n→ 报错 error"),
        ("脑机接口  Brain–computer", "掉线补成 8 个 0\nFill a dropout with zeros\n→ 类别 class 0\n与静息相同\nSame as rest", "录上的 8 个点\nEight recorded samples\n→ 类别 class 1, go\n空包 Empty packet\n→ 报错 error"),
        ("下一动作  Next action", "只看眼前这一行\nThe visible row alone\n→ 动作 action 0", "按世界走一步\nOne tick of the world\n→ 动作 action 1\n空表 Empty table\n→ 报错 error"),
    ]
    for i, (name, big, small) in enumerate(cols):
        x = 36 + i * 548
        draw.rounded_rectangle((x, 140, x + 520, 830), radius=16, fill=CARD, outline=(48, 54, 61), width=2)
        draw.text((x + 20, 156), name, font=font(22), fill=TEXT)
        panel(draw, (x + 16, 200, x + 504, 490), AMBER_BG, AMBER, "补全  Completion", big)
        panel(draw, (x + 16, 510, x + 504, 810), GREEN_BG, GREEN, "一步  One tick", small)
    canvas.save(HERE / "story.png", quality=92)


def campaign_figure() -> None:
    W, H = 1680, 780
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 24), "10,000 trials  ·  seed 20260919  ·  一万次，种子 20260919", font=font(18), fill=MUTED)
    draw.text((36, 52), "一万次里，补全和一步没有一次相同。", font=font(28), fill=TEXT)
    draw.text((36, 90), "In all 10,000 trials, completion and one tick disagree.", font=font(20), fill=MUTED)
    rows = [
        ("世界模型", "World model", "补全可达 8", "Completion reaches 8", "10,000 / 10,000", "一步可达 2", "One tick reaches 2", "10,000 / 10,000"),
        ("脑机接口", "EEG", "补 0 = 静息 0", "Zeros match rest", "10,000 / 10,000", "录上的类 1", "Recorded class 1", "10,000 / 10,000"),
        ("下一动作", "Next action", "眼前这一行 = 0", "Visible row = 0", "10,000 / 10,000", "走一步 = 1", "One tick = 1", "10,000 / 10,000"),
    ]
    for i, (name, en, a, ae, an, b, be, bn) in enumerate(rows):
        y = 140 + i * 200
        draw.rounded_rectangle((36, y, 1644, y + 180), radius=16, fill=CARD, outline=(48, 54, 61), width=2)
        draw.text((56, y + 36), name, font=font(26), fill=TEXT)
        draw.text((56, y + 78), en, font=font(18), fill=MUTED)
        draw.text((340, y + 28), a, font=font(22), fill=AMBER)
        draw.text((340, y + 64), ae, font=font(18), fill=AMBER)
        draw.text((340, y + 110), an, font=font(28), fill=TEXT)
        draw.text((980, y + 28), b, font=font(22), fill=GREEN)
        draw.text((980, y + 64), be, font=font(18), fill=GREEN)
        draw.text((980, y + 110), bn, font=font(28), fill=TEXT)
    canvas.save(HERE / "campaign.png", quality=92)


def main() -> None:
    compose(
        "hand-product.png",
        "hand-delta.png",
        "DEXTEROUS HAND  ·  灵巧手",
        "手指还没碰到任何东西  Nothing has been touched",
        "有数字时代价仍是 2  With numbers the cost stays 2",
        "MuJoCo 空模型加载成功\nEmpty model loads\n→ accepted\n\nmunkres 空表\nEmpty table\n→ []",
        "空表  Empty table\n→ 报错 error\n\n2×2\n→ 代价 cost 2",
    )
    compose(
        "bci-product.png",
        "bci-delta.png",
        "BRAIN-COMPUTER INTERFACE  ·  脑机接口",
        "这段脑电没录上  This clip was not recorded",
        "录上的一段仍是 8 个点  The recorded clip is still 8 samples",
        "MNE 空录音  Empty recording\n→ 时长 duration 0\n\nNumPy 空平均  Empty mean\n→ nan",
        "空录音  Empty recording\n→ 报错 error\n\n录上的一段  Recorded\n→ 8 点，go / end",
    )
    compose(
        "robot-product.png",
        "robot-delta.png",
        "MOBILE ROBOT  ·  移动机器人",
        "这一步只亮两格  This step lights two cells",
        "第三格还在后面  The third cell is still ahead. Large map: 24, then 214",
        "NetworkX 空地图  Empty map\n→ 地点 places 0\n\n三格一次走到头\nThree cells, one call\n→ 3",
        "这一步是空的  Empty step\n→ 报错 error\n\n走一步 One tick → 2\n走到头 To the end → 3",
    )
    compose(
        "vehicle-product.png",
        "vehicle-delta.png",
        "VEHICLE  ·  车",
        "雷达这一帧是空的  This lidar frame is empty",
        "真有回波：两点算作 1，三次观测算作 3",
        "NumPy 空雷达  Empty lidar\n→ 长度 length 0.0\n\nFilterPy 空更新  Empty update\n→ 位置 position 0.0",
        "空雷达  Empty lidar\n→ 报错 error\n\n两个点 Two points → 1\n三次观测 Three updates → 3",
    )
    story()
    campaign_figure()


if __name__ == "__main__":
    main()
