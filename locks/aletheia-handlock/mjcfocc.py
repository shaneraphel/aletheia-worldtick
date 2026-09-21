"""MJCF numeric-cost occupancy. An empty custom table is absence, not cost 0.

A grasp assigner can store a square cost tape as MJCF <numeric data>.
Zero entries refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_mjcf_cost(path, cost):
    if cost is None or not cost:
        raise ValueError("uncompiled MJCF cost is absence")
    n = len(cost)
    if any(len(row) != n for row in cost):
        raise ValueError("uncompiled MJCF cost is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    flat = " ".join(str(int(v)) for row in cost for v in row)
    dest.write_text(
        '<mujoco model="grasp">\n'
        "  <custom>\n"
        f'    <numeric name="cost" size="{n * n}" data="{flat}"/>\n'
        "  </custom>\n"
        "  <worldbody>\n"
        '    <body name="palm"/>\n'
        "  </worldbody>\n"
        "</mujoco>\n"
    )
    return dest


def read_mjcf_cost(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<mujoco" not in text:
        raise ValueError("uncompiled MJCF cost is absence")
    m = re.search(r'<numeric name="cost"[^>]*data="([^"]+)"', text)
    if not m:
        raise ValueError("uncompiled MJCF cost is absence")
    vals = [int(x) for x in m.group(1).split() if x]
    if not vals:
        raise ValueError("uncompiled MJCF cost is absence")
    n = int(len(vals) ** 0.5)
    if n * n != len(vals):
        raise ValueError("uncompiled MJCF cost is absence")
    return [vals[i * n : (i + 1) * n] for i in range(n)]


def mjcf_occupancy(path):
    cost = read_mjcf_cost(path)
    return len(cost) * len(cost[0])
