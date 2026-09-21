"""Hitachi occupancy. An empty recording is absence, not 0 samples.

A Hitachi ETG-7000 `3x5` CSV is Header plus 44 optical columns. Official
MNE `read_raw_hitachi` copies the first column as `S1_D1 695`. An empty
sample list refuses. Hitachi has no NIRx-style evt bits; NIRx keeps the
numeric stim channel.
"""
from __future__ import annotations

from pathlib import Path

Z = -1
N_NIRS = 44  # ETG-7000 3x5 pairing, two wavelengths


def _ch_names():
    names = []
    for i in range(N_NIRS):
        wl = "695.0" if i % 2 == 0 else "830.0"
        names.append(f"CH{i + 1}({wl})")
    return names


def write_hitachi(path, samples):
    if samples is None or not samples:
        raise ValueError("uncompiled Hitachi recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    chs = _ch_names()
    lines = [
        "Header",
        "File Version,1.00",
        "AnalyzeMode,Continuous",
        "Sampling Period[s],1",
        "Mode,3x5",
        "Date,9/20/26 14:00",
        "Wave[nm],695,830",
        "Name,aletheia tape",
        "Age,26y",
        "ID,tape",
        "Comment,aletheia",
        "Wave Length," + ",".join(chs),
        "Data",
        "Time," + ",".join(chs),
    ]
    for t, s in enumerate(samples):
        row = [str(t), str(float(int(s)))] + ["0"] * (N_NIRS - 1)
        lines.append(",".join(row))
    path.write_text("\n".join(lines) + "\n")
    return path


def read_hitachi(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError("uncompiled Hitachi recording is absence")
    text = path.read_text()
    if not text.startswith("Header"):
        raise ValueError("uncompiled Hitachi recording is absence")
    parts = text.split("Data\n", 1)
    if len(parts) != 2:
        raise ValueError("uncompiled Hitachi recording is absence")
    rows = [ln for ln in parts[1].splitlines() if ln.strip()]
    if len(rows) < 2:
        raise ValueError("uncompiled Hitachi recording is absence")
    samples = []
    for ln in rows[1:]:
        cols = ln.split(",")
        if len(cols) < 2:
            continue
        samples.append(int(float(cols[1])))
    if not samples:
        raise ValueError("uncompiled Hitachi recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def hitachi_occupancy(path):
    return read_hitachi(path)["n_samples"]
