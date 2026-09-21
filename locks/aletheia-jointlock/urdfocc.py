"""URDF occupancy. An empty robot is absence, not 0 links.

Dexterous-hand and arm descriptions ship as URDF. This writer emits a
two-link planar arm. Zero links refuse.
"""
from __future__ import annotations

import re
from pathlib import Path

Z = -1


def write_urdf(path, l1, l2):
    if l1 is None or l2 is None or l1 <= 0 or l2 <= 0:
        raise ValueError("uncompiled URDF is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        '<?xml version="1.0"?>\n'
        '<robot name="two_link">\n'
        '  <link name="base"/>\n'
        '  <link name="upper"/>\n'
        '  <link name="fore"/>\n'
        f'  <joint name="shoulder" type="revolute"><parent link="base"/><child link="upper"/>'
        f'<origin xyz="{l1} 0 0"/></joint>\n'
        f'  <joint name="elbow" type="revolute"><parent link="upper"/><child link="fore"/>'
        f'<origin xyz="{l2} 0 0"/></joint>\n'
        "</robot>\n"
    )
    return dest


def read_urdf(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if "<robot" not in text:
        raise ValueError("uncompiled URDF is absence")
    origins = re.findall(r'<origin xyz="([0-9.]+) 0 0"/>', text)
    if len(origins) < 2:
        raise ValueError("uncompiled URDF is absence")
    l1, l2 = float(origins[0]), float(origins[1])
    if l1 <= 0 or l2 <= 0:
        raise ValueError("uncompiled URDF is absence")
    n_link = text.count("<link ")
    if n_link < 1:
        raise ValueError("uncompiled URDF is absence")
    return {"n_links": n_link, "l1": l1, "l2": l2}


def urdf_occupancy(path):
    return read_urdf(path)["n_links"]
