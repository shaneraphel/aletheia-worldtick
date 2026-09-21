"""Neuroscan CNT occupancy. An empty recording is absence, not 0 channels.

Neuroscan `.cnt` is a 900-byte SETUP, 75-byte ELECTLOC per channel, then
int16 samples. Events are EVENT1 stim codes at a TEEG table. Official
MNE `read_raw_cnt` reads those stims as annotation descriptions. An empty
sample list or empty event list refuses. This is not ANT Neuro CNT.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1

SETUP = 900
ELECTLOC = 75
SFREQ = 1


def _poke_str(buf: bytearray, offset: int, width: int, text: str) -> None:
    raw = text.encode("ascii")
    if len(raw) > width:
        raise ValueError("uncompiled CNT recording is absence")
    buf[offset : offset + width] = raw + b"\x00" * (width - len(raw))


def _norm_events(events, sfreq: int):
    if events is not None and not events:
        raise ValueError("uncompiled CNT recording is absence")
    if events is None:
        events = [(1.0, 1), (2.0, 2)]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, (int, float)) and not isinstance(item, bool):
            onset, stim = float(i + 1), int(item)
        elif isinstance(item, str):
            onset, stim = float(i + 1), item
        elif isinstance(item, dict):
            onset, stim = float(item["onset"]), item["stim"]
        elif len(item) >= 2:
            onset, stim = float(item[0]), item[1]
        else:
            raise ValueError("uncompiled CNT recording is absence")
        if isinstance(stim, str):
            if stim == "go":
                stim = 1
            elif stim == "end":
                stim = 2
            else:
                raise ValueError("uncompiled CNT recording is absence")
        stim = int(stim)
        if stim < 1:
            raise ValueError("uncompiled CNT recording is absence")
        rows.append((int(round(onset * sfreq)), stim))
    if not rows:
        raise ValueError("uncompiled CNT recording is absence")
    return rows


def write_cnt(path, samples, events=None, *, label="Cz"):
    if samples is None or not samples:
        raise ValueError("uncompiled CNT recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled CNT recording is absence")
    if not label or not str(label).isascii():
        raise ValueError("uncompiled CNT recording is absence")
    nch = 1
    n_bytes = 2
    n = len(samples)
    rows = _norm_events(events, SFREQ)
    data_start = SETUP + ELECTLOC * nch
    event_pos = data_start + n_bytes * nch * n
    buf = bytearray(event_pos + 9 + 8 * len(rows))
    _poke_str(buf, 0, 12, "aletheia")
    _poke_str(buf, 225, 10, "09/20/26")
    _poke_str(buf, 235, 12, "14:56:00")
    buf[143] = ord("U")
    buf[144] = ord("U")
    struct.pack_into("<H", buf, 370, nch)
    struct.pack_into("<H", buf, 376, SFREQ)
    struct.pack_into("<I", buf, 864, n)
    struct.pack_into("<i", buf, 886, event_pos)
    struct.pack_into("<f", buf, 890, 0.0)
    struct.pack_into("<i", buf, 894, 1)
    el = SETUP
    _poke_str(buf, el, 10, str(label)[:10])
    struct.pack_into("<ff", buf, el + 19, 0.0, 0.1)
    struct.pack_into("<h", buf, el + 47, 0)
    struct.pack_into("<f", buf, el + 59, 204.8)
    struct.pack_into("<f", buf, el + 71, 1.0)
    for i, value in enumerate(samples):
        struct.pack_into("<h", buf, data_start + 2 * i, int(value))
    struct.pack_into("<Bll", buf, event_pos, 1, 8 * len(rows), 0)
    for i, (sample, stim) in enumerate(rows):
        off = SETUP + ELECTLOC * nch + (sample + 1) * nch * n_bytes
        struct.pack_into("<HBcl", buf, event_pos + 9 + 8 * i, stim, 0, b"\x00", off)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(bytes(buf))
    return dest


def read_cnt(path):
    dest = Path(path)
    if not dest.exists() or dest.stat().st_size < SETUP + ELECTLOC + 2:
        raise ValueError("uncompiled CNT recording is absence")
    raw = dest.read_bytes()
    nch = struct.unpack_from("<H", raw, 370)[0]
    n = struct.unpack_from("<I", raw, 864)[0]
    if nch < 1 or n < 1:
        raise ValueError("uncompiled CNT recording is absence")
    start = SETUP + ELECTLOC * nch
    need = start + 2 * nch * n
    if len(raw) < need:
        raise ValueError("uncompiled CNT recording is absence")
    samples = [struct.unpack_from("<h", raw, start + 2 * i)[0] for i in range(n)]
    return {"n_channels": nch, "n_samples": n, "samples": samples}


def read_cnt_events(path):
    dest = Path(path)
    if not dest.exists() or dest.stat().st_size < SETUP + 9:
        raise ValueError("uncompiled CNT recording is absence")
    raw = dest.read_bytes()
    event_pos = struct.unpack_from("<i", raw, 886)[0]
    if event_pos < SETUP or event_pos + 9 > len(raw):
        raise ValueError("uncompiled CNT recording is absence")
    kind, total, _off = struct.unpack_from("<Bll", raw, event_pos)
    if kind != 1 or total < 8:
        raise ValueError("uncompiled CNT recording is absence")
    start = event_pos + 9
    if start + total > len(raw):
        raise ValueError("uncompiled CNT recording is absence")
    stims = []
    for i in range(total // 8):
        stim, _kb, _pad, _off = struct.unpack_from("<HBcl", raw, start + 8 * i)
        if stim < 1:
            continue
        stims.append(str(stim))
    if not stims:
        raise ValueError("uncompiled CNT recording is absence")
    return stims


def cnt_occupancy(path):
    return read_cnt(path)["n_samples"]
