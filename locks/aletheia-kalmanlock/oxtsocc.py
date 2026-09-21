"""KITTI OXTS occupancy. An empty IMU tape is absence, not 0 samples.

KITTI raw oxts is one space-separated pose/IMU row per sample. Zero rows
or a non-positive satellite count refuse.
"""
from __future__ import annotations

from pathlib import Path

Z = -1

# https://www.cvlibs.net/datasets/kitti/raw_data.php
NUMSATS = 26
POS_ACCURACY = 23
N_FIELDS = 30


def write_oxts(path, steps):
    if steps is None or not steps:
        raise ValueError("uncompiled OXTS tape is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for n_obs, noise in steps:
        if n_obs < 1 or noise < 0:
            raise ValueError("uncompiled OXTS tape is absence")
        fields = [0.0] * N_FIELDS
        fields[0] = 48.984553
        fields[1] = 8.429361
        fields[2] = 116.0
        fields[POS_ACCURACY] = float(noise)
        fields[NUMSATS] = float(n_obs)
        lines.append(" ".join(f"{v:.6f}" for v in fields))
    dest.write_text("\n".join(lines) + "\n")
    return dest


def read_oxts(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    steps = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        if len(parts) < N_FIELDS:
            raise ValueError("uncompiled OXTS tape is absence")
        n_obs = int(float(parts[NUMSATS]))
        noise = int(float(parts[POS_ACCURACY]))
        if n_obs < 1 or noise < 0:
            raise ValueError("uncompiled OXTS tape is absence")
        steps.append((n_obs, noise))
    if not steps:
        raise ValueError("uncompiled OXTS tape is absence")
    return steps


def oxts_occupancy(path):
    return len(read_oxts(path))
