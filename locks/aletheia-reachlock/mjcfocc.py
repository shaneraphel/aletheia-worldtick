"""MJCF two-link occupancy. An empty arm is absence, not rest-pose 0.

Capsule fromto lengths are the compiled links. Zero geoms refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_mjcf_arm(path, l1, l2):
    if l1 is None or l2 is None or l1 <= 0 or l2 <= 0:
        raise ValueError("uncompiled MJCF arm is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        '<mujoco model="two_link">\n'
        "  <worldbody>\n"
        f'    <body name="upper"><geom type="capsule" size="0.05" fromto="0 0 0 {l1} 0 0"/>\n'
        f'      <body name="fore"><geom type="capsule" size="0.05" fromto="0 0 0 {l2} 0 0"/></body>\n'
        "    </body>\n"
        "  </worldbody>\n"
        "</mujoco>\n"
    )
    return dest


def read_mjcf_arm(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<mujoco" not in text:
        raise ValueError("uncompiled MJCF arm is absence")
    pairs = re.findall(r'fromto="([0-9.]+) 0 0 ([0-9.]+) 0 0"', text)
    if len(pairs) < 2:
        raise ValueError("uncompiled MJCF arm is absence")
    l1 = float(pairs[0][1]) - float(pairs[0][0])
    l2 = float(pairs[1][1]) - float(pairs[1][0])
    if l1 <= 0 or l2 <= 0:
        raise ValueError("uncompiled MJCF arm is absence")
    return {"l1": l1, "l2": l2, "n_geoms": len(pairs)}


def mjcf_occupancy(path):
    return read_mjcf_arm(path)["n_geoms"]
