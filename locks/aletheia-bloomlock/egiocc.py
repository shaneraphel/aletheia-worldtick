"""EGI occupancy. An empty recording is absence, not 0 samples.

An EGI simple-binary file is a Net Station header plus multiplexed int16
and named event codes. Official MNE `read_raw_egi` copies those codes as
annotation descriptions. An empty sample list or empty event list refuses.
EGI codes are four-character names like EyeLink MSG; Curry `.cef` keeps
integer event numbers.
"""
from __future__ import annotations

import struct
from pathlib import Path

Z = -1


def _norm_events(events):
    if events is not None and not events:
        raise ValueError("uncompiled EGI recording is absence")
    if events is None:
        events = [(1.0, "DIN1"), (2.0, "DIN2")]
    rows = []
    for i, item in enumerate(events):
        if isinstance(item, str):
            onset, code = float(i + 1), item
        elif len(item) >= 2:
            onset, code = float(item[0]), str(item[1])
        else:
            raise ValueError("uncompiled EGI recording is absence")
        code = code.ljust(4)[:4]
        if not code.strip():
            raise ValueError("uncompiled EGI recording is absence")
        rows.append((int(onset), code))
    if not rows:
        raise ValueError("uncompiled EGI recording is absence")
    return rows


def write_egi(path, samples, events=None):
    if samples is None or not samples:
        raise ValueError("uncompiled EGI recording is absence")
    if events is not None and not events:
        raise ValueError("uncompiled EGI recording is absence")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = _norm_events(events)
    codes = []
    seen = set()
    for _, code in rows:
        if code not in seen:
            seen.add(code)
            codes.append(code)
    n = len(samples)
    # version 2 written so little-endian read byteswaps to 2
    buf = bytearray()
    buf += struct.pack("<i", 0x02000000)
    buf += struct.pack(">hhhhhh", 2026, 9, 21, 1, 0, 0)
    buf += struct.pack(">i", 0)
    buf += struct.pack(">hhhhh", 1, 1, 1, 0, 0)
    buf += struct.pack(">i", n)
    buf += struct.pack(">h", len(codes))
    for code in codes:
        buf += code.encode("ascii")
    marks = {t: c for t, c in rows}
    for t, s in enumerate(samples):
        buf += struct.pack(">h", int(s))
        for code in codes:
            buf += struct.pack(">h", 1 if marks.get(t) == code else 0)
    path.write_bytes(bytes(buf))
    return path


def read_egi(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size < 36:
        raise ValueError("uncompiled EGI recording is absence")
    raw = path.read_bytes()
    n_samples = struct.unpack(">i", raw[30:34])[0]
    n_events = struct.unpack(">h", raw[34:36])[0]
    off = 36 + n_events * 4
    row = 2 + n_events * 2
    samples = []
    for i in range(n_samples):
        sl = raw[off + i * row : off + i * row + 2]
        if len(sl) < 2:
            break
        samples.append(struct.unpack(">h", sl)[0])
    if not samples:
        raise ValueError("uncompiled EGI recording is absence")
    return {"n_samples": len(samples), "samples": samples}


def read_egi_events(path):
    path = Path(path)
    if not path.exists() or path.stat().st_size < 36:
        raise ValueError("uncompiled EGI recording is absence")
    raw = path.read_bytes()
    n_samples = struct.unpack(">i", raw[30:34])[0]
    n_events = struct.unpack(">h", raw[34:36])[0]
    if n_events < 1:
        raise ValueError("uncompiled EGI recording is absence")
    codes = [raw[36 + 4 * i : 40 + 4 * i].decode("ascii") for i in range(n_events)]
    off = 36 + n_events * 4
    row = 2 + n_events * 2
    texts = []
    for i in range(n_samples):
        base = off + i * row
        for ei, code in enumerate(codes):
            sl = raw[base + 2 + 2 * ei : base + 4 + 2 * ei]
            if len(sl) == 2 and struct.unpack(">h", sl)[0] != 0:
                texts.append(code)
    if not texts:
        raise ValueError("uncompiled EGI recording is absence")
    return texts


def egi_occupancy(path):
    return read_egi(path)["n_samples"]
