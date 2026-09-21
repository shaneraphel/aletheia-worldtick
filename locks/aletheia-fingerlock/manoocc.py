"""MANO-shaped joint occupancy. An empty pose is absence, not 0 joints.

MANO uses 16 hand joints. This tape stores those joint sites as MIT JSON.
The MPI MANO model weights are not in this file and are not rewritten.
Zero joints refuse.
"""
from __future__ import annotations

import json
from pathlib import Path

Z = -1

N_MANO_JOINTS = 16


def write_mano(path, joints):
    if joints is None or not joints:
        raise ValueError("uncompiled MANO pose is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, j in enumerate(joints):
        name = j.get("name", "") if isinstance(j, dict) else ""
        xyz = j.get("xyz") if isinstance(j, dict) else j
        if not xyz or len(xyz) < 2:
            raise ValueError("uncompiled MANO pose is absence")
        x, y = int(xyz[0]), int(xyz[1])
        z = int(xyz[2]) if len(xyz) > 2 else 0
        rows.append({"i": i, "name": name, "xyz": [x, y, z]})
    dest.write_text(json.dumps({"mano_joints": rows}, indent=2) + "\n")
    return dest


def read_mano(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    if not text.strip():
        raise ValueError("uncompiled MANO pose is absence")
    try:
        rec = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("uncompiled MANO pose is absence") from exc
    rows = rec.get("mano_joints") if isinstance(rec, dict) else None
    if not rows:
        raise ValueError("uncompiled MANO pose is absence")
    return rows


def read_mano_points(path):
    pts = []
    for row in read_mano(path):
        xyz = row.get("xyz") if isinstance(row, dict) else None
        if not xyz or len(xyz) < 2:
            raise ValueError("uncompiled MANO pose is absence")
        pts.append((int(xyz[0]), int(xyz[1])))
    if not pts:
        raise ValueError("uncompiled MANO pose is absence")
    return pts


def read_mano_word(path):
    letters = []
    for row in read_mano(path):
        name = row.get("name") if isinstance(row, dict) else ""
        if name and name.isalpha() and len(name) == 1:
            letters.append(name.upper())
    word = "".join(letters)
    if not word:
        raise ValueError("uncompiled MANO pose is absence")
    return word


def mano_occupancy(path):
    return len(read_mano(path))
