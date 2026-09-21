"""MJCF occupancy. An empty hand is absence, not 0 sites.

MuJoCo MJCF names sites on a dexterous hand. Zero <site> elements refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_mjcf_sites(path, word):
    if word is None or not word:
        raise ValueError("uncompiled MJCF hand is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sites = "\n".join(f'      <site name="{ch}"/>' for ch in word)
    dest.write_text(
        '<mujoco model="fingers">\n'
        "  <worldbody>\n"
        '    <body name="hand">\n'
        f"{sites}\n"
        "    </body>\n"
        "  </worldbody>\n"
        "</mujoco>\n"
    )
    return dest


def read_mjcf_word(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<mujoco" not in text:
        raise ValueError("uncompiled MJCF hand is absence")
    names = re.findall(r'<site name="([^"]+)"', text)
    word = "".join(names)
    if not word:
        raise ValueError("uncompiled MJCF hand is absence")
    return word


def mjcf_occupancy(path):
    return len(read_mjcf_word(path))
