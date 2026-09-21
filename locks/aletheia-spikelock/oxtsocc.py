"""KITTI OXTS occupancy from Accel and Gyro tapes. An empty IMU is absence.

KITTI raw oxts is 30 space-separated fields. ax/ay/az and af/al/au
copy the three-axis accelerometer. wx/wy/wz and wf/wl/wu copy the
three-axis gyroscope. roll/pitch/yaw copy the Orient stream. Zero
rows refuse.
"""
from __future__ import annotations

from pathlib import Path

Z = -1

ROLL, PITCH, YAW = 3, 4, 5
AX, AY, AZ = 11, 12, 13
AF, AL, AU = 14, 15, 16
WX, WY, WZ = 17, 18, 19
WF, WL, WU = 20, 21, 22
NUMSATS = 26
N_FIELDS = 30


def write_oxts_accel(path, accels, gyros=None, orients=None):
    if accels is None or not accels:
        raise ValueError("uncompiled OXTS tape is absence")
    if gyros is not None and not gyros:
        raise ValueError("uncompiled OXTS tape is absence")
    if orients is not None and not orients:
        raise ValueError("uncompiled OXTS tape is absence")
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for i, row in enumerate(accels):
        if row is None or len(row) < 3:
            raise ValueError("uncompiled OXTS tape is absence")
        ax, ay, az = float(row[0]), float(row[1]), float(row[2])
        fields = [0.0] * N_FIELDS
        fields[0], fields[1], fields[2] = 48.984553, 8.429361, 116.0
        fields[AX], fields[AY], fields[AZ] = ax, ay, az
        fields[AF], fields[AL], fields[AU] = ax, ay, az
        if gyros is not None:
            grow = gyros[i] if i < len(gyros) else None
            if grow is None or len(grow) < 3:
                raise ValueError("uncompiled OXTS tape is absence")
            wx, wy, wz = float(grow[0]), float(grow[1]), float(grow[2])
            fields[WX], fields[WY], fields[WZ] = wx, wy, wz
            fields[WF], fields[WL], fields[WU] = wx, wy, wz
        if orients is not None:
            orow = orients[i] if i < len(orients) else None
            if orow is None or len(orow) < 3:
                raise ValueError("uncompiled OXTS tape is absence")
            fields[ROLL], fields[PITCH], fields[YAW] = float(orow[0]), float(orow[1]), float(orow[2])
        fields[NUMSATS] = 4.0
        lines.append(" ".join(f"{v:.6f}" for v in fields))
    dest.write_text("\n".join(lines) + "\n")
    return dest


def read_oxts_accel(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    rows = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        if len(parts) < N_FIELDS:
            raise ValueError("uncompiled OXTS tape is absence")
        rows.append((float(parts[AX]), float(parts[AY]), float(parts[AZ])))
    if not rows:
        raise ValueError("uncompiled OXTS tape is absence")
    return rows


def read_oxts_gyro(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    rows = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        if len(parts) < N_FIELDS:
            raise ValueError("uncompiled OXTS tape is absence")
        rows.append((float(parts[WX]), float(parts[WY]), float(parts[WZ])))
    if not rows:
        raise ValueError("uncompiled OXTS tape is absence")
    return rows


def read_oxts_orient(path):
    text = Path(path).read_text() if Path(path).exists() else ""
    rows = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        if len(parts) < N_FIELDS:
            raise ValueError("uncompiled OXTS tape is absence")
        rows.append((float(parts[ROLL]), float(parts[PITCH]), float(parts[YAW])))
    if not rows:
        raise ValueError("uncompiled OXTS tape is absence")
    return rows


def oxts_occupancy(path):
    return len(read_oxts_accel(path))
